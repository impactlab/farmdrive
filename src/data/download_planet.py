import collections
from glob import glob
from itertools import compress
import json
import os
from subprocess import check_output, CalledProcessError, STDOUT
import time
import traceback

import click
import dotenv
import rasterio
from rasterio import features
from rasterio.merge import merge
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

import download_planet_lib as planet_lib
from image_processing import resize_for_inceptionv3

# get variables from .env file
dotenv.load_dotenv(dotenv.find_dotenv())

# fallback to localhost database
engine = create_engine(os.environ.get('DATABASE_URL',
                                      'postgresql://localhost/farmdrive'))
session = sessionmaker(bind=engine)()

PLANET_DATA_ROOT = os.path.abspath(os.path.join(__file__,
                                                os.pardir,
                                                os.pardir,
                                                os.pardir,
                                                'data',
                                                'raw',
                                                'planet'))


def query_for_aois(county_name, crop_table, crop_name):
    """ Gets the areas of interest for a particular
        county_name
        crop_table
        crop_name
    """

    # individual geojson polygons for each raster pixel
    query = """
    SELECT
    json_build_object(
        'type', 'Feature',
        'id', (poly_pixels.x || '_' || poly_pixels.y),
        'geometry', ST_AsGeoJSON(1, poly_pixels.geom, 15, 2) :: JSON,
        'properties', json_build_object('{crop_name}_yield', poly_pixels.val)
    )
    FROM
      (SELECT (ST_PixelAsPolygons(ST_Union(ST_Clip("{crop_table}".rast, clipped_geom.geom)))).*
        FROM
          "{crop_table}",
          (SELECT county.geom FROM county WHERE county.county = '{county_name}') AS clipped_geom
        WHERE ST_Intersects("{crop_table}".rast, clipped_geom.geom)
      ) AS poly_pixels;
    """

    query = query.format(crop_name=crop_name,
                         crop_table=crop_table,
                         county_name=county_name)

    # Execute the query in the session
    result = session.execute(query)

    aoi_raster = result.fetchall()
    return aoi_raster


def write_and_reproject_per_pixel_geojson(aoi_geojson, county_pixel_dir):
    """ Operates on a single geojson AOI to write out the current
        projection and the projection we need to work with planet.
    """
    geojson_input = os.path.join(county_pixel_dir, 'geojson_epsg4326.geojson')
    geojson_output = os.path.join(county_pixel_dir, 'geojson_epsg32637.geojson')

    with open(geojson_input, 'w') as gj_file:
        json.dump(aoi_geojson, gj_file)

    try:
        check_output(['ogr2ogr',
                      '-f',
                      'GeoJSON',
                      geojson_output,
                      '-t_srs',
                      'EPSG:32637',
                      geojson_input], stderr=STDOUT)

    except CalledProcessError as e:
        print(e.output)
        raise


def build_planet_query(geojson_aoi,
                       min_date="2016-07-31T00:00:00.000Z",
                       max_date="2016-10-31T00:00:00.000Z",
                       cloud_cover=0.05):
    """ Creates a query for the planet v1 api with a date range,
        area of interest, max cloud cover %
    """
    if 'geometry' in geojson_aoi:
        geojson_aoi = geojson_aoi['geometry']

    # filter for items the overlap with our chosen geometry
    geometry_filter = {
      "type": "GeometryFilter",
      "field_name": "geometry",
      "config": geojson_aoi
    }

    # MAIZE harvest season in Kenya is Aug - Oct
    date_range_filter = {
      "type": "DateRangeFilter",
      "field_name": "acquired",
      "config": {
        "gte": min_date,
        "lte": max_date
      }
    }

    # filter any images which are more than 10% clouds
    cloud_cover_filter = {
      "type": "RangeFilter",
      "field_name": "cloud_cover",
      "config": {
        "lte": cloud_cover
      }
    }

    # create a filter that combines our geo and date filters
    query_filter = {
      "type": "AndFilter",
      "config": [geometry_filter, date_range_filter, cloud_cover_filter]
    }

    return query_filter


def has_local_scene(scene_id, asset_type, asset_dir):
    scene_path = os.path.join(asset_dir, '{}_{}.tif'.format(scene_id,
                                                            asset_type))
    return os.path.exists(scene_path)


