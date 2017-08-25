import gc
from glob import glob
import os
import warnings

import click
import pandas as pd
import numpy as np
from tqdm import tqdm
import rasterio as rio

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


RAW_DATA_ROOT = os.path.abspath(os.path.join(__file__,
                                             os.pardir,
                                             os.pardir,
                                             os.pardir,
                                             'data',
                                             'raw'))

PLANET_DATA_ROOT = os.path.join(RAW_DATA_ROOT,
                                'planet')


def plot_normalized_indices(title, values, names, colormaps, output_folder=None, base_size=5):
    font = {'color': 'white'}

    fig, axes = plt.subplots(1,
                             len(names),
                             facecolor='black',
                             figsize=(base_size * len(names), base_size))

    fig.suptitle(title, fontdict=font)

    for ax, val, name, cmap in zip(axes, values, names, colormaps):

        im = ax.imshow(val, cmap=cmap, alpha=0.9, vmin=-1, vmax=1)
        fig.colorbar(im, ax=ax, orientation='horizontal', ticks=[])

        ax.set_title(name, fontdict=font)
        ax.axis('off')

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        plt.savefig(os.path.join(output_folder, title + '.png'))
    else:
        pass
        # plt.show()

    fig.clf()
    plt.close()


def summary_stats(measure):
    mean = np.nanmean(measure)
    std = np.nanstd(measure)

    not_nan_mask = ~np.isnan(measure)
    measure_no_nan = measure[not_nan_mask]

    # very_likely % (> 0.25, on the range of the measure -1..1)
    very_likely = (measure_no_nan > 0.25).sum() / not_nan_mask.sum()

    return mean, std, very_likely


def summary_stats_series(ward, a_b_tuples, names):
    """ For each tuple (a, b) in a_b_tuples:
        calculates (a - b) / (a + b) and associated
        stats.
    """
    try:
        measure_arr = np.zeros_like(a_b_tuples[0][0])

        with warnings.catch_warnings():
            # ignore warnings that some arrays are all NaNs
            warnings.filterwarnings('ignore')

            stats_labels = ['mean', 'std', 'pct_likely']

            series = dict()
            for n, a_b in zip(names, a_b_tuples):
                a, b = a_b
                np.true_divide((a - b), (a + b), measure_arr)

                for label, val in zip(stats_labels, summary_stats(measure_arr)):
                    series["{}_{}".format(n, label)] = val

            return pd.Series(series, name=ward)

    except MemoryError:
        return pd.Series([], name=ward)


def process_wards_normalized_indices(root_folder, plot=False):

    all_ward_data = []

    i = 0

    for f in tqdm(glob(os.path.join(root_folder, '*_fall'))):
        ward = f.split(str(os.path.sep))[-1].split("_")[0]

        # i += 1
        # if i > 130:
        #     break

        if ward != 'failed':
            analytic_file = os.path.join(f, "{}_fall_analytic.tif".format(ward))

            try:
                if os.path.exists(analytic_file):
                    data = rio.open(analytic_file)

                    b, g, r, re, nir = data.read()

                    ward_data = summary_stats_series(ward,
                                                     [(nir, re), (r, b), (g, re)],
                                                     ['re_ndvi', 'npcri', 're_ndwi'])

                    # Default GC is not aggressive enough.
                    # We force GC here and trade computational performance
                    # for getting our memory back.
                    del(r)
                    del(g)
                    del(b)
                    del(nir)
                    del(re)
                    gc.collect()

                    all_ward_data.append(ward_data)

                    # if plot:
                    #     plot_normalized_indices(ward,
                    #                             [re_ndvi, npcri, re_ndwi],
                    #                             ['Vegetation', 'Chlorophyll', 'Water'],
                    #                             [plt.cm.PRGn, plt.cm.PiYG, plt.cm.BrBG],
                    #                             output_folder=os.path.join(root_folder, 'ward_visualization'),
                    #                             base_size=2.5)

                else:
                    pass
                    print("DOES NOT EXIST: ", analytic_file)

            except MemoryError:
                all_ward_data.append(pd.Series([], name=ward))

    ward_df = pd.DataFrame(all_ward_data)
    ward_df.to_csv(os.path.join(root_folder, 'all_ward_data.csv'))


@click.command()
def process_wards():
    process_wards_normalized_indices(os.path.join(PLANET_DATA_ROOT, 'wards'))


if __name__ == '__main__':
    import logging
    np.seterr(divide='ignore', invalid='ignore')

    logging.basicConfig(level=logging.WARNING)
    process_wards()
