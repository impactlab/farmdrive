# -*- coding: utf-8 -*-
from glob import glob
import logging
import os
from subprocess import run

import click
from dotenv import find_dotenv, load_dotenv
from osgeo import ogr, osr
from tqdm import tqdm


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

# List of files that shouldn't be imported
BADFILES = [
    'GEFSOC-ISRIC-disclaimer.tif' # just an image, not actual raster data
]

@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    # load the shapefiles
    shp_pattern = str(os.path.join(PROJECT_ROOT, 'data', 'raw', '**', '*.shp'))
    shp_cmd = ['shp2pgsql', '-s', '4326', '-I']
    load_geo_info(shp_pattern, shp_cmd)

    # load the raster data
    tif_pattern = str(os.path.join(PROJECT_ROOT, 'data', 'raw', '**', '*.tif'))
    tif_cmd = ['raster2pgsql', '-s', '4326', '-I', '-l', '2,4,10']
    load_geo_info(tif_pattern, tif_cmd)


def load_geo_info(pattern, sql_generating_cmd):
    """ Finds files using the glob "pattern" and then executes
        the sql_generating_cmd to create a .sql script. Then executes
        the sql script to load the data into the datbase.

        Deletes the temporary .sql script unless executing that sql fails.
    """
    logger = logging.getLogger(__name__)
    logger.info('Loading files into postgis')

    for globbed_file in glob(pattern, recursive=True):
        if os.path.basename(globbed_file) in BADFILES:
            logger.warn("Skipping known bad files: '{}'".format(globbed_file))
        else:
            psql_path = os.path.splitext(globbed_file)[0] + os.path.extsep + 'sql'

            with open(psql_path, 'w') as psql_file:
                logger.info("Loading '{}'...".format(os.path.basename(globbed_file)))
                run(sql_generating_cmd + [globbed_file],
                    check=True,
                    stdout=psql_file)

            run(['psql', '-d', 'farmdrive', '-f', psql_path, '--quiet'], check=True)
            os.remove(psql_path)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
