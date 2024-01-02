from pathlib import Path
import os
import pandas as pd

# calibration config file
hec_version = '641'

cal_observed = False
cal_indirect = False
gen_hydrograph = True

structures = False  # will assign channel n to structures

# define relevant file paths, calibration parameters, and define channel centerline
prj_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\bozo_cr.prj')
ghdf_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\bozo_cr.g01.hdf')
phdf_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\bozo_cr.p04.hdf')
flow_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\bozo_cr.u04')
plan_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\bozo_cr.p04')
WSP_filename = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\indirect_cal\wse_profiles.csv')
Cntrln_filename = Path(r'Y:\ARCHIVE\WRD_20231206_Bozeman_Cr\cc_working files\centerline.shp')

# Output filepaths
working_dir = Path(r'G:\WATER_MG\HEC-RAS\BozemanCr_41H08990\ratings')
simplex_filename = Path('simplex_dataframe.csv')
iterations_filename = Path('model_iterations.csv')
wse_prof_filename = Path('wse_profiles_output.csv')
rating_curve_filename = Path('rating_curve.csv')

# define mannings values per region
Man_n_params = ['Riparian', 'Grassland', 'Road']  # 'Grassland', 'Road', 'NoData', 'Channel', 'Riparian'
Man_n_vals = [0.141, 0.035, 0.016]

Q_params = ['UpstreamBC']  # discharge is last in bounds/ initial guess
Q_params_vals = [30.5]

bounds = [(0.08, 0.2), (0.01, 0.08), (0.005, 0.03), (20, 50)]
i0_guess = [(0.140, 0.142), (0.03, 0.04), (0.01, 0.02), (30.0, 35.0)]
max_runs = 50

# rating curve and hydrograph info
max_q = 25.485
q_divisions = 18  # number of runs, set to 1 if you want to generate single event based on q
gauge_el_NAVD88m = 1440.271  # site specific

hydrograph_ramp = False  # True will generate hydrograph with incrementally increasing q with the last hour held at max, false will keep q constant
set_datetime = False  # True will allow for manual selection of hydrograph input time and enable the following settings
change_sim_time = False  # Changes sim time based on 15min input increments
sim_time_hr = 3  # min 1 hr
start_date = '12DEC2024'
start_time = '00:00'
end_date = '12DEC2024'
end_time = '03:00'
computation_interval = '0.5SEC'







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


# mod_results = h5py.File(phdf_filename, 'r')
#     ras_info = mod_results['Results/Summary/Compute Processes']
#     plan_params = mod_results['Plan Data/Plan Parameters']
#     plan_info = mod_results['Plan Data/Plan Information']
#     up_bc = mod_results[
#         'Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Boundary Conditions/Upstream BC']
#     dwn_bc = mod_results[
#         'Event Conditions/Unsteady/Boundary Conditions/Normal Depths/2D: Perimeter BCLine: Downstream BC']
