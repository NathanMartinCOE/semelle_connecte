# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 05 - 06

def GetStepEvent(VerticalGrf):
    """
    This function make two list with the index of HeelStrike time and ToeOff time.

    Args:
        VerticalGrf: vertical ground reaction force of all step.

    Outputs: 
        HeelStrike (list) : index of the heel strike for each step. 
        ToeOff (list)     : index of the toe of for each step.
    """
    if min(VerticalGrf) != 0 :
        thresfold = min(VerticalGrf) + 10 / 100 * min(VerticalGrf)
        print(f"Caution no 0 find in Vertical GRF dataframe : use of a thresfold at {thresfold}")
    else : thresfold = 0

    HeelStrike = []
    ToeOff = []
    for i in range(0,len(VerticalGrf)-1):
        if thresfold == 0:
            if VerticalGrf[i] == 0 and VerticalGrf[i+1] > 0 : 
                HeelStrike.append(i)
            if VerticalGrf[i] > 0 and VerticalGrf[i+1] == 0 : 
                ToeOff.append(i)
        else :
            if VerticalGrf[i] < thresfold  and VerticalGrf[i+1] > thresfold : 
                HeelStrike.append(i)
            if VerticalGrf[i] > thresfold and VerticalGrf[i+1] < thresfold : 
                ToeOff.append(i)
    return HeelStrike, ToeOff
