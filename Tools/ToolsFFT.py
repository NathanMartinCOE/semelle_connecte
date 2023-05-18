# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 05 - 10

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

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

def VisuTransformFourrier(data, seuil_initial):
    # Création du graphique
    fig, ax = plt.subplots()
    # Ajuster les marges pour faire de la place au curseur
    plt.subplots_adjust(bottom=0.25)  
    # Initialiser les données du graphique
    line, = plt.plot(data)
    line, = plt.plot(TransformFourrier(data, seuil=seuil_initial))
    # Création du curseur
    ax_seuil = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    seuil_slider = Slider(ax_seuil, 'Seuil', 0, 20000, valinit=seuil_initial)
    # Fonction de mise à jour du graphique lorsque le curseur est modifié
    def update(val):
        seuil = seuil_slider.val
        line.set_ydata(TransformFourrier(data, seuil=seuil))
        fig.canvas.draw_idle()
    seuil_slider.on_changed(update)
    plt.show()
    return seuil_slider.val