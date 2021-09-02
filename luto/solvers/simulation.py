#!/bin/env python3
#
# simulation.py - maintain state and handle iteration and data-view changes.
#
# This module functions as a singleton class. It is intended to be the _only_
# part of the model that has 'global' varying state.
#
# Author: Fjalar de Haan (f.dehaan@deakin.edu.au)
# Created: 2021-08-06
# Last modified: 2021-09-02
#

import numpy as np
from scipy.interpolate import interp1d

import luto.data as bdata
from luto.data.economic import exclude
from luto.economics.cost import get_cost_matrices
from luto.economics.quantity import get_quantity_matrices
from luto.economics.transitions import ( get_transition_matrices
                                       , get_exclude_matrices )
from luto.solvers.solver import solve


class Data():
    """Provide simple object to mimic 'data' namespace from `luto.data`."""

    def __init__( self
                , lumap # Land-use map from which spatial domain is inferred.
                , resfactor # Spatial course-graining factor.
                ):
        """Initialise Data object based on land-use map `lumap`."""

        # Most data is taken over as is.
        for key in bdata.__dict__:
            if key.isupper():
             self.__dict__[key] = bdata.__dict__[key]
        self.LU2PR = bdata.LU2PR
        self.PR2CM = bdata.PR2CM

        # Mask from lumap.
        self.mask_lu_code = -1 # The lu code to exclude.
        self.lumask = lumap != self.mask_lu_code # True means _included_.
        # Mask from resfactor is superimposed on lumap mask.
        if resfactor != 1:
            self.rfmask = resmask(bdata.LUMAP, resfactor)
            self.mask = self.lumask * self.rfmask
        else:
            self.mask = self.lumask

        # Spatial data is sub-setted based on the above masks.
        self.NCELLS = self.mask.sum()
        self.EXCLUDE = bdata.EXCLUDE[:, self.mask, :]
        self.AGEC_CROPS = bdata.AGEC_CROPS.iloc[self.mask]
        self.AGEC_LVSTK = bdata.AGEC_LVSTK.iloc[self.mask]
        self.REAL_AREA = bdata.REAL_AREA[self.mask]
        self.LUMAP = bdata.LUMAP[self.mask]
        self.LMMAP = bdata.LMMAP[self.mask]
        self.WATER_REQUIRED = bdata.WATER_REQUIRED[self.mask]
        self.WATER_LICENCE_PRICE = bdata.WATER_LICENCE_PRICE[self.mask]
        self.WATER_DELIVERY_PRICE = bdata.WATER_DELIVERY_PRICE[self.mask]
        self.FEED_REQ = bdata.FEED_REQ[self.mask]
        self.PASTURE_KG_DM_HA = bdata.PASTURE_KG_DM_HA[self.mask]
        self.SAFE_PUR_MODL = bdata.SAFE_PUR_MODL[self.mask]
        self.SAFE_PUR_NATL = bdata.SAFE_PUR_NATL[self.mask]

# Placeholder for module-global data object. To be set by `prep()`.
data = None

# Is the model ready for the next simulation step? Set by `prep()`.
ready = False

# Optionally course grain spatial domain. (Set to 1 to bypass.)
resfactor = 1

# Containers for simulation output. First entry from base data.
lumaps = [bdata.LUMAP]
lmmaps = [bdata.LMMAP]
shapes = []

def get_year():
    """Return the current time step, i.e. number of years since ANNUM."""
    return len(lumaps) - 1

def is_ready():
    """Return True if model ready for next simulation step, False otherwise."""
    return ready

def get_resfactor():
    """Return the resfactor (spatial course-graining factor)."""
    return resfactor

def set_resfactor(factor):
    global resfactor
    resfactor = factor

def get_shape(year=None):
    """Return the shape (NLMS, NCELLS, NLUS) of the problem at `year`."""
    if year is None:
        return data.NLMS, data.NCELLS, data.NLUS
    else:
        return shapes[year]

# Obtain local versions of get_*_matrices.
def get_c_mrj():
    return get_cost_matrices(data, get_year())
def get_q_mrp():
    return get_quantity_matrices(data, get_year())
def get_t_mrj():
    return get_transition_matrices( data
                                  , get_year()
                                  , lumaps[-1][data.mask]
                                  , lmmaps[-1][data.mask]
                                  )
