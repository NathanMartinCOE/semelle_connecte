# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 29
# Modified : 2023 - 04 - 05

import pandas as pd
import numpy as np

from Tools.ToolsInterpolationGrf import InterpolationGrf


class AbstractWalkingDataProcessingProcedure(object):
    """abstract procedure """
    def __init__(self):
        pass
    def run(self):
        pass


class CutDataProcessingProcedure(AbstractWalkingDataProcessingProcedure):
    """ This procedure cut the complete records in a number of cut chosen by user and save all 
    the Ground Reaction Force for each axes in each cut for the two legs.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        DictOfDataFrameCutGrf a dictionnary with 3 DataFrame of Ground Reaction Force one
        for each axes "VerticalGrf" "ApGrf" "MediolateralGrf"

        DictOfDataFrameCutGrf is save in walking.setDictOfDataFrameCutGrf

        DictOfDataFrameCutGrf {
                                "VerticalGrf"       = DataFrame(Left(i), Right(i)),
                                "ApGrf"             = DataFrame(Left(i), Right(i)),
                                "MediolateralGrf"   = DataFrame(Left(i), Right(i))
                                }
        for i in [1 : number of cut]
        Left(i) = all Ground Reaction Force value for the i part of records

    Exemple :
        Left VerticalGrf record = 0,1,2,3,4,5,6,7,8,9,10,11
        Right VerticalGrf record = a,b,c,d,e,f,g,h,i,j,k,l
        You want 3 portions for this records the procedure give you this :

        DictOfDataFrameCutGrf {
                                "VerticalGrf" = pd.DatFrame(
                                                            Left1 = 0,1,2,3
                                                            Right1 = a,b,c,d
                                                            Left2 = 4,5,6,7
                                                            Right2 = e,f,g,h
                                                            Left3 = 8,9,10,11
                                                            Right3 = i,j,k,l
                                                            )

                            }           
    """

    def __init__(self):
        super(CutDataProcessingProcedure, self).__init__()
        self.m_CutNumber = int
    
    def setCutNumber(self, n_cut):
        self.m_CutNumber = n_cut

    def run(self, walking):
        n_cut = self.m_CutNumber
        def CutDataGrf(GrfLeft, GrfRight, n_cut):
            GrfDataframeCut = pd.DataFrame()
            if n_cut != 0 : 
                indexLeft = GrfLeft.shape[0] // n_cut
                indexRight = GrfRight.shape[0] // n_cut
                valindexLeft = indexLeft
                valindexRight = indexRight
                ListIndexLeft = [0]
                ListIndexRight = [0]
                for cut in np.arange(n_cut):
                    ListIndexLeft.append(valindexLeft)
                    valindexLeft = valindexLeft + indexLeft
                    ListIndexRight.append(valindexRight)
                    valindexRight = valindexRight + indexRight
                for index in zip(range(0, len(ListIndexLeft[0: -1])), range(0, len(ListIndexRight[0: -1]))):
                    GrfDataframeCut[f"Left{index[0]+1}"] = GrfLeft[ListIndexLeft[index[0]] : ListIndexLeft[index[0]+1]]
                    GrfDataframeCut[f"Right{index[1]+1}"] = GrfRight[ListIndexRight[index[1]] : ListIndexRight[index[1]+1]]
            elif n_cut == 0 :
                GrfDataframeCut["Left"] = GrfLeft
                GrfDataframeCut["Right"] = GrfRight
            return GrfDataframeCut
        
        DictOfDataFrameCutGrf = dict()
        axis = ["VerticalGrf", "ApGrf", "MediolateralGrf"]
        for axe in axis :
            if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                GrfDataframeCut = CutDataGrf(GrfLeft = pd.array(walking.m_sole["LeftLeg"].data[axe]), 
                                             GrfRight = pd.array(walking.m_sole["RightLeg"].data[axe]), 
                                             n_cut = n_cut)
                DictOfDataFrameCutGrf[axe] = GrfDataframeCut
            else :
                DictOfDataFrameCutGrf[axe] = None
                print(f"No value for {axe} Ground Reaction Force")
            
        walking.setDictOfDataFrameCutGrf(DictOfDataFrameCutGrf)


class NormalisationProcedure(AbstractWalkingDataProcessingProcedure):
    """ This procedure normalized Ground Reaction in % of cycle for all step in 
    walking.m_StepGrfValue. Note that if walking.m_StepGrfValue is empty this procedure
    run GroundReactionForceKinematicsProcedure() for get the Ground Reaction Force of each step.
    
    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        update walking.m_StepGrfValue with normalized value of Ground Reaction in % of cycle
    """

    def __init__(self):
        super(NormalisationProcedure, self).__init__()
    
    def run(self, walking):
        if len(walking.m_StepGrfValue)==0 :
            from Walking.WalkingFilters import WalkingKinematicsFilter
            from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure

            procedure = GroundReactionForceKinematicsProcedure()
            WalkingKinematicsFilter(walking, procedure).run()
        

        mass = walking.m_mass

        Legs = ["LeftLeg", "RightLeg"]
        Axes = ["VerticalGrf", "ApGrf"]   # l'axe  "MediolateralGrf" pas encore présent dans le dict
        Steps = np.arange(len(walking.m_StepGrfValue['LeftLeg']['VerticalGrf']))
        GrfValues = np.arange(len(walking.m_StepGrfValue['LeftLeg']['VerticalGrf'][0]))
        for leg in Legs:
            for axe in Axes:
                for step in Steps:
                    xnormalised, ynormalised = InterpolationGrf(walking.m_StepGrfValue[leg][axe][step]) # Normalisation en % cycle
                    ynormalised = ynormalised/ mass                                                     # Normalisation en % poids
                    walking.m_StepGrfValue[leg][axe][step] = ynormalised


