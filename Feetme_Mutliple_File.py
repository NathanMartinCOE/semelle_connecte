import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

from Walking.Walking import Walking
from SOLE.FeetMe import readFeetMeMultipleCsv


# StoragePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\test\\"
# file_names = ["nathan_TDM_1.csv", "nathan_TDM_2.csv", "nathan_TDM_3.csv", "nathan_TDM_4.csv"]
# file_names = ["nathan_R_1.csv", "nathan_R_2.csv", "nathan_R_3.csv", "nathan_R_4.csv"]
# mass = 60

# fullfilenames = []
# for file_name in file_names:
#     fullfilenames.append(os.path.join(StoragePath, file_name))


# SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames, freq = 110)

# walking = Walking(mass)
# walking.setLeftLegSole(SoleInstanceLeft)
# walking.setRightLegSole(SoleInstanceRight)

# from Walking.WalkingFilters import WalkingKinematicsFilter
# from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
# procedure = GroundReactionForceKinematicsProcedure()
# WalkingKinematicsFilter(walking, procedure).run()
# from Walking.WalkingFilters import WalkingDataProcessingFilter
# from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
# procedure = NormalisationProcedure()
# WalkingDataProcessingFilter(walking, procedure).run()
# from Walking.WalkingFilters import WalkingKinematicsFilter
# from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
# procedure = DynamicSymetryFunctionComputeProcedure()
# WalkingKinematicsFilter(walking, procedure).run()


# from Writer.Writer import Writer
# StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
# Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_nathan_TDM.hdf5").writeh5()
# Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_nathan_R.hdf5").writeh5()


from Reader.Reader import Reader
StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_TDM.hdf5')
walking_TDM = Reader(DataPath).readh5()
DataPath = os.path.join(StoragePathHDF5, 'walking_nathan_R.hdf5')
walking_R = Reader(DataPath).readh5()

for walking in [walking_TDM, walking_R]:
    from Walking.WalkingFilters import WalkingKinematicsFilter
    from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()

    from Walking.WalkingFilters import WalkingDataProcessingFilter
    from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()

    from Walking.WalkingFilters import WalkingGraphicsFilter
    from Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure

    procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
    WalkingGraphicsFilter(walking, procedure).run()

