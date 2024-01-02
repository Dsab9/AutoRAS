import os
import scipy.optimize
import pandas as pd
import geopandas as gpd
import numpy as np
import shapely
from model import HecRas
import config
from objectivefun import RMSE
from reporting import hecras_calibration_report
import random


def calc_obj_function(input_n_vals):
    # save mannings to hdf
    #n_values = str(output_n)
    hecmodel = HecRas(config.prj_filename, config.ghdf_filename, config.phdf_filename, config.flow_filename, config.plan_filename)
    man_n_params_bn = hecmodel.string_to_binary(config.Man_n_params)
    print(f"n values in: {input_n_vals}")
    new_n = hecmodel.assign_param_vals(input_n_vals, man_n_params_bn)
    hecmodel.change_Base_Mannings(config.ghdf_filename, new_n)

    #dr = pd.date_range('2022-06-12 01:00:00', freq='H', periods=2)
    #vals = np.array([13.17, 13.17])
    #ts = pd.Series(vals, index=pd.DatetimeIndex(dr))

    #hecmodel.change_unsteady_flow(ts)

    # Run RAS
    hecmodel.run_model()

    phdf = hecmodel.load_current_plan_results(config.phdf_filename)
    # get last time step of simulation
    ras_wse = phdf[-1]
    # get Manning's n values for calibration parameters
    Man_tab = hecmodel.get_Mannings_calibration_regions(config.ghdf_filename)
    # Zone names
    ParamNames = hecmodel.binary_to_string(Man_tab['Land Cover Name'].tolist())
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
    if not config.iterations_filename.is_file():
        it_df = pd.DataFrame(ParamVals.reshape(-1, len(ParamVals)), columns=ParamNames)
        last_iteration = it_df.index[-1]
        it_df['iteration'] = last_iteration + 1
        it_df['Obj_Func_Value'] = rmse
        it_df.to_csv(config.iterations_filename, index=False)
    # if it exists, open the table, append, and save it
    else:
        it_df = pd.read_csv(config.iterations_filename)
        last_iteration = it_df['iteration'].iloc[-1]
        appd_lst = ParamNames + ['iteration', 'Obj_Func_Value']
        appd_vals = ParamVals.tolist() + [last_iteration + 1, rmse]
        appd_dict = dict(zip(appd_lst, appd_vals))
        appd_df = pd.DataFrame(appd_dict, index=[0])
        nw_it_df = pd.concat([it_df, appd_df])
        nw_it_df.to_csv(config.iterations_filename, index=False)

    # archives wse profiles for each model run with additional cell information
    # if it doesn't exist, initialize it by creating the 1st entry
    if not config.wse_prof_filename.is_file():
        cell_df = Obs_df[['CODE', 'Cell_Index', 'Channel_Distance', 'Elev_m']]
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(config.wse_prof_filename, index=False)
    else:
        cell_df = pd.read_csv(config.wse_prof_filename)
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(config.wse_prof_filename, index=False)

    return rmse


def scipy_nelder_mead(initial_simplex=None):
    initial_values = config.Man_n_vals
    x0 = np.array(initial_values)
    if initial_simplex is None:
        result = scipy.optimize.minimize(calc_obj_function, x0, method='Nelder-Mead',
                                         options={'disp': True, 'xatol': 1e-5, 'maxiter': config.max_runs})

    else:
        result = scipy.optimize.minimize(calc_obj_function, x0, method='Nelder-Mead', bounds=config.bounds,
                                         options={'xatol': 1e-5,
                                                  'maxiter': config.max_runs,
                                                  'initial_simplex': initial_simplex,
                                                  'disp': True})
    print(f"Nelder-Mead result: {result}")


def create_i0_simplex(i0_guess):
    array_list = []
    temp_list = []
    for tup in range(0, len(i0_guess)):
        lwr_nval = i0_guess[tup][0]
        temp_list.append(lwr_nval)
    array_list.append(temp_list)
    temp_list = []

    if len(i0_guess) > 1:
        for i in range(0, (len(i0_guess) - 1)):
            for tup in range(0, len(i0_guess)):
                nval = round(random.uniform(i0_guess[tup][0], i0_guess[tup][1]), 2)
                temp_list.append(nval)
            array_list.append(temp_list)
            temp_list = []

    for tup in range(0, len(i0_guess)):
        upr_nval = i0_guess[tup][1]
        temp_list.append(upr_nval)
    array_list.append(temp_list)

    i0_simplex = np.array(array_list)
    return i0_simplex


if __name__ == "__main__":
    # Load measured WSE data
    Obs_df = pd.read_csv(config.WSP_filename)
    # read channel centerline for referencing water surface profiles (display only)
    cntrln_df = gpd.read_file(config.Cntrln_filename)
    # Remove points outside the model grid
    Obs_df = Obs_df[Obs_df['Cell_Index'] != 0.0].reset_index()
    # Shapely points geometry
    obs_pnts = gpd.GeoSeries(map(shapely.geometry.Point, zip(Obs_df['WGS84UTME'], Obs_df['WGS84UTMN'])))
    # get distances along centerline
    cntrl_dists = shapely.line_locate_point(cntrln_df.geometry[0], obs_pnts)
    # append distances with observation points
    Obs_df['Channel_Distance'] = cntrl_dists

    # Try initial simplex
    i0_simp = create_i0_simplex(config.i0_guess)
    print(i0_simp)

    # set working directory
    os.chdir(config.working_dir)
    # run nelder-mead algorithm
    scipy_nelder_mead(i0_simp)
    # create calibration report
    hecras_calibration_report(config.working_dir, "HECRAS_MC_Calibration_Report.ipynb")









