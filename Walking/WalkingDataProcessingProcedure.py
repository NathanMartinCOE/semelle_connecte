# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 29
# Modified : 2023 - 04 - 05

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Tools.ToolsInterpolationGrf import InterpolationGrf
from Tools.ToolsInterpolationGrf import Interpolation


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
        """ To choose the number of cut
        Args: 
            n_cut(int) : the number for cut the data
        """
        self.m_CutNumber = n_cut

    def run(self, walking):
        n_cut = self.m_CutNumber
        def CutDataGrf(GrfLeft, GrfRight, n_cut):
            from Tools.ToolsGetStepEvent import GetStepEvent
            from Tools.ToolsInterpolationGrf import Interpolation

            GrfDataframeCut = pd.DataFrame()
            if n_cut != 0 : 
                HeelStrikeLeft, ToeOffLeft = GetStepEvent(walking.m_sole["LeftLeg"].data["VerticalGrf"])
                HeelStrikeRight, ToeOffRight = GetStepEvent(walking.m_sole["RightLeg"].data["VerticalGrf"])
                index_Left = 0
                index_Right = 0
                index = 0
                n_stepLeft = len(HeelStrikeLeft) // 3
                n_stepRight = len(HeelStrikeRight) // 3
                Len = min([len(GrfLeft[HeelStrikeLeft[0]: ToeOffLeft[0 + n_stepLeft - 1]]), len(GrfRight[HeelStrikeRight[0]: ToeOffRight[0 + n_stepRight - 1]])])
                
                for cut in np.arange(n_cut):
                    x, GrfDataframeCut[f"Left{index}"] = Interpolation(GrfLeft[HeelStrikeLeft[index_Left]: ToeOffLeft[index_Left + n_stepLeft - 1] + 10], xnew_num= Len)
                    x, GrfDataframeCut[f"Right{index}"] = Interpolation(GrfRight[HeelStrikeRight[index_Right]: ToeOffRight[index_Right + n_stepRight - 1] + 10], xnew_num= Len)
                    index_Left += n_stepLeft
                    index_Right += n_stepRight
                    index += 1

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
    """ This procedure normalized Ground Reaction in % of cycle for all step in walking.m_StepGrfValue. 

    /!\ Note that if walking.m_StepGrfValue is empty this procedure run GroundReactionForceKinematicsProcedure() for 
    get the Ground Reaction Force of each step. /!\ 
    
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
        Axes = ["VerticalGrf", "ApGrf", "MediolateralGrf"]   # MediolateralGrf peut entrainer des bug

        for leg in Legs:
            Steps = np.arange(len(walking.m_StepGrfValue[leg]['VerticalGrf']))
            for axe in Axes:
                for step in Steps:
                    try :
                        xnormalised, ynormalised = Interpolation(walking.m_StepGrfValue[leg][axe][step], 1000) # Normalisation en % cycle
                    except :
                        ynormalised = [np.nan] * 1000
                    # ynormalised = ynormalised/ mass    ## deja normalisé sur la mass lors de l'import    # Normalisation en % poids
                    walking.m_StepGrfValue[leg][axe][step] = ynormalised


class DeleteStepProcedure(AbstractWalkingDataProcessingProcedure):
    """ This procedure show you each Right and Left step of walkingm_StepGrfValue and 
    if you find that one of this step is poor du to data filtered and random noise you can
    delete it.

    Use 'l' for delete Left ; 'r' for delete Right ; 'lr' for delete both and 'n' for next figure.
    If you want to interrupt the code you can type: 'exit-e'.
    
    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        update walking.m_StepGrfValue with nan in step you delete
    """

    def __init__(self):
        super(DeleteStepProcedure, self).__init__()
    
    def run(self, walking):
        if len(walking.m_StepGrfValue)==0 :
            from Walking.WalkingFilters import WalkingKinematicsFilter
            from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure

            procedure = GroundReactionForceKinematicsProcedure()
            WalkingKinematicsFilter(walking, procedure).run()
        
        if len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"]) != len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"]):
            LEN = max([len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"]), len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"])])
        else:
            LEN = len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])
        
        FrameRate = 10
        ##### if the event are not at the good index it may be explain by the use of normalisation procedure before this procedure

        from tqdm import tqdm

        for step in tqdm(np.arange(LEN)):
            plt.figure()
            plt.subplot(1,2,1)
            plt.title("Left Step")
            try :
                FirstPeak = walking.m_GroundReactionForces["LeftLeg"][step][0]
                MidstanceValley = walking.m_GroundReactionForces["LeftLeg"][step][1]
                SecondPeak = walking.m_GroundReactionForces["LeftLeg"][step][2]
                FirtPeakTimeTo = walking.m_GroundReactionForces["LeftLeg"][step][3] * FrameRate
                MidstanceValleyTimeTo = walking.m_GroundReactionForces["LeftLeg"][step][4] * FrameRate
                SecondPeakTimeTo = walking.m_GroundReactionForces["LeftLeg"][step][5] * FrameRate
                TimeFromMidstanceValleyToToeOff = walking.m_GroundReactionForces["LeftLeg"][step][6] * FrameRate

                plt.plot(walking.m_StepGrfValue['LeftLeg']['VerticalGrf'][step], c="r")
                plt.scatter(x=FirtPeakTimeTo ,y=FirstPeak, c ="r", label="FirstPeak")
                plt.scatter(x=SecondPeakTimeTo ,y=SecondPeak, c="g", label="SecondPeak")
                plt.scatter(x=MidstanceValleyTimeTo ,y=MidstanceValley, c="b", label="MidstanceValley")
                plt.hlines(y=MidstanceValley, xmin=MidstanceValleyTimeTo, xmax=TimeFromMidstanceValleyToToeOff+MidstanceValleyTimeTo,
                        colors ="r", ls="--", label='TimeFromMidstanceValleyToToeOff')
            except:
                plt.text(x=5, y=5, s="No value for step Left")
            plt.subplot(1,2,2)
            plt.title("Right Step")
            try :
                FirstPeak = walking.m_GroundReactionForces["RightLeg"][step][0]
                MidstanceValley = walking.m_GroundReactionForces["RightLeg"][step][1]
                SecondPeak = walking.m_GroundReactionForces["RightLeg"][step][2]
                FirtPeakTimeTo = walking.m_GroundReactionForces["RightLeg"][step][3] * FrameRate
                MidstanceValleyTimeTo = walking.m_GroundReactionForces["RightLeg"][step][4] * FrameRate
                SecondPeakTimeTo = walking.m_GroundReactionForces["RightLeg"][step][5] * FrameRate
                TimeFromMidstanceValleyToToeOff = walking.m_GroundReactionForces["RightLeg"][step][6] * FrameRate

                plt.plot(walking.m_StepGrfValue['RightLeg']['VerticalGrf'][step], c="b")
                plt.scatter(x=FirtPeakTimeTo ,y=FirstPeak, c ="r", label="FirstPeak")
                plt.scatter(x=SecondPeakTimeTo ,y=SecondPeak, c="g", label="SecondPeak")
                plt.scatter(x=MidstanceValleyTimeTo ,y=MidstanceValley, c="b", label="MidstanceValley")
                plt.hlines(y=MidstanceValley, xmin=MidstanceValleyTimeTo, xmax=TimeFromMidstanceValleyToToeOff+MidstanceValleyTimeTo,
                        colors ="r", ls="--", label='TimeFromMidstanceValleyToToeOff')
            except:
                plt.text(x=5, y=5, s="No value for step Right")
            plt.legend()
            plt.show()

            while True:
                key = input("Use 'l' for delete Left ; 'r' for delete Right ; 'lr' for delete both and 'n' for next figure:")
                if key == "n":
                    break
                elif key == "l":
                    try:
                        walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step] = [np.nan] * len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step])
                    except:
                        pass
                    break
                elif key == "r":
                    try:
                        walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step] = [np.nan] * len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step])
                    except:
                        pass
                    break
                elif key == "lr":
                    try:
                        walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step] = [np.nan] * len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step])
                    except:
                        pass
                    try:
                        walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step] = [np.nan] * len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step])
                    except:
                        pass
                    break
                elif key == "exit-e":
                    exit()
                





