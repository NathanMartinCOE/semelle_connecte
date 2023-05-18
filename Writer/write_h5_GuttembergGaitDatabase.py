import h5py
import pandas as pd
import numpy as np
import os
from tqdm import tqdm

path = "C:\\Users\\Nathan\\Desktop\\Guttenberg Gait Database\\"

# Left 
GRF_F_V_PRO_left = pd.read_csv(os.path.join(path,'GRF_F_V_PRO_left.csv'))
GRF_F_AP_PRO_left = pd.read_csv(os.path.join(path,'GRF_F_AP_PRO_left.csv'))
GRF_F_ML_PRO_left = pd.read_csv(os.path.join(path,'GRF_F_ML_PRO_left.csv'))

# Right lower extremity
GRF_F_V_PRO_right = pd.read_csv(os.path.join(path,'GRF_F_V_PRO_right.csv'))
GRF_F_AP_PRO_right = pd.read_csv(os.path.join(path,'GRF_F_AP_PRO_right.csv'))
GRF_F_ML_PRO_right = pd.read_csv(os.path.join(path,'GRF_F_ML_PRO_right.csv'))

def TransformDataFrame(DataFrame):
    DataFrame = DataFrame.drop(['DATASET_ID', 'SUBJECT_ID', 'SESSION_ID', 'TRIAL_ID'], axis = 1)
    DataFrame = DataFrame.T
    return DataFrame

def SelectSuject(ID, DataLeft, DataRight):
    DataSubjectLeft = DataLeft[DataLeft['SUBJECT_ID'] == ID]
    DataSubjectRight = DataRight[DataRight['SUBJECT_ID'] == ID]
    DataSubjectLeft = TransformDataFrame(DataSubjectLeft)
    DataSubjectRight = TransformDataFrame(DataSubjectRight)
    return DataSubjectLeft, DataSubjectRight

def MeanData(DataLeft, DataRight):
    MeanData = pd.DataFrame()
    MeanData["Left"] =  DataLeft.mean(axis = 1)
    MeanData["Right"] = DataRight.mean(axis = 1)
    return  MeanData["Left"], MeanData["Right"]

def TabGrfTotal(DataSubjectLeft, DataSubjectRight, decalage):
    GrfRight = [-999]
    GrfLeft = [-999]

    SwingLeft = [0] * (100 - (2 *decalage))
    SwingRight = [0] * (100 - (2 *decalage))
    
    for col in zip(DataSubjectLeft.columns, DataSubjectRight.columns):
        GrfLeft = np.concatenate((GrfLeft, DataSubjectLeft[col[0]], SwingLeft), axis = 0)
        GrfRight = np.concatenate((GrfRight, DataSubjectRight[col[1]], SwingRight), axis = 0)

    GrfLeft = GrfLeft[1:]
    GrfRight = GrfRight[1:]
    GrfLeft = GrfLeft[(100 - decalage):]
    GrfRight = GrfRight[ : (len(GrfRight)-(100 - decalage))]
    GrfLeft[:decalage+10] = 0
    GrfRight[-decalage - 102:] = 0
    GrfRight[0] = 0
    
    return GrfLeft, GrfRight

StorageDataPath = "C:/Users/Nathan/Desktop/Recherche/Github/semelle_connecte/Test/Dataset_test/"
f = h5py.File(os.path.join(StorageDataPath, "GuttenbergGaitDatabase.hdf5"), "w")
for ID in tqdm(np.arange(1,350)):
    decalage_entre_deux_pas = 15

    VerticalGrfLeft, VerticalGrfRight = SelectSuject(ID, DataLeft = GRF_F_V_PRO_left, DataRight = GRF_F_V_PRO_right)
    VerticalGrfLeft, VerticalGrfRight = TabGrfTotal(DataSubjectLeft = VerticalGrfLeft, DataSubjectRight = VerticalGrfRight, decalage = decalage_entre_deux_pas)

    ApGrfLeft, ApGrfRight = SelectSuject(ID, DataLeft = GRF_F_AP_PRO_left, DataRight = GRF_F_AP_PRO_right)
    ApGrfLeft, ApGrfRight = TabGrfTotal(DataSubjectLeft = ApGrfLeft, DataSubjectRight = ApGrfRight, decalage = decalage_entre_deux_pas)

    MediolateralGrfLeft, MediolateralGrfRight = SelectSuject(ID, DataLeft = GRF_F_ML_PRO_left, DataRight = GRF_F_ML_PRO_right)
    MediolateralGrfLeft, MediolateralGrfRight = TabGrfTotal(DataSubjectLeft = MediolateralGrfLeft, DataSubjectRight = MediolateralGrfRight, decalage = decalage_entre_deux_pas)

    grp = f.create_group(f"{ID}")
    grp.create_dataset("VerticalGrfLeft" ,shape= None ,dtype = None, data = VerticalGrfLeft)
    grp.create_dataset("ApGrfLeft" ,shape= None ,dtype = None, data = ApGrfLeft)
    grp.create_dataset("MediolateralGrfLeft" ,shape= None ,dtype = None, data = MediolateralGrfLeft)
    grp.create_dataset("VerticalGrfRight" ,shape= None ,dtype = None, data = VerticalGrfRight)
    grp.create_dataset("ApGrfRight" ,shape= None ,dtype = None, data = ApGrfRight)
    grp.create_dataset("MediolateralGrfRight" ,shape= None ,dtype = None, data = MediolateralGrfRight)