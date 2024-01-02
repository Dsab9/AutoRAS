## Extrememly Limited Capability at this point
#       - Can change only a "Flow Hydrograph" parameter in pre-formated .u0 file and run dates in .p0 file
#       - Does not differentiate Upstream and Downstream Boundary Condition.
#       - LOTS to-do: Make each boundary condition selectable, make all parameters replaceable, etc.

import numpy as np
import pandas as pd
import re
import config_indirect
import math



class FlowFileParser:

    def __init__(self, flowfl_pth):
        self.flowfile = flowfl_pth
        self._lines = None
        self._param_dict = self._create_dict()

    def _create_dict(self):
        out_dict = {}

        with open(self.flowfile) as f:
            lines = f.readlines()
            self._lines = lines
            hydrograph = []
            for l in lines:
                if re.match(r'\s', l) is not None:
                    hydgrph = [hydrograph.append(char.strip()) for char in l.split()]
                else:
                    stdata = [char.strip() for char in l.split('=')]

                if len(stdata) > 2:
                    out_dict['='.join(stdata[:-1])] = stdata[-1]
                else:
                    out_dict[stdata[0]] = stdata[1]

            out_dict['Flow Hydrograph'] = [len(hydrograph), np.array(hydrograph, dtype=float)]

        return out_dict

    def update_unsteady_flow(self, hydrograph):
        """

        :param hydrograph: pandas time-series (Series with datetimeindex)
        :return: None, updates dictionary and file lines
        """

        time_interval_dict = {'H': '1HOUR'}
        interv = time_interval_dict[hydrograph.index.freqstr]
        hydrgrph = [len(hydrograph), hydrograph.values]
        print(hydrgrph)

        self._param_dict['Interval'] = interv
        self._param_dict['Flow Hydrograph'] = hydrgrph

        formatted_hydrgrph = self.format_hydrograph_input(hydrgrph[0], hydrgrph[1])
        # print(formatted_hydrgrph)

        str_ind = []
        for i, line in enumerate(self._lines):
            if 'Flow Hydrograph=' in line:
                str_ind.append(i)
                i_sub = i + 1
                l_sub = self._lines[i_sub]
                while re.match(r'\s', l_sub) is not None:
                    str_ind.append(i_sub)
                    i_sub += 1
                    l_sub = self._lines[i_sub]
            else:
                pass

        print(str_ind)

        top_blck = self._lines[:str_ind[0]]
        top_blck[-1] = '{0}={1}\n'.format('Interval', self._param_dict['Interval'])
        print(top_blck)
        btm_blck = self._lines[(str_ind[-1] + 1):]
        print(btm_blck)
        top_blck.extend(formatted_hydrgrph)
        print(top_blck)

        top_blck.extend(btm_blck)
        self._lines = top_blck

        updt_txt = ''.join(top_blck)
        with open(self.flowfile, 'r+') as f:
            f.seek(0)
            f.write(updt_txt)
            f.truncate()

    # def get_unsteady_flow_info(self, planfl_pth):
    #     time_interval_dict = {'H': '1HOUR'}
    #     pln = PlanFileParser(planfl_pth)
    #     datestr = [item.strip() for item in pln._param_dict['Simulation Date'].split(',')]
    #     startstr = ' '.join(dates[:2])
    #     start = pd.Timestamp.strptime(start, "%d%b%Y %H%M")
    #     values = self._param_dict['Flow Hydrograph']
    #     for key, item in time_interval_dict.items():
    #         if item == '1HOUR':
    #             interval = key
    #         else:
    #             pass
    #     dates = pd.date_range(start, freq=interval, periods=values[0])
    #     FS = pd.Series(values[1], index=pd.DatetimeIndex(dates))
    #
    #     return FS



    # This has been updated, will reformat u_files based on previous q result
    # Need to pass in Q and friction slope (needs developemnt)
    def format_hydrograph_input(self, new_q_val):
        print(f"Q= {new_q_val}")
        with open(config_indirect.flow_filename, 'r', encoding='utf-8') as flow_plan:
            lines = flow_plan.readlines()
            entries = int(lines[5].split()[-1])
            rows = int(math.ceil(entries / 10))
            new_hydrogrh = []
            increment = new_q_val / (entries - 1)

            for v in range(0, entries):
                if v == 0:
                    new_hydrogrh.append(0)
                elif v == (entries - 2) or v == (entries - 1):
                    new_hydrogrh.append(new_q_val)
                else:
                    val = round(v * increment, 3)
                    new_hydrogrh.append(val)
            # print(new_hydrogrh)

            hydrogrph_list = [[] for i in range(rows)]
            list_num = 0
            counter = 0
            for v in new_hydrogrh:
                if counter < 10:
                    hydrogrph_list[list_num].append(str(v))
                    counter += 1
                else:
                    counter = 1
                    list_num += 1
                    hydrogrph_list[list_num].append(str(v))
            # print(hydrogrph_list)

            format_list = []
            for lis in hydrogrph_list:
                format_row_list = []
                for string in lis:
                    leng = len(string)
                    for i in range(8 - leng):
                        format_row_list.append(' ')
                    format_row_list.append(string)
                format_list.append(''.join(format_row_list))
            # print(format_list)

            line_cntr = 0
            for i in range(6, (6 + rows)):
                lines[i] = format_list[line_cntr]
                lines[i] = lines[i] + '\n'
                line_cntr += 1
            # print(lines)

        with open(config_indirect.flow_filename, 'w', encoding='utf-8') as flow_plan:
            flow_plan.writelines(lines)
        print("Hydrograph successfully changed")



