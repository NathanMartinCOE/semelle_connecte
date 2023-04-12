# FeetMe Sole class 
# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 04 - 03

import numpy as np
import pandas as pd

from pyCGM2.External.ktk.kineticstoolkit import timeseries
# from semelle_connecte.SOLE import sole
from SOLE import sole

class FeetMe(sole.Sole):
    """
    a Sole-inherited class to work with FeetMe Sole

    Args:
       freq(integer):  frequency in hertz
    """

    def __init__(self,freq):
        super(FeetMe, self).__init__(freq)
    
    def constructTimeseries(self):
        """construct a kinetictoolkit timeseries
        """
        frames = np.arange(0, self.m_GroundReactionForce["Vertical"].shape[0])

        self.m_timeseries = timeseries.TimeSeries()
        self.m_timeseries.time = frames*1/self.m_freq
        self.m_timeseries.data["VerticalGrf"] = self.m_GroundReactionForce["Vertical"]
        self.m_timeseries.data["ApGrf"] = self.m_GroundReactionForce["Ap"]
        self.m_timeseries.data["MediolateralGrf"] = self.m_GroundReactionForce["Mediolateral"]


def readFeetMeCsv(fullfilename,freq): #### à modifier quand j'aurais un csv ..
    data = pd.read_csv(fullfilename)

    SoleInstance = FeetMe(freq)

    SoleInstance.SetGroundReactionForce("Vertical", data["VerticalVGrf"].to_numpy())
    SoleInstance.SetGroundReactionForce("Ap", data["ApGrf"].to_numpy())
    SoleInstance.SetGroundReactionForce("Mediolateral", data["MediolateralGrf"].to_numpy())
    
    return SoleInstance