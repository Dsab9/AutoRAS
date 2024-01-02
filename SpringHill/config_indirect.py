from pathlib import Path
import os
import pandas as pd

# Versioning
hec_version = '641'
observed_cal = False
indirect_cal = True

# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.prj')
ghdf_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.g01.hdf')
phdf_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.p02.hdf')
flow_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.u02')
plan_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.p02')
WSP_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\Channel_calibration_data\channel_cal.csv')
Cntrln_filename = Path(r'G:\WATER_MG\HEC-RAS\SpringHill_41O03000\Terrain\cntr_line.shp')

# Output file paths
working_dir = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\output_files')
simplex_filename = Path('simplex_dataframe_ind.csv')
iterations_filename = Path('model_iterations_ind.csv')
wse_prof_filename = Path('wse_profiles_output_ind.csv')

# define mannings values per region
Man_n_params = ['NoData', 'Riparian']
Man_n_vals = [0.1, 0.2]

Q_params = ['upstrmQ']
Q_params_vals = [42.5]

bounds = ((0.001, 0.9), (0.001, 0.9), (24.5, 84.0))
i0_guess = ((0.15, 0.2), (0.3, .2), (30, 40))
max_runs = 70

date_range = pd.date_range('2023-05-18 00:00:00', freq='H', periods=2)


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