def download_tiles_from_aoi(planet_query,
                            data_dir,
                            asset_type='analytic',
                            search_type='PSOrthoTile'):
    """ Activates the scenes in the planet query and downloads
        them to the data_dir if they are not there already.
    """

    # get the planet scenes IDs for our query
    scene_ids = planet_lib.run_search({'item_types': [search_type],
                                       'filter': planet_query})

    # check for scenes that we _don't_ already have
    not_local_scene_ids = [sid for sid in scene_ids if not \
                           has_local_scene(sid, asset_type, data_dir)]

    # mark the scenes we want for activation
    planet_lib.process_activation(planet_lib.activate,
                                  not_local_scene_ids,
                                  search_type,
                                  asset_type)

    # wait for assets to activate; can take 8-10 mins, we'll wait up to 30 min
    SLEEP_PERIODS = 120
    for i in tqdm(range(SLEEP_PERIODS)):
        activated = planet_lib.process_activation(planet_lib.check_activation,
                                                  not_local_scene_ids,
                                                  search_type,
                                                  asset_type)

        if all(activated):
            print('All scenes activated!')
            break
        else:
            time.sleep(15)

    if not all(activated):
        fail_path = os.path.join(data_dir, 'failed_scenes.log')
        with open(fail_path, 'w') as fail_log:
            failed_ids = list(compress(not_local_scene_ids, activated))
            fail_log.write(failed_ids)
        print("Wrote scenes that failed to activate to {}".format(fail_path))

    downloaded = planet_lib.process_download(data_dir,
                                             not_local_scene_ids,
                                             search_type,
                                             asset_type,
                                             False)

    if not all(downloaded):
        fail_path = os.path.join(data_dir, 'failed_downloads.log')
        with open(fail_path, 'w') as fail_log:
            failed_ids = list(compress(not_local_scene_ids, downloaded))
            fail_log.write(failed_ids)
        print("Wrote scenes that failed to download to {}".format(fail_path))

    return scene_ids


def merge_scenes(scene_ids, asset_dir, county_pixel_dir, asset_type):
    paths = [os.path.join(asset_dir, '{}_{}.tif'.format(sid, asset_type)) \
             for sid in scene_ids]

    vrt_path = os.path.join(county_pixel_dir, 'mosaic.vrt')
    gj_path = os.path.join(county_pixel_dir, 'geojson_epsg32637.geojson')

    pixel_id = os.path.split(county_pixel_dir)[1]
    print("PID: ", pixel_id)
    output_tiff = os.path.join(county_pixel_dir,
                               pixel_id + '_{}.tif'.format(asset_type))

    try:
        check_output(['gdalbuildvrt', '-overwrite', vrt_path] + paths,
                      stderr=STDOUT)
    except CalledProcessError as e:
        print(e.output)
        raise

    try:
        check_output(['gdalwarp',
                      '-of',
                      'GTiff',
                      '-cutline',
                      gj_path,
                      '-crop_to_cutline',
                      '-overwrite',
                      vrt_path,
                      output_tiff],
                     stderr=STDOUT)

    # print("Wrote merged tiff to {}".format(output_tiff))

    except CalledProcessError as e:
        print(e.output)
        raise

    return output_tiff



#
# def merge_scenes_rasterio(scene_ids, asset_dir, county_pixel_dir, asset_type):
#     paths = [glob(os.path.join(asset_dir, '{}_{}.tif')
#                          .format(sid, asset_type))[0] for sid in scene_ids]
#
#     planet_crs = {'proj': 'utm',
#                   'zone': 37,
#                   'ellps': 'WGS84',
#                   'datum': 'WGS84',
#                   'units': 'm',
#                   'no_defs': True}
#
#     srcs = [rasterio.open(p, crs=planet_crs) for p in paths]
#
#     geojson_proj_file = os.path.join(county_pixel_dir,
#                                      'geojson_epsg32637.geojson')
#     with open(geojson_proj_file) as gj_file:
#         reprojgeoj = json.load(gj_file)
#
#     out_image, out_transform = merge(srcs, bounds=features.bounds(reprojgeoj))
#
#     # save the resulting raster
#     out_meta = srcs[0].meta.copy()
#     out_meta.update({"driver": "GTiff",
#                      "height": out_image.shape[1],
#                      "width": out_image.shape[2],
#                      "transform": out_transform})
#
#     pixel_id = os.path.dirname(county_pixel_dir)
#     raster_merged_path = os.path.join(county_pixel_dir,
#                                       pixel_id + '.tif')
#
#     with rasterio.open(raster_merged_path, "w", **out_meta) as dest:
#         dest.write(out_image)


