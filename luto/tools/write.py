# Copyright 2022 Fjalar J. de Haan and Brett A. Bryan at Deakin University
#
# This file is part of LUTO 2.0.
#
# LUTO 2.0 is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# LUTO 2.0 is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# LUTO 2.0. If not, see <https://www.gnu.org/licenses/>.

"""
Writes model output and statistics to files.
"""


import os
from datetime import datetime

import numpy as np
import pandas as pd
import luto.settings as settings
from luto.tools import get_production
from luto.tools.spatializers import *
from luto.tools.compmap import *
from luto.economics.water import *
from luto.economics.ghg import *


def get_path():
    """Create a folder for storing outputs and return folder name."""
    
    path = datetime.today().strftime('%Y_%m_%d__%H_%M_%S')
    path = 'output/' + path 
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def write_outputs(sim, year, d_c, path):
    write_files(sim, path)
    write_production(sim, year, d_c, path)
    write_water(sim, year, path)
    write_ghg(sim, year, path)


def write_files(sim, path):
    """Writes numpy arrays and geotiffs to file"""
    
    print('\nWriting outputs to', path, '\n')
    
    for year in sim.lumaps:
        
        # Save raw decision variables (boolean array).
        X_mrj_fname = 'X_mrj_' + str(year) + '.npy'
        np.save(os.path.join(path, X_mrj_fname), sim.dvars[year])
        
        # Write out raw numpy arrays for land-use and land management
        lumap_fname = 'lumap_' + str(year) + '.npy'
        lmmap_fname = 'lmmap_' + str(year) + '.npy'
        np.save(os.path.join(path, lumap_fname), sim.lumaps[year])
        np.save(os.path.join(path, lmmap_fname), sim.lmmaps[year])

        # Recreate full resolution 2D arrays and write out GeoTiffs for land-use and land management
        lumap, lmmap = recreate_2D_maps(sim, year)
        
        lumap_fname = 'lumap_' + str(year) + '.tiff'
        lmmap_fname = 'lmmap_' + str(year) + '.tiff'
        write_gtiff(lumap, os.path.join(path, lumap_fname))
        write_gtiff(lmmap, os.path.join(path, lmmap_fname))


def write_production(sim, year, d_c, path):
    """Write out land-use and production data"""
    
    # Calculate data for quantity comparison between base year and target year
    prod_base = get_production(sim, sim.data.ANNUM)     # Get commodity quantities produced in 2010 
    prod_targ = get_production(sim, year)               # Get commodity quantities produced in target year
    demands = d_c[year - sim.data.ANNUM]                # Get commodity demands for target year
    abs_diff = prod_targ - demands                      # Diff between target year production and demands in absolute terms (i.e. tonnes etc)
    prop_diff = (abs_diff / prod_targ) * 100            # Diff between target year production and demands in relative terms (i.e. %)
    
    # Write to pandas dataframe
    df = pd.DataFrame()
    df['Commodity'] = sim.data.COMMODITIES
    df['Prod_base_year (tonnes, KL)'] = prod_base
    df['Prod_targ_year (tonnes, KL)'] = prod_targ
    df['Demand (tonnes, KL)'] = demands
    df['Abs_diff (tonnes, KL)'] = abs_diff
    df['Prop_diff (%)'] = prop_diff
    df.to_csv(os.path.join(path, 'quantity_comparison.csv'), index = False)

    # LUS = ['Non-agricultural land'] + sim.data.LANDUSES
    ctlu, swlu = crossmap(sim.lumaps[sim.data.ANNUM], sim.lumaps[year], sim.data.LANDUSES)
    ctlm, swlm = crossmap(sim.lmmaps[sim.data.ANNUM], sim.lmmaps[year])

    cthp, swhp = crossmap_irrstat( sim.lumaps[sim.data.ANNUM], sim.lmmaps[sim.data.ANNUM]
                                 , sim.lumaps[year], sim.lmmaps[year]
                                 , sim.data.LANDUSES )

    ctlu.to_csv(os.path.join(path, 'crosstab-lumap.csv'))
    ctlm.to_csv(os.path.join(path, 'crosstab-lmmap.csv'))

    swlu.to_csv(os.path.join(path, 'switches-lumap.csv'))
    swlm.to_csv(os.path.join(path, 'switches-lmmap.csv'))

    cthp.to_csv(os.path.join(path, 'crosstab-irrstat.csv'))
    swhp.to_csv(os.path.join(path, 'switches-irrstat.csv'))


