import numpy as np
from luto.settings import NON_AG_LAND_USES

from luto.data import Data
from luto import tools


def get_w_net_yield_matrix_env_planting(data: Data) -> np.ndarray:
    """
    Get water requirements vector of environmental plantings.

    To get the water requirements of environmental plantings, subtract the baseline 
    water yields from the shallow-rooted water yields in the data. This represents
    how much water would be used if modified (i.e., cleared) land area was reforested
    with native pre-European vegetation communities (WATER_YIELD_HIST_NL). Pre-European 
    communities include both deep-rooted (i.e., forests/woodlands) and shallow-rooted 
    communities - natural vegetation is not all deep-rooted.

    Returns
    -------
    1-D array, indexed by cell.
    """
    # Water yield
    # w_yield_dr = data.get_water_dr_yield_for_yr_idx(yr_idx)
    # w_yield_sr = data.get_water_sr_yield_for_yr_idx(yr_idx)
    # w_yield_nl = data.get_water_nl_yield_for_yr_idx(yr_idx, w_yield_dr, w_yield_sr)
    # wyield = w_yield_nl * data.REAL_AREA
    wyield = data.WATER_YIELD_HIST_NL * data.REAL_AREA
    return wyield


def get_w_net_yield_matrix_carbon_plantings_block(data: Data) -> np.ndarray:
    """
    Get water requirements vector of carbon plantings (block arrangement).

    To get the water requirements of carbon plantings, subtract the deep-rooted 
    water yields from the shallow-rooted water yields in the data. This represents
    how much water would be used if modified (i.e., cleared) land area was reforested
    with wall-to-wall deep-rooted tree species (WATER_YIELD_HIST_DR). The assumption 
    here is that plantations are all deep-rooted and hence use more water.
    
    Returns
    -------
    1-D array, indexed by cell.
    """
    # Water yield
    # w_yield_dr = data.get_water_dr_yield_for_yr_idx(yr_idx)
    # wyield = w_yield_dr * data.REAL_AREA
    wyield = data.WATER_YIELD_HIST_DR * data.REAL_AREA
    return wyield


def get_w_net_yield_matrix_rip_planting(data: Data) -> np.ndarray:
    """
    Get water requirements vector of riparian plantings.

    To get the water requirements of riparian plantings, subtract the deep-rooted
    water yields from the shallow-rooted water yields in the data.

    Note: this is the same as for environmental plantings.

    Returns
    -------
    1-D array, indexed by cell.
    """
    return get_w_net_yield_matrix_env_planting(data)


def get_w_net_yield_agroforestry_base(data: Data) -> np.ndarray:
    """
    Get water requirements vector of agroforestry.

    To get the water requirements of agroforestry, subtract the baseline
    water yields from the shallow-rooted water yields in the data.

    Note: this is the same as for environmental plantings.

    Returns
    -------
    1-D array, indexed by cell.
    """
    return get_w_net_yield_matrix_env_planting(data)


def get_wreq_sheep_agroforestry(
    data: Data, 
    ag_w_mrj: np.ndarray, 
    agroforestry_x_r: np.ndarray
) -> np.ndarray:
    """
    Parameters
    ------
    data: Data object.
    ag_w_mrj: agricultural water requirements matrix.
    agroforestry_x_r: Agroforestry exclude matrix.

    Returns
    ------
    Numpy array indexed by r
    """
    sheep_j = tools.get_sheep_code(data)

    # Only use the dryland version of sheep
    sheep_w_net_yield = ag_w_mrj[0, :, sheep_j]
    base_agroforestry_w_net_yield = get_w_net_yield_agroforestry_base(data)

    # Calculate contributions and return the sum
    agroforestry_contr = base_agroforestry_w_net_yield * agroforestry_x_r
    sheep_contr = sheep_w_net_yield * (1 - agroforestry_x_r)
    return agroforestry_contr + sheep_contr


def get_wreq_beef_agroforestry(
    data: Data, 
    ag_w_mrj: np.ndarray, 
    agroforestry_x_r: np.ndarray
) -> np.ndarray:
    """
    Parameters
    ------
    data: Data object.
    ag_w_mrj: agricultural wreq matrix.
    agroforestry_x_r: Agroforestry exclude matrix.

    Returns
    ------
    Numpy array indexed by r
    """
    beef_j = tools.get_beef_code(data)

    # Only use the dryland version of beef
    beef_w_net_yield = ag_w_mrj[0, :, beef_j]
    base_agroforestry_w_net_yield = get_w_net_yield_agroforestry_base(data)

    # Calculate contributions and return the sum
    agroforestry_contr = base_agroforestry_w_net_yield * agroforestry_x_r
    beef_contr = beef_w_net_yield * (1 - agroforestry_x_r)
    return agroforestry_contr + beef_contr


def get_wreq_carbon_plantings_belt_base(data) -> np.ndarray:
    """
    Get water requirements vector of carbon plantings (belt arrangement).

    Note: this is the same as for carbon plantings.

    Returns
    -------
    1-D array, indexed by cell.
    """
    return get_w_net_yield_matrix_carbon_plantings_block(data)


