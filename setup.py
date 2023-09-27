from pathlib import Path
import os

# ______File intended for initializing run conditions______ #


# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\WestForkRockCree.prj')
ghdf_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\WestForkRockCree.g01.hdf')
phdf_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\WestForkRockCree.p01.hdf')
WSP1_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\Spatial_Data\WFRC_20220927_WSE.txt')
WSP2_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\Spatial_Data\WFRC_20220628_WSE.txt')
HWM_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\Spatial_Data\WFRC_20220628_HWMs.txt')
Cntrln_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\WF_Rock_Cr\Spatial_Data\WFRC_Chan.zip')

# Output file paths
simplex_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\autoras\output\simplex_dataframe.csv')
iterations_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\autoras\output\model_iterations.csv')
wse_prof_filename = Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\autoras\output\wse_profiles.csv')

# define mannings values per region
Man_n_params = ['UP_R_CHN', 'UP_L_CHN', 'DWN_R_CHN', 'DWN_L_CHN']
Man_n_vals = [0.02, 0.03, 0.02, 0.03]
uppr_bounds = 0.15 # [0.15, 0.15, 0.15, 0.15]
lwr_bounds = 0.005 # [0.005, 0.005, 0.005, 0.005]
max_runs = 50


# working directory
def directory():
    os.chdir(Path(r'C:\Users\CND367\Documents\MIHMs\HECRAS\autoras\output'))


# prior_n = [.02, .02, .02, .02]
# man_n = [.02, .03, .02, .02]
#
# if man_n[0] != prior_n:
#     updt_man[3] = (b'UP_R_CHN', 0.02, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan)

