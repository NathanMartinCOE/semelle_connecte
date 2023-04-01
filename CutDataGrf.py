# CutDataGrf
# Author : Nathan Martin 
# Modified : 2023 - 03 - 29

import pandas as pd
import numpy as np

def CutDataGrf(GrfLeft, GrfRight, n_cut):
    GrfDataframeCut = pd.DataFrame()
    if n_cut != 0 : 
        indexLeft = GrfLeft.shape[0] // n_cut
        indexRight = GrfRight.shape[0] // n_cut
        valindexLeft = indexLeft
        valindexRight = indexRight
        ListIndexLeft = [0]
        ListIndexRight = [0]
        for cut in np.arange(n_cut):
            ListIndexLeft.append(valindexLeft)
            valindexLeft = valindexLeft + indexLeft
            ListIndexRight.append(valindexRight)
            valindexRight = valindexRight + indexRight
        for index in zip(range(0, len(ListIndexLeft[0: -1])), range(0, len(ListIndexRight[0: -1]))):
            GrfDataframeCut[f"Left{index[0]+1}"] = GrfLeft[ListIndexLeft[index[0]] : ListIndexLeft[index[0]+1]]
            GrfDataframeCut[f"Right{index[1]+1}"] = GrfRight[ListIndexRight[index[1]] : ListIndexRight[index[1]+1]]
    elif n_cut == 0 :
        GrfDataframeCut["Left"] = GrfLeft
        GrfDataframeCut["Right"] = GrfRight
    return GrfDataframeCut


from MakeDictStep import MakeDictStep
from math import nan

def MeanCutDataGrf(GrfDataframeCut):
    antGrf = [0] * GrfDataframeCut.shape[0]
    MeanCutDataGrf = pd.DataFrame()

    for colname in GrfDataframeCut.columns:
        VerticalGrfStep, ant_vide = MakeDictStep(pd.array(GrfDataframeCut[colname]), antGrf)
        ListNa0 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[0]))
        ListNa40 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[len(VerticalGrfStep) - 1]))
        VerticalGrfStep[0] = np.concatenate((ListNa0, VerticalGrfStep[0]))
        VerticalGrfStep[len(VerticalGrfStep) - 1] = np.concatenate((VerticalGrfStep[len(VerticalGrfStep) - 1], ListNa40))
        VerticalGrfStepDataFrame = pd.DataFrame()
        for i in range(0, len(VerticalGrfStep)-1):
            VerticalGrfStepDataFrame[f"Step{i}"] = VerticalGrfStep[i]  
        MeanCutDataGrf[f"Mean{colname}"] = VerticalGrfStepDataFrame.mean(axis = 1)

    return MeanCutDataGrf


import matplotlib.pyplot as plt

def PlotCutDataGrf(MeanGrfDataframeCut):

    MeanGrfDataframeCutLeft = pd.DataFrame()
    MeanGrfDataframeCutRight = pd.DataFrame()
    for colIndex in zip(range(0, MeanGrfDataframeCut.shape[1], 2),
                        range(1,MeanGrfDataframeCut.shape[1] + 1, 2)):
        MeanGrfDataframeCutLeft[colIndex] = MeanGrfDataframeCut[MeanGrfDataframeCut.columns[colIndex[0]]]
        MeanGrfDataframeCutRight[colIndex] = MeanGrfDataframeCut[MeanGrfDataframeCut.columns[colIndex[1]]]
    MeanGrfDataframeCutLeft["MeanOfLeft"] = MeanGrfDataframeCutLeft.mean(axis = 1)
    MeanGrfDataframeCutRight["MeanOfRight"] = MeanGrfDataframeCutRight.mean(axis = 1)

    figIndex = 0
    plt.figure(figsize=(15,5))
    for cut in np.arange(MeanGrfDataframeCut.columns.shape[0]//2):
        plt.subplot(1, MeanGrfDataframeCut.columns.shape[0]//2, cut+1)
        plt.plot(MeanGrfDataframeCut[MeanGrfDataframeCut.columns[figIndex]], c="red", label="Left")
        plt.plot(MeanGrfDataframeCut[MeanGrfDataframeCut.columns[figIndex +1]], c="blue", label="Right")
        plt.plot(MeanGrfDataframeCutLeft["MeanOfLeft"], c="red", ls="--", label="Left Mean")
        plt.plot(MeanGrfDataframeCutRight["MeanOfRight"], c="blue", ls="--", label="Right Mean")
        figIndex += 2
    plt.legend(ncol = 4,
               loc = "center",
               bbox_to_anchor = (((-0.61 * ((MeanGrfDataframeCut.columns.shape[0]//2)-2)) - 0.11), -0.14))

