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
        pass

        ### I want to compute a DataFrame for plot the same graph as FeetMe but better with right and left   
        ### But The plot is not possible because indexing is false

