import os
import scipy.optimize
import pandas as pd
import geopandas as gpd
import numpy as np
import shapely
from model import HecRas
import config_indirect
from objectivefun import RMSE
from reporting import hecras_calibration_report, hecras_indirectQ_report
import random


def calc_obj_function(input_vals):
    # save mannings to hdf
    #n_values = str(output_n)
    # Initialize an existing HEC-RAS model
    hecmodel = HecRas(config_indirect.prj_filename, config_indirect.ghdf_filename, config_indirect.phdf_filename, config_indirect.flow_filename, config_indirect.plan_filename)
    # Convert Manning's n calibration parameters to binary encoded
    man_n_params_bn = hecmodel.string_to_binary(config_indirect.Man_n_params)
    print(f"All values in: {input_vals}")
    # Build Manning's n parameter dictionary
    new_n = hecmodel.assign_param_vals(input_vals[:-1], man_n_params_bn)
    # Update only the specified Manning's n region values with new values
    hecmodel.change_Base_Mannings(config_indirect.ghdf_filename, new_n)
    # Create value array for unsteady flow timeseries
    vals = np.empty(len(dr))
    vals.fill(input_vals[-1])
    rvals = np.round(vals, decimals=2)
    # Initialize a timeseries to change unsteady flows # This needs to be an option in config if uplading new hydrograph
    # ts = pd.Series(rvals, index=pd.DatetimeIndex(dr))
    # Update unsteady Q in HEC-RAS flowfile
    hecmodel.change_unsteady_flow(input_vals[-1])

    # Run RAS
    hecmodel.run_model()

    phdf = hecmodel.load_current_plan_results(config_indirect.phdf_filename)
    # get last time step of simulation
    ras_wse = phdf[-1]
    # get Manning's n values for calibration parameters
    Man_tab = hecmodel.get_Mannings_calibration_regions(config_indirect.ghdf_filename)
    # Zone names
    ParamNames = hecmodel.binary_to_string(Man_tab['Land Cover Name'].tolist())
    # n values
    ParamVals = Man_tab["Base Manning's n Value"]
    # Get upstream boundary condition inflow
    Qval = hecmodel.get_inflow()
    # get water surface elevation data at reference points for model run
    ras_wse_pnts = ras_wse[Obs_df['Cell_Index'].astype(int).tolist()]
    # append to observation data frame
    Obs_df['Modeled_WSE'] = ras_wse_pnts
    # calculate objective function
    rmse = RMSE(Obs_df['Modeled_WSE'], Obs_df['Elev_m'])
    print(f"RMSE: {rmse}")

    # .csv that tracks model iteration, parameter values, and objective function
    # if it doesn't exist, initialize the dataframe
    if not config_indirect.iterations_filename.is_file():
        it_df = pd.DataFrame(ParamVals.reshape(-1, len(ParamVals)), columns=ParamNames)
        last_iteration = it_df.index[-1]
        it_df['{0}'.format(config_indirect.Q_params)] = Qval[-1, 1]
        it_df['iteration'] = last_iteration + 1
        it_df['Obj_Func_Value'] = rmse
        it_df.to_csv(config_indirect.iterations_filename, index=False)
    # if it exists, open the table, append, and save it
    else:
        it_df = pd.read_csv(config_indirect.iterations_filename)
        last_iteration = it_df['iteration'].iloc[-1]
        appd_lst = ParamNames + ['{0}'.format(config_indirect.Q_params), 'iteration', 'Obj_Func_Value']
        appd_vals = ParamVals.tolist() + [Qval[-1, 1], last_iteration + 1, rmse]
        appd_dict = dict(zip(appd_lst, appd_vals))
        appd_df = pd.DataFrame(appd_dict, index=[0])
        nw_it_df = pd.concat([it_df, appd_df], ignore_index=True)
        nw_it_df.to_csv(config_indirect.iterations_filename, index=False)

    # archives wse profiles for each model run with additional cell information
    # if it doesn't exist, initialize it by creating the 1st entry
    if not config_indirect.wse_prof_filename.is_file():
        cell_df = Obs_df[['CODE', 'Cell_Index', 'Channel_Distance', 'Elev_m']]
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(config_indirect.wse_prof_filename, index=False)
    else:
        cell_df = pd.read_csv(config_indirect.wse_prof_filename)
        cell_df['I{0}'.format(last_iteration + 1)] = ras_wse_pnts
        cell_df.to_csv(config_indirect.wse_prof_filename, index=False)

    return rmse


def scipy_nelder_mead(initial_simplex=None):
    initial_values = config_indirect.Man_n_vals + config_indirect.Q_params_vals
    x0 = np.array(initial_values)
    if initial_simplex is None:
        result = scipy.optimize.minimize(calc_obj_function, x0, method='Nelder-Mead',
                                         options={'disp': True, 'xatol': 1e-5, 'maxiter': config_indirect.max_runs})

    else:
        result = scipy.optimize.minimize(calc_obj_function, x0, method='Nelder-Mead', bounds=config_indirect.bounds,
                                         options={'xatol': 1e-5,
                                                  'maxiter': config_indirect.max_runs,
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
    Obs_df = pd.read_csv(config_indirect.WSP_filename)
    # read channel centerline for referencing water surface profiles (display only)
    cntrln_df = gpd.read_file(config_indirect.Cntrln_filename)
    # Remove points outside the model grid
    Obs_df = Obs_df[Obs_df['Cell_Index'] != 0.0].reset_index()
    # Shapely points geometry
    obs_pnts = gpd.GeoSeries(map(shapely.geometry.Point, zip(Obs_df['WGS84UTME'], Obs_df['WGS84UTMN'])))
    # get distances along centerline
    cntrl_dists = shapely.line_locate_point(cntrln_df.geometry[0], obs_pnts)
    # append distances with observation points
    Obs_df['Channel_Distance'] = cntrl_dists
    # Create date_range for unsteady flow hydrograph
    dr = config_indirect.date_range

    # Try initial simplex
    i0_simp = create_i0_simplex(config_indirect.i0_guess)
    print(f"initial simplex: {i0_simp}")

    # set working directory
    os.chdir(config_indirect.working_dir)
    # run nelder-mead algorithm
    scipy_nelder_mead(i0_simp)
    # create calibration report
    hecras_indirectQ_report(config_indirect.working_dir, "HECRAS_MC_Indirect_Report.ipynb")








