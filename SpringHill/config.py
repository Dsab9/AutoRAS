from pathlib import Path
import os
import pandas as pd

# calibration config file
hec_version = '641'

cal_observed = True
cal_indirect = False

# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Springhill_lrg.prj')
ghdf_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Springhill_lrg.g01.hdf')
phdf_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Springhill_lrg.p01.hdf')
flow_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Springhill_lrg.u01')
plan_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Springhill_lrg.p01')
WSP_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\Channel_calibration_data\channel_cal.csv')
Cntrln_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\Terrain\cntr_line.shp')

# Outputfilepaths
working_dir = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\SpringHill_lrg\output files')
simplex_filename = Path('simplex_dataframe.csv')
iterations_filename = Path('model_iterations.csv')
wse_prof_filename = Path('wse_profiles_output.csv')

# definemanningsvaluesperregion
Man_n_params = ['Channel']
Man_n_vals = [0.06]

Q_params = ['UpstreamBC']
Q_params_vals = [42.5]

bounds = [(0.015, 0.105)]
i0_guess = [(0.045, 0.055)]
max_runs = 100

# date_range = pd.date_range('2023-06-1700:02:00',freq='H',periods=2)




# prior_n = [.02, .02, .02, .02]
# man_n = [.02, .03, .02, .02]
#
# if man_n[0] != prior_n:
#     updt_man[3] = (b'UP_R_CHN', 0.02, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan)

# TODO:
# add datetime start to config, or pull from hecras
#launch QGIS with .bat and get cell index for wsel points
#
# simplex setup based n_val inputs - done
# make flexible call to rascontroller based on version from user input - done

# redefine normal depth based on prior results
# mod_results = h5py.File(phdf_filename, 'r')
#     ras_info = mod_results['Results/Summary/Compute Processes']
#     plan_params = mod_results['Plan Data/Plan Parameters']
#     plan_info = mod_results['Plan Data/Plan Information']
#     up_bc = mod_results[
#         'Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Boundary Conditions/Upstream BC']
#     dwn_bc = mod_results[
#         'Event Conditions/Unsteady/Boundary Conditions/Normal Depths/2D: Perimeter BCLine: Downstream BC']
