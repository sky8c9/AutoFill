class Input:
    FORM = "f940.pdf"
    SHEET = "940_data_template.xlsx"

class Tax:
    TAX_INFO_COLUMN_START = 6
    FUTA_TAX = 0.006

class ThirdParty:
    THIRD_PARTY_DESIGNEE = [["Designee Name"], ["Phone"], ["PIN"]]

class Preparer:
    PREPARER_INFO = [["Tax Preparer Name"], ["PTIN"], ["Firm Name"], ["EIN"], ["Firm Address"], ["Phone"], ["City"], ["State"], ["Zip"]]

class MetaDataLoc:
    COMPANY_LOC = [1, 1]
    HEADER1_LOC = [2, 1]
    PART6_LOC = [2, 13]
    PART7_LOC = [2, 16]
    VOUCHER_LOC = [3, 1]

class LineLoc:
    LINE1A = [1, 19]
    LINE3 = [1, 21]
    LINE4 = [1, 23]
    LINE5 = [1, 25]
    LINE6 = [1, 27]
    LINE12 = [1, 39]
    LINE14 = [1, 43]
    LINE15 = [1, 45]

class CheckBoxLoc:
    PART6_THIRD_PARTY_CHECKBOX = [2, 1]
    PART7_PAID_PREPARER_CHECKBOX = [2, 2]
    OVERPAYMENT_CHECKBOX = [1, 12]
