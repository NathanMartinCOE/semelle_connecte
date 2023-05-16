# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 05 - 15

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from Tools.ToolsFFT import TransformFourrier



def ReadMottekc3d(Path, mass):
    acq = btkTools.smartReader(Path)
    grwc = btkTools.getForcePlateWrench(acq)

    forces = []
    items = [0,1]
    for it in items:
        forces.append(grwc.GetItem(it).GetForce().GetValues() / (mass * 9.81) * 100)

    dataLeft = pd.DataFrame()
    dataLeft["VerticalVGrf"] = TransformFourrier(forces[1][:,2], seuil=10000) 
    dataLeft["VerticalVGrf"][dataLeft["VerticalVGrf"] < 20] = 0
    dataLeft["ApGrf"] = TransformFourrier(forces[1][:,1], seuil=5000)
    dataLeft["MediolateralGrf"] = TransformFourrier(forces[1][:,0] * -1, seuil=1300)

    dataRight = pd.DataFrame()
    dataRight["VerticalVGrf"] = TransformFourrier(forces[0][:,2], seuil=10000) 
    dataRight["VerticalVGrf"][dataRight["VerticalVGrf"] < 20] = 0
    dataRight["ApGrf"] = TransformFourrier(forces[0][:,1], seuil=5000)
    dataRight["MediolateralGrf"] = TransformFourrier(forces[0][:,0], seuil=1300)

    return dataLeft, dataRight




