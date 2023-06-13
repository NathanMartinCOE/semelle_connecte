import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.SOLE.FeetMe import readFeetMeMultipleCsv


StoragePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\test\\"
file_names = ["nathan_TDM_1.csv", "nathan_TDM_2.csv", "nathan_TDM_3.csv", "nathan_TDM_4.csv"]
file_names = ["nathan_R_1.csv", "nathan_R_2.csv", "nathan_R_3.csv", "nathan_R_4.csv"]
mass = 60
fullfilenames = []
for file_name in file_names:
    fullfilenames.append(os.path.join(StoragePath, file_name))

def WriteWalkingh5():
    SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames, freq = 110)

    walking = Walking(mass)
    walking.setLeftLegSole(SoleInstanceLeft)
    walking.setRightLegSole(SoleInstanceRight)

    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
    from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()
    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
    procedure = DynamicSymetryFunctionComputeProcedure()
    WalkingKinematicsFilter(walking, procedure).run()

    from semelle_connecte.Writer.Writer import Writer
    StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
    Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_nathan_TDM.hdf5").writeh5()
    Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_nathan_R.hdf5").writeh5()

def ComputeAssymForEachStepOfTwoWalking():
    from semelle_connecte.Reader.Reader import Reader
    StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
    DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_TDM.hdf5')
    walking_TDM = Reader(DataPath).readh5()
    DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_R.hdf5')
    walking_R = Reader(DataPath).readh5()

    Assym = pd.DataFrame()
    for walking, name in zip([walking_TDM, walking_R], ["TDM", "SRU"]):

        if len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"]) < len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"]):
            N_Steps = len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])
        elif len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"]) > len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"]):
            N_Steps = len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"])

        Assym_method = []
        for step in np.arange(0,N_Steps):
            DataFrameGrf = pd.DataFrame({
                'yRight': walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step],
                'yLeft': walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]
                                        })
            FunctionDynamicAssym = []
            rangexdt = max(DataFrameGrf['yRight']) - min(DataFrameGrf['yRight'])
            rangexgt = max(DataFrameGrf['yLeft']) - min(DataFrameGrf['yLeft'])
            for grf in range(0, DataFrameGrf.shape[0]):
                FunctionDynamicAssym.append(2*(DataFrameGrf['yRight'][grf] - DataFrameGrf['yLeft'][grf]) / (rangexdt + rangexgt) * 100)
            
            Assym_method.append(np.mean(FunctionDynamicAssym))
        
        try :
            Assym[f"{name}"] = Assym_method
        except:
            if len(Assym_method) != Assym.shape[0]:
                Assym_method = Assym_method[ : Assym.shape[0]]
                Assym[f"{name}"] = Assym_method

    Assym.to_csv('C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\assym_step.csv')

def PlotAssym():
    from semelle_connecte.Reader.Reader import Reader
    StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
    DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_TDM.hdf5')
    walking_TDM = Reader(DataPath).readh5()
    DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_R.hdf5')
    walking_R = Reader(DataPath).readh5()

    for walking, name in zip([walking_TDM, walking_R], ["TDM", "SRU"]):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure
        procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
        WalkingGraphicsFilter(walking, procedure).run()


# WriteWalkingh5()
# PlotAssym()
# ComputeAssymForEachStepOfTwoWalking()

import ipdb; ipdb.set_trace()