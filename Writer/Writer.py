# coding: utf-8
# Modified : 2023.05.20

import h5py
import os
import pandas as pd
import numpy as np


class Writer(object):
    """ Class to write h5 file

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        path: the path to save the h5 file
        file_name(str): the name for the h5 file
    """

    def __init__(self, walking, path, file_name):
        self.m_walking = walking
        self.m_path = path
        self.m_file_name = file_name


    def writeh5(self):
        """
        Write an h5df file with all data store in a walking object
        """

        walking = self.m_walking

        StorageDataPath = self.m_path
        f = h5py.File(os.path.join(StorageDataPath, self.m_file_name), "w")

        # Save the Unique Value
        grp_UniqueValue = f.create_group("UniqueValue")
        grp_UniqueValue.create_dataset("mass", shape= None ,dtype = None, data = walking.m_mass)

        # Save the Dictionary
        grp_dict = f.create_group("dict")

        grp_sole = grp_dict.create_group("sole")
        for leg in ["LeftLeg", "RightLeg"]:
            grp_leg = grp_sole.create_group(leg)
            for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
                try:
                    grp_leg.create_dataset(axe, shape= None ,dtype = None, data = walking.m_sole[leg].data[axe])
                except:
                    print(f"No value in  walking.m_sole[{leg}].data[{axe}]")

        grp_StepGrfValue = grp_dict.create_group("StepGrfValue")
        for leg in ["LeftLeg", "RightLeg"]:
            grp_leg = grp_StepGrfValue.create_group(leg)
            for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
                grp_axe = grp_leg.create_group(axe)
                try :
                    for step in np.arange(len(walking.m_StepGrfValue[leg][axe])):
                        grp_axe.create_dataset(f"{step}", shape= None ,dtype = None, data = walking.m_StepGrfValue[leg][axe][step])
                except:
                    print(f"No value in walking.m_StepGrfValue[{leg}][{axe}]]")

        grp_GroundReactionForces = grp_dict.create_group("GroundReactionForces")
        for leg in ["LeftLeg", "RightLeg"]:
            grp = grp_GroundReactionForces.create_group(leg)
            try:
                grp.create_dataset("DataGroundReactionForces", shape= None ,dtype = None, data = pd.DataFrame(walking.m_GroundReactionForces[leg]).T )
            except:
                print(f"No value in walking.m_GroundReactionForces[{leg}]")

        grp_DictOfDataFrameCutGrf = grp_dict.create_group("DictOfDataFrameCutGrf")
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                grp_DictOfDataFrameCutGrf.create_dataset(axe, shape= None ,dtype = None, data = walking.m_DictOfDataFrameCutGrf[axe])
            except:
                print(f"No value in walking.m_DictOfDataFrameCutGrf[{axe}]")
                
        grp_FunctionDynamicAssym = grp_dict.create_group("FunctionDynamicAssym")
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                grp_FunctionDynamicAssym.create_dataset(axe, shape= None ,dtype = None, data = walking.m_FunctionDynamicAssym[axe])
            except:
                print(f"No value in walking.m_FunctionDynamicAssym[{axe}]")

        # Save the DataFrame
        grp_DataFrame = f.create_group("DataFrame")
        grp_DataFrame.create_dataset("DataFrameLeftRight" ,shape= None ,dtype = None, data = walking.m_DataFrameLeftRight)
        grp_DataFrame.create_dataset("DataFrameRightLeft" ,shape= None ,dtype = None, data = walking.m_DataFrameRightLeft)
        grp_DataFrame.create_dataset("DataFrameDynamicSymetryScore" ,shape= None ,dtype = None, data = walking.m_DataFrameDynamicSymetryScore)
        grp_DataFrame.create_dataset("DataFrameSpatioTemporal_Left" ,shape= None ,dtype = None, data = walking.m_DataFrameSpatioTemporal_Left)
        grp_DataFrame.create_dataset("DataFrameSpatioTemporal_Right" ,shape= None ,dtype = None, data = walking.m_DataFrameSpatioTemporal_Right)
            
        f.close()












        