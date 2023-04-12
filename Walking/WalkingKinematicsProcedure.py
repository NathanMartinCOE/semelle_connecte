# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 01
# Modified : 2023 - 04 - 04

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass
from matplotlib import animation
from scipy.interpolate import interp1d
from scipy.signal import argrelextrema


class AbstractWalkingKinematicsProcedure(object):
    """abstract procedure """
    def __init__(self):
        pass
    def run(self):
        pass


class GroundReactionForceKinematicsProcedure(AbstractWalkingKinematicsProcedure):
    """ Computation of the ground reaction force kinematics according Vaverka's article :
    System of gait analysis based on ground reaction force assessment.
    Acta Gymnica. 31 déc 2015;45(4):187-93. 

    This function make one dictionnary of the values of the ground reaction force in vertical axes and
    anteroposterior axes avec chaque pas en index.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        GroundReactionForces a dictionnary of the values for each legs of vertical and anteroposterior 
        ground reaction force of each step. 

    0 : FirtPeak                                    10 : BrakingPeak
    1 : MidstanceValley                             11 : PropulsivePeak
    2 : SecondPeak                                  12 : BrakePhaseDuration
    3 : FirtPeakTimeTo                              13 : PropulsivePhaseDuration
    4 : MidstanceValleyTimeTo                       14 : BrakePhaseTimeTo
    5 : SecondPeakTimeTo                            15 : PropulsivePhaseTimeTo
    6 : TimeFromMidstanceValleyToToeOff             16 : BrakingImpulse
    7 : FirtAndMidstanceImpulse                     17 : PropulsiveImpulse
    8 : SecondAndPreswingImpulse
    9 : TotalVerticalGrfImpulse 
    """

    def __init__(self):
        super(GroundReactionForceKinematicsProcedure, self).__init__()

    def run(self, walking):
        # from semelle_connecte.Tools.ToolsMakeDictStep import MakeDictStep
        from Tools.ToolsMakeDictStep import MakeDictStep

        def grf(VerticalGrf,ApGrf,FrameRate = 10):
            """
            This function quantifies variables related to vertical and anteroposterior
            ground reaction forces during walking. Impulses are found by integrating the 
            force curve with respect to time. This script assumes that the vertical force 
            is positive, the anteroposterior braking force is negative, the anteroposterior 
            propulsive force is positive.

            Inputs: support phase vertical ground reaction force, support phase
                anteroposterior ground reaction force, frame rate

            Outputs: 
                (VERTICAL GRF) :
                    Peak : FirtPeak, MidstanceValley, SecondPeak,
                    Time to : FirtPeakTimeTo, MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff,
                    Impulse : FirtAndMidstanceImpulse, SecondAndPreswingImpulse, TotalVerticalGrfImpulse,
                (ANTPOST GRF) :
                    Peak : BrakingPeak, PropulsivePeak, BrakePhaseDuration,
                    Duration : PropulsivePhaseDuration,
                    Time to : BrakePhaseTimeTo,
                    Impulse : PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse
            """
            # Function for change dtype to list
            def ToList(data):
                if type(data) == list:
                    pass
                elif type(data) == np.ndarray:
                    data = list(data)
                elif type(data) == pd.core.series.Series:
                    data = data.to_list()
                return data
            
            VerticalGrf = ToList(VerticalGrf)
            ApGrf = ToList(ApGrf)
            TabVGrf = np.array(VerticalGrf)

            #Index
            if argrelextrema(TabVGrf, np.greater)[0].shape[0] > 2:
                LocalMaxDataFrame = pd.DataFrame()
                LocalMaxDataFrame["ListIndexMax"] = list(argrelextrema(TabVGrf, np.greater)[0])
                LocalMaxDataFrame["ListValueMax"] = [VerticalGrf[index] for index in LocalMaxDataFrame["ListIndexMax"]]
                LocalMaxDataFrame = LocalMaxDataFrame.sort_values(by="ListValueMax", ascending=False)
                index0, index1 = LocalMaxDataFrame["ListIndexMax"][0:2].values
                if index0 < index1 :
                    FirtPeakIndex = index0
                    SecondPeakIndex = index1
                elif index0 > index1 :
                    FirtPeakIndex = index1
                    SecondPeakIndex = index0
            else :
                FirtPeakIndex = argrelextrema(TabVGrf, np.greater)[0][0]
                SecondPeakIndex = argrelextrema(TabVGrf, np.greater)[0][1]
            MidstanceValleyIndex = argrelextrema(TabVGrf[FirtPeakIndex : SecondPeakIndex], np.less)[0][0] + FirtPeakIndex

            #Peak
            FirtPeak = VerticalGrf[FirtPeakIndex]
            MidstanceValley = VerticalGrf[MidstanceValleyIndex]
            SecondPeak = VerticalGrf[SecondPeakIndex]

            #Time to ..
            FirtPeakTimeTo = len(VerticalGrf[ :FirtPeakIndex])/FrameRate
            MidstanceValleyTimeTo = len(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
            SecondPeakTimeTo = len(VerticalGrf[ :SecondPeakIndex])/FrameRate
            TimeFromMidstanceValleyToToeOff = len(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
            
            #Impulse
            FirtAndMidstanceImpulse = np.trapz(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
            SecondAndPreswingImpulse = np.trapz(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
            TotalVerticalGrfImpulse = np.trapz(VerticalGrf)/FrameRate

            """
            ----------- ANTEROPOSTERIOR GRFS -----------
            """

            #Index
            ApGrfIndexBrakingPeak = ApGrf.index(min(ApGrf))
            ApGrfIndexPropulsivePeak = ApGrf.index(max(ApGrf))
            ApGrfPower = [grf ** 2 for grf in ApGrf[ApGrfIndexBrakingPeak : ApGrfIndexPropulsivePeak]]
            ApGrfIndexZero = ApGrfIndexBrakingPeak + ApGrfPower.index(min(ApGrfPower))

            #Peak 
            BrakingPeak = min(ApGrf)
            PropulsivePeak = max(ApGrf)

            #Duration
            BrakePhaseDuration = len(ApGrf[ :ApGrfIndexZero])/FrameRate
            PropulsivePhaseDuration = len(ApGrf[ApGrfIndexZero: ])/FrameRate
            
            #Time to ..
            BrakePhaseTimeTo = len(ApGrf[ :ApGrfIndexBrakingPeak])/FrameRate
            PropulsivePhaseTimeTo = len(ApGrf[ApGrfIndexZero:ApGrfIndexPropulsivePeak])/FrameRate

            #Impulse
            BrakingImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue < 0])/FrameRate
            PropulsiveImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue > 0])/FrameRate

            return FirtPeak, MidstanceValley, SecondPeak, FirtPeakTimeTo, MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff, FirtAndMidstanceImpulse, SecondAndPreswingImpulse, TotalVerticalGrfImpulse, BrakingPeak, PropulsivePeak, BrakePhaseDuration, PropulsivePhaseDuration, BrakePhaseTimeTo, PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse 
        
            """
            This function make two dictionnary of the ground reaction force in vertical axes and
            anteroposterior axes with each step in index. Use a rolling median with a step size of 30 
            to smooth out data loss.

            Inputs: support phase vertical ground reaction force, support phase
                anteroposterior ground reaction force

            Outputs: Dictionnary of the vertical ground reaction force of each step, 
            Dictionnary of the anteroposterior ground reaction force of each step  
            """
            if min(VerticalGrf) != 0 :
                thresfold = min(VerticalGrf) + 10 / 100 * min(VerticalGrf)
                print(f"Caution no 0 find in Vertical GRF dataframe : use of a thresfold at {thresfold}")
            else : thresfold = 0

            def GetStepEvent(VerticalGrf):
                HeelStrike = []
                ToeOff = []
                for i in range(0,len(VerticalGrf)-1):
                    if thresfold == 0:
                        if VerticalGrf[i] == 0 and VerticalGrf[i+1] > 0 : 
                            HeelStrike.append(i)
                        if VerticalGrf[i] > 0 and VerticalGrf[i+1] == 0 : 
                            ToeOff.append(i)
                    else :
                        if VerticalGrf[i] < thresfold  and VerticalGrf[i+1] > thresfold : 
                            HeelStrike.append(i)
                        if VerticalGrf[i] > thresfold and VerticalGrf[i+1] < thresfold : 
                            ToeOff.append(i)
                return HeelStrike, ToeOff
            
            def RollingMedian(VerticalGrf, RollingMedianStep = 30):
                RollingMedianGrf = [abs(value) for value in VerticalGrf]
                RollingMedianGrf = pd.DataFrame(RollingMedianGrf)
                RollingMedianGrf = RollingMedianGrf.rolling(window = RollingMedianStep, center = True).median()
                RollingMedianGrf = RollingMedianGrf.fillna(0)
                RollingMedianGrf = RollingMedianGrf[0].tolist()
                return RollingMedianGrf
            
            # HeelStrike, ToeOff = GetStepEvent(RollingMedian(VerticalGrf)) # Si présence de NaN dans les data peut être utile
            HeelStrike, ToeOff = GetStepEvent(VerticalGrf)
            VerticalGrfStep = {i : VerticalGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)}
            ApGrfStep = {i : ApGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)}
            return VerticalGrfStep, ApGrfStep

        GroundReactionForces = dict()
        StepGrfValue = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            VerticalGrfStep, ApGrfStep = MakeDictStep(VerticalGrf = walking.m_sole[leg].data["VerticalGrf"],
                                                      ApGrf = walking.m_sole[leg].data["ApGrf"])
            GrfValues = {i : grf(VerticalGrfStep[i],ApGrfStep[i], FrameRate = 10) for i in range(0, len(VerticalGrfStep))}
            StepGrfValue[leg] = {"VerticalGrf" : VerticalGrfStep,
                                 "ApGrf" : ApGrfStep}
            GroundReactionForces[leg] = GrfValues

        walking.setStepGrfValue(StepGrfValue)
        walking.setGroundReactionForces(GroundReactionForces)


