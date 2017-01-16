import collections
from glob import glob
from itertools import compress
import json
import os
from subprocess import check_output, CalledProcessError, STDOUT
import sys
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
import shapefile

import download_planet_lib as planet_lib
import download_planet
from image_processing import resize_for_inceptionv3

# get variables from .env file
dotenv.load_dotenv(dotenv.find_dotenv())

# host is empty string (for unix socket) on linux; else, localhost
# this fallback can be overridden with the .env file
host = '' if 'linux' in sys.platform else 'localhost'
engine = create_engine(os.environ.get('DATABASE_URL',
                                      'postgresql://{}/farmdrive'.format(host)))
session = sessionmaker(bind=engine)()

PLANET_DATA_ROOT = os.path.abspath(os.path.join(__file__,
                                                os.pardir,
                                                os.pardir,
                                                os.pardir,
                                                'data',
                                                'raw',
                                                'planet'))

data_root = os.path.join(PLANET_DATA_ROOT, os.pardir)


sf = shapefile.Reader(data_root + "/KEN_outline_SHP/ken")
bbox = sf.bbox
q_bbox = download_planet.build_planet_query(bbox=bbox, min_date="2016-09-01T00:00:00.000Z")

scenes = planet_lib.run_search({'item_types': ['PSOrthoTile'],
                                         'filter': q_bbox})

scenes = sorted(scenes,
                key=lambda x: (x['properties']['cloud_cover'], x['properties']['updated']),
                reverse=True)

scene_ids = [s['id'] for s in scenes]

# mark the scenes we want for activation
planet_lib.process_activation(planet_lib.activate,
                              scene_ids,
                              'PSOrthoTile',
                              'analytic')

# wait for assets to activate; can take 8-10 mins, we'll wait up to 30 min
SLEEP_PERIODS = 120
for i in tqdm(range(SLEEP_PERIODS)):
    activated = planet_lib.process_activation(planet_lib.check_activation,
                                              scene_ids,
                                              'PSOrthoTile',
                                              'analytic')

    if all(activated):
        print('All scenes activated!')
        break
    else:
        time.sleep(15)

if not all(activated):
    print("NOT ALL SCENES ACTIVATED")
    fail_path = os.path.join(PLANET_DATA_ROOT, 'failed_scenes.log')
    with open(fail_path, 'w') as fail_log:
        failed_ids = list(compress(scene_ids, activated))
        fail_log.write(failed_ids)
    print("Wrote scenes that failed to activate to {}".format(fail_path))
