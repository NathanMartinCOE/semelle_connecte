import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking
from Tools.ToolsFFT import TransformFourrier
from Reader.MottekReader import ReadMottekc3d

""" Definition du chemin d'accès """
DataPath = 'C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\grf\\'
# Path = DataPath + 'gait_test4.c3d' 
# Path = DataPath + 'gait_test5.c3d' # fait 50 pas

X = []
Labels = []
# list_path = ['gait_test4.c3d', 'gait_test5.c3d']
# list_name = ["Test_4", "Test_5"]
list_path = ["condition_normal.c3d", "condition_boiterie_jb_dom.c3d", "condition_boiterie_jb_non_dom.c3d"]
list_name = ["norm", "jb_dom", "jb_non_don"]
for path, name in zip(list_path, list_name):
    Path = DataPath + path

    """ mass du sujet """
    mass = 60 # en kg

    """ lecture du fichier c3d """
    dataLeft, dataRight = ReadMottekc3d(Path, mass)

    """ Création de l'objet walking """
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

    from Walking.WalkingFilters import WalkingKinematicsFilter
    from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("GroundReactionForceKinematicsProcedure --------------- done")

    from Walking.WalkingFilters import WalkingDataProcessingFilter
    from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()
    print("NormalisationProcedure --------------- done")

    # from Walking.WalkingFilters import WalkingDataProcessingFilter
    # from Walking.WalkingDataProcessingProcedure import DeleteStepProcedure
    # procedure = DeleteStepProcedure()
    # WalkingDataProcessingFilter(walking, procedure).run()
    # print("DeleteStepProcedure --------------- done")

    # from Walking.WalkingFilters import WalkingGraphicsFilter
    # from Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure
    # procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
    # WalkingGraphicsFilter(walking, procedure).run()
    # print("PlotDynamicSymetryFunctionNormalisedProcedure --------------- done")


    from Walking.WalkingFilters import WalkingKinematicsFilter
    from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
    procedure = DynamicSymetryFunctionComputeProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("DynamicSymetryFunctionComputeProcedure --------------- done")


    x = [walking.m_FunctionDynamicAssym["VerticalGrf"], walking.m_FunctionDynamicAssym["ApGrf"], walking.m_FunctionDynamicAssym["MediolateralGrf"]]
    labels = [f"Vertical_{name}", f"Ap_{name}", f"ML_{name}"]
    X.append(x)
    Labels.append(labels)

# combine_x = [X[0][0], X[1][0], X[2][0], X[0][1], X[1][1], X[2][1], X[0][2],  X[1][2], X[2][2]]
# combine_labels = [Labels[0][0], Labels[1][0], Labels[2][0], Labels[0][1], Labels[1][1], Labels[2][1], Labels[0][2], Labels[1][2], Labels[2][2]]

# plt.figure()
# plt.boxplot(x= combine_x, labels= combine_labels)
# plt.hlines(y=5, xmin=0, xmax= (len(combine_x)+1) , ls="--", colors="black")
# plt.hlines(y=-5, xmin=0, xmax= (len(combine_x)+1), ls="--", colors="black")
# low, high = plt.ylim()
# bound = max(abs(low), abs(high))
# plt.ylim(-bound, bound)
# plt.ylabel("Values of Dynamic Assymetry Function")
# plt.show()


# """ Début des procédure 2 (cf nom de la procédure et documentation) """

    # from Walking.WalkingFilters import WalkingDataProcessingFilter
    # from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    # procedure = NormalisationProcedure()
    # WalkingDataProcessingFilter(walking, procedure).run()

    # from Walking.WalkingFilters import WalkingKinematicsFilter
    # from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    # procedure = GroundReactionForceKinematicsProcedure()
    # WalkingKinematicsFilter(walking, procedure).run()

    # from Walking.WalkingFilters import WalkingKinematicsFilter
    # from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

    # procedure = DynamicSymetryFunctionComputeProcedure()
    # WalkingKinematicsFilter(walking, procedure).run()

    # from Walking.WalkingFilters import WalkingGraphicsFilter
    # from Walking.WalkingGraphicsProcedure import PlotWorthAndBestStepProcedure
    # procedure = PlotWorthAndBestStepProcedure()
    # WalkingGraphicsFilter(walking, procedure).run()


    from Walking.WalkingFilters import WalkingDataProcessingFilter
    from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

    procedure = CutDataProcessingProcedure()
    procedure.setCutNumber(n_cut=3)
    WalkingDataProcessingFilter(walking, procedure).run()

    from Walking.WalkingFilters import WalkingGraphicsFilter
    from Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
    
    procedure = PlotCutGroundReactionForceProcedure()
    WalkingGraphicsFilter(walking, procedure).run()