class DynamicSymetryFunctionComputeProcedure(AbstractWalkingKinematicsProcedure):
    """
    This function compute the dynamic symetry function for all value in walking.m_GroundReactionForces

    Args:
        walking.m_GroundReactionForces get by (semelle_connecte.Walking.WalkingKinematicsProcedure.GroundReactionForceKinematicsProcedure)


    Outputs:
        DataFrameDynamicSymetryScore a DataFrame of the Dynamic Symetry Function for each values of vertical and anteroposterior 
        ground reaction force of each step.

    Dynamic Symetry of :
    0 : FirtPeak                                    10 : BrakingPeak
    1 : MidstanceValley                             11 : PropulsivePeak
    2 : SecondPeak                                  12 : BrakePhaseDuration
    3 : FirtPeakTimeTo                              13 : PropulsivePhaseDuration
    4 : MidstanceValleyTimeTo                       14 : BrakePhaseTimeTo
    5 : SecondPeakTimeTo                            15 : PropulsivePhaseTimeTo
    6 : TimeFromMidstanceValleyToToeOff             16 : BrakingImpulse
    7 : FirtAndMidstanceImpulse                     17 : PropulsiveImpulse
    8 : SecondAndPreswingImpulse
    9 : TotalVerticalGrfImpulse    
    """

    def __init__(self):
        super(DynamicSymetryFunctionComputeProcedure, self).__init__()

    def run(self, walking):

        if len(walking.m_GroundReactionForces) == 0:
            print("!!! Caution : No Ground Reaction Forces in walking object, please run the GroundReactionForceKinematicsProcedure !!!")
        else :
            DataFrameGrfValueLeft = pd.DataFrame(walking.m_GroundReactionForces["LeftLeg"]).T
            DataFrameGrfValueRight = pd.DataFrame(walking.m_GroundReactionForces["RightLeg"]).T
            DataFrameDynamicSymetryScore = pd.DataFrame(np.zeros(DataFrameGrfValueLeft.shape))

            def FSD(ligne, col):
                xdt = DataFrameGrfValueRight.iloc[ligne,col]
                xgt = DataFrameGrfValueLeft.iloc[ligne,col]
                if max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) == 0 :
                        rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) + 1
                elif max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) != 0 :
                        rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col])  
                if max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) == 0 :
                    rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) + 1
                elif max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) != 0 :
                    rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col])
                return 2*(xdt-xgt)/(rangexdt+rangexgt)

            for ligne in range(0,DataFrameGrfValueLeft.shape[0]):
                for col in range(0,DataFrameGrfValueLeft.shape[1]):
                    DataFrameDynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)

            DataFrameDynamicSymetryScore = DataFrameDynamicSymetryScore.rename(columns={0:"FirtPeak", 1 : "MidstanceValley", 2 : "SecondPeak", 3 : "FirtPeakTimeTo", 
            4 : "MidstanceValleyTimeTo", 5 : "SecondPeakTimeTo", 6 : "TimeFromMidstanceValleyToToeOff", 7 : "FirtAndMidstanceImpulse", 8 :
            "SecondAndPreswingImpulse", 9 : "TotalVerticalGrfImpulse", 10 : "BrakingPeak", 11 : "PropulsivePeak", 12 : "BrakePhaseDuration", 13 :
            "PropulsivePhaseDuration", 14 : "BrakePhaseTimeTo", 15 : "PropulsivePhaseTimeTo", 16 : "BrakingImpulse", 17 : "PropulsiveImpulse"})

            walking.setDataFrameDynamicSymetryScore(DataFrameDynamicSymetryScore)