def get_x_mrj():
    return get_exclude_matrices(data, lumaps[-1][data.mask])

def reconstitute(l_map, filler=-1):
    """Return l?map reconstituted to original size spatial domain."""
    indices = np.cumsum(data.lumask) - 1
    return np.where(data.lumask, l_map[indices], filler)

def uncoursify(lxmap):
    """Restore the l?map to pre-resfactored extent."""

    if data.mask.sum() != lxmap.shape[0]:
        raise ValueError("Map and mask shapes do not match.")
    else:
        # Array with all x-coordinates on the larger map.
        domain = np.arange(data.mask.shape[0])
        # Array of x-coordinates on larger map of entries in lxmap.
        xs = domain[data.mask]
        # Instantiate an interpolation function.
        f = interp1d(xs, lxmap, kind='nearest', fill_value='extrapolate')
        # The uncoursified map is obtained by interpolating the missing values.
        return f(domain).astype(np.int8)

def resmask(lxmap, resfactor, sampling='linear'):
    if sampling == 'linear':
        xs = np.zeros_like(lxmap)
        xs[::resfactor] = 1
        return xs.astype(bool)
    elif sampling == 'quadratic':
        ...
        # nlum_mask = data.NLUM_MASK.copy()
        # rf_nlum = nlum_mask[::resfactor, ::resfactor]
    else:
        raise ValueError("Unknown sampling style: %s" % sampling)

def prep():
    """Prepare for the next simulation step."""
    global data, ready
    data = Data(lumaps[-1], resfactor)
    ready = True

def step( d_j # Demands.
        , p   # Penalty level.
        ):
    """Solve the upcoming time step (year)."""
    global ready
    if not is_ready(): prep()

    shapes.append(get_shape())

    # Magic.
    lumap, lmmap = solve( get_t_mrj()
                        , get_c_mrj()
                        , get_q_mrp()
                        , d_j
                        , p
                        , get_x_mrj()
                        , data.LU2PR
                        , data.PR2CM )

    # First undo the doings of resfactor.
    lumap = uncoursify(lumap)
    lmmap = uncoursify(lmmap)

    # Then put the excluded land-use and land-man back where they were.
    lumaps.append(reconstitute(lumap, filler=data.mask_lu_code))
    lmmaps.append(reconstitute(lmmap, filler=0))

    ready = False

def info():
    """Return information about state of the simulation."""

    print( "Current time step (year):"
         , str(get_year())
         , "(" + str(bdata.ANNUM + get_year()) + ")")

    if resfactor == 1:
        print("Resfactor set at 1. Spatial course graining bypassed.")
    else:
        print( "Resfactor set at %i." % resfactor
             , "Sampling one of every %i cells in spatial domain." % resfactor )


    if get_year() > 0:
        print()
        print("Year", "\t", "Cells [#]", "\t", "Cells [%]")
    for year in range(get_year()):
        ncells = get_shape(year)[1]
        percentage = 100 * ncells / bdata.NCELLS
        print( year + bdata.ANNUM
             , "\t"
             , ncells, "\t\t"
             , "%.2f%%" % percentage )
        if year == get_year()-1: print()

    if is_ready():
        print("Simulation is ready to solve next time step. Run `step()`")
    else:
        print("Simulation is not ready to solve next time step. Run `prep()`.")

def get_results(year=None):
    """Return the simulation results for `year` or all if `year is None`."""
    if year is None:
        return np.stack(lumaps), np.stack(lmmaps)
    else:
        return lumaps[year], lmmaps[year]

def demands():
    """Return demands based on current production."""
    if not is_ready(): prep()
    lumap = data.LUMAP
    lmmap = data.LMMAP
    _, _, nlus = get_shape()
    q_mrj = get_q_mrj()

    d_j = np.zeros(nlus) # Prepare the demands array - one cell per LU.
    for j in range(nlus):
        # The demand for LU j is the dot product of the yield vector with a
        # summation vector indicating where LU actually occurs as per SID array.
        d_j[j] = ( q_mrj[0].T[j] @ np.where((lumap==j) & (lmmap==0), 1, 0)
                + q_mrj[1].T[j] @ np.where((lumap==j) & (lmmap==1), 1, 0) )

    return d_j
