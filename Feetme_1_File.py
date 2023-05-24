import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

from SOLE.FeetMe import readFeetMeCsv
from Walking.Walking import Walking



StoragePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\test\\"
# FilesNames = ["nathan.csv","fabien.csv"]
FilesNames= ["nathan.csv"]

def ProcessFiles():
    for FileName in FilesNames:
        mass = 60

        DataPath = os.path.join(StoragePath, FileName)

        SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = DataPath, freq = 10)

        walking = Walking(mass)
        walking.setLeftLegSole(SoleInstanceLeft)
        walking.setRightLegSole(SoleInstanceRight)

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()
        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()


        from Writer.Writer import Writer
        StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
        Writer(walking = walking, path = StoragePathHDF5, file_name = f"walking_{FileName}.hdf5").writeh5()

# ProcessFiles()

from Reader.Reader import Reader
StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
DataPath = os.path.join(StoragePathHDF5, 'walking_nathan.csv.hdf5')
DataPath = os.path.join(StoragePathHDF5, 'walking_fabien.csv.hdf5')
walking = Reader(DataPath).readh5()

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

