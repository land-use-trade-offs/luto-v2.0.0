#!/bin/env python3
#
# economic.py - sub module to load and prepare agro-economic (spatial) data.
#
# Author: Fjalar de Haan (f.dehaan@deakin.edu.au)
# Created: 2021-07-09
# Last modified: 2021-07-28
#

import os.path

import pandas as pd
import numpy as np

def concord(concordance, data, columns=None, lus=None, lms=None):
    """Return LUTO-cell wise, multi-indexed column-landuse-landman DataFrame."""

    # If no list of columns is provided, infer it from provided data.
    if columns is None:
        columns = data.columns.to_list()

    # If no list of land uses provided, infer it from the SPREAD_CLASS column.
    if lus is None:
        lus = sorted(data['SPREAD_CLASS'].unique().tolist())

    # If no list of land managements provided, use irrigation status only.
    if lms is None:
        lms = ['dry', 'irr']

    # Prepare column-wise multi-indexed pandas.DataFrame.
    mcolindex = pd.MultiIndex.from_product( [columns, lms, lus]
                                           , names = [ 'DATUM'
                                                     , 'LANDMANAGEMENT'
                                                     , 'LANDUSE' ] )
    index = range(concordance.shape[0])
    df = pd.DataFrame(columns=mcolindex, index=index)

    # Perform merges and put resulting arrays in DataFrame.
    colluirr = [ (col, lu, irr) for col in columns
                                for lu in lus
                                for irr in (0, 1) ]
    for col, lu, irr in colluirr:
        if irr == 0: irrstatus = 'dry'
        else: irrstatus = 'irr'
        mask = ( (data['SPREAD_CLASS'] == lu)
               & (data['IRRIGATED'] == irr) )
        merged = concordance.merge(data[mask], how='left')
        df[col, irrstatus, lu] = merged[col].values

    return df

def exclude(df):
    """Return exclude matrix inferred from passed AGEC mjr-dataframe."""
    # The set of all land-management tyoes.
    lms = {t[1] for t in df.columns}

    # Any economic variable will do. Here, choose `Q1`.
    dfq = df['Q1']

    # Build a tuple of slices, each slice a boolean exclude matrix for a lm.
    slices = tuple( dfq[lm].where(pd.isna, True).where(pd.notna, False)
                    for lm in lms )

    return np.stack(slices)
