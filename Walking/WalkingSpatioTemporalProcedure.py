# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 06 - 09
# Modified : 


class AbstractWalkingSpatioTemporalProcedure(object):
    """abstract procedure """
    def __init__(self):
        pass
    def run(self):
        pass



class SpatioTemporalGaitCycleProcedure(AbstractWalkingSpatioTemporalProcedure):
    def __init__(self):
        super(SpatioTemporalGaitCycleProcedure, self).__init__()

    def run(self, walking):
        try :
            DataFrameSpatioTemporal = walking.m_DataFrameSpatioTemporal
        except :
            exit()
        
        ## The plot is not possible because indexing is false

