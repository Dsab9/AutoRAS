import scipy.optimize
import pandas as pd
import numpy as np
from support import *
from setup import *


def n_m_function(output_n):
    # save mannings to hdf
    n_values = str(output_n)
    man_n_params_bn = string_to_binary(Man_n_params)
    print(f"n values in: {n_values}")
    new_n = assign_param_vals(Man_n_vals, man_n_params_bn)
    change_Base_Mannings(ghdf_filename, new_n)


    # Run RAS
    run_ras(prj_filename)

    # Load measured WSE data
    Obs_df = pd.read_csv(WSP2_filename)
    # Remove points outside the model grid
    Obs_df = Obs_df[Obs_df['Cell_Index'] != 0.0].reset_index()
    # Shapely points geometry
    obs_pnts = gpd.GeoSeries(map(shapely.geometry.Point, zip(Obs_df['WGS84UTME'], Obs_df['WGS84UTMN'])))
    # get distances along centerline
    cntrl_dists = shapely.line_locate_point(cntrln_df.geometry[0], obs_pnts)
    # append distances with observation points
    Obs_df['Channel_Distance'] = cntrl_dists
    # load plan .hdf WSE results
    phdf = load_current_plan_results(phdf_filename)
    # get last time step of simulation
    ras_wse = phdf[-1]
    # get Manning's n values for calibration parameters
    Man_tab = get_Mannings_calibration_regions(ghdf_filename)
    # Zone names
    ParamNames = binary_to_string(Man_tab['Land Cover Name'].tolist())
    # n values
    ParamVals = Man_tab["Base Manning's n Value"]
    # get water surface elevation data at reference points for model run
    ras_wse_pnts = ras_wse[Obs_df['Cell_Index'].astype(int).tolist()]
    # append to observation data frame
    Obs_df['Modeled_WSE'] = ras_wse_pnts
    # calculate objective function
    rmse = RMSE(Obs_df['Modeled_WSE'], Obs_df['Elev_m'])
    print(f"RMSE: {rmse}")

    # .csv that tracks model iteration, parameter values, and objective function
    # if it doesn't exist, initialize the dataframe
    if not iterations_filename.is_file():
        it_df = pd.DataFrame(ParamVals.reshape(-1, len(ParamVals)), columns=ParamNames)
        last_iteration = it_df.index[-1]
        it_df['iteration'] = last_iteration + 1
        it_df['Obj_Func_Value'] = rmse
        it_df.to_csv(iterations_filename, index=False)
    # if it exists, open the table, append, and save it
    else:
        it_df = pd.read_csv(iterations_filename)
        last_iteration = it_df['iteration'].iloc[-1]
        appd_lst = ParamNames + ['iteration', 'Obj_Func_Value']
        appd_vals = ParamVals.tolist() + [last_iteration + 1, rmse]
        appd_dict = dict(zip(appd_lst, appd_vals))
        appd_df = pd.DataFrame(appd_dict, index=[0])
        nw_it_df = pd.concat([it_df, appd_df])
        nw_it_df.to_csv(iterations_filename, index=False)

    # archives wse profiles for each model run with additional cell information
    # if it doesn't exist, initialize it by creating the 1st entry
    if not wse_prof_filename.is_file():
        cell_df = Obs_df[['CODE', 'Cell_Index', 'Channel_Distance', 'Elev_m']]
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(wse_prof_filename, index=False)
    else:
        cell_df = pd.read_csv(wse_prof_filename)
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(wse_prof_filename, index=False)

    return rmse


def scipy_nelder_mead():
    initial_values = Man_n_vals
    x0 = np.array(initial_values)
    result = scipy.optimize.minimize(n_m_function, x0, method='Nelder-Mead',
                                     options={'disp': True, 'xatol': 1e-5, 'maxiter': max_runs})
                                              # 'bounds': (lwr_bounds, uppr_bounds)})
    print(f"Nelder-Mead result: {result}")


def RMSE(modeled, observed):
    """

    Parameters
    ----------
    modeled : numpy 1d array of modeled WSE at reference points.
    observed : numpy 1d array of the observed WSE at reference points.

    Returns
    -------
    scalar RMSE value

    """
    err = modeled - observed
    err_sqr = err ** 2
    RMSE = np.sqrt(err_sqr.mean())

    return RMSE


# ________________initialize____________________ #
# encode for use in HEC-RAS output indexing/changing values
Man_n_params_bn = string_to_binary(Man_n_params)
# read channel centerline for referencing water surface profiles (display only)
cntrln_df = gpd.read_file(Cntrln_filename)
# set working directory
directory()
# run nelder-mead algorithm
scipy_nelder_mead()










