'''
In this case, we will attempt to use the Inception V3 network
on the planet dataset.

In this test, we'll attempt to fine-tune the Inception V3 network
for the planet dataset.
'''

import os

import click
import pandas as pd
import numpy as np
import rasterio

from sklearn.model_selection import train_test_split

from keras.preprocessing.image import ImageDataGenerator
from keras.layers import GlobalAveragePooling2D, Dense
from keras.optimizers import RMSprop, SGD
from keras.models import Model

from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as iv3_preproc

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as vgg_preproc

@click.command()
@click.argument('image_directory')
@click.argument('labels_path')
@click.argument('output_path')
@click.option('--n_validation_samples', default=0.2)
@click.option('--n_epoch', default=30)
@click.option('--asset_type', default='visual')
@click.option('--model', default='InceptionV3')
@click.option('--loss', default='mean_absolute_error')
def train_model(image_directory,
                labels_path,
                output_path,
                n_validation_samples,
                n_epoch,
                asset_type,
                model,
                loss):
    """
    """
    labels = pd.read_csv(labels_path, index_col=0)

    if model == 'InceptionV3':
        img_width = 299
        img_height = 299
        model_class = InceptionV3
        preprocess_func = iv3_preproc
        freeze_depth = 172
    elif model == 'VGG16':
        img_width = 224
        img_height = 224
        model_class = VGG16
        preprocess_func = vgg_preproc
        freeze_depth = 25
    else:
        raise Exception('{} is an unsupported model.'.format(model))

    images, targets = load_data(labels,
                                img_width,
                                img_height,
                                asset_type,
                                image_directory,
                                'maize_yield')

    X_train, X_valid, y_train, y_valid = train_test_split(images,
                                                          targets,
                                                          test_size=n_validation_samples,
                                                          random_state=2234)

    n_train_samples = y_train.shape[0]
    n_validation_samples = y_valid.shape[0]

    model, base_model = get_pretrained_model(model_class)

    train_generator, validation_generator = get_data_generators(X_train,
                                                                y_train,
                                                                X_valid,
                                                                y_valid,
                                                                preprocess_func)

    train_new_layers(model,
                     base_model,
                     train_generator,
                     n_train_samples,
                     validation_generator,
                     n_validation_samples,
                     n_epoch=10,  # we just need this for reasonable weights, not tuning
                     loss=loss)

    finetune_model(model,
                   train_generator,
                   n_train_samples,
                   validation_generator,
                   n_validation_samples,
                   freeze_depth,
                   n_epoch=n_epoch,
                   loss=loss)

    persist_model(model, output_path)


def load_data(labels, height, width, asset_type, data_root, target_var):
    X = []
    y = []

    # rescale target to 0-1
#    labels[target_var] = ((labels[target_var] - labels[target_var].min()) /
 #       (labels[target_var].max() - labels[target_var].min()))

    print('Read train images')
    for index, row in labels.iterrows():
        f_name_format = '{}_{}_{}x{}.tif'
        filename = f_name_format.format(index,
                                        asset_type,
                                        width,
                                        height)

        image_path = os.path.join(data_root, index, filename)

        if not os.path.exists(image_path):
            print('{} Does not exist. Skipping...'.format(image_path))
            continue

        with rasterio.open(image_path) as src:
            if asset_type == 'visual':
            # planet images from visual asset are processed to
            # bands red, green, blue, alpha
                r, g, b, a = src.read()
                x = np.array([r, g, b], dtype=np.float32)
            elif asset_type == 'analytic':
                r, g, b, nir = src.read()
                x = np.array([r, g, nir], dtype=np.float32)

        X.append(x)
        y.append([row[target_var]])

    X, y = np.array(X), np.array(y)

    # Normalize X in each channel
#    for i in range(3):
#        X[:,i,:,:] -= X[:,i,:,:].mean()
        #X[:,i,:,:] /= X[:,i,:,:].std()

    # we need to set tensorflow (tf) ordering for best performance
    return X.transpose((0, 2, 3, 1)), y


def get_pretrained_model(model_class, weights='imagenet'):
    """ Downloads a pretrained model of `model_class` (e.g., InceptionV3)
        with the given weights.

        Adds a new tops layers to create regression predictions.

        Returns the model (all layers) and the base_model (just the
        layers from `model_class`) since we often want to be able to
        freeze the base_model layers on training.
    """
    # create the base pre-trained model
    base_model = model_class(weights='imagenet', include_top=False)

    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    # let's add a fully-connected layer
    x = Dense(1024, activation='relu')(x)

    # and a final linear layer for regression
    predictions = Dense(1, activation='linear')(x)

    # this is the model we will train
    model = Model(input=base_model.input, output=predictions)

    return model, base_model


def get_data_generators(X_train,
                        y_train,
                        X_valid,
                        y_valid,
                        preprocess_func,
                        shear_range=0.5,
                        rotation_range=20,
                        vertical_flip=True,
                        horizontal_flip=True,
                        train_batch_size=65,
                        validation_batch_size=65):
    """ Creates flow objects to convert input images into a large dataset
        of different images with different shears, rotations, and flips.

        This augements our total number of training images.

        preprocess_func is often `keras.applications.inception_v3.preprocess_input`
    """
    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_func,
        shear_range=shear_range,
        rotation_range=rotation_range,
        vertical_flip=vertical_flip,
        horizontal_flip=horizontal_flip)

    test_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_func,
        shear_range=shear_range,
        rotation_range=rotation_range,
        vertical_flip=vertical_flip,
        horizontal_flip=horizontal_flip)

    train_generator = train_datagen.flow(
              X_train, y_train,
              batch_size=train_batch_size)

    validation_generator = test_datagen.flow(
              X_valid, y_valid,
              batch_size=validation_batch_size)

    return train_generator, validation_generator


def train_new_layers(model,
                     base_model,
                     train_generator,
                     n_train_samples,
                     validation_generator,
                     n_validation_samples,
                     n_epoch=30,
                     loss='mean_absolute_error'):
    """
    """
    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    for layer in base_model.layers:
        layer.trainable = False

    # compile the model (should be done *after* setting layers to non-trainable)
    rms = RMSprop(lr=0.01, rho=0.9, epsilon=1e-08, decay=0.0)
    model.compile(optimizer=rms, loss=loss)

    # train the model on the new data for a few epochs
    model.fit_generator(
            train_generator,
            samples_per_epoch=n_train_samples,
            nb_epoch=n_epoch,
            validation_data=validation_generator,
            nb_val_samples=n_validation_samples)


def finetune_model(model,
                   train_generator,
                   n_train_samples,
                   validation_generator,
                   n_validation_samples,
                   freeze_depth,
                   n_epoch=30,
                   loss='mean_absolute_error'):
    # we chose to train the top 2 inception blocks, i.e. we will freeze
    # the first 172 layers and unfreeze the rest:
    for layer in model.layers[:freeze_depth]:
        layer.trainable = False
    for layer in model.layers[freeze_depth:]:
        layer.trainable = True

    # we need to recompile the model for these modifications to take effect
    # we use SGD with a low learning rate
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9),
                  loss=loss)

    # we train our model again (this time fine-tuning the top 2 inception blocks
    # alongside the top Dense layers
    model.fit_generator(
            train_generator,
            samples_per_epoch=n_train_samples,
            nb_epoch=n_epoch,
            validation_data=validation_generator,
            nb_val_samples=n_validation_samples)


def persist_model(model, output_path):
    # need to unfreeze if we want the model to save/load properly.
    for layer in model.layers:
        layer.trainable = True

    model.save(output_path)


if __name__ == '__main__':
    train_model()
