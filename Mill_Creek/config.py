from pathlib import Path
import os

# calibration config file

# Versioning
hec_version = '641'

# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.prj')
ghdf_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.g01.hdf')
phdf_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.p04.hdf')
flow_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Mill_Creek_2023.u04')
plan_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990Mill_Creek_2023.p04')
WSP_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\output_files\channel_cal.csv')
Cntrln_filename = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\Calculated Layers\centerline.shp')

# Output file paths
working_dir = Path(r'G:\WATER_MG\HEC-RAS\MillCreek_43B05990\output_files')
simplex_filename = Path('simplex_dataframe.csv')
iterations_filename = Path('model_iterations.csv')
wse_prof_filename = Path('wse_profiles_output.csv')

# define mannings values per region
Man_n_params = ['Channel']
Man_n_vals = [0.01]

bounds = [(0.001, 0.6)]
i0_guess = [(0.08, 0.12)]
max_runs = 50




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