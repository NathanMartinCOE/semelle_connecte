"""
Coding : utf8
Author : Nathan Martin
Create : 30/05/2023

=========================================================  Documentation =========================================================

This file is used for save walking object proceded for one or more patient.
Details of Processing for each patient and each condition:
    walking having been instantiated with the reaction forces given by the Feetme soles (readFeetmeCsv or readFeetmeMultipleCsv)
    3 procedures: GroundReactionForceKinematicsProcedure   (for more informations please read procedure documentation)
                  StandardisationProcedure                (for more informations please read procedure documentation)
                  DynamicSymetryFunctionComputeProcedure  (for more informations please read procedure documentation)

Args :
    list_num(int): The list of test numbers
    list_mass(int): The list of each patient's mass for each test
    PathSEM_pressure: The path to the folder containing all the csv files (pressures).
    StoragePathHDF5_SEM: The path to the folder where walking_{name}_test{N}.hdf5 while be saved

Process:
    Create Walking instance (readFeetMeMultipleCsv)
    GroundReactionForceKinematicsProcedure
    NormalisationProcedure
    DynamicSymetryFunctionComputeProcedure
    Save Walking instance (Writer().writeh5())

Output :
    And hdf5 file with the walking object.

File storage:
    walking_{name}_test{N}.hdf5  // in the folder StoragePathHDF5_SEM 
    This file is use in python script (Feetme_SEM.py) 
"""

import os
import re
from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.SOLE.FeetMe import readFeetMeMultipleCsv


def main():

    list_num = range(1,28)
    list_mass = [60] * 27


    for num, mass in zip(list_num, list_mass):
        print(f" ================================================ Open new test ({num}) ================================================")

        PathSRU_pressure = f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\MSE\\data_pressure\\test{num}\\"

        files = os.listdir(PathSRU_pressure)
        csv_files = [file for file in files if file.endswith(".csv")]
        fullfilenames = []

        ### This loop must not loop with anything else
        for file_name in csv_files:
            fullfilenames.append(os.path.join(PathSRU_pressure, file_name))

        ### ======== Look for the name of participant ===========
        find_name = re.search(r"(.*?)_test", file_name) 
        if find_name:
            name = find_name.group(1)
        else:
            print("Name of participant not find. ----------- Please be sure to name the csv as name_testX_X.hdf5 ")
        ### ======== Look for the number of the test session =====
        find_N_test = re.search(r"test(.*?)_", file_name)
        if find_N_test:
            N_test = find_N_test.group(1)
        else:
            print("Number of test not find. ----------- Please be sure to name the csv as name_testX_X.hdf5 ")


        ### Instantiates the Walking object with pressure data from Feetme insoles
        SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames, freq = 110)
        walking = Walking(mass)
        walking.setLeftLegSole(SoleInstanceLeft)
        walking.setRightLegSole(SoleInstanceRight)
        print(f" =============================== Object Walking for {name} test {N_test} create ===============================")

        ### Processing
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
        print(f" =============================== Procedure for {name} test {N_test} done ===============================")

        ### Storage in hdf5
        from semelle_connecte.Writer.Writer import Writer
        StoragePathHDF5_SEM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\MSE\\"
        Writer(walking = walking, path = StoragePathHDF5_SEM, file_name = f"walking_{name}_test{N_test}.hdf5").writeh5()
        print(f" =============================== Walking for for {name} test {N_test} store ===============================")


if __name__ == '__main__':
    main()