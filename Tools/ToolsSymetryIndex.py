"""
Compute Symetry Index based on Alcantara's article.
Alcantara RS, Beck ON, Grabowski AM. Added lower limb mass does not affect biomechanical asymmetry but increases metabolic 
power in runners with a unilateral transtibial amputation. Eur J Appl Physiol. juin 2020;120(6):1449‑56. 
"""

def SymetryIndex(Left, Right):
    SymetryIndex_Values = []
    for left, right in zip(Left, Right):
        value = round(abs(((left-right) / (0.5*(left+right))) * 100),2)
        SymetryIndex_Values.append(value)
    return SymetryIndex_Values