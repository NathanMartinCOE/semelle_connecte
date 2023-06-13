# FeetMe Sole class 
# coding: utf-8 
# Author : Nathan Martin 
# Modified : 2023 - 04 - 03

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from pyCGM2.External.ktk.kineticstoolkit import timeseries
from semelle_connecte.SOLE import sole

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

def readFeetMeCsv(fullfilename,freq, show_graph = True, expert=False):
    """
    A reader function for csv pressures give by FeetMe insole. The use of this reader is not recommended, as FeetMe produces 
    several files, so it's better to use the readFeetMeMultipleCsv.

    Args:
        fullfilename = path of the csv pressure file
        freq = acquisition frequency in hz
        show_graph (boolean) = defaut is True
            True  -> show the graph of the data after selecting the data range and applying the threshold
            False -> (not recommended) don't show the graph 
        expert (boolean) = defaut is False
            True  -> (not recommended) use for test the function without choose on plot
            False -> does the same thing as if true were selected, but uses the values selected graphically
    Outputs:
        SoleInstanceRight -> an insole instance (semelle_connecte.SOLE.FeetMe.FeetMe)
        SoleInstanceLeft  -> an insole instance (semelle_connecte.SOLE.FeetMe.FeetMe)
    """

    def GetSeuilZero(data, seuil_initial):

        def update_seuil(val):
            seuil = slider.val
            seuil_line.set_ydata(seuil)
            fig.canvas.draw_idle()

        fig, ax = plt.subplots()
        line, = ax.plot(data)
        # ax.set_xlim(0, len(data) - 1)
        ax.set_xlim(data.index[0], data.index[data.shape[0] - 1])
        ax.set_ylim(min(data), max(data))
        seuil_line = ax.axhline(y=seuil_initial, color='red')
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        slider = Slider(slider_ax, 'Seuil', min(data), max(data), valinit=seuil_initial)
        slider.on_changed(update_seuil)
        plt.show()

        seuil_final = slider.val
        return seuil_final

    def SetZero(data, seuil_initial):
        if expert == False:
            seuil = GetSeuilZero(data["pressures"], seuil_initial)
        elif expert == True :
            seuil = seuil_initial
        data["pressures"][data["pressures"] < seuil] = 0

        return data

    def GetIndex(data):
        def update_curseurs(val):
            start = int(start_slider.val)
            end = int(end_slider.val)
            start_line.set_xdata(start)
            end_line.set_xdata(end)
            fig.canvas.draw_idle()  

        fig, ax = plt.subplots()
        ax.plot(data)
        ax.set_xlim(data.index[0], data.index[data.shape[0] - 1])
        ax.set_ylim(min(data), max(data))
        start_slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        end_slider_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
        # start_slider = Slider(start_slider_ax, 'Début', 0, len(data) - 1, valinit= 0, valstep=1)
        # end_slider = Slider(end_slider_ax, 'Fin', 0, len(data) - 1, valinit= len(data) - 1, valstep=1)
        start_slider = Slider(start_slider_ax, 'Début', 0, data.index[data.shape[0] - 1], valinit= data.index[0], valstep=1)
        end_slider = Slider(end_slider_ax, 'Fin', 0, data.index[data.shape[0] - 1], valinit= data.index[data.shape[0] - 1], valstep=1)
        start_line = ax.axvline(x=0, color='g', linestyle='--', linewidth=2)
        # end_line = ax.axvline(x=len(data) - 1, color='r', linestyle='--', linewidth=2)
        end_line = ax.axvline(x= data.index[data.shape[0] - 1], color='r', linestyle='--', linewidth=2)
        start_slider.on_changed(update_curseurs)
        end_slider.on_changed(update_curseurs)
        plt.show()

        start_index = int(start_slider.val)
        end_index = int(end_slider.val)

        return start_index, end_index

    def AdjustIndex(data, index):
        try :
            index_row   = data["index"][data.index == index].values[0]
        except:
            index_max = index
            index_min = index
            while len(data["index"][data.index == index_max].values) == 0:
                index_max += 1
            while len(data["index"][data.index == index_min].values) == 0:
                index_min -= 1 
            if abs(index_max-index) < abs(index_min-index):
                index = index_max
            elif abs(index_max-index) > abs(index_min-index):
                index = index_min
            elif abs(index_max-index) == abs(index_min-index):
                index = index_max
            index_row   = data["index"][data.index == index].values[0]

        return index_row

    def SetIndex(data):
        start_index, end_index = GetIndex(data["pressures"])

        start_row = AdjustIndex(data, index=start_index)
        end_row   = AdjustIndex(data, index=end_index) 

        return start_row, end_row


    df = pd.read_csv(fullfilename, header=None, skiprows=1)

    data = pd.DataFrame()
    data["clientTimestamp"] = df[0]
    data["tick"] = df[1]
    data["timestamp"] = df[2]
    data["pressures"] = df.iloc[ : ,3:21].sum(axis=1)
    data["side"] = df[21]

    dataRight = data[data["side"]=="right"]
    dataRight["index"] = np.arange(0, len(dataRight))
    dataRight["index_feetme"] = dataRight.index
    dataRight["Ap"] = np.nan * dataRight.shape[0]
    dataRight["Mediolateral"] = np.nan * dataRight.shape[0]
    dataRight = SetZero(dataRight, seuil_initial=4)
    if expert == False:
        start_row_right, end_row_right = SetIndex(dataRight)
    elif expert == True:
        start_row_right = AdjustIndex(dataRight, 362)
        end_row_right  = AdjustIndex(dataRight, 7150)

    dataLeft = data[data["side"]=="left"]
    dataLeft["index"] = np.arange(0, len(dataLeft))
    dataLeft["index_feetme"] = dataLeft.index
    dataLeft["Ap"] = np.nan * dataLeft.shape[0]
    dataLeft["Mediolateral"] = np.nan * dataLeft.shape[0]
    dataLeft = SetZero(dataLeft, seuil_initial=4)
    if expert == False:
        start_row_left, end_row_left = SetIndex(dataLeft)
    elif expert == True:
        start_row_left = AdjustIndex(dataLeft, 175)
        end_row_left = AdjustIndex(dataLeft, 7045)

    if show_graph == True:
        plt.figure()
        plt.plot(dataRight["pressures"][start_row_right:end_row_right], label="right", c="b")
        plt.plot(dataLeft["pressures"][start_row_left:end_row_left], label="left", c="r")
        plt.legend()
        plt.show()

    SoleInstanceRight = FeetMe(freq)
    SoleInstanceRight.SetGroundReactionForce("Vertical", dataRight["pressures"][start_row_right:end_row_right].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Ap", dataRight["Ap"][start_row_right:end_row_right].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Mediolateral", dataRight["Mediolateral"][start_row_right:end_row_right].to_numpy()) 
    SoleInstanceRight.constructTimeseries()

    SoleInstanceLeft = FeetMe(freq)
    SoleInstanceLeft.SetGroundReactionForce("Vertical", dataLeft["pressures"][start_row_left:end_row_left].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Ap", dataLeft["Ap"][start_row_right:end_row_right].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Mediolateral", dataLeft["Mediolateral"][start_row_right:end_row_right].to_numpy())
    SoleInstanceLeft.constructTimeseries()
    
    return SoleInstanceRight, SoleInstanceLeft



