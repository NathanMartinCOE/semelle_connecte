import pandas as pd
import matplotlib.pyplot as plt

from math import sqrt


def RichardBacker_SEM(data, columns_names, condition, pdf, plot_graph = False):
    """
    A function for compute an plot the SEM (standard error of measure) as described by richard backer.
    For more info please see : https://wwrichard.net/introduction-to-the-sem/

    Args:
        data (pd.Series) : in each row -> "id", "test", "leg", "value_0" to "value_n" 
            (a single value for the space-time parameters, 1000 for the vertical reaction force)
        columns_names (list) : names to use for creat the pd.DataFrame
        condition (str) : condition name  
        pdf (matplotlib.backends.backend_pdf.PdfPages) 
        plot_graph (Boolean) by defaut is False
            True  -> For use when you want to represent the value of the SEM over a gait cycle 
            False -> Don't plot the value of the SEM
    Outputs:
        when plot_graph == True -> save the fig in the pdf
        SEM_left  (int) -> value of the SEM for the left  leg
        SEM_right (int) -> value of the SEM for the right leg
    """

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