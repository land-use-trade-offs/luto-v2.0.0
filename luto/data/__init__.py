#!/bin/env python3
#
# __init__.py
#
# Author: Fjalar de Haan (f.dehaan@deakin.edu.au)
# Created: 2021-03-22
# Last modified: 2021-08-18
#

import os

import pandas as pd
import numpy as np

from luto.settings import INPUT_DIR, OUTPUT_DIR
from luto.data.economic import exclude

# Load the agro-economic data (constructed w/ fns from data.economic module).
fpath = os.path.join(INPUT_DIR, "agec-crops-c9.hdf5")
AGEC_CROPS = pd.read_hdf(fpath, 'agec_crops')
fpath = os.path.join(INPUT_DIR, "agec-lvstk-c9.hdf5")
AGEC_LVSTK = pd.read_hdf(fpath, 'agec_lvstk')

# Derive NCELLS (number of spatial cells) from AGEC.
NCELLS, = AGEC_CROPS.index.shape

# Read in lexicographically ordered list of land uses.
LANDUSES = np.load(os.path.join(INPUT_DIR, 'landuses.npy')).tolist()
LANDUSES.remove('Non-agricultural land') # Remove this non land-use.
LANDUSES.sort() # Ensure lexicographic order.
NLUS = len(LANDUSES)

# Some useful sub-sets of the land uses.
LU_CROPS = [ lu for lu in LANDUSES if 'Beef' not in lu
                                and 'Sheep' not in lu
                                and 'Dairy' not in lu
                                and 'Unallocated' not in lu
                                and 'Non-agricultural' not in lu ]
LU_LVSTK = [ lu for lu in LANDUSES if 'Beef' in lu
                                or 'Sheep' in lu
                                or 'Dairy' in lu ]

# Derive LANDMANS (land-managements) from AGEC.
LANDMANS = {t[1] for t in AGEC_CROPS.columns} # Set comp., unique entries.
LANDMANS = list(LANDMANS) # Turn into list.
LANDMANS.sort() # Ensure lexicographic order.
NLMS = len(LANDMANS)

# List of products. Everything upper case to avoid mistakes.
PR_CROPS = [s.upper() for s in LU_CROPS]
PR_LVSTK = [ ('' if 'DAIRY' in s.upper() else p+' ') + s.upper()
             for s in LU_LVSTK
             for p in ['LIVEXPORT', 'DOMCONSUM'] ]
PR_LVSTK += [ 'WOOL ' + s.upper() for s in LU_LVSTK if 'SHEEP' in s.upper() ]
PRODUCTS = PR_CROPS + PR_LVSTK
PRODUCTS.sort() # Ensure lexicographic order.


# Actual hectares per cell, including projection corrections.
REAL_AREA = np.load(os.path.join(INPUT_DIR, 'real-area.npy'))

# Initial (2010) land-use map.
LUMAP = np.load(os.path.join(INPUT_DIR, 'lumap.npy'))

# Initial (2010) land-man map.
LMMAP = np.load(os.path.join(INPUT_DIR, 'lmmap.npy'))

# The base year, i.e. year == 0.
ANNUM = 2010

# ---------------------------------- #
# Temporal and spatio-temporal data. #
# ---------------------------------- #

# Yield increases.
fpath = os.path.join(INPUT_DIR, "yieldincreases-c9.hdf5")
YIELDINCREASE = pd.read_hdf(fpath, 'yieldincreases')

# Climate damages to pastures and dryland as NYEARS x NCELLS shaped bricks.
AG_PASTURE_DAMAGE = np.load(os.path.join(INPUT_DIR, 'ag-pasture-damage.npy'))
AG_DRYLAND_DAMAGE = np.load(os.path.join(INPUT_DIR, 'ag-dryland-damage.npy'))

# Price paths.
price_paths = pd.read_csv(os.path.join(INPUT_DIR, 'pricepaths.csv'))
DIESEL_PRICE_PATH = price_paths['diesel_price_path']


# --------------- #
# All other data. #
# --------------- #

# Raw transition cost matrix. In AUD/ha and ordered lexicographically.
fpath = os.path.join(INPUT_DIR, 'tmatrix.csv')
TMATRIX = pd.read_csv(fpath, index_col=0)
TMATRIX = TMATRIX.sort_index(axis='index').sort_index(axis='columns')

# Boolean x_mrj matrix with allowed land uses j for each cell r under lm.
X_MRJ = exclude(AGEC_CROPS)