def readFeetMeMultipleCsv(fullfilenames,freq, show_graph = True, expert=False):
    """
    A reader function for csv pressures give by FeetMe insole. The use of this reader is recommended, as FeetMe produces 
    several files.

    Args:
        fullfilenames = a list with all the path of the csv pressure files 
            PLEASE ---> Be careful to give the files in the order given by feetme
        freq = acquisition frequency in hz
        show_graph (boolean) = defaut is True
            True  -> show the graph of the data after selecting the data range and applying the threshold
            False -> (not recommended) don't show the graph 
        expert (boolean) = defaut is False
            True  -> (not recommended) use for test the function without choose on plot
            False -> does the same thing as if true were selected, but uses the values selected graphically
    Outputs:
        SoleInstanceRight -> an insole instance (semelle_connecte.SOLE.FeetMe.FeetMe)
        SoleInstanceLeft  -> an insole instance (semelle_connecte.SOLE.FeetMe.FeetMe)
    """

    def AdjustIndex(data, index):
        try :
            index_row   = data["index"][data.index == index].values[0]
        except:
            index_max = index
            index_min = index
            while len(data["index"][data.index == index_max].values) == 0:
                index_max += 1
            while len(data["index"][data.index == index_min].values) == 0:
                index_min -= 1 
            if abs(index_max-index) < abs(index_min-index):
                index = index_max
            elif abs(index_max-index) > abs(index_min-index):
                index = index_min
            elif abs(index_max-index) == abs(index_min-index):
                index = index_max
            index_row   = data["index"][data.index == index].values[0]

        return index_row

    def GetSeuilZero(data, seuil_initial):

        def update_seuil(val):
            seuil = slider.val
            seuil_line.set_ydata(seuil)
            fig.canvas.draw_idle()

        fig, ax = plt.subplots()
        ax.plot(data)
        seuil_line = ax.axhline(y=seuil_initial, color='red')
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        slider = Slider(slider_ax, 'Seuil', min(data), max(data), valinit=seuil_initial)
        slider.on_changed(update_seuil)
        plt.show()

        seuil_final = slider.val
        return seuil_final

    def SetZero(data, seuil_initial):
        if expert == False:
            seuil = GetSeuilZero(data = data["pressures"], seuil_initial = seuil_initial)
        elif expert == True :
            seuil = seuil_initial
        data["pressures"][data["pressures"] < seuil] = 0

        return data

    def GetIndex(data):
        def update_curseurs(val):
            start = int(start_slider.val)
            end = int(end_slider.val)
            start_line.set_xdata(start)
            end_line.set_xdata(end)
            fig.canvas.draw_idle()  

        def on_key(event):
            step = 1
            if event.key == 'down':
                if event.inaxes == start_slider_ax:
                    start_slider.set_val(start_slider.val - step)
                elif event.inaxes == end_slider_ax:
                    end_slider.set_val(end_slider.val - step)
            elif event.key == 'up':
                if event.inaxes == start_slider_ax:
                    start_slider.set_val(start_slider.val + step)
                elif event.inaxes == end_slider_ax:
                    end_slider.set_val(end_slider.val + step)

        fig, ax = plt.subplots()
        ax.plot(data)
        ax.set_xlim(data.index[0], data.index[data.shape[0] - 1])
        ax.set_ylim(min(data), max(data))
        start_slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        end_slider_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
        start_slider = Slider(start_slider_ax, 'Début', 0, data.index[data.shape[0] - 1], valinit=data.index[0], valstep=1)
        end_slider = Slider(end_slider_ax, 'Fin', 0, data.index[data.shape[0] - 1], valinit=data.index[data.shape[0] - 1], valstep=1)
        start_line = ax.axvline(x=0, color='g', linestyle='--', linewidth=2)
        end_line = ax.axvline(x=data.index[data.shape[0] - 1], color='r', linestyle='--', linewidth=2)
        start_slider.on_changed(update_curseurs)
        end_slider.on_changed(update_curseurs)
        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()

        start_index = int(start_slider.val)
        end_index = int(end_slider.val)

        return start_index, end_index

    def SetIndex(data):
        start_index, end_index = GetIndex(data = data["pressures"])
        start_row = AdjustIndex(data, index=start_index)
        end_row   = AdjustIndex(data, index=end_index) 

        return start_row, end_row


    df = pd.read_csv(fullfilenames[0], header=None, skiprows=1)
    for fullfilname in fullfilenames[1:]:
        df_supp = pd.read_csv(fullfilname, header=None)
        df = pd.concat([df, df_supp])

    data = pd.DataFrame()
    data["clientTimestamp"] = df[0]
    data["tick"] = df[1]
    data["timestamp"] = df[2]
    data["pressures"] = df.iloc[ : ,3:21].sum(axis=1)
    data["side"] = df[21]

    dataRight = data[data["side"]=="right"] * 10
    dataRight["index"] = np.arange(0, len(dataRight))
    dataRight["index_feetme"] = dataRight.index
    dataRight["Ap"] = np.nan * dataRight.shape[0]
    dataRight["Mediolateral"] = np.nan * dataRight.shape[0]
    dataRight = dataRight.set_index(dataRight["index"])
    dataRight = SetZero(dataRight, seuil_initial=40)
    if expert == False:
        start_row_right, end_row_right = SetIndex(dataRight)
    elif expert == True:
        start_row_right = AdjustIndex(dataRight, 362)
        end_row_right = AdjustIndex(dataRight, 7150)

    dataLeft = data[data["side"]=="left"] * 10
    dataLeft["index"] = np.arange(0, len(dataLeft))
    dataLeft["index_feetme"] = dataLeft.index
    dataLeft["Ap"] = np.nan * dataLeft.shape[0]
    dataLeft["Mediolateral"] = np.nan * dataLeft.shape[0]
    dataLeft = dataLeft.set_index(dataLeft["index"])
    dataLeft = SetZero(dataLeft, seuil_initial=40)
    if expert == False:
        start_row_left, end_row_left = SetIndex(dataLeft)
    elif expert == True:
        start_row_left = AdjustIndex(dataLeft, 175)
        end_row_left = AdjustIndex(dataLeft, 7045)

    if show_graph == True:
        plt.figure()
        plt.plot(dataRight["pressures"][start_row_right:end_row_right], label="right", c="b")
        plt.plot(dataLeft["pressures"][start_row_left:end_row_left], label="left", c="r")
        plt.legend()
        plt.show()

    SoleInstanceRight = FeetMe(freq)
    SoleInstanceRight.SetGroundReactionForce("Vertical", dataRight["pressures"][start_row_right:end_row_right].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Ap", dataRight["Ap"][start_row_right:end_row_right].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Mediolateral", dataRight["Mediolateral"][start_row_right:end_row_right].to_numpy()) 
    SoleInstanceRight.constructTimeseries()

    SoleInstanceLeft = FeetMe(freq)
    SoleInstanceLeft.SetGroundReactionForce("Vertical", dataLeft["pressures"][start_row_left:end_row_left].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Ap", dataLeft["Ap"][start_row_right:end_row_right].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Mediolateral", dataLeft["Mediolateral"][start_row_right:end_row_right].to_numpy())
    SoleInstanceLeft.constructTimeseries()
    
    return SoleInstanceRight, SoleInstanceLeft


def ReadSpatioTemporalCsv(fullfilenames):
    """
    A reader function for csv metrics give by FeetMe insole.

    Args:
        fullfilenames = the path of the csv metric
    Outputs:
        DataFrameSpatioTemporal_Left  = pd.DataFrame() with Spatio-Temporal Parameters
        DataFrameSpatioTemporal_Right = pd.DataFrame() with Spatio-Temporal Parameters
    """

    DataFrameSpatioTemporal = pd.read_csv(fullfilenames, header=1)
    DataFrameSpatioTemporal = DataFrameSpatioTemporal.loc[: ,["side", "stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)", "stancePercentage (%)", "singleSupportPercentage (%)", "doubleSupportPercentage (%)", "swingPercentage (%)"]]
    
    DataFrameSpatioTemporal_Left = DataFrameSpatioTemporal[DataFrameSpatioTemporal["side"] == "left"].drop(columns=["side"])
    DataFrameSpatioTemporal_Right = DataFrameSpatioTemporal[DataFrameSpatioTemporal["side"] == "right"].drop(columns=["side"])

    return DataFrameSpatioTemporal_Left, DataFrameSpatioTemporal_Right