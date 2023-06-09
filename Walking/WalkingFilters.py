# coding: utf-8
# Modified : 2023.04.03

class WalkingKinematicsFilter(object):
    """Filter to calculate walking patient kinematics

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        procedure (semelle_connecte.Walking.AbstractKinematicsProcedure): a walking Kinematics procedure instance
    """

    def __init__(self, walking, procedure):
        self.m_walking = walking
        self.m_procedure = procedure


    def run(self):
        """run the filter
        """
        self.m_procedure.run(self.m_walking)


class WalkingGraphicsFilter(object):
    """Filter to plot walking patient kinematics

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        procedure (semelle_connecte.Walking.AbstractWalkingGraphicsProcedure): a walking Graphics procedure instance
    """

    def __init__(self, walking, procedure):
        self.m_walking = walking
        self.m_procedure = procedure


    def run(self):
        """run the filter
        """
        self.m_procedure.run(self.m_walking)


class WalkingDataProcessingFilter(object):
    """Filter to process the data of walking patient

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        procedure (semelle_connecte.Walking.AbstractWalkingDataProcessingProcedure): a walking DataProcessing procedure instance
    """

    def __init__(self, walking, procedure):
        self.m_walking = walking
        self.m_procedure = procedure


    def run(self):
        """run the filter
        """
        self.m_procedure.run(self.m_walking)


class WalkingSpatioTemporalFilter(object):
    """Filter to calculate walking patient Spatio Temporal

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance
        procedure (semelle_connecte.Walking.AbstractWalkingSpatioTemporalProcedure): a walking SpatioTemporal procedure instance
    """

    def __init__(self, walking, procedure):
        self.m_walking = walking
        self.m_procedure = procedure


    def run(self):
        """run the filter
        """
        self.m_procedure.run(self.m_walking)