def get_wreq_sheep_carbon_plantings_belt(
    data: Data, 
    ag_w_mrj: np.ndarray, 
    cp_belt_x_r: np.ndarray
) -> np.ndarray:
    """
    Parameters
    ------
    data: Data object.
    ag_w_mrj: agricultural water requirements matrix.
    cp_belt_x_r: Carbon plantings belt exclude matrix.

    Returns
    ------
    Numpy array indexed by r
    """
    sheep_j = tools.get_sheep_code(data)

    # Only use the dryland version of sheep
    sheep_w_net_yield = ag_w_mrj[0, :, sheep_j]
    base_cp_w_net_yield = get_wreq_carbon_plantings_belt_base(data)

    # Calculate contributions and return the sum
    cp_contr = base_cp_w_net_yield * cp_belt_x_r
    sheep_contr = sheep_w_net_yield * (1 - cp_belt_x_r)
    return cp_contr + sheep_contr


def get_wreq_beef_carbon_plantings_belt(
    data: Data, 
    ag_w_mrj: np.ndarray, 
    cp_belt_x_r: np.ndarray
) -> np.ndarray:
    """
    Parameters
    ------
    data: Data object.
    ag_w_mrj: agricultural water requirements matrix.
    cp_belt_x_r: Carbon plantings belt exclude matrix.

    Returns
    ------
    Numpy array indexed by r
    """
    beef_j = tools.get_beef_code(data)

    # Only use the dryland version of beef
    beef_w_net_yield = ag_w_mrj[0, :, beef_j]
    base_cp_w_net_yield = get_wreq_carbon_plantings_belt_base(data)

    # Calculate contributions and return the sum
    cp_contr = base_cp_w_net_yield * cp_belt_x_r
    beef_contr = beef_w_net_yield * (1 - cp_belt_x_r)
    return cp_contr + beef_contr


def get_wreq_matrix_beccs(data) -> np.ndarray:
    """
    Get water requirements vector of BECCS.

    Note: this is the same as for carbon plantings.

    Returns
    -------
    1-D array, indexed by cell.
    """
    return get_w_net_yield_matrix_carbon_plantings_block(data)


def get_w_net_yield_matrix(data: Data, ag_w_mrj: np.ndarray, lumap: np.ndarray) -> np.ndarray:
    """
    Get the water requirements matrix for all non-agricultural land uses.

    Parameters
    ----------
    data : object
        The data object containing necessary information for calculating the water requirements.

    Returns
    -------
    np.ndarray
        The water requirements matrix for all non-agricultural land uses.
        Indexed by (r, k) where r is the cell index and k is the non-agricultural land usage index.
    """
    agroforestry_x_r = tools.get_exclusions_agroforestry_base(data, lumap)
    cp_belt_x_r = tools.get_exclusions_carbon_plantings_belt_base(data, lumap)

    non_agr_wreq_matrices = {use: np.zeros((data.NCELLS, 1)) for use in NON_AG_LAND_USES}

    # reshape each non-agricultural matrix to be indexed (r, k) and concatenate on the k indexing
    if NON_AG_LAND_USES['Environmental Plantings']:
        non_agr_wreq_matrices['Environmental Plantings'] = get_w_net_yield_matrix_env_planting(data).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['Riparian Plantings']:
        non_agr_wreq_matrices['Riparian Plantings'] = get_w_net_yield_matrix_rip_planting(data).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['Sheep Agroforestry']:
        non_agr_wreq_matrices['Sheep Agroforestry'] = get_wreq_sheep_agroforestry(data, ag_w_mrj, agroforestry_x_r).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['Beef Agroforestry']:
        non_agr_wreq_matrices['Beef Agroforestry'] = get_wreq_beef_agroforestry(data, ag_w_mrj, agroforestry_x_r).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['Carbon Plantings (Block)']:
        non_agr_wreq_matrices['Carbon Plantings (Block)'] = get_w_net_yield_matrix_carbon_plantings_block(data).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['Sheep Carbon Plantings (Belt)']:
        non_agr_wreq_matrices['Sheep Carbon Plantings (Belt)'] = get_wreq_sheep_carbon_plantings_belt(data, ag_w_mrj, cp_belt_x_r).reshape((data.NCELLS, 1))
    
    if NON_AG_LAND_USES['Beef Carbon Plantings (Belt)']:
        non_agr_wreq_matrices['Beef Carbon Plantings (Belt)'] = get_wreq_beef_carbon_plantings_belt(data, ag_w_mrj, cp_belt_x_r).reshape((data.NCELLS, 1))

    if NON_AG_LAND_USES['BECCS']:
        non_agr_wreq_matrices['BECCS'] = get_wreq_matrix_beccs(data).reshape((data.NCELLS, 1))

    non_agr_wreq_matrices = list(non_agr_wreq_matrices.values())

    return np.concatenate(non_agr_wreq_matrices, axis=1)
