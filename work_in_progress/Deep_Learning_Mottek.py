import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from semelle_connecte.SOLE.FeetMe import FeetMe
from semelle_connecte.Walking.Walking import Walking

from semelle_connecte.Tools.ToolsFFT import TransformFourrier, VisuTransformFourrier
from semelle_connecte.Tools.ToolsGetStepEvent import GetStepEvent

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


    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    print("GroundReactionForceKinematicsProcedure --------------- done")

    from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
    from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
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
dataLeft["VerticalVGrf"][dataLeft["VerticalVGrf"] < 40] = 0
dataLeft["ApGrf"] = forces[1][:,1]
dataLeft["MediolateralGrf"] = forces[1][:,0] * -1

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = forces[0][:,2]
dataRight["VerticalVGrf"][dataRight["VerticalVGrf"] < 40] = 0
dataRight["ApGrf"] = forces[0][:,1]
dataRight["MediolateralGrf"] = forces[0][:,0]

walking = Procedures(dataLeft, dataRight)

data_noised_df = pd.DataFrame()
for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
    if sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_noised_df[f"{step}"] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]


data_noised = np.zeros((len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"]), 1000))
for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
    if np.sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_noised[step, :] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]

    

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

from semelle_connecte.SOLE.FeetMe import FeetMe
from semelle_connecte.Walking.Walking import Walking

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

data_clean_df  = pd.DataFrame()
for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
    if sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_clean_df[f"{step}"] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]
data_clean_df = data_clean_df.iloc[ : , : 51]

data_clean = np.zeros((len(data_noised), 1000))
for step in np.arange(len(data_noised)):
    if np.sum(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]) > 1:
        data_clean[step, :] = walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step]


# =============================================================  AE
def ModeleAutoEncoder(data_noised, data_clean):
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

    plt.figure()
    plt.plot(data_noised.mean(axis=1), label="Noised", c="r")
    plt.plot(denoised_df.mean(axis=1), label="Denoised", c="g")
    plt.legend()
    plt.show()

ModeleAutoEncoder(data_noised=data_noised_df, data_clean=data_clean_df)


def ModeleAutoEncoder_2():
    import tensorflow as tf
    from tensorflow import keras
    import matplotlib.pyplot as plt

    # Créer l'encodeur
    input_shape = (1000, 1)

    encoder_input = keras.Input(shape=input_shape)
    encoder = keras.layers.Conv1D(32, 3, activation='relu', padding='same')(encoder_input)
    encoder = keras.layers.MaxPooling1D(2, padding='same')(encoder)
    encoder = keras.layers.Conv1D(64, 3, activation='relu', padding='same')(encoder)
    encoder = keras.layers.MaxPooling1D(2, padding='same')(encoder)
    encoder = keras.layers.Flatten()(encoder)
    latent_dim = 10  # Dimension latente
    latent_vector = keras.layers.Dense(latent_dim)(encoder)

    encoder_model = keras.Model(encoder_input, latent_vector)

    # Créer le décodeur
    decoder_input = keras.Input(shape=(latent_dim,))
    decoder = keras.layers.Dense(250, activation='relu')(decoder_input)
    decoder = keras.layers.Reshape((250, 1))(decoder)
    decoder = keras.layers.Conv1DTranspose(64, 3, activation='relu', padding='same')(decoder)
    decoder = keras.layers.UpSampling1D(2)(decoder)
    decoder = keras.layers.Conv1DTranspose(32, 3, activation='relu', padding='same')(decoder)
    decoder = keras.layers.UpSampling1D(2)(decoder)
    decoder_output = keras.layers.Conv1DTranspose(1, 3, activation='linear', padding='same')(decoder)

    decoder_model = keras.Model(decoder_input, decoder_output)

    # Créer l'autoencodeur en combinant l'encodeur et le décodeur
    autoencoder_input = keras.Input(shape=input_shape)
    latent_representation = encoder_model(autoencoder_input)
    decoded_output = decoder_model(latent_representation)

    autoencoder_model = keras.Model(autoencoder_input, decoded_output)

    # Compiler l'autoencodeur
    autoencoder_model.compile(optimizer='adam', loss='mse')

    # Entraîner l'autoencodeur
    history = autoencoder_model.fit(data_noised, data_clean, epochs=100, batch_size=32, validation_split=0.2)

    # Afficher la courbe d'apprentissage (perte)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Courbe d\'apprentissage')
    plt.xlabel('Époque')
    plt.ylabel('Perte')
    plt.legend(['Entraînement', 'Validation'])
    plt.show()

    # Utiliser l'autoencodeur pour débruiter les données
    denoised_data = autoencoder_model.predict(data_noised)

    # Afficher les données bruitées et débruitées pour certaines courbes
    plt.figure(figsize=(10, 6))

    # Indice des courbes à afficher
    indices = [0, 10, 20, 30, 40]

    for idx in indices:
        plt.subplot(len(indices), 2, 2*indices.index(idx)+1)
        plt.plot(data_noised[idx], label='Bruitée', color='red')
        plt.title(f'Courbe {idx} - Bruitée')
        plt.subplot(len(indices), 2, 2*indices.index(idx)+2)
        plt.plot(denoised_data[idx], label='Débruitée', color='green')
        plt.title(f'Courbe {idx} - Débruitée')

    plt.tight_layout()
    plt.show()

# ModeleAutoEncoder_2()