@click.command()
@click.argument('county_name')
@click.argument('crop_table')
@click.argument('crop_name')
@click.option('--aoi_selector', default=None, type=str, help='Index of aoi to use if we want just a few; accepts integers and ranges (e.g, 1:10).')
@click.option('--min_date', default='', help='Start date in ISO8601')
@click.option('--max_date', default='', help='End date in ISO8601')
@click.option('--cloud_cover', default='', help='Percent cloud cover allowed')
@click.option('--asset_type', default='analytic', help="'analytic' or 'visual' assets from the Planet API")
@click.option('--resize', is_flag=True, help="Create a resized image after it is downloaded.")
def download_county_crop_tiles(county_name,
                               crop_table,
                               crop_name,
                               aoi_selector,
                               min_date,
                               max_date,
                               cloud_cover,
                               asset_type,
                               resize):
    """ This script downloads planet labs data for the crop_table in county_name
        and saves it as the crop_name.

        Example: python download_planet.py Nakuru 'maiz_p--ssa' maize
    """
    # get the areas of interest from the postgres database
    geojson_aois = query_for_aois(county_name, crop_table, crop_name)

    if aoi_selector:
        if ':' in aoi_selector:
            mini, maxi = map(int, aoi_selector.split(':'))
            geojson_aois = geojson_aois[mini:maxi]
        else:
            geojson_aois = geojson_aois[int(aoi_selector)]

    if not isinstance(geojson_aois, collections.Iterable):
        geojson_aois = [(geojson_aois, )]

    # download images for every area of interest
    failed_aois = []
    for aoi in geojson_aois:
        if isinstance(aoi, sqlalchemy.engine.result.RowProxy):
            aoi = aoi[0]

        try:
            # create directories if we need to
            county_data = os.path.join(PLANET_DATA_ROOT,
                                       county_name)

            county_pixel_dir = os.path.join(county_data,
                                            aoi['id'])

            asset_dir = os.path.join(county_data,
                                     'assets')

            os.makedirs(county_pixel_dir, exist_ok=True)
            os.makedirs(asset_dir, exist_ok=True)

            # get the geojson and write in both projections
            write_and_reproject_per_pixel_geojson(aoi, county_pixel_dir)

            # override defaults if they are passed
            extra_query_kwargs = {}
            if min_date:
                extra_query_args['min_date'] = min_date
            if max_date:
                extra_query_args['max_date'] = max_date
            if cloud_cover:
                extra_query_args['cloud_cover'] = cloud_cover

            # get the representation of the query
            planet_query = build_planet_query(aoi, **extra_query_kwargs)

            # activate and download the tiles
            scence_ids = download_tiles_from_aoi(planet_query,
                                                 asset_dir,
                                                 asset_type=asset_type,
                                                 search_type='PSOrthoTile')

            output_path = merge_scenes(scence_ids,
                                       asset_dir,
                                       county_pixel_dir,
                                       asset_type)

            resize_for_inceptionv3(output_path)


        except Exception as e:
            print('>>>>>>>>>>>>>> FAILURE TO DOWNLOAD AOI >>>>>>>>>>>>>')
            print(e)
            print(traceback.print_exc())
            failed_aois.append(aoi)

    print('{} of {} aois did not download correctly.'.format(len(failed_aois),
                                                             len(geojson_aois)))

    if failed_aois:
        fail_path = os.path.join(county_data, 'failed_aois.json')
        with open(fail_path, 'w') as fail_log:
            json.dump(failed_aois, fail_log)
        print("Wrote scenes that failed to activate to {}".format(fail_path))



if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    download_county_crop_tiles()
