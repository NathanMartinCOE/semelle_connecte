# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 04 - 03

import pandas as pd


class Walking():
    """ Class to define a walking patient
    """

    def __init__(self, mass):
        self.m_mass = mass
        self.m_anthropometric = dict()
        self.m_sole = dict()
        self.m_IMU = dict()
        self.m_GroundReactionForces = dict()
        self.m_StepGrfValue = dict()
        self.m_DataFrameDynamicSymetryScore = pd.DataFrame()
        self.m_DictOfDataFrameCutGrf = dict()
    
    def SetAnthropometric(self, RightLegSize, LeftLegSize, RightArmSize, LeftArmSize, Size):
        """ all anthropometric data are in (m) """
        self.m_anthropometric["RightLegSize"] = RightLegSize
        self.m_anthropometric["LeftLegSize"] = LeftLegSize
        self.m_anthropometric["RightArmSize"] = RightArmSize
        self.m_anthropometric["LeftArmSize"] = LeftArmSize
        self.m_anthropometric["size"] = Size

    def setLeftLegSole(self, SoleInstance):  
        """place an Sole to the left leg

        Args:
            SoleInstance (semelle_connecte.SOLE.sole) : an Semelle instance
        """
        SoleInstance.constructTimeseries()
        self.m_sole["LeftLeg"] = SoleInstance.m_timeseries

    def setRightLegSole(self, SoleInstance):  
        """place an Sole to the right leg

        Args:
            SoleInstance (semelle_connecte.SOLE.sole) : an Semelle instance
        """
        SoleInstance.constructTimeseries()
        self.m_sole["RightLeg"] = SoleInstance.m_timeseries
    
    def setLeftLegIMU(self, imuInstance):
        """attach an IMU to the left leg

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["LeftLeg"] = imuInstance.m_timeseries

    def setRightLegIMU(self, imuInstance):
        """attach an IMU to the right leg

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["RightLeg"] = imuInstance.m_timeseries

    def setLeftArmIMU(self, imuInstance):
        """attach an IMU to the left arm

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["LeftArm"] = imuInstance.m_timeseries

    def setRightArmIMU(self, imuInstance):
        """attach an IMU to the right arm

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["RightArm"] = imuInstance.m_timeseries 
    
    def setThoraxIMU(self, imuInstance):
        """attach an IMU to the Thorax (Sternum or T6-T8)

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["Thorax"] = imuInstance.m_timeseries 

    def setPelvisIMU(self, imuInstance):
        """attach an IMU to the pelvis (S2)

        Args:
            imuInstance (pyCGM2.IMU.imu.Imu): an IMU instance
        """
        imuInstance.constructTimeseries()
        self.m_IMU["Pelvis"] = imuInstance.m_timeseries 
    
    def setGroundReactionForces(self, GroundReactionForces):
        """ Add a dict with GroundReactionForces to Walking patient
        
        Args:
            GroundReactionForces get by (Walking.WalkingKinematicsProcedure.GroundReactionForceKinematicsProcedure)
        """
        self.m_GroundReactionForces = GroundReactionForces
    
    def setStepGrfValue(self, StepGrfValue):
        """ Add a dict with StepGrfValue to Walking patient
        
        Args:
            StepGrfValue get by (Walking.WalkingKinematicsProcedure.GroundReactionForceKinematicsProcedure)
        """
        self.m_StepGrfValue = StepGrfValue
    
    def setDataFrameDynamicSymetryScore(self, DataFrameDynamicSymetryScore):
        """ Add a DataFrame with the dynamic symetry function for all value 
        in walking.m_GroundReactionForces
        
        Args:
            DataFrameDynamicSymetryScore get by (Walking.WalkingKinematicsProcedure.DynamicSymetryFunctionComputeProcedure)
        """
        self.m_DataFrameDynamicSymetryScore = DataFrameDynamicSymetryScore
    
    def setDictOfDataFrameCutGrf(self, DictOfDataFrameCutGrf):
        """ Add a dict with 3 dataframe (one for each axis) of the data of Ground Reaction Forces cut in "x" parts.

        Args:
            DataFrameCutGrf get by (Walking.WalkingDataProcessingProcedure.CutDataProcessingProcedure)
        """
        self.m_DictOfDataFrameCutGrf = DictOfDataFrameCutGrf

