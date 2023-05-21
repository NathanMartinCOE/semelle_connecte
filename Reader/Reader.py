# coding: utf-8
# Modified : 2023.05.21

import h5py

from Walking.Walking import Walking




class Reader(object):
    """ Class to read h5 file

    Args:
        h5df file
    Outputs:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
    """

    def __init__(self, path):
        self.m_path = path
    
    def readh5(self):
        f = h5py.File(self.m_path, "r")
        mass = f["UniqueValue"]["mass"][0]




        walking = Walking(mass)
        walking.setLeftLegSole()

        return walking
    

# test.keys()
# test["dict"].keys()
# test["dict"]["GroundReactionForces"].keys()
# test["dict"]["GroundReactionForces"]["LeftLeg"].keys()
# test["dict"]["GroundReactionForces"]["LeftLeg"]["DataGroundReactionForces"]

# test["dict"]["StepGrfValue"].keys()
# test["dict"]["StepGrfValue"]["LeftLeg"].keys()
# test["dict"]["StepGrfValue"]["LeftLeg"]["VerticalGrf"].keys()

# test["dict"]["DictOfDataFrameCutGrf"].keys()
# test["dict"]["DictOfDataFrameCutGrf"]["VerticalGrf"]

# test["dict"]["FunctionDynamicAssym"].keys()
# test["dict"]["FunctionDynamicAssym"]["VerticalGrf"]