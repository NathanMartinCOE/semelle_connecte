# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 06 - 10

def SymetryIndex(Left, Right):
    """
    Compute Symetry Index based on Alcantara's article.
    Alcantara RS, Beck ON, Grabowski AM. Added lower limb mass does not affect biomechanical asymmetry but increases metabolic 
    power in runners with a unilateral transtibial amputation. Eur J Appl Physiol. juin 2020;120(6):1449‑56. 

    Args: 
        Left:  values of the left leg
        Right: values of the right leg
    Outputs:
        SymetryIndex_Values: values of the Symetry Index in %
    """
    SymetryIndex_Values = []
    for left, right in zip(Left, Right):
        value = round(abs(((left-right) / (0.5*(left+right))) * 100),2)
        SymetryIndex_Values.append(value)

    return SymetryIndex_Values