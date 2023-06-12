# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 05 - 10

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import fftpack

def TransformFourrier(data, seuil):
    """
    This function can be used to process noise in the signal using the Fourier Transform.

    Args:
        data: the data to be processed
        seuil: frequency threshold below which noise is suppressed
    Outputs:
        filtered: the processed data (real part of the Fourrier Transform)
    """
    # == Fourrier transformation ===
    fourrier = fftpack.fft(data)
    fq = fftpack.fftfreq(len(data))
    power = np.abs(fourrier)
    fq = np.abs(fq)
    # == noise processing ==========
    fourrier[power < seuil] = 0
    # == Inverse Fourier Transform =
    filtered = fftpack.ifft(fourrier)
    return np.real(filtered)

def VisuTransformFourrier(data, seuil_initial):
    """
    This function shows the impact of the threshold used on signal processing.

    Args:
        data: the data to be processed
        seuil_initial: initial frequency threshold 
    Outputs:
        seuil_slider.val: frequency threshold choose when closing the fig
    """

    def update(val):
        seuil = seuil_slider.val
        line.set_ydata(TransformFourrier(data, seuil=seuil))
        fig.canvas.draw_idle()

    fig, ax = plt.subplots()    
    plt.subplots_adjust(bottom=0.25)  
    line, = plt.plot(data)
    line, = plt.plot(TransformFourrier(data, seuil=seuil_initial))
    ax_seuil = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    seuil_slider = Slider(ax_seuil, 'Seuil', 0, 20000, valinit=seuil_initial)
    seuil_slider.on_changed(update)
    plt.show()

    return seuil_slider.val