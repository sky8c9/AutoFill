class Input:
    FORM = "../form/f940.pdf"
    SHEET = "../template/940_data_template.xlsx"

class Tax:
    TAX_INFO_COLUMN_START = 6
    FUTA_TAX = 0.006

class ThirdParty:
    THIRD_PARTY_DESIGNEE = [["Designee Name"], ["Phone"], ["PIN"]]

class Preparer:
    PREPARER_INFO = [["Tax Preparer Name"], ["PTIN"], ["Firm Name"], ["EIN"], ["Firm Address"], ["Phone"], ["City"], ["State"], ["Zip"]]

class MetaDataLoc:
    COMPANY_LOC = [1, 1]
    PART6_LOC = [2, 11]
    PART7_LOC = [2, 14]
    VOUCHER_LOC = [3, 1]

class LineLoc:
    LINE1A = [1, 12]
    LINE3 = [1, 14]
    LINE4 = [1, 16]
    LINE5 = [1, 18]
    LINE6 = [1, 20]
    LINE12 = [1, 32]
    LINE14 = [1, 36]
    LINE15 = [1, 38]

class CheckBoxLoc:
    PART6_THIRD_PARTY_CHECKBOX = [2, 1]
    PART7_PAID_PREPARER_CHECKBOX = [2, 2]
    OVERPAYMENT_CHECKBOX = [1, 12]
