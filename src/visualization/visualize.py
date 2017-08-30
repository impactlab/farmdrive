import os
import shutil

import click
import h5py
import keras


from quiver_engine import server


@click.command()
@click.argument('model_path')
@click.argument('input_images_path')
def runserver(model_path, input_images_path):
    try:
        model = keras.models.load_model(model_path)
    except ValueError:
        new_model_path = os.path.abspath(model_path) + ".edited"
        shutil.copy(model_path, new_model_path)

        f = h5py.File(new_model_path, 'r+')
        del f['optimizer_weights']
        f.close()

        model = keras.models.load_model(new_model_path)

    server.launch(
        model,  # a Keras Model

        classes='regression',  # list of output classes from the model to present (if not specified 1000 ImageNet classes will be used)

        # a folder where input images are stored
        input_folder=input_images_path,

        # the localhost port the dashboard is to be served on
        port=5000
    )


if __name__ == "__main__":
    runserver()
