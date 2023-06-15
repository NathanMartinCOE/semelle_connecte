# coding: utf-8
# Modified : 2023.05.20

import pandas as pd
import numpy as np
import shutil
import h5py
import yaml
import os


import semelle_connecte
from semelle_connecte.Reader.Reader import Reader
from semelle_connecte.Tools.ToolsWriterHDF5 import ConvertWalkingToHDF5, ConvertMetadataYamlToHDF5 

class Writer(object):
    """ Class to write h5 file

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        path: the path to save the h5 file
        file_name(str): the name for the h5 file
    """

    def __init__(self, walking, path, file_name):
        self.m_walking = walking
        self.m_path = path
        self.m_file_name = file_name
        self.m_TemplateMetadata = os.path.join(semelle_connecte.Connected_Insole_Path, "semelle_connecte\\Writer\\Template_Metadata.yml")

    def writeh5(self):
        """
        Write an h5df file with all data store in a walking object
        """
        walking = self.m_walking

        StorageDataPath = self.m_path
        f = h5py.File(os.path.join(StorageDataPath, self.m_file_name), "w")
        ConvertWalkingToHDF5(f, walking)
        f.close()

        shutil.copy2(self.m_TemplateMetadata, os.path.join(StorageDataPath, "Metadata.yml"))




class WriterHDF5DataBase(object):
    """ Class to udpate the HDF5 Database

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
    """

    def __init__(self, walking=None, DataBaseName= "NantesDataBase"):
        self.m_walking = walking #### faire en list
        self.m_DataBaseName = DataBaseName
        self.m_StoragePath = os.path.join(semelle_connecte.Connected_Insole_Path, "semelle_connecte\\DataBase\\")
        self.m_DataBasePath = os.path.join(self.m_StoragePath, self.m_DataBaseName)

    def CreateHDF5DataBase(self):
        """
        This function creates an empty HDF5 database in semelle_connecte DataBase if it does not exist.
        """

        try:
            f = h5py.File(f'{self.m_DataBasePath}.hdf5', "r")
            print(f"The {self.m_DataBaseName} database already exists and is available in:")
            print(self.m_StoragePath)
        except:
            f = h5py.File(f'{self.m_DataBasePath}.hdf5','w-') # w- -> Create file, fail if exists (allows you to protect the database)
            grp_IPP = f.create_group("IPP")
            print(f"The {self.m_DataBaseName} database has been created and is available in:")
            print(self.m_StoragePath)

    def UdpateHDF5DataBase(self,path_walking, path_metadata):
        """
        This function is used to add data to the database.
        Checks whether the database exists. If it exists, continues in write mode, otherwise asks the user if he 
        wants to create it.

        Implements the database with walking and metadata files.
        """

        yaml_file = open(path_metadata, 'r')
        yaml_content = yaml.load(yaml_file)
        if yaml_content["YamlInfo"]["FileVersion"] != 1.0:
            print(f'The metadata version {yaml_content["YamlInfo"]["FileVersion"]} is not recognised')
            exit()

        IPP = str(yaml_content["SubjectInfo"]["Ipp"])  
        Test = yaml_content["Protocol"]["Test"]
        SessionNumber = yaml_content["VisitInfo"]["SessionNumber"]

        walking = Reader(path_walking).readh5() ### faire aussi list de walking + si pas un hdf5 attend metric pressure

        try:
            f = h5py.File(f'{self.m_DataBasePath}.hdf5','r+') # r+ -> Read/write, file must exist
        except:
            print(f"The {self.m_DataBaseName} database does not exist.")
            while True:
                key = input(f"Do you want to create {self.m_DataBaseName} database? yes=[y] ; no=[n]:")
                if key == "y":
                    WriterHDF5DataBase(DataBaseName=self.m_DataBaseName).CreateHDF5DataBase()
                    f = h5py.File(f'{self.m_DataBasePath}.hdf5','r+') # r+ -> Read/write, file must exist
                    break
                elif key == "n":
                    print(f"Please create {self.m_DataBaseName} database with WriterHDF5DataBase().CreateHDF5DataBase() before update")
                    exit()


        grp_IPP = f["IPP"]
        try:
            grp_IPP.create_group(IPP)
            print(f"New patient add to the DataBase with IPP: {IPP}")
        except:
            print(f"Patient with IPP: {IPP} found in the DataBase")
            pass

        grp_patient = f["IPP"][IPP]
        try:
            grp_patient.create_group(Test)
            print(f"First time this patient do a: {Test}")
        except:
            print(f"{Test} found for patient {IPP} in the DataBase")
            pass

        # Create visit session after last visit
        grp_Test = f["IPP"][IPP][Test]
        grp_visit = grp_Test.create_group(str(len(grp_Test)))

        # Add metadata to the visit session
        grp_metadata = grp_visit.create_group("metadata")
        ConvertMetadataYamlToHDF5(grp_metadata, path_metadata)

        # Add walking data to the visit session
        grp_walking = grp_visit.create_group("walking")
        ConvertWalkingToHDF5(grp_walking, walking)

        f.close()



if __name__ == '__main__':
    path_walking = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\APA\\161095\\Parcours_1\\walking_161095_Parcours_1.hdf5"
    path_metadata = "C:\\Users\\Nathan\\Desktop\\Recherche\\Github\\semelle_connecte\\semelle_connecte\\Writer\\Template_Metadata.yml"
    WriterHDF5DataBase().UdpateHDF5DataBase(path_walking= path_walking, path_metadata=path_metadata)
    
    import ipdb; ipdb.set_trace()




        