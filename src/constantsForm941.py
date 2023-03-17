class Input:
    FORM = "../form/f941.pdf"
    SHEET = "../template/941_data_template.xlsx"

class Tax:
    TAX_INFO_COLUMN_START = 8
    SS_TAX_RATE = 0.124
    MED_TAX_RATE = 0.029

class ThirdParty:
    THIRD_PARTY_DESIGNEE = [["Designee Name"], ["Phone"], ["PIN"]]

class Preparer:
    PREPARER_INFO = [["Tax Preparer Name"], ["PTIN"], ["Firm Name"], ["EIN"], ["Firm Address"], ["Phone"], ["City"], ["State"], ["Zip"]]

'''
Below is the locations of some common components within 941 tax form
Location format
    Text field
        fi_j[0] - i : page number, j : field index within page
    Checkbox: 
        ci_j[k] - i : page number, j : checkbox index within page, k: number of choices
'''

class MetaDataLoc:
    COMPANY_LOC = [1, 1]
    PART2_LOC = [2, 34]
    PART4_LOC = [3, 24]
    PART5_LOC = [3, 27]
    VOUCHER_LOC = [5, 1]

class LineLoc:
    LINE1 = [1, 12]
    LINE5A = [1, 17]
    LINE5B = [1, 29]
    LINE5E = [1, 41]
    LINE6 = [1, 45]
    LINE10 = [1, 53]
    LINE12 = [2, 10]
    LINE13G = [2, 24]
    LINE14 = [2, 30]
    LINE15 = [2, 32]

class CheckBoxLoc:
    TAX_QUARTER_CHECKBOX = [1, 1]
    OVERPAYMENT_CHECKBOX = [2, 1]
    PART2_CHECKBOX = [2, 2]
    PART4_THIRD_PARTY_CHECKBOX = [3, 4]
    PART5_PAID_PREPARER_CHECKBOX = [3, 5]
    PAYMENT_VOUCHER_CHECKBOX = [5, 1]