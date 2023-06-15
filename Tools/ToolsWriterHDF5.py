# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 06 - 13

import yaml


def ConvertWalkingToHDF5(f, walking):
    """ This function convert an walking instanc in a HDF5 structure

    Args: 
        f (h5py.File()) or (h5py.File().create_group())
        walking (semelle_connecte.Walking) an walking instance
    """

    # Save the Unique Value
    grp_UniqueValue = f.create_group("UniqueValue")
    grp_UniqueValue.create_dataset("mass", shape= None ,dtype = None, data = walking.m_mass)

    # Save the Dictionary
    grp_dict = f.create_group("dict")

    grp_sole = grp_dict.create_group("sole")
    for leg in ["LeftLeg", "RightLeg"]:
        grp_leg = grp_sole.create_group(leg)
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            try:
                grp_leg.create_dataset(axe, shape= None ,dtype = None, data = walking.m_sole[leg].data[axe])
            except:
                print(f"No value in  walking.m_sole[{leg}].data[{axe}]")

    grp_StepGrfValue = grp_dict.create_group("StepGrfValue")
    for leg in ["LeftLeg", "RightLeg"]:
        grp_leg = grp_StepGrfValue.create_group(leg)
        for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
            grp_axe = grp_leg.create_group(axe)
            try :
                for step in np.arange(len(walking.m_StepGrfValue[leg][axe])):
                    grp_axe.create_dataset(f"{step}", shape= None ,dtype = None, data = walking.m_StepGrfValue[leg][axe][step])
            except:
                print(f"No value in walking.m_StepGrfValue[{leg}][{axe}]]")

    grp_GroundReactionForces = grp_dict.create_group("GroundReactionForces")
    for leg in ["LeftLeg", "RightLeg"]:
        grp = grp_GroundReactionForces.create_group(leg)
        try:
            grp.create_dataset("DataGroundReactionForces", shape= None ,dtype = None, data = pd.DataFrame(walking.m_GroundReactionForces[leg]).T )
        except:
            print(f"No value in walking.m_GroundReactionForces[{leg}]")

    grp_DictOfDataFrameCutGrf = grp_dict.create_group("DictOfDataFrameCutGrf")
    for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
        try:
            grp_DictOfDataFrameCutGrf.create_dataset(axe, shape= None ,dtype = None, data = walking.m_DictOfDataFrameCutGrf[axe])
        except:
            print(f"No value in walking.m_DictOfDataFrameCutGrf[{axe}]")
            
    grp_FunctionDynamicAssym = grp_dict.create_group("FunctionDynamicAssym")
    for axe in ["VerticalGrf", "ApGrf", "MediolateralGrf"]:
        try:
            grp_FunctionDynamicAssym.create_dataset(axe, shape= None ,dtype = None, data = walking.m_FunctionDynamicAssym[axe])
        except:
            print(f"No value in walking.m_FunctionDynamicAssym[{axe}]")

    # Save the DataFrame
    grp_DataFrame = f.create_group("DataFrame")
    grp_DataFrame.create_dataset("DataFrameLeftRight" ,shape= None ,dtype = None, data = walking.m_DataFrameLeftRight)
    grp_DataFrame.create_dataset("DataFrameRightLeft" ,shape= None ,dtype = None, data = walking.m_DataFrameRightLeft)
    grp_DataFrame.create_dataset("DataFrameDynamicSymetryScore" ,shape= None ,dtype = None, data = walking.m_DataFrameDynamicSymetryScore)
    grp_DataFrame.create_dataset("DataFrameSpatioTemporal_Left" ,shape= None ,dtype = None, data = walking.m_DataFrameSpatioTemporal_Left)
    grp_DataFrame.create_dataset("DataFrameSpatioTemporal_Right" ,shape= None ,dtype = None, data = walking.m_DataFrameSpatioTemporal_Right)



def ConvertMetadataYamlToHDF5(f, yaml_path):
    """ This function convert an walking instanc in a HDF5 structure

    Args: 
        f (h5py.File()) or (h5py.File().create_group())
        yaml_path (path) the path of a Metadata.yml 
    
    Caution: Metadata.yml must be in the form of the Template_Metadata.yml file
        Supported FileVersion: 1.0
    """

    yaml_file = open(yaml_path, 'r')
    yaml_content = yaml.load(yaml_file)

    if yaml_content["YamlInfo"]["FileVersion"] != 1.0:
        print(f'The metadata version {yaml_content["YamlInfo"]["FileVersion"]} is not recognised')
        exit()

    for grp_name in yaml_content.keys():
        grp_1 = f.create_group(grp_name)
        for key_1, value_1 in yaml_content[grp_name].items():
            try:
                grp_1.create_dataset(key_1, shape= None ,dtype = None, data = value_1)
            except:
                if value_1 == None:
                    grp_1.create_dataset(key_1, shape= None ,dtype = None, data = [])
                else:
                    grp_2 = grp_1.create_group(key_1)
                    for key_2, value_2 in yaml_content[grp_name][key_1].items():
                        try:    
                            grp_2.create_dataset(key_2, shape= None ,dtype = None, data = value_2)
                        except:
                            if value_2 == None:
                                grp_2.create_dataset(key_2, shape= None ,dtype = None, data = [])
                            else:
                                print("You have more than two level of subgroup")
                                print(f"Error for [{grp_name}][{key_1}][{key_2}]")