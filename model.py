import pandas as pd
import numpy as np
import shapely
import geopandas as gpd
from pathlib import Path
import h5py
import os
import win32com.client
import copy
from rasfileparser import FlowFileParser, PlanFileParser


class HydraulicModel:
    def __init__(self):
        pass


class HecRas(HydraulicModel):

    def __init__(self, project_file, geom_hdf, plan_hdf, flowfile, planfile):
        super().__init__()
        self.project_path = project_file
        self.geom_hdf = geom_hdf
        self.plan_hdf = plan_hdf
        self.flowfile = flowfile
        self.planfile = planfile

    def change_unsteady_flow(self, time_series):
        u0file = FlowFileParser(self.flowfile)
        p0file = PlanFileParser(self.planfile)

        u0file.update_unsteady_flow(time_series)
        p0file.update_simulation_date(time_series)

    def get_inflow(self):
        with h5py.File(self.plan_hdf, 'r') as phf:
            sg_flw_tab = phf[
                'Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Boundary Conditions/Upstream Inflow']
            sg_flw_arr = np.array(sg_flw_tab)

        return sg_flw_arr

    def run_model(self):
        """
            Runs the saved Hec-Ras project file and closes upon completion
            -------
            """
        # Hard coded for v6.4.1
        # TODO - make flexible call to rascontroller based on version from user input
        hec = win32com.client.Dispatch("RAS641.HECRASController")
        hec.ShowRas()  # show HEC-RAS window
        # full filename of the RAS project
        RASProject = os.path.join(os.getcwd(), self.project_path)
        hec.Project_Open(RASProject)
        # to be populated: number and list of messages, blocking mode
        NMsg, TabMsg, block = None, None, True
        # computations of the current plan
        v1, NMsg, TabMsg, v2 = hec.Compute_CurrentPlan(NMsg, TabMsg, block)
        hec.QuitRas()  # close HEC-RAS
        del hec  # delete HEC-RAS controller

    def get_2D_refinement_region(self, geometry_hdf):
        with h5py.File(geometry_hdf, 'r') as ghf:
            Ref_Reg_Pnts = ghf["Geometry/2D Flow Area Refinement Regions/Polygon Points"]
            Ref_Reg_array = np.array(Ref_Reg_Pnts)
            geom = shapely.geometry.Polygon(Ref_Reg_array)

        return geom

    def load_current_plan_results(self, currentPlanFile):
        """
        Load the current plan results to ras_2d_data
        Returns
        -------
        """

        # check whether the hdf file exists
        if not os.path.isfile(currentPlanFile):
            raise Exception(
                "The result HDF file for current plan does not exist."
                " Make sure to run HEC-RAS before calling this function.")
        else:
            # self._ras_2d_data = RAS_2D_Data(currentPlanFile + ".hdf", terrainFileName)

            # Temp change here, just need to get the 2D results per grid cell for calibration
            with h5py.File(currentPlanFile, 'r') as rslt:
                WSE = np.array(rslt[
                                   "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/"
                                   "2D Flow Area/Water Surface"])

        return WSE

    def extract_WSE_timeseries(self, grid_cells, currentPlanFile):
        wat_el = self.load_current_plan_results(currentPlanFile)
        ref_pnts = wat_el[grid_cells, :]

        return ref_pnts

    def get_Mannings_calibration_regions(self, geometry_hdf):
        """

        Parameters
        ----------
        geometry_hdf : Path to the geometry .hdf file for the HEC-RAS Project.

        Returns
        -------
        An array of the Manning's n values for calibration regions, including the Base
        Override values.

        """

        with h5py.File(geometry_hdf, 'r') as ghf:
            Man_tab = ghf["Geometry/Land Cover (Manning's n)/Calibration Table"]
            Nw_arr = np.array(Man_tab)

        return Nw_arr

    def change_Base_Mannings(self, geometry_hdf, new_param_dict):
        """

        Parameters
        ----------
        geomtery_hdf : Path to the geometry .hdf file for the HEC-RAS Project.

        update_params_func : A function that determines how to distribute new
        paramter value assignments.

        Returns
        -------
        None.

        """

        Man_n = self.get_Mannings_calibration_regions(geometry_hdf)
        updt_man = Man_n.copy()
        print(f"updt_man: {updt_man}")
        new_params = new_param_dict
        print(f"new_params: {new_params}")

        new_n_vals = []
        for i in updt_man['Land Cover Name']:
            if i in new_params.keys():
                n = new_params[i]
            else:
                n = updt_man["Base Manning's n Value"][updt_man['Land Cover Name'] == i]
            new_n_vals.append(n)

        #print(f"new_n_vals: {new_n_vals}")
        updt_man["Base Manning's n Value"] = new_n_vals

        with h5py.File(geometry_hdf, 'r+') as ghf:
            Man_tab = ghf["Geometry/Land Cover (Manning's n)/Calibration Table"]
            Man_tab[...] = updt_man

        #Man_n = get_Mannings_calibration_regions(geometry_hdf)
        #updt_man = Man_n.copy()
        # updt_man = np.where(updt_man[4] == 0.02, 0.03, 0.04)
        #bmnv = "Base Manning's n Value"
        #print(f"updt_man: {updt_man[bmnv][4]}")
        #print(updt_man.dtype)

    def assign_param_vals(self, n, params_list):
        if len(n) != len(params_list):
            if len(n) == 1:
                nvals = np.full(len(params_list), n).tolist()
                new_param_vals = dict(zip(params_list, nvals))
                print(
                    "Only 1 new parameter value given with >1 parameters to change:\n "
                    "Assigning one value to all parameters")
            else:
                raise ValueError(
                    "Number of new values is >1 but < number of parameters to change. No parameter values assigned.")
        else:
            new_param_vals = dict(zip(params_list, n))

        return new_param_vals
        #new_param_vals = dict(zip(params_list, n))
        #return new_param_vals
    # this function was not working despite the same len

    def string_to_binary(self, string):
        # input string or list of strings
        if type(string) is list:
            binary_lst = []
            for i in string:
                bn = bytes(i, 'utf-8')
                binary_lst.append(bn)
        else:
            binary_lst = bytes(string, 'utf-8')

        return binary_lst

    def binary_to_string(self, binry):
        # input encoded object or list of encoded binary objects
        if type(binry) is list:
            st_lst = []
            for i in binry:
                st = i.decode()
                st_lst.append(st)
        else:
            st_lst = binry.decode()

        return st_lst

    # copied from pyHMT2D
    def change_ManningsN_v60(self, materialIDs, newManningsNValues, materialNames):
        """ Change materialID's Mannings n values to new values and save to file (for HEC-RAS v6)

        Parameters
        ----------
        materialIDs
        newManningsNValues
        materialNames

        Returns
        -------

        """

        # get land cover (Manning's n) file name and layer name
        hf = h5py.File(self.hdf_filename, 'r')

        self.landcover_filename = hf['Geometry'].attrs['Land Cover Filename']
        self.landcover_layername = hf['Geometry'].attrs['Land Cover Layername']

        hf.close()

        # Some time HEC-RAS does not save land cover filename and layername to HDF because the
        # geometry association of terrain or land cover (Manning's n) is removed after the 2D area geometry
        # computation has been done.
        if len(self.landcover_filename) == 0 or len(self.landcover_layername) == 0:
            print("Land Cover Filename or Land Cover Layername in result HDF is empty. "
                  "Will use the default Manning's n value.")

            raise Exception("Modification of default constant Manning's n has not been implemented.")

        else:
            # read the Manning n zones (land cover zones)
            if os.path.dirname(self.hdf_filename) == '':
                fileBase = b''
            else:
                fileBase = str.encode(os.path.dirname(self.hdf_filename) + '/')

            hfManningN = h5py.File(fileBase + self.landcover_layername, 'r+')

            dset_raster_map = hfManningN['Raster Map']
            dset_variables = hfManningN['Variables']     #This dataset needs to be modified because ManningsN is in it.

            # with dset_raster_map['ID'].astype(np.uint8):
            IDs = dset_raster_map['ID']

            IDs = IDs.tolist()

            ManningN = np.array(dset_variables['ManningsN'])

            Names = dset_variables['Name']

            # make a copy of the original Manning's n values
            #ManningN_new = copy.deepcopy(ManningN)
            dset_variables_new = copy.deepcopy(dset_variables)

            # print("IDs =", IDs)
            # print("ManningN =", ManningN)
            # print("Names =", Names)

            for i in range(len(materialIDs)):
                materialID = materialIDs[i]
                if materialID in IDs:
                    # also check whether the name is consistent
                    if materialNames[i] == Names[IDs.index(materialID)].decode("ASCII"):
                        print("    Old Manning's n value =", dset_variables['ManningsN'][IDs.index(materialID)],
                                           "for material ID = ", materialID)
                        dset_raster_map['ManningsN'][IDs.index(materialID)] = newManningsNValues[i]
                        print("    New Manning's n value =", dset_variables_new['ManningsN'][IDs.index(materialID)],
                                           "for material ID = ", materialID)
                    else:
                        raise Exception(
                            "The materialI and material name are not consistent. Please make sure they are consistent with HEC-RAS case."
                            "You can check the content of the Manning's n HDF file with HDFViewer.")
                else:
                    raise Exception(
                        "The specified materialID %d is not in the Manning's n list. Please check." % materialID)

            dset_variables[...] = dset_variables_new  # assign new values to data

            # save and close the HDF file
            hfManningN.close()

            # need to re-build 2D Manning's n zones information after update
            self.build2DManningNZones()