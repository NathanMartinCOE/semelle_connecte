# Sole class 
# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 04 - 03

import numpy as np

from pyCGM2.External.ktk.kineticstoolkit import timeseries

class Sole(object):
    """
    the Sole Class

    Args:
       freq(integer):  frequency in hertz
    """

    def __init__(self,freq):
        self.m_freq =  freq

        self.m_GroundReactionForce = dict()
    
    def SetGroundReactionForce(self, axis, values):
        """ set the values of the Ground Reaction Force in a members of the sole
        
        Args:
            axis : "Vertical" or "Ap" or "Mediolateral"
            values : value of the Ground Reaction Force
        """
        self.m_GroundReactionForce[axis] = values
        
    def constructTimeseries(self):
        """construct a kinetictoolkit timeseries
        """
        frames = np.arange(0, self.m_GroundReactionForce["Vertical"].shape[0])

        self.m_timeseries = timeseries.TimeSeries()
        self.m_timeseries.time = frames*1/self.m_freq
        self.m_timeseries.data["VerticalGrf"] = self.m_GroundReactionForce["Vertical"]
        self.m_timeseries.data["ApGrf"] = self.m_GroundReactionForce["Ap"]
        self.m_timeseries.data["MediolateralGrf"] = self.m_GroundReactionForce["Mediolateral"]
