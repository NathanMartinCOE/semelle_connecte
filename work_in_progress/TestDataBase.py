import os
import re

from tkinter import Tk
from tkinter.filedialog import askdirectory

from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.SOLE.FeetMe import readFeetMeMultipleCsv, ReadSpatioTemporalCsv
from semelle_connecte.Writer.Writer import Writer, WriterHDF5DataBase


root = Tk()
root.withdraw()
DataBasePath = askdirectory()
root.destroy() # Without this the matplotlib.widget doesn't work
# DataBasePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\DataBase\\"

folders = os.listdir(DataBasePath)
while True:
    key = input("Name of the DataBase:")
    DataBaseName = str(key)
    break
# DataBaseName= "TESTDataBase"

for folder in folders:
    folderPath = os.path.join(DataBasePath, folder)
    SubFolders = os.listdir(folderPath)

    for subfolder in SubFolders:
        subfolderPath = os.path.join(folderPath, subfolder)
        files = os.listdir(subfolderPath)

        # Look for HDF5 and YAML
        try :
            hdf5_name = [file for file in files if file.endswith(".hdf5")][0]
            hdf5_fullfilename = os.path.join(subfolderPath, hdf5_name)
            yaml_name = [file for file in files if file.endswith(".yml")][0]
            yaml_fullfilename = os.path.join(subfolderPath, yaml_name)
            # ========= /!\ ici rajouter une vérif que le YAML a ete modifié ========= #
            WriterHDF5DataBase(DataBaseName= DataBaseName).UdpateHDF5DataBase(path_walking= hdf5_fullfilename, path_metadata= yaml_fullfilename)
        except:
            print("HDF5 and YAML not found --------------------- Creation in progress.")
            # Look for metric file
            metrics_file = [file for file in files if file.endswith("metrics.csv")][0]
            fullfilename_metrics = os.path.join(subfolderPath, metrics_file)

            # Look for pressure file
            pressures_files = [file for file in files if file.endswith("pressure.csv")]
            fullfilenames_pressures = []
            for pressures_file in pressures_files:
                fullfilenames_pressures.append(os.path.join(subfolderPath, pressures_file))

            # Create and instantiate Walking with Metrics and Pressures
            SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames_pressures, freq = 110)
            DataFrameSpatioTemporal_Left, DataFrameSpatioTemporal_Right = ReadSpatioTemporalCsv(fullfilename_metrics)
            while True:
                key = input(f"Body mass of the patient {folder} [integer or float in kg]:")
                try:
                    mass = int(key)
                    break
                except:
                    print(f"{key} is not a valid data. Exemple: 80")
            walking = Walking(mass=80)
            walking.setLeftLegSole(SoleInstanceLeft)
            walking.setRightLegSole(SoleInstanceRight)
            walking.setDataFrameSpatioTemporal_Left(DataFrameSpatioTemporal_Left)
            walking.setDataFrameSpatioTemporal_Right(DataFrameSpatioTemporal_Right)

            # Save the HDF5 and create the YAML (CAUTION the YAML MUST be modified)
            Writer(walking = walking, path = subfolderPath, file_name = "walking.hdf5").writeh5()

