class Input:
    FORM = "f941sb.pdf"

class MetaDataLoc:
    EIN_LOC = [1, 1]

class DepositInfo:
    '''
    M1_DEPOSIT = [1, 15]
    M1_TOTAL = [1, 77]
    M2_DEPOSIT = [1, 79]
    M2_TOTAL = [1, 141]
    M3_DEPOSIT = [1, 143]
    M3_TOTAL = [1, 205]
    SUM = [1, 207]
    '''
    FIRST_DEPOSIT_LOC = 15
    GAP_TO_TOTAL = 62

class CheckBoxLoc:
    TAX_QUARTER_CHECKBOX = [1, 1]