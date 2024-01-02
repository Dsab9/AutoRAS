import numpy as np
import pandas as pd
import random
import config

from model import HecRas
import h5py



# # define mannings values per region
# Man_n_params = ['UP_R_OVRB', 'UP_L_OVRB', 'DWN_R_OVRB', 'DWN_L_OVRB']
# Man_n_vals = [0.02, 0.03, 0.02, 0.03]
# Q_params = ['upstrmQ']
# Q_params_vals = [42.5]
# bounds = ((0.09, 0.3), (0.09, 0.3), (0.09, 0.3), (0.09, 0.3), (28.3, 85))
# i0_guess = ((0.09, 0.16), (0.09, 0.16), (0.09, 0.16), (0.09, 0.16), (42.0, 70.0))
# max_runs = 75
#
#
# i0_simp = np.array([[0.09, 0.09, 0.15, 0.15, 42.5],
#                     [0.09, 0.09, 0.15, 0.15, 70],
#                     [0.15, 0.15, 0.09, 0.09, 42.5],
#                     [0.15, 0.15, 0.09, 0.09, 70],
#                     [0.16, 0.16, 0.16, 0.16, 42.5],
#                     [0.09, 0.09, 0.09, 0.09, 70]])
#
# array_list = []
# temp_list = []
# for tup in range(0, len(i0_guess)):
#     lwr_nval = i0_guess[tup][0]
#     temp_list.append(lwr_nval)
# array_list.append(temp_list)
# temp_list = []
#
# if len(i0_guess) > 1:
#     for i in range(0, (len(i0_guess) - 1)):
#         for tup in range(0, len(i0_guess)):
#             nval = round(random.uniform(i0_guess[tup][0], i0_guess[tup][1]), 2)
#             temp_list.append(nval)
#         array_list.append(temp_list)
#         temp_list = []
#
# for tup in range(0, len(i0_guess)):
#     upr_nval = i0_guess[tup][1]
#     temp_list.append(upr_nval)
# array_list.append(temp_list)
#
#
# i0_simp = np.array(array_list)
# print(i0_simp)


# # Obs_df = pd.read_csv(config.WSP_filename)
# hecmodel = HecRas(config.prj_filename, config.ghdf_filename, config.phdf_filename, config.flow_filename, config.plan_filename)
# phdf = hecmodel.load_current_plan_results(config.phdf_filename)
# # get last time step of simulation
# ras_wse = phdf[-1]
# print(ras_wse)
# # get water surface elevation data at reference points for model run
# # ras_wse_pnts = ras_wse[Obs_df['Cell_Index'].astype(int).tolist()]
# # append to observation data frame
# # Obs_df['Modeled_WSE'] = ras_wse_pnts
#


# # read HDF5

with h5py.File(config.phdf_filename, 'r') as rslt:
    # for key in rslt.keys():
    #     print(key)
    #     print(type(rslt[key]))
    print(rslt['Event Conditions/Unsteady/Boundary Conditions/Normal Depths/2D: 2D area BCLine: BC Downstream'].keys())


    # WSE = np.array(rslt["Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/"
    #                     "2D Flow Areas/2D Flow Area/Water Surface"])

# 'Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Boundary Conditions/Upstream Inflow'