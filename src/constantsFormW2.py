class Input:
    W2_IN = "../W2_in"
    W2_OUT = "../W2_out"
    FORM = "../form/fw2.pdf"
    FILE_NAME = "../template/w2_data_template.xlsx"
    EMPLOYER_SHEET = "Employer"
    EMPLOYEE_SHEET = "Employee"

class W2:
    '''
    Employer & Employee info section
        + pos#0 : column index
        + pos#1 : row index within data block
    '''
    EMPLOYER_INFO_META = [1, 0]
    EMPLOYEE_INFO_META = [1, 0]

    # Employee earning
    MULTIPLE_ENTRY_COL_START = 13

    # Tax constants
    SS_MAX_22 = 147000
    SS_RATE_22 = 0.062
    MC_RATE_22 = 0.0145
    EPSILON = 0.01