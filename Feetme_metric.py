### Parametres cinématiques


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_column', 70)

Path = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe"
Name = "2023-05-24_15-46-27_metrics.csv"

DataPath = os.path.join(Path, Name)

data = pd.read_csv(DataPath, header=1)

data = data[data.columns[data.isna().sum()/data.shape[0] <0.99]]

data = data.loc[: ,["side", "stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "cadence (stride/min)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]]

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
for ligne in range(0, dataLeft.shape[0]):
    for col in range(0, dataLeft.shape[1]):
        import ipdb; ipdb.set_trace()
        DynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)


import ipdb; ipdb.set_trace()