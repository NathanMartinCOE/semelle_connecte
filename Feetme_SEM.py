"""
Coding : utf8
Author : Nathan Martin
Create : 30/05/2023

=========================================================  Documentation =========================================================

This file is used to process all walking_{name}_test{X}.hdf5 files for compute the standard error of measurement.

Input :
    PathMSE: the path to the folder containing all the hdf5 files (walking).

hdf5 file (walking):
    The files are created by the python script (Feetme_SEM_Create_Walking_hdf5.py)
    File contents :
        walking having been instantiated with the reaction forces given by the Feetme soles (readFeetmeCsv or readFeetmeMultipleCsv)
        3 procedures: GroundReactionForceKinematicsProcedure   (for more informations please read procedure documentation)
                       StandardisationProcedure                (for more informations please read procedure documentation)
                       DynamicSymetryFunctionComputeProcedure  (for more informations please read procedure documentation)
        All stored in the .hdf5 file
    File storage:
        walking_{name}_test{X}.hdf5 // in PathMSE

Output:
This outputs a plot with 2 sublopts for each leg : 
    Left plot for left leg // Right plot for right leg
    For each subplot the MSE for the leg is write in the title.
Legend :
    Red   : mean ground reaction force of Left leg 
    Blue  : mean ground reaction force of Right leg
    Black : standard error of measurement at each time
    Dashed gray : all ground reaction force for the corresponding leg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from math import sqrt
from Reader.Reader import Reader

PathMSE = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\MSE\\"

files = os.listdir(PathMSE)
hdf5_files = [file for file in files if file.endswith(".hdf5")]

### =============== For DataRaw ================
frames = ["Frame_" + str(i) for i in range(1000)]
columns_names = ["id", "test", "leg"] + frames
data = []

for file in hdf5_files:
    PathHDF5 = PathMSE
    NameFileHDF5 = str(file)
    DataPathHDF5 = os.path.join(PathHDF5, NameFileHDF5)
    walking = Reader(DataPathHDF5).readh5()

    ### ======== look for the name of participant ===========
    find_name = re.search(r"walking_(.*?)_test", NameFileHDF5)
    if find_name:
        name = find_name.group(1)
    else:
        print("No name find. ----------- Please be sure to name the hdf5 as walking_name_testX.hdf5 ")
    ### ======== look for the number of the test session =====
    find_N_test = re.search(r"test(.*?).hdf5", NameFileHDF5)
    if find_N_test:
        N_test = find_N_test.group(1)
    else:
        print("Number of test not find. ----------- Please be sure to name the hdf5 as walking_name_testX.hdf5 ")

    ### == Instanciated one row_data witch contain "name", "test number", "leg side", GRF value for 0-1000 =====
    DataMeanGrf = pd.DataFrame()
    for leg in ["LeftLeg", "RightLeg"]:
        DataStepGrfValue = pd.DataFrame()
        for step in np.arange(0, len(walking.m_StepGrfValue[leg]["VerticalGrf"])):
            DataStepGrfValue[f"step{step}"] = walking.m_StepGrfValue[leg]["VerticalGrf"][step]
        DataMeanGrf[leg] = DataStepGrfValue.mean(axis=1, skipna=True)
        row_data = [name, N_test, leg]
        row_data = row_data + DataMeanGrf[leg].values.tolist()
        ### == Add row_data to data for the DataFrame DataRaw ==
        data.append(row_data)


### ======= Compute Standard Deviation of each subject beetween all they test for Right and Left leg ================
DataRaw = pd.DataFrame(data, columns= columns_names)
DataRawRight = DataRaw[DataRaw["leg"]=="RightLeg"]
DataRawLeft = DataRaw[DataRaw["leg"]=="LeftLeg"]
DataSdRight = DataRawRight.drop("test", axis='columns').groupby([DataRawRight["id"]]).std()
DataSdLeft = DataRawLeft.drop("test", axis='columns').groupby([DataRawLeft["id"]]).std()

### ======= Compute the Root Mean Squared Avarage for Right and Left leg ============================================
def RMSA(DataSd):
    DataSdSquared = DataSd**2
    SEM = []
    for col in DataSdSquared.columns:
        SEM.append(sqrt(DataSdSquared[col].sum()/DataSdSquared.shape[0]))
    DataSEM = pd.DataFrame()
    DataSEM["SEM"] = SEM
    return DataSEM.T

DataSEMRight = RMSA(DataSdRight)
DataSEMLeft = RMSA(DataSdLeft)

### =============================== Compute SEM for Right and Left leg ===============================================
SEM_right = DataSEMRight.mean(axis="columns").values[0]
print(f"The standard error of measurement for right is -------------------- {round(SEM_right,4)}")
SEM_left = DataSEMLeft.mean(axis="columns").values[0]
print(f"The standard error of measurement for left is -------------------- {round(SEM_left,4)}")



MeanValueGrfRight = DataRawRight.drop(["test", "id", "leg"], axis='columns').mean(axis=0).values
MeanValueGrfLeft = DataRawLeft.drop(["test", "id", "leg"], axis='columns').mean(axis=0).values

plt.figure()
plt.subplot(1,2,1)
plt.title(f"Left Leg --- SEM = {round(SEM_left,4)}")
plt.plot(MeanValueGrfLeft, label='Left Leg', c='r')
plt.plot(DataSEMLeft.T.values, label="SEM", c="black")
for grf in DataRawLeft.drop(["test", "id", "leg"], axis='columns').values:
    plt.plot(grf, c='grey', ls="--")
plt.legend()
plt.subplot(1,2,2)
plt.title(f"Right Leg --- SEM = {round(SEM_right,4)}")
plt.plot(MeanValueGrfRight, label='Right Leg', c='b')
plt.plot(DataSEMRight.T.values, label="SEM", c="black")
for grf in DataRawRight.drop(["test", "id", "leg"], axis='columns').values:
    plt.plot(grf, c='grey', ls="--")
plt.legend()
plt.show()
