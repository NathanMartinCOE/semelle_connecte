import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from semelle_connecte.SOLE.FeetMe import FeetMe
from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.Tools.ToolsFFT import TransformFourrier

DataPath = 'C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\grf\\'

X = []
Labels = []
list_path = ["vicon_normal.c3d", "vicon_boiterie_jb_dom.c3d", "vicon_boiterie_jb_non_dom.c3d"]
list_name = ["norm", "jb_dom", "jb_non_don"]

for path, name in zip(list_path, list_name):

    Path = DataPath + path
    acq = btkTools.smartReader(Path)
    grwc = btkTools.getForcePlateWrench(acq)
    mass = 60 # en kg

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


    """ Début des procédure (cf nom de la procédure et documentation) """

    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("GroundReactionForceKinematicsProcedure --------------- done")

    from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
    from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()
    print("NormalisationProcedure --------------- done")


    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
    procedure = DynamicSymetryFunctionComputeProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("DynamicSymetryFunctionComputeProcedure --------------- done")


    x = [walking.m_FunctionDynamicAssym["VerticalGrf"], walking.m_FunctionDynamicAssym["ApGrf"], walking.m_FunctionDynamicAssym["MediolateralGrf"]]
    labels = [f"Vertical_{name}", f"Ap_{name}", f"ML_{name}"]
    X.append(x)
    Labels.append(labels)


    from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
    from semelle_connecte.Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

    procedure = CutDataProcessingProcedure()
    procedure.setCutNumber(n_cut=3)
    WalkingDataProcessingFilter(walking, procedure).run()

    from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
    from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
    
    procedure = PlotCutGroundReactionForceProcedure()
    WalkingGraphicsFilter(walking, procedure).run()


combine_x = [X[0][0], X[1][0], X[2][0], X[0][1], X[1][1], X[2][1], X[0][2],  X[1][2], X[2][2]]
combine_labels = [Labels[0][0], Labels[1][0], Labels[2][0], Labels[0][1], Labels[1][1], Labels[2][1], Labels[0][2], Labels[1][2], Labels[2][2]]

plt.figure()
plt.boxplot(x= combine_x, labels= combine_labels)
plt.hlines(y=5, xmin=0, xmax= (len(combine_x)+1) , ls="--", colors="black")
plt.hlines(y=-5, xmin=0, xmax= (len(combine_x)+1), ls="--", colors="black")
low, high = plt.ylim()
bound = max(abs(low), abs(high))
plt.ylim(-bound, bound)
plt.ylabel("Values of Dynamic Assymetry Function")
plt.show()

