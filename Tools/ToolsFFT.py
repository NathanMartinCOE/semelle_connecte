# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 05 - 10

import numpy as np

def TransformFourrier(data, seuil):
    from scipy import fftpack
    #### Transformation de fourrier
    fourrier = fftpack.fft(data)
    fq = fftpack.fftfreq(len(data))
    power = np.abs(fourrier)
    fq = np.abs(fq)
    #### TTT du bruit
    fourrier[power < seuil] = 0
    #### Transformation de fourrier inversé
    filtered = fftpack.ifft(fourrier)
    return np.real(filtered)