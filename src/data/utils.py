import os
import re

import numpy as np
import pandas as pd
import xlrd


def date_from_filename(f):
    """ Takes a filename that roughly has a format like:
        DD-MM-YYYY.xls or DD.MM.YYYY.xls and extracts the date using a regex
    """
    warning_str = "WARNING: Date extraction from filename failed on '{}'." +
                " If there is not a full date including day, " +
                "this can be ignored."

    REGEX = re.compile(r"([0-9]{1,2})(\(1\))?(\s)?([-\.])(\s)?([0-9]{1,2})(\s)?([-\.])?(\s)?([0-9]{2,4})")
    m = REGEX.search(f)

    if m is None:
        print(warning_str.format(f))
        return np.nan

    day = m.groups()[0]
    month = m.groups()[5]
    year = m.groups()[9]

    # special case not having a separator between mo and year when both are 2 digits:
    if len(month) == 2 and len(year) == 2 and m.groups()[7] is None:
        print(warning_str.format(f))
        return np.nan

    if len(day) == 1:
        day = "0" + day

    if len(month) == 1:
        month = "0" + month

    if len(year) == 3:
        year = "2" + year
    elif len(year) == 2:
        year = "20" + year

    iso_date = "{}-{}-{}".format(year, month, day)
    return pd.to_datetime(iso_date)


def find_header_row(path):
    """ Opens a Crop Prices Excel file and looks for the header row, which
        has 'commodity' or 'crop' in the second column.
    """
    wb = xlrd.open_workbook(path)
    sheet = wb.sheets()[0]

    header_row = 0
    while sheet.cell(header_row, 1).value.lower() not in ['commodity', 'crop'] and header_row < 20:
        header_row += 1

    if header_row == 20:
        raise Exception("Failed to find header row for {}".format(path))

    return header_row
