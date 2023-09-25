# Copyright 2023 Brett A. Bryan at Deakin University
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
Pure functions to calculate greenhouse gas emissions by lm, lu.
"""

from typing import Dict
import numpy as np
from luto.economics.agricultural.quantity import get_yield_pot, lvs_veg_types
import luto.settings as settings
import luto.tools as tools
from luto.ag_managements import AG_MANAGEMENTS_TO_LAND_USES


def get_ghg_crop( data     # Data object or module.
                , lu       # Land use.
                , lm       # Land management.
                , yr_idx   # Number of years post base-year ('YR_CAL_BASE').
                ):
    """Return crop GHG emissions [tCO2e/cell] of `lu`+`lm` in `yr_idx` as np array.

    `data`: data object/module -- assumes fields like in `luto.data`.
    `lu`: land use (e.g. 'Winter cereals' or 'Beef - natural land').
    `lm`: land management (e.g. 'dry', 'irr').
    `yr_idx`: number of years from base year, counting from zero.
    
    Crop GHG emissions include:
        'CO2E_KG_HA_CHEM_APPL', 
        'CO2E_KG_HA_CROP_MGT', 
        'CO2E_KG_HA_CULTIV', 
        'CO2E_KG_HA_FERT_PROD', 
        'CO2E_KG_HA_HARVEST', 
        'CO2E_KG_HA_IRRIG', 
        'CO2E_KG_HA_PEST_PROD', 
        'CO2E_KG_HA_SOIL_N_SURP', 
        'CO2E_KG_HA_SOWING'
    """
    
    # Check if land-use/land management combination exists (e.g., dryland Pears/Rice do not occur), if not return zeros
    if lu not in data.AGGHG_CROPS[data.AGGHG_CROPS.columns[0][0], lm].columns:
        ghg_t = np.zeros((data.NCELLS))
        
    else:
            
        # Calculate total GHG emissions in kg of CO2eq/ha
        ghg_t = data.AGGHG_CROPS.loc[:, (slice(None), lm, lu)].sum(axis = 1)
        
        # Convert to tonnes of CO2e per ha. 
        ghg_t = ghg_t.to_numpy() / 1000
        
        # Convert to tonnes GHG per cell including resfactor
        ghg_t *= data.REAL_AREA
        
    # Return total greenhouse gas emissions as numpy array.
    return ghg_t


def get_ghg_lvstk( data     # Data object or module.
                 , lu       # Land use.
                 , lm       # Land management.
                 , yr_idx   # Number of years post base-year ('YR_CAL_BASE').
                 ):
    """Return livestock GHG emissions [tCO2e/cell] of `lu`+`lm` in `yr_idx` as np array.

    `data`: data object/module -- assumes fields like in `luto.data`.
    `lu`: land use (e.g. 'Winter cereals' or 'Beef - natural land').
    `lm`: land management (e.g. 'dry', 'irr').
    `yr_idx`: number of years from base year, counting from zero.
    
    Livestock GHG emissions include:    
        'CO2E_KG_HEAD_ENTERIC', 
        'CO2E_KG_HEAD_MANURE_MGT', 
        'CO2E_KG_HEAD_IND_LEACH_RUNOFF', 
        'CO2E_KG_HEAD_DUNG_URINE', 
        'CO2E_KG_HEAD_SEED', 
        'CO2E_KG_HEAD_FODDER', 
        'CO2E_KG_HEAD_FUEL', 
        'CO2E_KG_HEAD_ELEC'
    """
    
    # Get livestock and vegetation type.
    lvstype, vegtype = lvs_veg_types(lu)

    # Get the yield potential, i.e. the total number of heads per hectare.
    yield_pot = get_yield_pot(data, lvstype, vegtype, lm, yr_idx)
    
    # Calculate total GHG emissions in kg CO2e per hectare
    ghg_t = data.AGGHG_LVSTK.loc[:, (lvstype, slice(None))].sum(axis = 1) * yield_pot
    
    # Add pasture irrigation emissions based on emissions associated with hay production.
    if lm == 'irr': 
        ghg_t += data.AGGHG_CROPS['CO2E_KG_HA_CHEM_APPL', 'irr', 'Hay'] + \
                 data.AGGHG_CROPS['CO2E_KG_HA_FERT_PROD', 'irr', 'Hay'] + \
                 data.AGGHG_CROPS['CO2E_KG_HA_IRRIG', 'irr', 'Hay'] + \
                 data.AGGHG_CROPS['CO2E_KG_HA_PEST_PROD', 'irr', 'Hay'] + \
                 data.AGGHG_CROPS['CO2E_KG_HA_SOIL_N_SURP', 'irr', 'Hay'] + \
                 data.AGGHG_CROPS['CO2E_KG_HA_SOWING', 'irr', 'Hay'] 
       
    # Convert to tonnes of CO2e per ha. 
    ghg_t = ghg_t.to_numpy() / 1000
    
    # Convert to tonnes CO2e per cell including resfactor
    ghg_t *= data.REAL_AREA
    
    # Return total greenhouse gas emissions as numpy array.
    return ghg_t


def get_ghg( data    # Data object or module.
           , lu      # Land use.
           , lm      # Land management.
           , yr_idx  # Number of years post base-year ('YR_CAL_BASE').
           ):
    """Return GHG emissions [tCO2e/cell] of `lu`+`lm` in `yr_idx` as np array.

    `data`: data object/module -- assumes fields like in `luto.data`.
    `lu`: land use (e.g. 'Winter cereals').
    `lm`: land management (e.g. 'dry', 'irr').
    `yr_idx`: number of years from base year, counting from zero.
    """
    # If it is a crop, it is known how to get GHG emissions.
    if lu in data.LU_CROPS:
        return get_ghg_crop(data, lu, lm, yr_idx)
    
    # If it is livestock, it is known how to get GHG emissions.
    elif lu in data.LU_LVSTK:
        return get_ghg_lvstk(data, lu, lm, yr_idx)
    
    # If neither crop nor livestock but in LANDUSES it is unallocated land.
    elif lu in data.AGRICULTURAL_LANDUSES:
        return np.zeros(data.NCELLS)
    
    # If it is none of the above, it is not known how to get the GHG emissions.
    else:
        raise KeyError("Land use '%s' not found in data.LANDUSES" % lu)


def get_ghg_transition_penalties(data, lumap) -> np.ndarray:
    """
    Gets the one-off greenhouse gas penalties for transitioning natural land to
    unnatural land. The penalty represents the carbon that is emitted when
    clearing natural land.
    """
    _, ncells, n_ag_lus = data.AG_L_MRJ.shape
    # Set up empty array of penalties
    penalties_rj = np.zeros((ncells, n_ag_lus), dtype=np.float32)
    natural_lu_cells, _ = tools.get_natural_and_unnatural_lu_cells(data, lumap)

    # Calculate penalties and add to g_rj matrix
    penalties_r = (
          data.NATURAL_LAND_T_CO2_HA[natural_lu_cells]
        * data.REAL_AREA[natural_lu_cells]
    )
    for lu in data.LU_UNNATURAL:
        penalties_rj[natural_lu_cells, lu] = penalties_r

    penalties_mrj = np.stack([penalties_rj] * 2)

    return penalties_mrj


def get_ghg_matrix(data, lm, yr_idx):
    """Return g_rj matrix of tCO2e/cell per lu under `lm` in `yr_idx`."""
    
    g_rj = np.zeros((data.NCELLS, len(data.AGRICULTURAL_LANDUSES)))
    for j, lu in enumerate(data.AGRICULTURAL_LANDUSES):
        g_rj[:, j] = get_ghg(data, lu, lm, yr_idx)
        
    # Make sure all NaNs are replaced by zeroes.
    g_rj = np.nan_to_num(g_rj)

    return g_rj


def get_ghg_matrices(data, yr_idx):
    """Return g_mrj matrix of GHG emissions per cell as 3D Numpy array."""

    g_mrj = np.stack(tuple( get_ghg_matrix(data, lm, yr_idx)
                           for lm in data.LANDMANS ))
    return g_mrj



def get_ghg_limits(data):
    """Return greenhouse gas emissions limits as specified in settings.py."""
    
    # If using GHG emissions as a percentage of 2010 agricultural emissions
    if settings.GHG_LIMITS_TYPE == 'percentage':
        # Get GHG emissions from agriculture for 2010 in tCO2e per cell in mrj format.
        yr_idx = 0
        g_mrj = get_ghg_matrices(data, yr_idx)
        
        # Calculate total greenhouse gas emissions of current land-use and land management.
        ghg_limits = (g_mrj * data.AG_L_MRJ).sum() * (1 - settings.GHG_REDUCTION_PERCENTAGE / 100)
    
    # If using GHG emissions as a total tonnage of CO2e
    elif settings.GHG_LIMITS_TYPE == 'tonnes':
        ghg_limits = settings.GHG_LIMITS
        
    else: 
        print('Unknown GHG limit type...')
        exit()
        
    return ghg_limits


def get_asparagopsis_effect_g_mrj(data, yr_idx):
    """
    Applies the effects of using asparagopsis to the GHG data
    for all relevant agr. land uses.
    """
    land_uses = AG_MANAGEMENTS_TO_LAND_USES['Asparagopsis taxiformis']
    year = 2010 + yr_idx

    # Set up the effects matrix
    new_g_mrj = np.zeros((data.NLMS, data.NCELLS, len(land_uses))).astype(np.float32)

    # Update values in the new matrix, taking into account the CH4 reduction of asparagopsis
    for lu_idx, lu in enumerate(land_uses):
        ch4_reduction_perc = 1 - data.ASPARAGOPSIS_DATA[lu].loc[year, "MitEff_CH4"]

        if ch4_reduction_perc != 0:
            for lm in data.LANDMANS:
                if lm == 'irr':
                    m = 0
                else:
                    m = 1

                # Subtract enteric fermentation emissions multiplied by reduction multiplier
                lvstype, vegtype = lvs_veg_types(lu)

                yield_pot = get_yield_pot(data, lvstype, vegtype, lm, yr_idx)

                reduction_amnt = (
                    data.AGGHG_LVSTK[lvstype, "CO2E_KG_HEAD_ENTERIC"].to_numpy()
                    * yield_pot
                    * ch4_reduction_perc
                    / 1000            # convert to tonnes
                    * data.REAL_AREA  # adjust for resfactor
                )
                new_g_mrj[m, :, lu_idx] = -reduction_amnt

    return new_g_mrj


def get_precision_agriculture_effect_g_mrj(data, yr_idx):
    """
    Applies the effects of using precision agriculture to the GHG data
    for all relevant agr. land uses.
    """
    land_uses = AG_MANAGEMENTS_TO_LAND_USES['Precision Agriculture']
    year = 2010 + yr_idx

    # Set up the effects matrix
    new_g_mrj = np.zeros((data.NLMS, data.NCELLS, len(land_uses))).astype(np.float32)

    # Update values in the new matrix
    for lu_idx, lu in enumerate(land_uses):
        lu_data = data.PRECISION_AGRICULTURE_DATA[lu]

        for lm in data.LANDMANS:
            if lm == 'dry':
                m = 0
            else:
                m = 1
        
            for co2e_type in [
                'CO2E_KG_HA_CHEM_APPL',
                'CO2E_KG_HA_CROP_MGT',
                'CO2E_KG_HA_PEST_PROD',
                'CO2E_KG_HA_SOIL_N_SURP',
            ]:
                # Some crop land uses do not emit any GHG emissions, e.g. 'Rice'
                if lu not in data.AGGHG_CROPS[data.AGGHG_CROPS.columns[0][0], lm].columns:
                    continue

                reduction_perc = 1 - lu_data.loc[year, co2e_type]
                if reduction_perc != 0:
                    reduction_amnt = (
                        np.nan_to_num(data.AGGHG_CROPS[co2e_type, lm, lu].to_numpy(), 0)
                        * reduction_perc
                        / 1000            # convert to tonnes
                        * data.REAL_AREA  # adjust for resfactor
                    )
                    new_g_mrj[m, :, lu_idx] -= reduction_amnt

    if np.isnan(new_g_mrj).any():
        raise ValueError("Error in data: NaNs detected in agricultural management options' GHG effect matrix.")

    return new_g_mrj


def get_ecological_grazing_effect_g_mrj(data, yr_idx):
    """
    Applies the effects of using ecological grazing to the GHG data
    for all relevant agr. land uses.
    """
    land_uses = AG_MANAGEMENTS_TO_LAND_USES['Precision Agriculture']
    year = 2010 + yr_idx

    # Set up the effects matrix
    new_g_mrj = np.zeros((data.NLMS, data.NCELLS, len(land_uses))).astype(np.float32)

    # Update values in the new matrix
    for lu_idx, lu in enumerate(land_uses):
        lu_data = data.PRECISION_AGRICULTURE_DATA[lu]

        for lm in data.LANDMANS:
            if lm == 'dry':
                m = 0
            else:
                m = 1
        
            # Some crop land uses do not emit any GHG emissions, e.g. 'Rice'
            if lu not in data.AGGHG_CROPS[data.AGGHG_CROPS.columns[0][0], lm].columns:
                continue

            reduction_perc = 1 - lu_data.loc[year, 'CO2E_KG_HEAD_IND_LEACH_RUNOFF']
            if reduction_perc != 0:
                reduction_amnt = (
                    np.nan_to_num(data.AGGHG_CROPS['CO2E_KG_HEAD_IND_LEACH_RUNOFF', lm, lu].to_numpy(), 0)
                    * reduction_perc
                    / 1000            # convert to tonnes
                    * data.REAL_AREA  # adjust for resfactor
                )
                new_g_mrj[m, :, lu_idx] = -reduction_amnt

    return new_g_mrj


def get_agricultural_management_ghg_matrices(data, g_mrj, yr_idx) -> Dict[str, np.ndarray]:
    asparagopsis_data = get_asparagopsis_effect_g_mrj(data, yr_idx)
    precision_agriculture_data = get_precision_agriculture_effect_g_mrj(data, yr_idx)
    eco_grazing_data = get_ecological_grazing_effect_g_mrj(data, yr_idx)

    ag_management_data = {
        'Asparagopsis taxiformis': asparagopsis_data,
        'Precision Agriculture': precision_agriculture_data,
        'Ecological Grazing': eco_grazing_data,
    }

    return ag_management_data
