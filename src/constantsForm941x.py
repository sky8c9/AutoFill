class Input:
    FORM = "../form/f941x.pdf"
    SHEET = "../template/941X_data_template.xlsx"

class Tax:
    TAX_INFO_COLUMN_START = 8
    ERC_RATE = {2020 : 0.5, 2021 : 0.7}
    NON_REF_RATE = 0.062

class Preparer:
    PREPARER_INFO = [["Tax Preparer Name"], ["Firm Name"], ["Firm Address"], ["City"], ["State"], ["PTIN"], ["EIN"], ["Phone"], ["Zip"]]

class MetaDataLoc:
    DATE = [1, 13]
    COMPANY_LOC = [1, 1]
    HEADER_YEAR = [1, 12]
    HEADER_QUARTER = [2, 3]
    PART5_LOC = [5, 32]

class LineLoc:
    LINE18A = [2, 99]
    LINE23 = [3, 139]
    LINE26A = [3, 157]
    LINE27 = [3, 181]
    LINE30 = [3, 195]

class CheckBoxLoc:
    TAX_QUARTER_CHECKBOX = [1, 2]

    # Below is the default setting for ERC checkboxes - change if needed
    FORM_TYPE_CHECKBOX = [1, 1]
    OVERREPORTED_CLAIM_CHECKBOX = [1, 3]
    CERTIFY_CHECKBOX = [1, 4]
    SS_MC_EMPLOYER_CHECKBOX = [1, 10]
    PART4_CHECKBOX = [5, 1]
