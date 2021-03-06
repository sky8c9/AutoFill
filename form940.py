from constantsForm940 import Input, Tax, ThirdParty, Preparer, MetaDataLoc, LineLoc, CheckBoxLoc
from form import Form

class Form940(Form):
    def __init__(self, data):
        super().__init__(Input.FORM)

        # Entity metadata
        self.ein, self.legal_name, self.trade_name, self.address, self.sign, self.futa_state = data.iloc[0:Tax.TAX_INFO_COLUMN_START].fillna("").astype(str)
        
        # Tax info starting from column #6
        self.tax_info = data.iloc[Tax.TAX_INFO_COLUMN_START:].fillna(0).astype(float)

    def fill(self):
        print(f"{self.trade_name} - 940 ...")
        self.fillMeta()
        self.taxFill()
        self.output(Input.FORM, self.trade_name)

    def taxFill(self): 
        # Line 1a
        self.setField(LineLoc.LINE1A, [self.futa_state])

        total_payment = self.tax_info["Line3"]
        total_payment_over_7k = self.tax_info["Line5"]
        payments_exempt_from_futa = self.tax_info["Line4"]

        # Line 3
        self.setField(LineLoc.LINE3, [self.reportVal(total_payment)])

        # Line 4
        self.setField(LineLoc.LINE4, [self.reportVal(payments_exempt_from_futa)])

        # Line 5
        self.setField(LineLoc.LINE5, [self.reportVal(total_payment_over_7k)])

        # Line 6, 7 & 8
        subtotal = total_payment_over_7k + payments_exempt_from_futa
        total_futa_wages = total_payment - subtotal
        futa_tax_before_adjustment = total_futa_wages * Tax.FUTA_TAX
        self.setField(LineLoc.LINE6, [self.reportVal(subtotal), self.reportVal(total_futa_wages), self.reportVal(futa_tax_before_adjustment)])

        # Line 9 & 10 - Add if needed

        # Line 12, 13
        futa_tax_after_adjustment = futa_tax_before_adjustment
        futa_tax_deposit = self.tax_info["Line13"]
        self.setField(LineLoc.LINE12, [self.reportVal(futa_tax_after_adjustment), self.reportVal(futa_tax_deposit)])

        # Balance Due
        self.balanceDue(futa_tax_after_adjustment - futa_tax_deposit)

    def balanceDue(self, tax_balance):
        tax_balance = 0 if abs(tax_balance) < 0.1 else tax_balance
        address_elements = self.address.split(", ")
        street = address_elements[0]
        other = ", ".join(address_elements[1:])

        if tax_balance > 0: # Create payment voucher
            self.setField(LineLoc.LINE14, [self.reportVal(tax_balance)])
            self.setField(MetaDataLoc.VOUCHER_LOC, [[self.ein], self.reportVal(tax_balance), [self.legal_name], [street], [other]])
        elif tax_balance < 0: # Over payment - Send a refund as default option
            self.setField(LineLoc.LINE15, [self.reportVal(abs(tax_balance))])
            self.setCheckBox(CheckBoxLoc.OVERPAYMENT_CHECKBOX, "Send", 2)

    def fillMeta(self):        
        # Company
        ein_reformat = [c for c in list(self.ein) if c != "-"]
        self.setField(MetaDataLoc.COMPANY_LOC, [ein_reformat, [self.legal_name], [self.trade_name], self.address.split(", ")])

        # Header
        self.setField(MetaDataLoc.HEADER1_LOC, [[self.legal_name], [self.ein]])

        # PART 6 - 3rd party designee contact
        if ThirdParty.THIRD_PARTY_DESIGNEE:
            self.setCheckBox(CheckBoxLoc.PART6_THIRD_PARTY_CHECKBOX, "Yes", 2)
            self.setField(MetaDataLoc.PART6_LOC, ThirdParty.THIRD_PARTY_DESIGNEE)
        else:
            self.setCheckBox(CheckBoxLoc.PART6_THIRD_PARTY_CHECKBOX, "No", 2)

        # PART 5 - Sign
        self.setField(MetaDataLoc.PART7_LOC, [self.sign.split(", ")])
        
        # PART 5 - Paid Preparer
        if Preparer.PREPARER_INFO:
            pnum, offset = MetaDataLoc.PART7_LOC
            self.setCheckBox(CheckBoxLoc.PART7_PAID_PREPARER_CHECKBOX, 1, 1)
            self.setField([pnum, offset + 3], Preparer.PREPARER_INFO)