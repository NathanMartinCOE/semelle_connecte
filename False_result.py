import pandas as pd
import random
import os

stanceDuration = []
singleSupportDuration = []
doubleSupportDuration = []
swingDuration = []
VerticalGrf = []

for _ in range(100):
    stanceDuration.append(random.uniform(-30.0, 30.0))
    singleSupportDuration.append(random.uniform(-10.0, 10.0))
    doubleSupportDuration.append(random.uniform(-20.0, 20.0))
    swingDuration.append(random.uniform(-10.0, 10.0))
    VerticalGrf.append(random.uniform(-100.0, 100.0))

DynamicSymetryScoreMean_SRU = pd.DataFrame({"stanceDuration" :  stanceDuration,
                                            "singleSupportDuration" : singleSupportDuration,
                                            "doubleSupportDuration" :  doubleSupportDuration,
                                            "swingDuration" : swingDuration,
                                            "VerticalGrf" : VerticalGrf})

stanceDuration = []
singleSupportDuration = []
doubleSupportDuration = []
swingDuration = []
VerticalGrf = []

for _ in range(100):
    stanceDuration.append(random.uniform(-15.0, 15.0))
    singleSupportDuration.append(random.uniform(-5.0, 5.0))
    doubleSupportDuration.append(random.uniform(-10.0, 10.0))
    swingDuration.append(random.uniform(-5.0, 5.0))
    VerticalGrf.append(random.uniform(-40.0, 40.0))
   
DynamicSymetryScoreMean_TDM = pd.DataFrame({"stanceDuration" :  stanceDuration,
                                            "singleSupportDuration" : singleSupportDuration,
                                            "doubleSupportDuration" :  doubleSupportDuration,
                                            "swingDuration" : swingDuration,
                                            "VerticalGrf" : VerticalGrf})

PathSaveData = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\"
DynamicSymetryScoreMean_SRU.to_csv(os.path.join(PathSaveData, "FALSE_DynamicSymetryScoreMean_SRU.csv"))
DynamicSymetryScoreMean_TDM.to_csv(os.path.join(PathSaveData, "FALSE_DynamicSymetryScoreMean_TDM.csv"))


pointure = []

for _ in range(100):
     pointure.append(random.randint(35, 46))

import numpy as np
print(np.mean(pointure))
print(np.std(pointure))