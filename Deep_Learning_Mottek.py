import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking

from Tools.ToolsFFT import TransformFourrier, VisuTransformFourrier
from Tools.ToolsGetStepEvent import GetStepEvent

# =========================================================  Fonction pour instancier Walking et construire le dataset

def Procedures(dataLeft, dataRight):
    
    SoleInstanceLeft = FeetMe(1000)
    SoleInstanceLeft.SetGroundReactionForce("Vertical", dataLeft["VerticalVGrf"].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Ap", dataLeft["ApGrf"].to_numpy())
    SoleInstanceLeft.SetGroundReactionForce("Mediolateral", dataLeft["MediolateralGrf"].to_numpy())
    SoleInstanceLeft.constructTimeseries()

    SoleInstanceRight = FeetMe(1000)
    SoleInstanceRight.SetGroundReactionForce("Vertical", dataRight["VerticalVGrf"].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Ap", dataRight["ApGrf"].to_numpy())
    SoleInstanceRight.SetGroundReactionForce("Mediolateral", dataRight["MediolateralGrf"].to_numpy())
    SoleInstanceRight.constructTimeseries()

    walking = Walking(mass)
    walking.setLeftLegSole(SoleInstanceLeft)
    walking.setRightLegSole(SoleInstanceRight)


    from Walking.WalkingFilters import WalkingKinematicsFilter
    from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("GroundReactionForceKinematicsProcedure --------------- done")

    from Walking.WalkingFilters import WalkingDataProcessingFilter
    from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()
    print("NormalisationProcedure ------------------------------- done")

    return walking

# =========================================================  Donnée tapis = data_noised

DataPath = 'C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\grf\\'
Path = DataPath + 'gait_test5.c3d' # fait 50 pas

acq = btkTools.smartReader(Path)
grwc = btkTools.getForcePlateWrench(acq)

mass = 60 # en kg
forces = []
items = [0,1]
for it in items:
    forces.append(grwc.GetItem(it).GetForce().GetValues() / (mass * 9.81) * 100)

dataLeft = pd.DataFrame()
dataLeft["VerticalVGrf"] = forces[1][:,2]
dataLeft["VerticalVGrf"][dataLeft["VerticalVGrf"] < 30] = 0
dataLeft["ApGrf"] = forces[1][:,1]
dataLeft["MediolateralGrf"] = forces[1][:,0] * -1

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = forces[0][:,2]
dataRight["VerticalVGrf"][dataRight["VerticalVGrf"] < 30] = 0
dataRight["ApGrf"] = forces[0][:,1]
dataRight["MediolateralGrf"] = forces[0][:,0]

walking = Procedures(dataLeft, dataRight)

data_noised = pd.DataFrame()
for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
    if sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_noised[f"{step}"] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]

# ========================================================== Donnée database = data_clean

import h5py
ID = 1
mass = 60
DataPath = "C:/Users/Nathan/Desktop/Recherche/Github/semelle_connecte/Test/Dataset_test/"
GuttembergGaitDatabase = h5py.File(os.path.join(DataPath, "GuttenbergGaitDatabase.hdf5"), "r")
VerticalGrfLeft = GuttembergGaitDatabase[f"{ID}"]["VerticalGrfLeft"]
ApGrfLeft = GuttembergGaitDatabase[f"{ID}"]["ApGrfLeft"]
MediolateralGrfLeft = GuttembergGaitDatabase[f"{ID}"]["MediolateralGrfLeft"]
VerticalGrfRight = GuttembergGaitDatabase[f"{ID}"]["VerticalGrfRight"]
ApGrfRight = GuttembergGaitDatabase[f"{ID}"]["ApGrfRight"]
MediolateralGrfRight = GuttembergGaitDatabase[f"{ID}"]["MediolateralGrfRight"]

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking

dataLeft = pd.DataFrame()
dataLeft["VerticalVGrf"] = VerticalGrfLeft
dataLeft["ApGrf"] = ApGrfLeft
dataLeft["MediolateralGrf"] = MediolateralGrfLeft
dataLeft = dataLeft * 100 # permets de travailler avec des forces de réaction au sol d'un ordre de grandeur de 100

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = VerticalGrfRight
dataRight["ApGrf"] = ApGrfRight
dataRight["MediolateralGrf"] = MediolateralGrfRight
dataRight = dataRight * 100 # permets de travailler avec des forces de réaction au sol d'un ordre de grandeur de 100

walking = Procedures(dataLeft, dataRight)

data_clean = pd.DataFrame()
for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
    if sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_clean[f"{step}"] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]

data_clean = data_clean.iloc[ : , : 52]


# =============================================================  AE

def ModeleAutoEncoder():
    import tensorflow as tf
    from tensorflow import keras
    from sklearn.model_selection import train_test_split

    # Diviser les données en ensembles d'entraînement et de test
    train_noised, test_noised, train_clean, test_clean = train_test_split(data_noised, data_clean, test_size=0.2)  # Vous pouvez ajuster la taille du jeu de test selon vos besoins

    # Normaliser les données
    train_noised = (train_noised - train_noised.mean()) / train_noised.std()
    test_noised = (test_noised - test_noised.mean()) / test_noised.std()
    train_clean = (train_clean - train_clean.mean()) / train_clean.std()
    test_clean = (test_clean - test_clean.mean()) / test_clean.std()

    # Définir le modèle de l'autoencodeur
    input_dim = train_noised.shape[1]
    encoding_dim = 10  # Nombre de neurones dans la couche d'encodage

    input_layer = keras.layers.Input(shape=(input_dim,))
    encoder = keras.layers.Dense(encoding_dim, activation='relu')(input_layer)
    decoder = keras.layers.Dense(input_dim, activation='linear')(encoder)

    autoencoder = keras.models.Model(inputs=input_layer, outputs=decoder)

    # Compiler le modèle
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')

    # Entraîner le modèle en utilisant les données bruitées et les données débruitées
    history = autoencoder.fit(train_noised, train_clean, epochs=100, batch_size=32, validation_data=(test_noised, test_clean))

    # Afficher la courbe d'apprentissage (perte)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Courbe d\'apprentissage')
    plt.xlabel('Époque')
    plt.ylabel('Perte')
    plt.legend(['Entraînement', 'Validation'])
    plt.show()

    # Utiliser le modèle pour débruiter les signaux
    denoised_data = autoencoder.predict(data_noised)

    # Convertir les données débruitées en DataFrame
    denoised_df = pd.DataFrame(denoised_data, columns=data_noised.columns)

    # Afficher des résultats
    plt.figure()
    plt.subplot(2,2,1)
    plt.plot(data_noised["10"], label="Noised", c="r")
    plt.plot(denoised_df["10"], label="Denoised", c="g")
    plt.subplot(2,2,2)
    plt.plot(data_noised["20"], label="Noised", c="r")
    plt.plot(denoised_df["20"], label="Denoised", c="g")
    plt.subplot(2,2,3)
    plt.plot(data_noised["30"], label="Noised", c="r")
    plt.plot(denoised_df["30"], label="Denoised", c="g")
    plt.subplot(2,2,4)
    plt.plot(data_noised["40"], label="Noised", c="r")
    plt.plot(denoised_df["40"], label="Denoised", c="g")
    plt.legend()
    plt.show()

ModeleAutoEncoder()
