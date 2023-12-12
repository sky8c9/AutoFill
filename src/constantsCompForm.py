class Constants:
    ROOT = "../"

class FW2(Constants):
    # Form info
    FORM_NAME = "w2"
    FORM_CLASS = "FormW2"

    # IO Path
    FORM = f"{Constants.ROOT}form/fw2.pdf"
    IN = f"{Constants.ROOT}/W2_in"
    OUT = f"{Constants.ROOT}/W2_out"

    # Sheet
    PAYER_SHEET = "Employer"
    PAYEE_SHEET = "Employee"

    # Employee earning
    MULTIPLE_ENTRY_COL_START = 13

    # Name loc
    NAME_LOC = [1, 0]

    # 2023 Tax constants
    SS_MAX = 160200
    SS_RATE = 0.062
    MC_RATE = 0.0145
    EPSILON = 0.05

class F1099NEC(Constants):
    # Form info
    FORM_NAME = "1099-NEC"
    FORM_CLASS = "Form1099NEC"

    # IO Path
    FORM = f"{Constants.ROOT}form/f1099NEC.pdf"
    IN = f"{Constants.ROOT}1099NEC_in"
    OUT = f"{Constants.ROOT}1099NEC_out"
    
    # Sheet
    PAYER_SHEET = "Payer"
    PAYEE_SHEET = "Recipient"

    # Employee earning
    MULTIPLE_ENTRY_COL_START = 1

    # Name loc
    NAME_LOC = [1, 0]