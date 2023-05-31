import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking
from Tools.ToolsFFT import TransformFourrier

DataPath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\"
mass = 60 # en kg


# ======================================================= VICON =====================================================
run_vicon = False
if run_vicon == True:
    file_name = "feetme_vicon.c3d"
    Path = DataPath + file_name
    acq = btkTools.smartReader(Path)
    grwc = btkTools.getForcePlateWrench(acq)

    def RollingMean(data, Step = 10):
        filtered = [value for value in data]
        filtered = pd.DataFrame(filtered)
        filtered = filtered.rolling(window = Step, center = True).mean()
        filtered = filtered.fillna(0)
        filtered = filtered[0].tolist()
        return np.array(filtered)

    def SetZeroVertical(filtered):
        for index in np.arange(len(filtered)):
            if filtered[index] < 1:
                filtered[index] = 0
        return filtered

    forces = dict()
    plateformes = [0,1,2]

    for plateforme in plateformes:
        data = grwc.GetItem(plateforme).GetForce().GetValues() / mass 
        filtered0 = RollingMean(data[:,0])
        filtered1 = RollingMean(data[:,1])
        filtered2 = SetZeroVertical(RollingMean(data[:,2]))
        forces[plateforme] = {"Ve" : np.abs(filtered2),
                            "Ap" : filtered1,
                            "Ml" : filtered0}    

    dataLeft = pd.DataFrame()
    dataLeft["VerticalVGrf"] = forces[1]["Ve"] #VerticalGrfLeft
    dataLeft["ApGrf"] = forces[1]["Ap"]#ApGrfLeft
    dataLeft["MediolateralGrf"] = forces[1]["Ml"] #MediolateralGrfLeft

    dataRight = pd.DataFrame()
    dataRight["VerticalVGrf"] = forces[2]["Ve"] #VerticalGrfRight
    dataRight["ApGrf"] = forces[2]["Ap"] #ApGrfRight
    dataRight["MediolateralGrf"] = forces[2]["Ml"] #MediolateralGrfRight

    SoleInstanceLeft = FeetMe(1000)
    SoleInstanceLeft.SetGroundReactionForce("Vertical", dataLeft["VerticalVGrf"].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Ap", dataLeft["ApGrf"].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Mediolateral", dataLeft["MediolateralGrf"].to_numpy())
    SoleInstanceLeft.constructTimeseries()

    SoleInstanceRight = FeetMe(1000)
    SoleInstanceRight.SetGroundReactionForce("Vertical", dataRight["VerticalVGrf"].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Ap", dataRight["ApGrf"].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Mediolateral", dataRight["MediolateralGrf"].to_numpy())
    SoleInstanceRight.constructTimeseries()

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
    Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_vicon(feetme_vicon).hdf5").writeh5()


# ============================================================== FeetMe =============================================
run_feetme = False
if run_feetme == True:
    file_name = "feetme_vicon.csv"
    Path = DataPath + file_name

    from SOLE.FeetMe import readFeetMeCsv
    SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = Path, freq = 110)

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
    Writer(walking = walking, path = StoragePathHDF5, file_name = "walking_feetme(feetme_vicon).hdf5").writeh5()




from Reader.Reader import Reader
StoragePathHDF5 = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\StorageH5Walking\\"
DataPath_feetme = os.path.join(StoragePathHDF5, 'walking_feetme(feetme_vicon).hdf5')
DataPath_vicon = os.path.join(StoragePathHDF5, 'walking_vicon(feetme_vicon).hdf5')
walking_feetme = Reader(DataPath_feetme).readh5()
walking_vicon = Reader(DataPath_vicon).readh5()

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title("Left Leg")
plt.plot(walking_feetme.m_StepGrfValue["LeftLeg"]["VerticalGrf"][0], label="feetme")
plt.plot(walking_vicon.m_StepGrfValue["LeftLeg"]["VerticalGrf"][0], label="vicon")
plt.legend()
plt.subplot(1,2,2)
plt.title("Right Leg")
plt.plot(walking_feetme.m_StepGrfValue["RightLeg"]["VerticalGrf"][0], label="feetme")
plt.plot(walking_vicon.m_StepGrfValue["RightLeg"]["VerticalGrf"][0], label="vicon")
plt.legend()
plt.show()