def write_water(sim, year, path):
    """Calculate water use totals. Takes a simulation object, a numeric
       target year (e.g., 2030), and an output path as input."""
    
    # Get 2010 water requirement in mrj format
    w_mrj = get_wreq_matrices(sim.data, 0) 

    # Prepare a data frame.
    df = pd.DataFrame( columns=[ 'REGION_ID'
                               , 'REGION_NAME'
                               , 'WATER_USE_LIMIT_ML'
                               , 'TOT_WATER_REQ_ML'
                               , 'ABS_DIFF_ML'
                               , 'PROPORTION_%'  ] )

    # Get water use limits used as constraints in model
    wuse_limits = get_wuse_limits(sim.data)


    # Set up data for river regions or drainage divisions
    if settings.WATER_REGION_DEF == 'RR':
        regions = settings.WATER_RIVREGS
        region_id = sim.data.RIVREG_ID
        region_dict = sim.data.RIVREG_DICT
        
    elif settings.WATER_REGION_DEF == 'DD':
        regions = settings.WATER_DRAINDIVS
        region_id = sim.data.DRAINDIV_ID
        region_dict = sim.data.DRAINDIV_DICT
        
    else: print('Incorrect option for WATER_REGION_DEF in settings')
    
    # Loop through specified water regions
    for i, region in enumerate(regions):
        
        # Get indices of cells in region
        ind = np.flatnonzero(region_id == region).astype(np.int32)
        
        # Calculate the 2010 water requirements by agriculture for region.
        wreq_reg = (          w_mrj[:, ind, :] * 
                    sim.dvars[year][:, ind, :]
                   ).sum()
        
        # Calculate absolute and proportional difference between water use target and actual water use
        wul = wuse_limits[i][1]
        abs_diff = wreq_reg - wul
        if wul > 0:
            prop_diff = (wreq_reg / wul) * 100
        else:
            prop_diff = np.nan
        
        # Add to dataframe
        df.loc[i] = ( region
                    , region_dict[region]
                    , wul
                    , wreq_reg 
                    , abs_diff
                    , prop_diff )
    
    # Write to CSV with 2 DP
    df.to_csv( os.path.join(path, 'water_demand_vs_use.csv')
             , index = False
             , float_format = '{:0,.2f}'.format)
    

def write_ghg(sim, year, path):
    """Calculate total GHG emissions. Takes a simulation object, a numeric
       target year (e.g., 2030), and an output path as input."""
    
    # Get greenhouse gas emissions in mrj format
    g_mrj = get_ghg_matrices(sim.data, year) 

    # Prepare a data frame.
    df = pd.DataFrame( columns=[ 'GHG_EMISSIONS_LIMIT_TCO2e'
                               , 'GHG_EMISSIONS_TCO2e' ] )

    # Get GHG emissions limits used as constraints in model
    ghg_limits = get_ghg_limits(sim.data)

    # Calculate the GHG emissions from agriculture for year.
    ghg_emissions = ( g_mrj * sim.dvars[year] ).sum()
    
    # Add to dataframe
    df.loc[0] = ("{:,.0f}".format(ghg_limits), "{:,.0f}".format(ghg_emissions))
    
    # Save to file
    df.to_csv(os.path.join(path, 'GHG_emissions.csv'), index = False)