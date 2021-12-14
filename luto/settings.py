#!/bin/env python3
#
# settings.py - neoLUTO settings.
#
# Author: Fjalar de Haan (f.dehaan@deakin.edu.au)
# Created: 2021-08-04
# Last modified: 2021-12-14
#

import os

# ---------------------------------------------------------------------------- #
# Directories.                                                                 #
# ---------------------------------------------------------------------------- #

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
DATA_DIR = '../../data/neoluto-data/new-data-and-domain'

# ---------------------------------------------------------------------------- #
# Parameters.                                                                  #
# ---------------------------------------------------------------------------- #

# Environmental constraint settings. In general there is some sort of 'cap'
# ('hard', 'soft' or 'none') and an optional requirement to further minimise.

# Water:
WATER_CONSTRAINT_TYPE = 'hard' # or 'soft' or None.
WATER_CONSTRAINT_MINIMISE = False # or True. Whether to also minimise.
WATER_CONSTRAINT_WEIGHT = 1.0 # Minimisation weight in objective function.
WATER_YIELD_STRESS_FRACTION = 0.4 # 3.0 # Water stress if yields below this fraction.
WATER_DRAINDIVS = ['Murray-Darling Basin'] # Drainage divisions to take into account.

# Climate change assumptions.
RCP = 'rcp4p5' # Representative Concentration Pathway string identifier.

