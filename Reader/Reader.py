# coding: utf-8
# Modified : 2023.05.21

import h5py
import numpy as np
import pandas as pd

from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.SOLE.FeetMe import FeetMe


class Reader(object):
    """ Class to read h5 file

    Args:
        h5df file
    Outputs:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
    """

    def __init__(self, path):
        self.m_path = path
    
    def readh5(self):
        f = h5py.File(self.m_path, "r")
        mass = f["UniqueValue"]["mass"][()]
        walking = Walking(mass)

        for leg in ["LeftLeg", "RightLeg"]:
            SoleInstance = FeetMe(1000)
            for axe, name in zip(["VerticalGrf", "ApGrf", "MediolateralGrf"],["Vertical", "Ap", "Mediolateral"]):
                try:
                    SoleInstance.SetGroundReactionForce(name, f["dict"]["sole"][leg][axe][:])
                except :
                    print(f'No value for ["dict"]["sole"][{leg}][{axe}]')
            try :
                SoleInstance.constructTimeseries()
            except :
                print("Error ====== SoleInstance.constructTimeseries()")
            if leg == "LeftLeg":
                try :
                    walking.setLeftLegSole(SoleInstance)
                except:
                    print("No value for Left Leg Sole")
            if leg == "RightLeg":
                try:
                    walking.setRightLegSole(SoleInstance)
                except:
                    print("No value for Right Leg Sole")

        StepGrfValue = dict()      
        for leg in ["LeftLeg", "RightLeg"]:
            StepGrfValue[leg] = dict()
            for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
                StepGrfValue[leg][axe] = dict()
                try:
                    for step in np.arange(len(f["dict"]["StepGrfValue"][leg][axe])):
                        StepGrfValue[leg][axe][step] = f["dict"]["StepGrfValue"][leg][axe][f"{step}"][:]
                except:
                    print(f'No value for ["dict"]["StepGrfValue"][{leg}][{axe}]')
        walking.setStepGrfValue(StepGrfValue)

        GroundReactionForces = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            GroundReactionForces[leg] = dict()
            try:
                GroundReactionForces[leg] = pd.DataFrame(f["dict"]["GroundReactionForces"][leg]["DataGroundReactionForces"][:])
            except:
                print(f'No value for ["dict"]["GroundReactionForces"][{leg}]["DataGroundReactionForces"]')
        walking.setGroundReactionForces(GroundReactionForces)

        DictOfDataFrameCutGrf = dict()
        FunctionDynamicAssym = dict()
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                DictOfDataFrameCutGrf[axe] = pd.DataFrame(f["dict"]["DictOfDataFrameCutGrf"][axe][:])
            except:
                print(f'No value for ["dict"]["DictOfDataFrameCutGrf"][{axe}]')
            try:
                FunctionDynamicAssym[axe] = pd.DataFrame(f["dict"]["FunctionDynamicAssym"][axe][:])
            except: 
                print(f'No value for ["dict"]["FunctionDynamicAssym"][{axe}]')
        walking.setDictOfDataFrameCutGrf(DictOfDataFrameCutGrf)
        walking.setFunctionDynamicAssym(FunctionDynamicAssym)
        
        walking.setDataFrameLeftRight(pd.DataFrame(f["DataFrame"]["DataFrameLeftRight"][:]))
        walking.setDataFrameRightLeft(pd.DataFrame(f["DataFrame"]["DataFrameRightLeft"][:]))
        walking.setDataFrameDynamicSymetryScore(pd.DataFrame(f["DataFrame"]["DataFrameDynamicSymetryScore"][:]))
        Columns_Names = ["stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]
        try:
            walking.setDataFrameSpatioTemporal_Left(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Left"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Left"]')
        try:
            walking.setDataFrameSpatioTemporal_Right(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Right"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Right"]')

        f.close()

        return walking
    
