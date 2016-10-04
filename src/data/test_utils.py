import os

import numpy as np
import pytest

import utils

def test_utils_date_from_filename():
    tests = [
        '16.8 .012.xls',
        '05.092013.xls',
        '07 -4-2015.xls',
        "07- 09-2015.xls",
        "16.4.2013.xls",
        "12.08.2013.xls",
        "20.11.2012..xls",
        "21.9.2012(1).xls",
        "10.2.012.xls",
        "5. 06. 011.xls",
        "Copy of 10.8.2010.xls",
        '2(1).7.2010.xls',
        'MICS - 001 - 2011.xls', #NEGATIVE
    ]

    dates = [utils.date_from_filename(t) for t in tests]

    assert np.isnan(dates[-1])


def test_utils_find_header_row():
    crop_prices_folder = os.path.abspath(os.path.join(__file__,
                                                      os.pardir,
                                                      os.pardir,
                                                      os.pardir,
                                                      'data',
                                                      'raw',
                                                      'Crop Prices',
                                                      'crop_prices'))

    test_files = [
        'Daily 2014/April 2014/08.04.2014.xls',
        'Daily 2014/April 2014/09.04.2014.xls',
        "Daily 2014/April 2014/01.04.2014.xls",
        "Daily2011/Feb/3.02.2011.xls"
    ]

    header_rows = [utils.find_header_row(os.path.join(crop_prices_folder, t))
                    for t in test_files]
    assert header_rows == [7, 7, 8, 6]
