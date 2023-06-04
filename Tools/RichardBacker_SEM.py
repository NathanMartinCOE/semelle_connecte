import pandas as pd
import matplotlib.pyplot as plt

from math import sqrt


def RichardBacker_SEM(data, columns_names, condition, pdf, plot_graph = False):

    ### ======= Compute Standard Deviation of each subject beetween all they test for Right and Left leg ================
    DataRaw = pd.DataFrame(data, columns= columns_names)
    DataRawRight = DataRaw[DataRaw["leg"]=="RightLeg"]
    DataRawLeft = DataRaw[DataRaw["leg"]=="LeftLeg"]
    DataSdRight = DataRawRight.drop("test", axis='columns').groupby([DataRawRight["id"]]).std()
    DataSdLeft = DataRawLeft.drop("test", axis='columns').groupby([DataRawLeft["id"]]).std()

    ### ======= Compute the Root Mean Squared Avarage for Right and Left leg ============================================
    def RMSA(DataSd):
        DataSdSquared = DataSd**2
        SEM = []
        for col in DataSdSquared.columns:
            SEM.append(sqrt(DataSdSquared[col].sum()/DataSdSquared.shape[0]))
        DataSEM = pd.DataFrame()
        DataSEM["SEM"] = SEM
        return DataSEM.T

    DataSEMRight = RMSA(DataSdRight)
    DataSEMLeft = RMSA(DataSdLeft)

    ### =============================== Compute SEM for Right and Left leg ===============================================
    SEM_right = DataSEMRight.mean(axis="columns").values[0]
    print(f"The standard error of measurement for right is -------------------- {round(SEM_right,4)}")
    SEM_left = DataSEMLeft.mean(axis="columns").values[0]
    print(f"The standard error of measurement for left  is -------------------- {round(SEM_left,4)}")

    ### =================== Plot SEM of Ground Reaction Force for each leg and each conditions ============================
    MeanValueGrfRight = DataRawRight.drop(["test", "id", "leg"], axis='columns').mean(axis=0).values
    MeanValueGrfLeft = DataRawLeft.drop(["test", "id", "leg"], axis='columns').mean(axis=0).values

    if plot_graph == True:
        plt.figure()
        plt.suptitle(f"{condition}")
        plt.subplot(1,2,1)
        plt.title(f"Left Leg --- SEM = {round(SEM_left,4)} kg/cm²")
        plt.plot(MeanValueGrfLeft, label='Left Leg', c='r')
        plt.plot(DataSEMLeft.T.values, label="SEM", c="black")
        plt.xlabel("Cyle (%)")
        plt.ylabel("Vertical Ground Reaction Force (kg/cm²)")
        for grf in DataRawLeft.drop(["test", "id", "leg"], axis='columns').values:
            plt.plot(grf, c='grey', ls="--")
        plt.legend()
        plt.subplot(1,2,2)
        plt.title(f"Right Leg --- SEM = {round(SEM_right,4)} kg/cm²")
        plt.plot(MeanValueGrfRight, label='Right Leg', c='b')
        plt.plot(DataSEMRight.T.values, label="SEM", c="black")
        for grf in DataRawRight.drop(["test", "id", "leg"], axis='columns').values:
            plt.plot(grf, c='grey', ls="--")
        plt.xlabel("Cyle (%)")
        plt.ylabel("Vertical Ground Reaction Force (kg/cm²)")
        plt.legend()

        pdf.savefig() ### Save the fig as a new page in pdf 
        plt.clf()     ### Clear plot

    
    return SEM_left, SEM_right