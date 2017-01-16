from glob import glob
import json
import os

import click
import pandas as pd


@click.command()
@click.argument('dir_path')
@click.argument('output_file')
@click.argument('input_filename')
@click.option('--crop', default='maize')
def gather_target_data(dir_path, output_file, input_filename, crop):
    """ We right out the per-pixel crop values to a geojson file
        as part of our querying and include that file in each
        directory with an image. This method parses each geojson
        file to get that yield value and then outputs a csv with the
        folder name and value to `output_file`.

        input_filename should be geojson_epsg4326.geojson by
        default
    """
    yields = []
    ids = []

    yield_str = '{}_yield'.format(crop)

    for gj_path in glob(os.path.join(dir_path, '**', input_filename)):
        with open(gj_path, 'r') as gj_file:
            gj_data = json.load(gj_file)

            crop_yield = gj_data['properties'][yield_str]
            pixel_id = gj_data['id']

            yields.append(crop_yield)
            ids.append(pixel_id)

    # write to csv
    (pd.DataFrame({'id': ids, yield_str: yields})
       .set_index('id')
       .to_csv(output_file))


if __name__ == '__main__':
    gather_target_data()
