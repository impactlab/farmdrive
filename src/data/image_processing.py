import glob
import logging
import os
from subprocess import check_output, CalledProcessError, STDOUT

import numpy as np

import rasterio

from rasterio.transform import guard_transform
from rio_hist.match import histogram_match, calculate_mask
from rio_hist.utils import cs_backward, read_mask

from tqdm import tqdm

logger = logging.getLogger(__file__)

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


def resize_for_vgg(input_path):
    """ The VGG16 and VGG19 models take images that are 224x224. This helper
        uses GDAL to resize tiffs to the proper size and output those
        files in the same folder with _224x224 appended to the filename.
    """
    path, ext = os.path.splitext(input_path)
    output_path = "{}{}{}".format(path, '_224x224', ext)

    resize_tiff(input_path, output_path, 224, 224)


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



def batch_hist_match_worker(ref_paths, match_proportion,
                            creation_options, bands, color_space, plot,
                            masked=True,
                            dst_suffix='_hist_matched'):

    """Matches the histogram of every image in ref_paths
       to the average histogram across all of the included images.

       Outputs each file with _hist_matched appended to the filename.

       Modified from:
       https://github.com/mapbox/rio-hist/blob/81e3d5f0f59ba1e4e15f8850592a818501957ed2/rio_hist/match.py
    """

    # we need one sample to setup the processing
    src_path = ref_paths[0]

    with rasterio.open(src_path) as src:
        print("THE SHAPE", src.read().shape)
        profile = src.profile.copy()
        src_arr = src.read(masked=masked)

        if masked:
            src_mask, src_fill = calculate_mask(src, src_arr)
            src_arr = src_arr.filled()
        else:
            src_mask, src_fill = None, None

    ref_out = np.zeros([len(ref_paths)] + list(src_arr.shape), dtype=src_arr.dtype)

    # no bands, just masks
    ref_mask_out = np.zeros([len(ref_paths)] + list(src_arr.shape[1:]), dtype=src_arr.dtype)

    n_bands = src_arr.shape[0]

    for i, ref_path in enumerate(ref_paths):
        with rasterio.open(ref_path) as ref:
            ref_arr = ref.read(masked=masked)

            if masked:
                ref_mask, ref_fill = calculate_mask(ref, ref_arr)
                ref_arr = ref_arr.filled()
            else:
                ref_mask, ref_fill = None, None

            ref_out[i, :, :, :] = ref_arr

            if ref_mask is None:
                ref_mask_out = None
            else:
                ref_mask_out[i, :, :] = ref_mask

    bixs = tuple([int(x) - 1 for x in bands.split(',')])
    # band_names = [color_space[x] for x in bixs]  # assume 1 letter per band

    # we only support rgb for now
    arrnorm_raw = ref_out.astype(np.float64) / np.iinfo(ref_out.dtype).max
    ref = arrnorm_raw[:, bixs, :, :]

    output_paths = []

    print("Matching histograms...")
    for src_path in tqdm(ref_paths):
        with rasterio.open(src_path) as src:
            profile = src.profile.copy()
            src_arr = src.read(masked=masked)

            if masked:
                src_mask, src_fill = calculate_mask(src, src_arr)
                src_arr = src_arr.filled()
            else:
                src_mask, src_fill = None, None

        src = cs_forward(src_arr, color_space, band_range=range(n_bands))

        target = src.copy()
        for i, b in enumerate(bixs):
            logger.debug("Processing band {}".format(b))
            src_band = src[b]
            ref_band = ref[:, b, :, :]

            # Re-apply 2D mask to each band
            if src_mask is not None:
                logger.debug("apply src_mask to band {}".format(b))
                src_band = np.ma.asarray(src_band)
                src_band.mask = src_mask
                src_band.fill_value = src_fill

            if ref_mask_out is not None:
                logger.debug("apply ref_mask to band {}".format(b))
                ref_band = np.ma.asarray(ref_band)
                ref_band.mask = ref_mask_out
                ref_band.fill_value = ref_fill

            target[b] = histogram_match(src_band, ref_band, match_proportion)

        target_rgb = cs_backward(target, color_space)

        # re-apply src_mask to target_rgb and write ndv
        if src_mask is not None:
            logger.debug("apply src_mask to target_rgb")
            if not np.ma.is_masked(target_rgb):
                target_rgb = np.ma.asarray(target_rgb)
            target_rgb.mask = np.array((src_mask, src_mask, src_mask))
            target_rgb.fill_value = src_fill

        profile['count'] = n_bands

        profile['dtype'] = 'uint8'
        profile['nodata'] = None
        profile['transform'] = guard_transform(profile['transform'])
        profile.update(creation_options)

        input_base_filepath = os.path.splitext(os.path.abspath(src_path))[0]
        dst_path = '{}{}.tif'.format(input_base_filepath, dst_suffix)

        logger.info("Writing raster {}".format(dst_path))
        with rasterio.open(dst_path, 'w', **profile) as dst:
            for b in bixs:
                dst.write(target_rgb[b], b + 1)

            if src_mask is not None:
                gdal_mask = (np.invert(src_mask) * 255).astype('uint8')

                # write to extra band
                dst.write(gdal_mask, bixs[-1] + 2)

        output_paths.append(dst_path)

    return output_paths


def cs_forward(arr, cs='rgb', band_range=range(3)):
    """ RGB (any dtype) to whatevs
    """
    arrnorm_raw = arr.astype('float64') / np.iinfo(arr.dtype).max
    arrnorm = arrnorm_raw[band_range]
    cs = cs.lower()
    if cs == 'rgb':
        return arrnorm
    elif cs == 'lch':
        return convert_arr(arrnorm,
                           src=ColorSpace.rgb,
                           dst=ColorSpace.lch)
    elif cs == 'lab':
        return convert_arr(arrnorm,
                           src=ColorSpace.rgb,
                           dst=ColorSpace.lab)
    elif cs == 'luv':
        return convert_arr(arrnorm,
                           src=ColorSpace.rgb,
                           dst=ColorSpace.luv)
    elif cs == 'xyz':
        return convert_arr(arrnorm,
                           src=ColorSpace.rgb,
                           dst=ColorSpace.xyz)
