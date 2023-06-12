# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 05 - 15

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from Tools.ToolsFFT import TransformFourrier, VisuTransformFourrier


def ReadMottekc3d(Path, mass, graph = True):
    """A reader function for read c3d give when you use M-Gait (Motek)

    Args:
        Path = path of the c3d file
        mass = mass of the subject in kg
        graph (boolean) = defaut is True 
            True  -> run VisuTransformFourrier (interactive graphic for selecting thresholds)
            False -> CAUTION (all thresholds will be selected by default)
    Outputs:
        dataLeft  = pd.DataFrame() with VerticalVGrf ; ApGrf ; MediolateralGrf for Ground Reaction Force in each axis
        dataRight = pd.DataFrame() with VerticalVGrf ; ApGrf ; MediolateralGrf for Ground Reaction Force in each axis
    """
    acq = btkTools.smartReader(Path)
    grwc = btkTools.getForcePlateWrench(acq)

    forces = []
    items = [0,1]
    for it in items:
        forces.append(grwc.GetItem(it).GetForce().GetValues() / (mass * 9.81) * 100)

    if graph == False:
        seuil_vertical = 10000
        seuil_antpost = 5000
        seuil_mediolat = 1300
    else :
        seuil_vertical = VisuTransformFourrier(forces[1][:,2], 10000)
        seuil_antpost = VisuTransformFourrier(forces[1][:,1], 5000)
        seuil_mediolat = VisuTransformFourrier(forces[1][:,0] * -1, 1300)

    dataLeft = pd.DataFrame()
    dataLeft["VerticalVGrf"] = TransformFourrier(forces[1][:,2], seuil= seuil_vertical) 
    dataLeft["VerticalVGrf"][dataLeft["VerticalVGrf"] < 20] = 0
    dataLeft["ApGrf"] = TransformFourrier(forces[1][:,1], seuil=seuil_antpost)
    dataLeft["MediolateralGrf"] = TransformFourrier(forces[1][:,0] * -1, seuil=seuil_mediolat)

    dataRight = pd.DataFrame()
    dataRight["VerticalVGrf"] = TransformFourrier(forces[0][:,2], seuil= seuil_vertical) 
    dataRight["VerticalVGrf"][dataRight["VerticalVGrf"] < 20] = 0
    dataRight["ApGrf"] = TransformFourrier(forces[0][:,1], seuil=seuil_antpost)
    dataRight["MediolateralGrf"] = TransformFourrier(forces[0][:,0], seuil=seuil_mediolat)

    return dataLeft, dataRight







