# coding: utf-8
# Modified : 2023.05.21

import h5py
import numpy as np
import pandas as pd

from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.SOLE.FeetMe import FeetMe


class Reader(object):
    """ Class to read walking h5 file or walking grp in an h5 file

    Args:
        path: h5df file path
    Outputs:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
    """

    def __init__(self, path):
        self.m_path = path
    
    def readh5(self):
        f = h5py.File(self.m_path, "r")
        mass = f["UniqueValue"]["mass"][()]
        walking = Walking(mass)

        for leg in ["LeftLeg", "RightLeg"]:
            SoleInstance = FeetMe(1000)
            for axe, name in zip(["VerticalGrf", "ApGrf", "MediolateralGrf"],["Vertical", "Ap", "Mediolateral"]):
                try:
                    SoleInstance.SetGroundReactionForce(name, f["dict"]["sole"][leg][axe][:])
                except :
                    print(f'No value for ["dict"]["sole"][{leg}][{axe}]')
            try :
                SoleInstance.constructTimeseries()
            except :
                print("Error ====== SoleInstance.constructTimeseries()")
            if leg == "LeftLeg":
                try :
                    walking.setLeftLegSole(SoleInstance)
                except:
                    print("No value for Left Leg Sole")
            if leg == "RightLeg":
                try:
                    walking.setRightLegSole(SoleInstance)
                except:
                    print("No value for Right Leg Sole")

        StepGrfValue = dict()      
        for leg in ["LeftLeg", "RightLeg"]:
            StepGrfValue[leg] = dict()
            for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
                StepGrfValue[leg][axe] = dict()
                try:
                    for step in np.arange(len(f["dict"]["StepGrfValue"][leg][axe])):
                        StepGrfValue[leg][axe][step] = f["dict"]["StepGrfValue"][leg][axe][f"{step}"][:]
                except:
                    print(f'No value for ["dict"]["StepGrfValue"][{leg}][{axe}]')
        walking.setStepGrfValue(StepGrfValue)

        GroundReactionForces = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            GroundReactionForces[leg] = dict()
            try:
                GroundReactionForces[leg] = pd.DataFrame(f["dict"]["GroundReactionForces"][leg]["DataGroundReactionForces"][:])
            except:
                print(f'No value for ["dict"]["GroundReactionForces"][{leg}]["DataGroundReactionForces"]')
        walking.setGroundReactionForces(GroundReactionForces)

        DictOfDataFrameCutGrf = dict()
        FunctionDynamicAssym = dict()
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                DictOfDataFrameCutGrf[axe] = pd.DataFrame(f["dict"]["DictOfDataFrameCutGrf"][axe][:])
            except:
                print(f'No value for ["dict"]["DictOfDataFrameCutGrf"][{axe}]')
            try:
                FunctionDynamicAssym[axe] = pd.DataFrame(f["dict"]["FunctionDynamicAssym"][axe][:])
            except: 
                print(f'No value for ["dict"]["FunctionDynamicAssym"][{axe}]')
        walking.setDictOfDataFrameCutGrf(DictOfDataFrameCutGrf)
        walking.setFunctionDynamicAssym(FunctionDynamicAssym)
        
        walking.setDataFrameLeftRight(pd.DataFrame(f["DataFrame"]["DataFrameLeftRight"][:]))
        walking.setDataFrameRightLeft(pd.DataFrame(f["DataFrame"]["DataFrameRightLeft"][:]))
        walking.setDataFrameDynamicSymetryScore(pd.DataFrame(f["DataFrame"]["DataFrameDynamicSymetryScore"][:]))
        Columns_Names = ["stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]
        try:
            walking.setDataFrameSpatioTemporal_Left(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Left"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Left"]')
        try:
            walking.setDataFrameSpatioTemporal_Right(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Right"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Right"]')

        f.close()

        return walking
    
    def readh5_grp(self, f):
        """
        Arg:
            f(hdf5 grp): is the grp walking in a big h5 file
        """
        mass = f["UniqueValue"]["mass"][()]
        walking = Walking(mass)

        for leg in ["LeftLeg", "RightLeg"]:
            SoleInstance = FeetMe(1000)
            for axe, name in zip(["VerticalGrf", "ApGrf", "MediolateralGrf"],["Vertical", "Ap", "Mediolateral"]):
                try:
                    SoleInstance.SetGroundReactionForce(name, f["dict"]["sole"][leg][axe][:])
                except :
                    print(f'No value for ["dict"]["sole"][{leg}][{axe}]')
            try :
                SoleInstance.constructTimeseries()
            except :
                print("Error ====== SoleInstance.constructTimeseries()")
            if leg == "LeftLeg":
                try :
                    walking.setLeftLegSole(SoleInstance)
                except:
                    print("No value for Left Leg Sole")
            if leg == "RightLeg":
                try:
                    walking.setRightLegSole(SoleInstance)
                except:
                    print("No value for Right Leg Sole")

        StepGrfValue = dict()      
        for leg in ["LeftLeg", "RightLeg"]:
            StepGrfValue[leg] = dict()
            for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
                StepGrfValue[leg][axe] = dict()
                try:
                    for step in np.arange(len(f["dict"]["StepGrfValue"][leg][axe])):
                        StepGrfValue[leg][axe][step] = f["dict"]["StepGrfValue"][leg][axe][f"{step}"][:]
                except:
                    print(f'No value for ["dict"]["StepGrfValue"][{leg}][{axe}]')
        walking.setStepGrfValue(StepGrfValue)

        GroundReactionForces = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            GroundReactionForces[leg] = dict()
            try:
                GroundReactionForces[leg] = pd.DataFrame(f["dict"]["GroundReactionForces"][leg]["DataGroundReactionForces"][:])
            except:
                print(f'No value for ["dict"]["GroundReactionForces"][{leg}]["DataGroundReactionForces"]')
        walking.setGroundReactionForces(GroundReactionForces)

        DictOfDataFrameCutGrf = dict()
        FunctionDynamicAssym = dict()
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                DictOfDataFrameCutGrf[axe] = pd.DataFrame(f["dict"]["DictOfDataFrameCutGrf"][axe][:])
            except:
                print(f'No value for ["dict"]["DictOfDataFrameCutGrf"][{axe}]')
            try:
                FunctionDynamicAssym[axe] = pd.DataFrame(f["dict"]["FunctionDynamicAssym"][axe][:])
            except: 
                print(f'No value for ["dict"]["FunctionDynamicAssym"][{axe}]')
        walking.setDictOfDataFrameCutGrf(DictOfDataFrameCutGrf)
        walking.setFunctionDynamicAssym(FunctionDynamicAssym)
        
        walking.setDataFrameLeftRight(pd.DataFrame(f["DataFrame"]["DataFrameLeftRight"][:]))
        walking.setDataFrameRightLeft(pd.DataFrame(f["DataFrame"]["DataFrameRightLeft"][:]))
        walking.setDataFrameDynamicSymetryScore(pd.DataFrame(f["DataFrame"]["DataFrameDynamicSymetryScore"][:]))
        Columns_Names = ["stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]
        try:
            walking.setDataFrameSpatioTemporal_Left(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Left"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Left"]')
        try:
            walking.setDataFrameSpatioTemporal_Right(pd.DataFrame(columns=Columns_Names, data = f["DataFrame"]["DataFrameSpatioTemporal_Right"][:]))
        except:
            print('No value for ["DataFrame"]["DataFrameSpatioTemporal_Right"]')

        return walking
    

class ReaderMetadata(object):
    """ Class to read metadata grp in an h5 file

    Args:
        f(hdf5 grp): metadata grp in an h5 file
    Outputs:
        metadata: an metadata instance wich can be save as an yaml file
    """

    def __init__(self, f):
        self.m_f = f
    
    def run(self):
        if self.m_f["YamlInfo"]["FileVersion"][()] != 1.0:
            print("Can not read a Metadata File Version != 1.0")
            return 

        metadata = dict()

        metadata["YamlInfo"] = dict()
        metadata["YamlInfo"]["FileVersion"] = float(self.m_f["YamlInfo"]["FileVersion"][()])

        metadata["SubjectInfo"] = dict()
        metadata["SubjectInfo"]["Ipp"] = int(self.m_f["SubjectInfo"]["Ipp"][()])
        metadata["SubjectInfo"]["Name"] = self.m_f["SubjectInfo"]["Name"][()].decode("utf-8")
        metadata["SubjectInfo"]["FirstName"] = self.m_f["SubjectInfo"]["FirstName"][()].decode("utf-8")
        metadata["SubjectInfo"]["Dob"] = self.m_f["SubjectInfo"]["Dob"][()].decode("utf-8")

        metadata["VisitInfo"] = dict()
        metadata["VisitInfo"]["Date"] = self.m_f["VisitInfo"]["Date"][()].decode("utf-8")
        metadata["VisitInfo"]["SessionNumber"] = int(self.m_f["VisitInfo"]["SessionNumber"][()])
        metadata["VisitInfo"]["Age"] = float(self.m_f["VisitInfo"]["Age"][()])

        metadata["ExamInfo"] = dict()
        metadata["ExamInfo"]["Goal"] = self.m_f["ExamInfo"]["Goal"][()].decode("utf-8")
        try:
            metadata["ExamInfo"]["Comments"] = self.m_f["ExamInfo"]["Comments"][()].decode("utf-8")
        except:
            metadata["ExamInfo"]["Comments"] = None

        metadata["MP"] = dict()
        metadata["MP"]["Bodymass"] = int(self.m_f["MP"]["Bodymass"][()])
        metadata["MP"]["LeftInsoleSize"] = float(self.m_f["MP"]["LeftInsoleSize"][()])
        metadata["MP"]["RightInsoleSize"] = float(self.m_f["MP"]["RightInsoleSize"][()])

        metadata["Protocol"] = dict()
        metadata["Protocol"]["Test"] = self.m_f["Protocol"]["Test"][()].decode("utf-8")
        metadata["Protocol"]["ResearchProtocol"] = bool(self.m_f["Protocol"]["ResearchProtocol"][()])
        metadata["Protocol"]["Conditions"] = dict()
        metadata["Protocol"]["Conditions"]["Context"] = self.m_f["Protocol"]["Conditions"]["Context"][()].decode("utf-8")
        try:
            metadata["Protocol"]["Conditions"]["ContextComments"] = self.m_f["Protocol"]["Conditions"]["ContextComments"][()].decode("utf-8")
        except:
            metadata["Protocol"]["Conditions"]["ContextComments"] = None
        metadata["Protocol"]["Conditions"]["Orthosis"] = bool(self.m_f["Protocol"]["Conditions"]["Orthosis"][()])
        metadata["Protocol"]["Conditions"]["ExternalAid"] = bool(self.m_f["Protocol"]["Conditions"]["ExternalAid"][()])
        metadata["Protocol"]["Conditions"]["PersonalAid"] = bool(self.m_f["Protocol"]["Conditions"]["PersonalAid"][()])
        try:
            metadata["Protocol"]["Conditions"]["Comments"] = self.m_f["Protocol"]["Conditions"]["Comments"][()].decode("utf-8")
        except:
            metadata["Protocol"]["Conditions"]["Comments"] = None
        metadata["Protocol"]["Conditions"]["Assessor"] = self.m_f["Protocol"]["Conditions"]["Assessor"][()].decode("utf-8")

        return metadata
        