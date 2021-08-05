#!/bin/env python3
#
# transitions.py - data about transition costs.
#
# Author: Fjalar de Haan (f.dehaan@deakin.edu.au)
# Created: 2021-04-30
# Last modified: 2021-08-05
#

import os.path

import numpy as np
import pandas as pd
import numpy_financial as npf

import luto.data as data

from luto.tools import timethis

def amortise(cost, rate=0.05, horizon=30):
    """Return amortised `cost` at `rate`interest over `horizon` years."""
    return -1 * npf.pmt(rate, horizon, pv=cost, fv=0, when='begin')

def get_transition_matrices(year, lumap, lmmap):
    """Return t_mrj transition-cost matrices.

    A transition-cost matrix gives the cost of switching a certain cell r to
    a certain land-use j under a certain land-management. The base costs are
    taken from the raw transition costs in the `data` module and additional
    costs are added depending on the land-management (e.g. costs of irrigation
    infrastructure). Switching costs further depend on both the current and the
    future land-use, so the present land-use map is needed.

    Parameters
    ----------

    year : int
        Number of years from base year, counting from zero.
    lumap : numpy.ndarray
        Present land-use map, i.e. highpos (shape=ncells, dtype=int).
    lmmap : numpy.ndarray
        Present land-management map (shape=ncells, dtype=int).

    Returns
    -------

    numpy.ndarray
        t_mrj transition-cost matrices. The m-slices correspond to the
        different land-management versions of the land-use `j` to switch _to_.
        With m==0 conventional dry-land, m==1 conventional irrigated.
    """

    # Raw transition-cost matrix is in AUD/Ha and lexigraphically ordered.
    t_ij = data.TMATRIX.to_numpy()

    # Infer number land-uses and cells from t_ij and lumap matrices.
    nlus = t_ij.shape[0]
    ncells = lumap.shape[0]

    # Transition costs to commodity j at cell r using present lumap (in AUD/ha).
    t_rj = np.stack(tuple(t_ij[lumap[r]] for r in range(ncells)))

    # Areas in hectares for each cell, stacked for each land-use (identical).
    realarea_rj = np.stack((data.REAL_AREA,) * nlus, axis=1).astype(np.float64)

    # Total aq lic costs = aq req [Ml/ha] x area/cell [ha] x lic price [AUD/Ml].
    wr_rj = data.AGEC['WR', 'irr'].to_numpy() # Water required in Ml/ha.
    wp_rj = data.AGEC['WP', 'irr'].to_numpy() # Water licence price in AUD/Ml.
    aqlic_rj = np.nan_to_num(wr_rj * realarea_rj * wp_rj) # The total lic costs.

    # Switching to irr, from and to an irr land-use, may incur licence costs.
    tdelta_toirr_rj = np.zeros((ncells, nlus))
    for r in range(ncells):
        lu = lumap[r]
        lm = lmmap[r]
        # IRR -> DRY / Difference with current licence paid or refunded.
        if lm == 1:
            tdelta_toirr_rj[r] = aqlic_rj[r] - aqlic_rj[r, lu]
        # DRY -> DRY / Licence cost + infrastructure cost @10kAUD/ha.
        else:
            tdelta_toirr_rj[r] = aqlic_rj[r] + (10**4 * realarea_rj[r])

    # Switching to dry, from and to an irr land-use, may incur licence refund.
    tdelta_todry_rj = np.zeros((ncells, nlus))
    for r in range(ncells):
        lu = lumap[r]
        lm = lmmap[r]
        # IRR -> DRY / Current licence refunded.
        if lm == 1:
            tdelta_todry_rj[r] = - aqlic_rj[r, lu]
        # DRY -> DRY / No additional costs.

    # Transition costs in AUD/ha converted to AUD per cell and amortised.
    t_rj_todry = amortise(t_rj * realarea_rj + tdelta_todry_rj)
    t_rj_toirr = amortise(t_rj * realarea_rj + tdelta_toirr_rj)

    # Stack the t_rj matrices into one t_mrj array.
    t_mrj = np.stack((t_rj_todry, t_rj_toirr))

    return t_mrj

def get_transition_matrix_old(year, lumap):
    """Return t_rj transition-cost matrix for `year` and `lumap` in AUD/cell."""

    # Raw transition-cost matrix is in AUD/Ha. Set NaNs to zero.
    t_ij = np.nan_to_num(data.TCOSTMATRIX)


    # Infer number land-uses and cells from t_ij and lumap matrices.
    nlus = t_ij.shape[0]
    ncells = lumap.shape[0]

    # Transition costs to commodity j at cell r using present lumap (in AUD/ha).
    t_rj_audperha = np.stack(tuple(t_ij[lumap[r]] for r in range(ncells)))

    # Areas in hectares for each cell, stacked for each land-use (identical).
    realarea_rj = np.stack((data.REAL_AREA,) * nlus, axis=1)

    # Total aq lic costs = aq req [Ml/ha] x area/cell [ha] x lic price [AUD/Ml].
    wr_rj = data.RAWEC['WR'].to_numpy() # Water required in Ml/ha.
    wp_rj = data.RAWEC['WP'].to_numpy() # Water licence price in AUD/Ml.
    aqlic_rj = np.nan_to_num(wr_rj * realarea_rj * wp_rj) # The total lic costs.

    # Switching from and to an _irr land-use can still incur licence costs.
    tdelta_rj = np.zeros((ncells, nlus))
    for r in range(ncells):
        j = lumap[r]
        if j % 2 == 1: # If it is currently an irrigated land use.
            # Difference with current licence is paid or refunded. TODO: TESTING.
            tdelta_rj[r] = aqlic_rj[r] - aqlic_rj[r, j]
            # # If licence cheaper than now, no pay. If not, pay difference.
            # tdelta_rj[r] = np.where( aqlic_rj[r] <= aqlic_rj[r, j]
                                   # , 0
                                   # , aqlic_rj[r] - aqlic_rj[r, j] )
        else: # If it is currently a non-irrigated land use.
            tdelta_rj[r] = aqlic_rj[r]

    # Transition costs to commodity j at cell r converted to AUD per cell.
    t_rj = t_rj_audperha * realarea_rj + tdelta_rj

    # Amortise the transition costs.
    t_rj = amortise(t_rj)

    return t_rj

if __name__ == '__main__':
    import luto.data as data
    from luto.economics.transitions import *

    lumap = np.load('input/lumap.npy')
    lmmap = np.load('input/lmmap.npy')
    lumapold = np.load('input/lumap-dryirr.npy')

    t_rj = get_transition_matrix_old(0, lumapold)
    t_rj_todry, t_rj_toirr = timethis(get_transition_matrix, 0, lumap, lmmap)

    rabrick = np.stack((data.REAL_AREA,) * 23, axis=1)
    rawbrick = np.stack((data.REAL_AREA,) * 46, axis=1)

    d = (t_rj[:, 1::2] - t_rj_toirr)

    print(d, (d == 0).all())