#### caution this procedure is not working actually
class GaitTrackingKineticsProcedure(AbstractWalkingKinematicsProcedure):
    """ This procedure track the position of IMU place on leg by using X-IO technologie code
    Gait-Tracking with IMU available on : https://github.com/xioTechnologies/Gait-Tracking

    Args:
        walking.m_IMU (semelle_connecte.Walking.Walking.m_IMU): a IMU members of a walking patient instance 
                       example : walking.m_IMU["LeftLeg"] for track the left leg

    Outputs:
        plot the process of Data
        plot the position in x and y axes by time
        creat an animation of position in x,y,z axes
    """

    def __init__(self):
        super(GaitTrackingKineticsProcedure, self).__init__()

    def run(self, walkingIMU):
        import imufusion
        
        sample_rate = 1125  # 1125 Hz
        timestamp = np.asarray(walkingIMU.time)
        gyroData = pd.DataFrame()
        gyroData["X"] = walkingIMU.data["Gyro.X"]
        gyroData["Y"] = walkingIMU.data["Gyro.Y"]
        gyroData["Z"] = walkingIMU.data["Gyro.Z"]
        gyroscope = np.asarray(gyroData)
        accelData = pd.DataFrame()
        accelData["X"] = walkingIMU.data["Accel.X"]
        accelData["Y"] = walkingIMU.data["Accel.Y"]
        accelData["Z"] = walkingIMU.data["Accel.Z"]
        accelerometer = np.asarray(accelData)

        #### Instantiate AHRS algorithms
        offset = imufusion.Offset(sample_rate)
        ahrs = imufusion.Ahrs()
        ahrs.settings = imufusion.Settings(0.5, 10, 0.0, 5 * sample_rate) 
        
        #### Process sensor data (Euler angles // Internal State // Accelleration)
        delta_time = np.diff(timestamp, prepend=timestamp[0])
        euler = np.empty((len(timestamp), 3))
        internal_states = np.empty((len(timestamp), 3))
        acceleration = np.empty((len(timestamp), 3))

        for index in range(len(timestamp)):
            gyroscope[index] = offset.update(gyroscope[index])

            ahrs.update_no_magnetometer(gyroscope[index], accelerometer[index], delta_time[index])

            euler[index] = ahrs.quaternion.to_euler()

            ahrs_internal_states = ahrs.internal_states
            internal_states[index] = np.array([ahrs_internal_states.acceleration_error,
                                                ahrs_internal_states.accelerometer_ignored,
                                                ahrs_internal_states.acceleration_rejection_timer])

            acceleration[index] = 9.81 * ahrs.earth_acceleration  # convert g to m/s/s

        # Identify moving periods
        is_moving = np.empty(len(timestamp))

        for index in range(len(timestamp)):
            is_moving[index] = np.sqrt(acceleration[index].dot(acceleration[index])) > 3  # threshold = 3 m/s/s

        margin = int(0.1 * sample_rate)  # 100 ms

        for index in range(len(timestamp) - margin):
            is_moving[index] = any(is_moving[index:(index + margin)])  # add leading margin

        for index in range(len(timestamp) - 1, margin, -1):
            is_moving[index] = any(is_moving[(index - margin):index])  # add trailing margin

        # Calculate velocity (includes integral drift)
        velocity = np.zeros((len(timestamp), 3))

        for index in range(len(timestamp)):
            if is_moving[index]:  # only integrate if moving
                velocity[index] = velocity[index - 1] + delta_time[index] * acceleration[index]

        # Find start and stop indices of each moving period
        is_moving_diff = np.diff(is_moving, append=is_moving[-1])


        @dataclass
        class IsMovingPeriod:
            start_index: int = -1
            stop_index: int = -1


        is_moving_periods = []
        is_moving_period = IsMovingPeriod()

        for index in range(len(timestamp)):
            if is_moving_period.start_index == -1:
                if is_moving_diff[index] == 1:
                    is_moving_period.start_index = index

            elif is_moving_period.stop_index == -1:
                if is_moving_diff[index] == -1:
                    is_moving_period.stop_index = index
                    is_moving_periods.append(is_moving_period)
                    is_moving_period = IsMovingPeriod()

        # Remove integral drift from velocity
        velocity_drift = np.zeros((len(timestamp), 3))

        for is_moving_period in is_moving_periods:
            start_index = is_moving_period.start_index
            stop_index = is_moving_period.stop_index

            t = [timestamp[start_index], timestamp[stop_index]]
            x = [velocity[start_index, 0], velocity[stop_index, 0]]
            y = [velocity[start_index, 1], velocity[stop_index, 1]]
            z = [velocity[start_index, 2], velocity[stop_index, 2]]

            t_new = timestamp[start_index:(stop_index + 1)]

            velocity_drift[start_index:(stop_index + 1), 0] = interp1d(t, x)(t_new)
            velocity_drift[start_index:(stop_index + 1), 1] = interp1d(t, y)(t_new)
            velocity_drift[start_index:(stop_index + 1), 2] = interp1d(t, z)(t_new)

        velocity = velocity - velocity_drift


        # Calculate position
        position = np.zeros((len(timestamp), 3))

        for index in range(len(timestamp)):
            position[index] = position[index - 1] + delta_time[index] * velocity[index]

        # Print error as distance between start and final positions
        print("Error: " + "{:.3f}".format(np.sqrt(position[-1].dot(position[-1]))) + " m")

        
        PlotSensorData = True
        """ This plots shows the processing """
        if PlotSensorData == True :
            #### First plot
            figure, axes = plt.subplots(nrows=6, sharex=True, gridspec_kw={"height_ratios": [6, 6, 6, 2, 1, 1]}, figsize=(15, 15))
            figure.suptitle("Sensors data, Euler angles, and AHRS internal states")

            axes[0].plot(timestamp, gyroscope[:, 0], "tab:red", label="Gyroscope X")
            axes[0].plot(timestamp, gyroscope[:, 1], "tab:green", label="Gyroscope Y")
            axes[0].plot(timestamp, gyroscope[:, 2], "tab:blue", label="Gyroscope Z")
            axes[0].set_ylabel("Degrees/s")
            axes[0].grid()
            axes[0].legend()

            axes[1].plot(timestamp, accelerometer[:, 0], "tab:red", label="Accelerometer X")
            axes[1].plot(timestamp, accelerometer[:, 1], "tab:green", label="Accelerometer Y")
            axes[1].plot(timestamp, accelerometer[:, 2], "tab:blue", label="Accelerometer Z")
            axes[1].set_ylabel("g")
            axes[1].grid()
            axes[1].legend()

            # Plot Euler angles
            axes[2].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
            axes[2].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
            axes[2].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
            axes[2].set_ylabel("Degrees")
            axes[2].grid()
            axes[2].legend()

            # Plot internal states
            axes[3].plot(timestamp, internal_states[:, 0], "tab:olive", label="Acceleration error")
            axes[3].set_ylabel("Degrees")
            axes[3].grid()
            axes[3].legend()

            axes[4].plot(timestamp, internal_states[:, 1], "tab:cyan", label="Accelerometer ignored")
            plt.sca(axes[4])
            plt.yticks([0, 1], ["False", "True"])
            axes[4].grid()
            axes[4].legend()

            axes[5].plot(timestamp, internal_states[:, 2], "tab:orange", label="Acceleration rejection timer")
            axes[5].set_xlabel("Seconds")
            axes[5].grid()
            axes[5].legend()

            #### Second plot
            # Plot acceleration
            _, axes = plt.subplots(nrows=4, sharex=True, gridspec_kw={"height_ratios": [6, 1, 6, 6]}, figsize=(15, 15))

            axes[0].plot(timestamp, acceleration[:, 0], "tab:red", label="X")
            axes[0].plot(timestamp, acceleration[:, 1], "tab:green", label="Y")
            axes[0].plot(timestamp, acceleration[:, 2], "tab:blue", label="Z")
            axes[0].set_title("Acceleration")
            axes[0].set_ylabel("m/s/s")
            axes[0].grid()
            axes[0].legend()

            # Plot moving periods
            axes[1].plot(timestamp, is_moving, "tab:cyan", label="Is moving")
            plt.sca(axes[1])
            plt.yticks([0, 1], ["False", "True"])
            axes[1].grid()
            axes[1].legend()

            # Plot velocity
            axes[2].plot(timestamp, velocity[:, 0], "tab:red", label="X")
            axes[2].plot(timestamp, velocity[:, 1], "tab:green", label="Y")
            axes[2].plot(timestamp, velocity[:, 2], "tab:blue", label="Z")
            axes[2].set_title("Velocity")
            axes[2].set_ylabel("m/s")
            axes[2].grid()
            axes[2].legend()

            # Plot position
            axes[3].plot(timestamp, position[:, 0], "tab:red", label="X")
            axes[3].plot(timestamp, position[:, 1], "tab:green", label="Y")
            axes[3].plot(timestamp, position[:, 2], "tab:blue", label="Z")
            axes[3].set_title("Position")
            axes[3].set_xlabel("Seconds")
            axes[3].set_ylabel("m")
            axes[3].grid()
            axes[3].legend()

            plt.figure()
            plt.plot(position[:, 0], position[:, 1])
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.show()

            plt.figure()
            plt.plot(position[:, 0], position[:, 2])
            plt.xlabel("X")
            plt.ylabel("Z")
            plt.show()

        # Create 3D animation (takes a long time change False -> True)
        run3D = "False"
        # run3D = "True"
        if run3D == "True":
            figure = plt.figure(figsize=(10, 10))

            axes = plt.axes(projection="3d")
            axes.set_xlabel("m")
            axes.set_ylabel("m")
            axes.set_zlabel("m")

            x = []
            y = []
            z = []

            scatter = axes.scatter(x, y, z)

            fps = 30
            samples_per_frame = int(sample_rate / fps)

            def update(frame):
                index = frame * samples_per_frame

                axes.set_title("{:.3f}".format(timestamp[index]) + " s")

                x.append(position[index, 0])
                y.append(position[index, 1])
                z.append(position[index, 2])

                scatter._offsets3d = (x, y, z)

                if (min(x) != max(x)) and (min(y) != max(y)) and (min(z) != max(z)):
                    axes.set_xlim3d(min(x), max(x))
                    axes.set_ylim3d(min(y), max(y))
                    axes.set_zlim3d(min(z), max(z))

                    axes.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))

                return scatter

            anim = animation.FuncAnimation(figure, update,
                                            frames=int(len(timestamp) / samples_per_frame),
                                            interval=1000 / fps,
                                            repeat=False)

            anim.save("animation.gif", writer=animation.PillowWriter(fps))

            plt.show()