class PlanFileParser:

    def __init__(self, planfl_pth):
        self.planfile = planfl_pth
        self._lines = None
        self._param_dict = self._create_dict()

    def _create_dict(self):
        out_dict = {}

        with open(self.planfile) as f:
            lines = f.readlines()
            self._lines = lines
            for l in lines:
                stdata = [char.strip() for char in l.split('=')]

                if len(stdata) < 2:
                    pass
                else:
                    out_dict[stdata[0]] = stdata[1]

        return out_dict

    def update_simulation_date(self, hydrograph):
        """

        :param hydrograph: pandas time-series (Series with datetimeindex)
        :return: None, updates dictionary and file lines
        """

        #2400 time replacement
        def tm_replace(in_time_str):
            if in_time_str == '0000':
                out_time_str = '2400'
            else:
                out_time_str = in_time_str

            return out_time_str

        time_interval_dict = {'H': '1HOUR'}
        interv = time_interval_dict[hydrograph.index.freqstr]
        strt = hydrograph.index[0]
        end = hydrograph.index[-1]

        strtdt_frmt = strt.strftime("%d%b%Y").upper()
        strttim_frmt = strt.strftime("%H%M")
        strttim_frmt = tm_replace(strttim_frmt)
        enddt_frmt = end.strftime("%d%b%Y").upper()
        endtim_frmt = end.strftime("%H%M")
        endtim_frmt = tm_replace(endtim_frmt)

        sim_dat_strs = [strtdt_frmt, strttim_frmt, enddt_frmt, endtim_frmt]

        self._param_dict['Simulation Date'] = ','.join(sim_dat_strs)
        self._param_dict['Instantaneous Interval'] = interv

        for i, line in enumerate(self._lines):
            if 'Simulation Date' in line:
                self._lines[i] = '{0}={1}\n'.format('Simulation Date', self._param_dict['Simulation Date'])
            elif 'Instantaneous Interval' in line:
                self._lines[i] = '{0}={1}\n'.format('Instantaneous Interval', self._param_dict['Instantaneous Interval'])
            else:
                pass

        updt_txt = ''.join(self._lines)
        with open(self.planfile, 'r+') as f:
            f.seek(0)
            f.write(updt_txt)
            f.truncate()



