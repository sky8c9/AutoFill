from constantsForm941x import Input, Tax, Preparer, MetaDataLoc, LineLoc, CheckBoxLoc
from form import Form

class Form941x(Form):
    def __init__(self, data):
        super().__init__(Input.FORM)

        # Entity metadata
        self.date, self.year, self.quarter, self.ein, self.legal_name, self.trade_name, self.address, self.sign = data.iloc[0:Tax.TAX_INFO_COLUMN_START].fillna("").astype(str)
        
        # Adjustment 
        self.tax_info = data.iloc[Tax.TAX_INFO_COLUMN_START:].fillna(0).astype(float)

    def fill(self):
        print(f"{self.trade_name} - 941X ...")
        self.fillMeta()
        self.erc()
        self.output(Input.FORM, self.trade_name)

    def fieldFormat(self, pNum, offset):
        return f"f{pNum}_0{offset}[0]" if offset < 10 else f"f{pNum}_{offset}[0]"

    def checkBoxFormat(self, pNum, offset, index):
        return f"c{pNum}_0{offset}[{index}]" if offset < 10 else f"c{pNum}_{offset}[{index}]"

    # Testing erc
    def erc(self):
        # Line 18a
        nonref = self.tax_info["Corrected"] * Tax.NON_REF_RATE
        self.setField(LineLoc.LINE18A, [self.reportVal(nonref), self.reportVal(0), self.reportVal(nonref), self.reportVal(-1*nonref)])

        # Line 23
        self.setField(LineLoc.LINE23, [self.reportVal(-1*nonref)])

        # Line 26a
        erc_ref = self.tax_info["Corrected"] * Tax.ERC_RATE[int(self.year)] - nonref
        self.setField(LineLoc.LINE26A, [self.reportVal(erc_ref), self.reportVal(0), self.reportVal(erc_ref), self.reportVal(-1*erc_ref)])

        # Line 27
        erc = erc_ref + nonref
        self.setField(LineLoc.LINE27, [self.reportVal(-1*erc)])

    def fillMeta(self):        
        # Company - Meta data may span over multiple pages (set mutiplePages flag to true)
        self.setField(MetaDataLoc.COMPANY_LOC, [self.ein.split("-"), [self.legal_name], [self.trade_name], self.address.split(", ")], multiplePages=True)

        # Fill each page header with year and quarter
        self.setField(MetaDataLoc.HEADER_YEAR, [[self.year]], multiplePages=True)
        self.setField(MetaDataLoc.HEADER_QUARTER, self.quarter, multiplePages=True)

        # Correcting metadata
        self.setCheckBox(CheckBoxLoc.TAX_QUARTER_CHECKBOX, self.quarter, 4)
        self.setField(MetaDataLoc.DATE, [self.date.split("-")])

        # ERC default checkboxes - change if needed
        self.setCheckBox(CheckBoxLoc.FORM_TYPE_CHECKBOX, 1, 2)
        self.setCheckBox(CheckBoxLoc.OVERREPORTED_CLAIM_CHECKBOX, 2, 2)
        self.setCheckBox(CheckBoxLoc.CERTIFY_CHECKBOX, 2, 1)
        self.setCheckBox(CheckBoxLoc.SS_MC_EMPLOYER_CHECKBOX, 2, 1)
        self.setCheckBox(CheckBoxLoc.PART4_CHECKBOX, 1, 1)

        # PART 5 - Sign
        self.setField(MetaDataLoc.PART5_LOC, [self.sign.split(", ")])

        # PART 5 - Paid Preparer
        if Preparer.PREPARER_INFO:
            pnum, offset = MetaDataLoc.PART5_LOC
            #self.setCheckBox(CheckBoxLoc.PART5_PAID_PREPARER_CHECKBOX, 1, 1)
            self.setField([pnum, offset + 3], Preparer.PREPARER_INFO)