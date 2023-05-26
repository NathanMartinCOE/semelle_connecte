import pandas as pd
import numpy as np
from tqdm import tqdm


def FeetmeDynamicSymetryScoreMetrics(DataPath):
    """
    This function compute the Dynamic Symetry Score for spatio-temporal parametre of each step.

    Args : 
        DataPath (the DataPath of the file metric get with Feetme)

    Outputs :
        DynamicSymetryScore a dataframe of Dynamic Symetry Score for :
            0   stanceDuration
            1   singleSupportDuration
            2   doubleSupportDuration
            3   swingDuration
            
    """
    data = pd.read_csv(DataPath, header=1)
    # data = data.loc[: ,["side", "stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "cadence (stride/min)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]]
    data = data.loc[: ,["side", "stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)"]]

    dataRight = data[data["side"] == "right"].drop("side", axis=1)
    dataLeft = data[data["side"] == "left"].drop("side",  axis=1)

    def FSD(ligne, col):
        xdt = dataRight.iloc[ligne,col]
        xgt = dataLeft.iloc[ligne,col]
        if max(dataRight.iloc[:,col])-min(dataRight.iloc[:,col]) == 0 :
                rangexdt = max(dataRight.iloc[:,col])-min(dataRight.iloc[:,col]) + 1
        elif max(dataRight.iloc[:,col])-min(dataRight.iloc[:,col]) != 0 :
                rangexdt = max(dataRight.iloc[:,col])-min(dataRight.iloc[:,col])  
        if max(dataLeft.iloc[:,col])-min(dataLeft.iloc[:,col]) == 0 :
            rangexgt = max(dataLeft.iloc[:,col])-min(dataLeft.iloc[:,col]) + 1
        elif max(dataLeft.iloc[:,col])-min(dataLeft.iloc[:,col]) != 0 :
            rangexgt = max(dataLeft.iloc[:,col])-min(dataLeft.iloc[:,col])
        return 2*(xdt-xgt)/(rangexdt+rangexgt)

    DynamicSymetryScore = pd.DataFrame(np.zeros((dataLeft.shape[0], dataLeft.shape[1])))
    for ligne in tqdm(range(0, dataLeft.shape[0])):
        for col in range(0, dataLeft.shape[1]):
            DynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)

    DynamicSymetryScore = DynamicSymetryScore.rename(columns={0:"stanceDuration", 
                                                            1:"singleSupportDuration", 
                                                            2:"doubleSupportDuration", 
                                                            3:"swingDuration"})
    
    return DynamicSymetryScore