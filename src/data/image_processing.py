import glob
import os
from subprocess import check_output, CalledProcessError, STDOUT


def resize_tiff(input_path, output_path, width, height, projection='EPSG:32637'):
    """ Uses gdalwarp to resize the tiff image at `input_path`
        to `width` x `height` and stores it at the `output_path`.
    """
    try:
        check_output(['gdalwarp',
                      '-t_srs',
                      projection,
                      '-ts',
                      str(width),
                      str(height),
                      '-overwrite',
                      input_path,
                      output_path],
                     stderr=STDOUT)

    except CalledProcessError as e:
        print(e.output)
        raise


def resize_for_inceptionv3(input_path):
    """ The InceptionV3 model takes images that are 299x299. This helper
        uses GDAL to resize tiffs to the proper size and output those
        files in the same folder with _299x299 appended to the filename.
    """
    path, ext = os.path.splitext(input_path)
    output_path = "{}{}{}".format(path, '_299x299', ext)

    resize_tiff(input_path, output_path, 299, 299)


def resize_all_in_dir(dir_path,
                      ext='.tiff',
                      recursive=True,
                      resize_func=resize_for_inceptionv3):
    """ Resizes all of the images in `dir_path` with `ext`
        using `resize_func`.
    """
    for filename in glob.glob(os.path.join(dir_path, '**', '*.{}'.format(ext)),
                              recursive=recursive):
        resize_func(filename)
