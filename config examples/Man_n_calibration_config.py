from pathlib import Path
import os

# calibration config file


# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\WFRC_lidar.prj')
ghdf_filename = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\WFRC_lidar.g01.hdf')
phdf_filename = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\WFRC_lidar.p01.hdf')
flow_filename = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\WFRC_lidar.u01')
plan_filename = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\WFRC_lidar.p01')
WSP_filename = Path(r'D:\ArcGIS_Projects\WF Rock Creek\Tabular\WFRC_20220628_HWMs.txt')
Cntrln_filename = Path(r'D:\ArcGIS_Projects\WF Rock Creek\Vector\WFRC_Chan\WFRC_Chan.zip')

# Output file paths
working_dir = Path(r'D:\HEC-RAS Projects\WF_Rock_Cr\Lidar_Terrain_Version\20220613_Indirect')
simplex_filename = Path('simplex_dataframe.csv')
iterations_filename = Path('model_iterations.csv')
wse_prof_filename = Path('wse_profiles.csv')

# define mannings values per region
Man_n_params = ['UP_R_CHN', 'UP_L_CHN', 'DWN_R_CHN', 'DWN_L_CHN']
Man_n_vals = [0.02, 0.03, 0.02, 0.03]
bounds = ((0.005, 0.15), (0.005, 0.15), (0.005, 0.15), (0.005, 0.15))
max_runs = 50



# prior_n = [.02, .02, .02, .02]
# man_n = [.02, .03, .02, .02]
#
# if man_n[0] != prior_n:
#     updt_man[3] = (b'UP_R_CHN', 0.02, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan)

