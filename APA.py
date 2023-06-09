# test APA
import os
import pandas as pd
import matplotlib.pyplot as plt

from docx import Document
from docx.shared import Inches

from Walking.Walking import Walking
from SOLE.FeetMe import readFeetMeMultipleCsv
from SOLE.FeetMe import ReadSpatioTemporalCsv
from Reader.Reader import Reader

ID = 161095
mass = 60
tests = ["Parcours_1", "Parcours_2", "Haie", "Salom", "doubleTache", "bande", "Back"]

document = Document()

for test in tests:

    document.add_heading(f'Condition : {test}', 0)
    
    DataPath = f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\APA\\{ID}\\{test}\\"

    files = os.listdir(DataPath)
    try :
        walking_name = [file for file in files if file.endswith(".hdf5")][0]
        fullfilename_walking = os.path.join(DataPath, walking_name)
    except:
        pass
    metrics_file = [file for file in files if file.endswith("metrics.csv")][0]
    fullfilename_metrics = os.path.join(DataPath, metrics_file)
    pressures_files = [file for file in files if file.endswith("pressure.csv")]
    fullfilenames_pressures = []
    for pressures_file in pressures_files:
        fullfilenames_pressures.append(os.path.join(DataPath, pressures_file))


    try:
        walking = Reader(fullfilename_walking).readh5()
        
    except:
        SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames_pressures, freq = 110)
        DataFrameSpatioTemporal_Left, DataFrameSpatioTemporal_Right = ReadSpatioTemporalCsv(fullfilename_metrics)
        
        walking = Walking(mass)
        walking.setLeftLegSole(SoleInstanceLeft)
        walking.setRightLegSole(SoleInstanceRight)
        walking.setDataFrameSpatioTemporal_Left(DataFrameSpatioTemporal_Left)
        walking.setDataFrameSpatioTemporal_Right(DataFrameSpatioTemporal_Right)

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import DeleteStepProcedure
        procedure = DeleteStepProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from Writer.Writer import Writer
        StoragePathHDF5 = DataPath
        Writer(walking = walking, path = StoragePathHDF5, file_name = f"walking_{ID}_{test}.hdf5").writeh5()

    from Walking.WalkingFilters import WalkingGraphicsFilter
    from Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure
    procedure = PlotDynamicSymetryFunctionNormalisedProcedure(show_graph = False, save_graph = True, StoragePath = DataPath)
    WalkingGraphicsFilter(walking, procedure).run()

    files = os.listdir(DataPath)
    figs = [file for file in files if file.endswith("VerticalGrf.png")]
    for fig in figs:
        FigPath = os.path.join(DataPath, fig)
        document.add_paragraph('Assymetry of the Vertical Ground Reaction Force')
        document.add_picture(FigPath, height = Inches(3.5))


    from Walking.WalkingFilters import WalkingDataProcessingFilter
    from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure
    procedure = CutDataProcessingProcedure()
    procedure.setCutNumber(n_cut=3)
    WalkingDataProcessingFilter(walking, procedure).run()

    from Walking.WalkingFilters import WalkingGraphicsFilter
    from Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
    procedure = PlotCutGroundReactionForceProcedure(show_graph = False, save_graph = True, StoragePath = DataPath)
    WalkingGraphicsFilter(walking, procedure).run()
    
    files = os.listdir(DataPath)
    figs = [file for file in files if file.endswith("CutDataGrf.png")]
    for fig in figs:
        FigPath = os.path.join(DataPath, fig)
        document.add_paragraph('Evolution of Vertical Ground Reaction Force during the test')
        document.add_picture(FigPath, width = Inches(7.5))


    document.save(f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\APA\\{ID}\\Report.docx")
    import ipdb; ipdb.set_trace()





document.save(f"C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\APA\\{ID}\\Report.docx")
import ipdb; ipdb.set_trace()