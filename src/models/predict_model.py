'''
In this case, we will attempt to use the Inception V3 network
on the planet dataset.

In this test, we'll attempt to fine-tune the Inception V3 network
for the planet dataset.
'''
from glob import glob
import json
import os

import click
import pandas as pd
import numpy as np
import rasterio

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from keras.preprocessing.image import ImageDataGenerator
from keras.layers import GlobalAveragePooling2D, Dense
from keras.optimizers import RMSprop, SGD
from keras.models import Model, load_model

from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as iv3_preproc

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as vgg_preproc

from train_model import load_data

PROJ_ROOT = os.path.abspath(os.path.join(__file__,
                                         os.pardir,
                                         os.pardir,
                                         os.pardir))

@click.command()
@click.argument('image_directory')
@click.argument('labels_path')
@click.option('--season', default='fall')
@click.option('--asset_type', default='visual')
@click.option('--model', default='InceptionV3')
@click.option('--crop', default='maize')
def predict_model(image_directory,
                  labels_path,
                  season,
                  asset_type,
                  model,
                  crop):
    labels = pd.read_csv(labels_path, index_col=0)

    if model == 'InceptionV3':
        model_name = model
        img_width = 299
        img_height = 299
        model_class = InceptionV3
        preprocess_func = iv3_preproc
        freeze_depth = 172
    elif model == 'VGG16':
        model_name = model
        img_width = 224
        img_height = 224
        model_class = VGG16
        preprocess_func = lambda x: x
        freeze_depth = 25
    else:
        raise Exception('{} is an unsupported model.'.format(model))

    output_base = '{}_{}_{}_{}'.format(model_name, asset_type, season, crop)
    model_path = os.path.join(PROJ_ROOT, 'models', output_base + '_keras.h5')
    model = load_model(model_path)

    images, targets, exisiting_image_ids = load_data(labels,
                                              img_width,
                                              img_height,
                                              asset_type,
                                              image_directory,
                                              season,
                                              '{}_yield'.format(crop))

    preds = model.predict(images)

    print(preds.shape)

    predicted_images = labels.loc[exisiting_image_ids, :].copy()
    predicted_images['prediction'] = preds

    preds_out_path = os.path.join(PROJ_ROOT, 'models', output_base + '_preds.csv')
    predicted_images.to_csv(preds_out_path)

    geojson_preds_out = os.path.join(PROJ_ROOT, 'models', output_base + '_preds.geojson')

    write_geojson_predictions(
        image_directory,
        "geojson_epsg4326_{}.geojson".format(crop),
        crop,
        predicted_images,
        geojson_preds_out
        )

def write_geojson_predictions(dir_path, input_filename, crop, preds, out_path):
    all_shapes = []
    for gj_path in glob(os.path.join(dir_path, '**', input_filename)):
        with open(gj_path, 'r') as gj_file:
            gj_data = json.load(gj_file)

            pixel_id = gj_data['id']

            print(pixel_id)

            if pixel_id in preds.index:
                print("Making preds")
                print(preds.prediction[pixel_id])
                gj_data['properties']['{}_prediction'.format(crop)] = float(preds.prediction[pixel_id])
            else:
                gj_data['properties']['{}_prediction'.format(crop)] = 0

            all_shapes.append(gj_data)

    with open(out_path, 'w') as out_file:
        final_geo_data = dict(
            type="FeatureCollection",
            features=all_shapes
          )
        json.dump(final_geo_data, out_file, indent=4)

if __name__ == '__main__':
    predict_model()


