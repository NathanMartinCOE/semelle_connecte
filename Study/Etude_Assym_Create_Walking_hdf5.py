"""
Coding : utf8
Author : Nathan Martin
Create : 26/05/2023

=========================================================  Documentation =========================================================

This file is used for save walking object proceded for one or more patient.
Details of Processing for each patient and each condition:
    walking having been instantiated with the reaction forces given by the Feetme soles (readFeetmeCsv or readFeetmeMultipleCsv)
    3 procedures: GroundReactionForceKinematicsProcedure   (for more informations please read procedure documentation)
                  StandardisationProcedure                (for more informations please read procedure documentation)
                  DynamicSymetryFunctionComputeProcedure  (for more informations please read procedure documentation)

Args :
    ID the id of the patient (int)
    mass the mass of the patient (int)
    PathSRU_pressure: the path to the folder containing all the csv files (pressures) for the SRU condition.
    PathTDM_pressure: the path to the folder containing all the csv files (pressures) for the TDM condition.
    StoragePathHDF5_SRU: the path to the folder where patient_{id}_SRU_walking.hdf5 while be saved
    StoragePathHDF5_TDM: the path to the folder where patient_{id}_TDM_walking.hdf5 while be saved

Process:
    Create Walking instance (readFeetMeMultipleCsv)
    GroundReactionForceKinematicsProcedure
    NormalisationProcedure
    DynamicSymetryFunctionComputeProcedure
    Save the Walking instance (Writer().writeh5())

Output :
    And hdf5 file with the walking object.

File storage:
    patient_{id}_SRU_walking.hdf5 (Condition Urban Walking Situation) // in the folder StoragePathHDF5_SRU 
    patient_{id}_TDM_walking.hdf5 (Walking Test Condition) // in the folder StoragePathHDF5_TDM
    This two files are use in python script (Etude_Assym_Compute_R_dataset.py) 
"""

import os
from Walking.Walking import Walking
from SOLE.FeetMe import readFeetMeMultipleCsv


def main():

    ID = 0
    mass = 60


    PathSRU_pressure = f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DataPatient_pressure\\p{ID}\\SRU\\"
    PathTDM_pressure = f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DataPatient_pressure\\p{ID}\\TDM\\"
    PathConditions = [PathSRU_pressure, PathTDM_pressure]
    Names = ["SRU", "TDM"]


    for PathCondition, name in zip(PathConditions, Names):

        files = os.listdir(PathCondition)
        csv_files = [file for file in files if file.endswith(".csv")]
        fullfilenames = []
        for file_name in csv_files:
            fullfilenames.append(os.path.join(PathCondition, file_name))

        ### Instantiates the Walking object with pressure data from Feetme insoles
        SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames, freq = 110)
        walking = Walking(mass)
        walking.setLeftLegSole(SoleInstanceLeft)
        walking.setRightLegSole(SoleInstanceRight)
        print(f" =============================== Object Walking for {name} of patient {ID} create ===============================")

        ### Processing
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
        print(f" =============================== Procedure for {name} of patient {ID} done ===============================")

        ### Storage in hdf5
        from Writer.Writer import Writer
        StoragePathHDF5_SRU = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\SRU\\"
        StoragePathHDF5_TDM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\TDM\\"
        if name == "SRU":
            Writer(walking = walking, path = StoragePathHDF5_SRU, file_name = f"patient_{ID}_SRU_walking.hdf5").writeh5()
        if name == "TDM":
            Writer(walking = walking, path = StoragePathHDF5_TDM, file_name = f"patient_{ID}_TDM_walking.hdf5").writeh5()
        print(f" =============================== Object Walking for {name} of patient {ID} save ===============================")


if __name__ == '__main__':
    main()