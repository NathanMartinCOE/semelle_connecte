# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 06 - 20
# Modified : 

import numpy as np
import pandas as pd

import os
import h5py
import yaml
import shutil  

import semelle_connecte
from semelle_connecte.Reader.Reader import Reader, ReaderMetadata
from semelle_connecte.Writer.Writer import Writer, WriterMetadata, WriterHDF5DataBase


class AbstractExtractor(object):
    """
    Abstract extractor

    Args:
        Request_Extractor(path): Request_Extractor.yml file path
        HDF5_file(path):         NameDataBase.h5 file path
        OutputFolder(path):     Output folder paths
        MultipleFiles(bool):          False(default) -> create a single h5 file with the sub-selection.
                                 True -> create one h5 file per patient who meets the selection criteria.
    """
    def __init__(self, Request_Extractor, HDF5_file, OutputFolder, MultipleFiles = False):
        self.m_Request_Extractor = Request_Extractor
        self.m_HDF5_file = HDF5_file
        self.m_OutputFolder = OutputFolder
        self.m_MultipleFiles = MultipleFiles
        
    def run(self):
        pass


class HDF5Extractor(AbstractExtractor):
    def __init__(self, Request_Extractor, HDF5_file, OutputFolder, MultipleFiles=False):
        super(HDF5Extractor, self).__init__(Request_Extractor, HDF5_file, OutputFolder, MultipleFiles)
        
    def run(self):
        # Checks that the extraction request file can be found
        try:
            yaml_file = open(self.m_Request_Extractor, 'r')
        except: 
            print(f"File {self.m_Request_Extractor} not found")
            exit()
        yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
        if yaml_content["ExtractorRequestInfo"]["FileVersion"] != 1.0:
            print(f'The Request Extractor version {yaml_content["ExtractorRequestInfo"]["FileVersion"]} is not recognised')
            exit()
        # Checks that the HDF5 file can be found
        try:
            hdf5_file = h5py.File(self.m_HDF5_file, "r")
        except: 
            print(f"File {self.m_HDF5_file} not found")
            exit()
        
        # =============================================================================================
        # ================================== DataBase Request =========================================
        # =============================================================================================
        Inclued =  yaml_content["DataBaseRequest"]["IPP"]["Inclued"]
        Exclued =  yaml_content["DataBaseRequest"]["IPP"]["Exclued"]
        Test =     yaml_content["DataBaseRequest"]["Test"]
        Sessions = yaml_content["DataBaseRequest"]["Sessions"]
        # == IPP Filter ==
        if Inclued == "All":
            IPP_list = [i for i in hdf5_file["IPP"].keys()]
        else:
            IPP_list = Inclued
        if Exclued != "None":
            for n in Exclued:
                IPP_list.remove(str(n))
        # == Test Filter ==
        if Test == "All":
            Test_list = ["6MWT", "10mWT", "400mWT", "25sWT", "FWT"]
        else:
            Test_list = Test
        # == Sessions Filter ==
        if Sessions != "All":
            Sessions_list = Sessions
        
        # Create a file tree: DataBaseRequest-IPP-Test-Session
        path_DataBaseRequest = os.path.join(self.m_OutputFolder, "DataBaseRequest")
        # shutil.rmtree(path_DataBaseRequest)  # === DELETE folder DataBaseRequest =======
        os.mkdir(path_DataBaseRequest)
        for ipp in IPP_list:
            path_IPP = os.path.join(path_DataBaseRequest, str(ipp))
            os.mkdir(path_IPP)
            for test in Test_list:
                path_test = os.path.join(path_IPP, str(test))
                os.mkdir(path_test)
                if Sessions == "All":
                    try:
                        Sessions_list = [i for i in hdf5_file["IPP"][ipp][test].keys()]
                        for session in Sessions_list:
                            path_session = os.path.join(path_test, str(session))
                            os.mkdir(path_session)
                            # Then put the walking.h5 and metadata.yaml files in it
                            try:
                                walking = Reader(None).readh5_grp(f= hdf5_file["IPP"][ipp][test][session]["walking"])
                                Writer(walking = walking, path = path_session, file_name = f"{ipp}_{test}_{session}_walking.hdf5").writeh5(CreateMetadata=False)
                            except:
                                print(f"No walking for [{ipp}][{test}][{session}]")
                            try:
                                metadata = ReaderMetadata(f= hdf5_file["IPP"][ipp][test][session]["metadata"]).run()
                                WriterMetadata(Metadata = metadata, StoragePath = path_session, FileName = f"{ipp}_{test}_{session}_metadata.yml").run()
                            except:
                                print(f"No walking for [{ipp}][{test}][{session}]")
                    except:
                        pass
                if Sessions != "All":
                    try:
                        for session in Sessions_list:
                            path_session = os.path.join(path_test, str(session))
                            os.mkdir(path_session)
                            # Then put the walking.h5 and metadata.yaml files in it
                            try:
                                walking = Reader(None).readh5_grp(f= hdf5_file["IPP"][ipp][test][session]["walking"])
                                Writer(walking = walking, path = path_session, file_name = f"{ipp}_{test}_{session}_walking.hdf5").writeh5(CreateMetadata=False)
                            except:
                                print(f"No walking for [{ipp}][{test}][{session}]")
                            try:
                                metadata = ReaderMetadata(f= hdf5_file["IPP"][ipp][test][session]["metadata"]).run()
                                WriterMetadata(Metadata = metadata, StoragePath = path_session, FileName = f"{ipp}_{test}_{session}_metadata.yml").run()
                            except:
                                print(f"No walking for [{ipp}][{test}][{session}]")
                    except:
                        pass
        
        # ============= Create an h5 Data Base with DataBaseRequest =========================
        folders = os.listdir(path_DataBaseRequest)
        for folder in folders:
            folderPath = os.path.join(path_DataBaseRequest, folder)
            SubFolders = os.listdir(folderPath)
            for subfolder in SubFolders:
                SubfolderPath = os.path.join(folderPath, subfolder)
                SubSubFolders = os.listdir(SubfolderPath)
                for subsubfolder in SubSubFolders:
                    subsubfolderPath = os.path.join(SubfolderPath, subsubfolder)
                    try:
                        files = os.listdir(subsubfolderPath)
                        hdf5_name = [file for file in files if file.endswith(".hdf5")][0]
                        hdf5_fullfilename = os.path.join(subsubfolderPath, hdf5_name)
                        yaml_name = [file for file in files if file.endswith(".yml")][0]
                        yaml_fullfilename = os.path.join(subsubfolderPath, yaml_name)
                        WriterHDF5DataBase(DataBaseName= "DataBaseRequest").UdpateHDF5DataBase(path_walking= hdf5_fullfilename, path_metadata= yaml_fullfilename)
                    except:
                        print(f"No data in {subsubfolderPath}")
        # ============= Delete the DataBaseRequest folder ===================================
        shutil.rmtree(path_DataBaseRequest)


        # # =============================================================================================
        # # ============================== MetadataRequest Request ======================================
        # # =============================================================================================
        # Dob =  yaml_content["MetadataRequest"]["SubjectInfo"]["Dob"]

        # # == Dob Filter ==

        import ipdb; ipdb.set_trace()




if __name__ == '__main__':
    Request_Extractor = "C:\\Users\\Nathan\\Desktop\\Recherche\\Extract_DataBase\\Extractor_Request.yml"
    HDF5_file = "C:\\Users\\Nathan\\Desktop\\Recherche\\Github\\semelle_connecte\\semelle_connecte\\DataBase\\NantesDataBase.hdf5"
    OutputFolder = "C:\\Users\\Nathan\\Desktop\\Recherche\\Extract_DataBase"
    HDF5Extractor(Request_Extractor, HDF5_file, OutputFolder, MultipleFiles=False).run()