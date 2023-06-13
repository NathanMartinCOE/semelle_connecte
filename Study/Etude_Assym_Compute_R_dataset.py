"""
Coding : utf8
Author : Nathan Martin
Create : 26/05/2023

=========================================================  Documentation =========================================================

This file is used to process all the "metrics" and "walking" files in order to calculate the asymmetry of the following walking parameters
stanceDuration (ms); singleSupportDuration (ms); doubleSupportDuration (ms); swingDuration (ms); VerticalGrf (%).
These are stored in a dataframe for each test condition.

Input :
    PathSRU: the path to the folder containing all the csv files (metrics) and hdf5 files (walking) for the SRU condition.
    PathTDM: the path to the folder containing all the csv files (metrics) and hdf5 files (walking) for the TDM condition.
    PathSaveData: the path of the folder where the csv files of the dataframes for each condition will be stored.

Csv file (metrics) :
    File given by feetme: {dd-mm-yyyy-hh-mm-ss}-metric.csv (This code is compatible with version 6)
    To organise the files better, I recommend renaming them: 
        patient_id_TDM_metrics.csv (Condition Test De Marche) // stored in the folder to which the PathTDM points
        patient_id_SRU_metrics.csv (Condition Situation de Randonnée Urbaine) // stored in the folder to which the PathSRU points

hdf5 file (walking):
    The files are created by the python script (Etude_Assym_Create_Walking_hdf5.py)
    File contents :
        walking having been instantiated with the reaction forces given by the Feetme soles (readFeetmeCsv or readFeetmeMultipleCsv)
        3 procedures: GroundReactionForceKinematicsProcedure   (for more informations please read procedure documentation)
                       StandardisationProcedure                (for more informations please read procedure documentation)
                       DynamicSymetryFunctionComputeProcedure  (for more informations please read procedure documentation)
        All stored in the .hdf5 file
        The VerticalGrf parameter (%) is the average of: walking.m_FunctionDynamicAssym["VerticalGrf"].
    File storage:
        patient_id_TDM_walking.hdf5 (Walking Test Condition) // in the folder to which the PathTDM points
        patient_id_SRU_walking.hdf5 (Condition Urban Walking Situation) // in the folder to which the PathSRU points.

Output:
This outputs a dataframe for each assessment condition, they are stored in the PathSaveData file.
    DynamicSymetryScoreMean_TDM (Walk Test Condition)
    DynamicSymetryScoreMean_SRU (Urban Walking Condition)
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():

    PathSRU = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\SRU\\"
    PathTDM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\TDM\\"
    PathConditions = [PathSRU, PathTDM]
    Names = ["SRU", "TDM"]

    for PathCondition, name in zip(PathConditions, Names):
        print(f" =============================== Processing for {name} dataset ===============================")

        files = os.listdir(PathCondition)

        stanceDuration = []
        singleSupportDuration = []
        doubleSupportDuration = []
        swingDuration = []
        VerticalGrf = []

        # Filter files by type
        csv_files = [file for file in files if file.endswith(".csv")]
        hdf5_files = [file for file in files if file.endswith(".hdf5")]

        # Use of csv (calculation of the asymmetry of average metrics)
        for file in csv_files:
            PathMetric = PathCondition
            NameFileMetric = str(file)
            DataPathMetric = os.path.join(PathMetric, NameFileMetric)

            from semelle_connecte.Tools.ToolsFeetmeDynamicSymetryScoreMetrics import FeetmeDynamicSymetryScoreMetrics
            DynamicSymetryScoreTotal = FeetmeDynamicSymetryScoreMetrics(DataPathMetric)

            stanceDuration.append(DynamicSymetryScoreTotal.mean(axis=0)["stanceDuration"])
            singleSupportDuration.append(DynamicSymetryScoreTotal.mean(axis=0)["singleSupportDuration"])
            doubleSupportDuration.append(DynamicSymetryScoreTotal.mean(axis=0)["doubleSupportDuration"])
            swingDuration.append(DynamicSymetryScoreTotal.mean(axis=0)["swingDuration"])

        # Use of hdf5 (calculation of the asymmetry of the average reaction force)
        for file in hdf5_files:
            from semelle_connecte.Reader.Reader import Reader
            PathHDF5 = PathCondition
            NameFileHDF5 = str(file)
            DataPathHDF5 = os.path.join(PathHDF5, NameFileHDF5)
            walking = Reader(DataPathHDF5).readh5()
            VerticalGrf.append(walking.m_FunctionDynamicAssym["VerticalGrf"].mean().values[0])

        if name == "SRU":
            DynamicSymetryScoreMean_SRU = pd.DataFrame({"stanceDuration" :  stanceDuration,
                                                    "singleSupportDuration" : singleSupportDuration,
                                                    "doubleSupportDuration" :  doubleSupportDuration,
                                                    "swingDuration" : swingDuration,
                                                    "VerticalGrf" : VerticalGrf})
        if name == "TDM":
            DynamicSymetryScoreMean_TDM = pd.DataFrame({"stanceDuration" :  stanceDuration,
                                                    "singleSupportDuration" : singleSupportDuration,
                                                    "doubleSupportDuration" :  doubleSupportDuration,
                                                    "swingDuration" : swingDuration,
                                                    "VerticalGrf" : VerticalGrf})
        
        print(f" =============================== Dataset {name} save ===============================")

    PathSaveData = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\"
    DynamicSymetryScoreMean_SRU.to_csv(os.path.join(PathSaveData, "DynamicSymetryScoreMean_SRU.csv"))
    DynamicSymetryScoreMean_TDM.to_csv(os.path.join(PathSaveData, "DynamicSymetryScoreMean_TDM.csv"))


if __name__ == '__main__':
    main()