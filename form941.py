from constantsForm941 import Input, Tax, ThirdParty, Preparer, MetaDataLoc, LineLoc, CheckBoxLoc
from form import Form
from form941sb import Form941sb

class Form941(Form):
    def __init__(self, data):
        super().__init__(Input.FORM)

        # Entity metadata
        self.quarter, self.scheduleB, self.ein, self.legal_name, self.trade_name, self.address, self.sign, self.employee_count = data.iloc[0:Tax.TAX_INFO_COLUMN_START].fillna("").astype(str)

        # Tax info
        self.tax_info = data.iloc[Tax.TAX_INFO_COLUMN_START:-3].fillna(0).astype(float)

        # Deposit info
        self.deposit_info = data.iloc[-3:]

    def fill(self):
        print(f"{self.trade_name} - 941 ...")
        self.fillMeta()
        self.taxFill()
        self.output(Input.FORM, self.trade_name)

    def fieldFormat(self, pNum, offset):
        return f"f{pNum}_{offset}[0]"

    def checkBoxFormat(self, pNum, offset, index):
        return f"c{pNum}_{offset}[{index}]"

    def part2(self, total_tax, total_deposit):
        if self.scheduleB == 'y' or self.scheduleB == 'Y':
            self.setCheckBox(CheckBoxLoc.PART2_CHECKBOX, 3, 3)      
        elif total_tax < 2500 and total_deposit == 0:
            self.setCheckBox(CheckBoxLoc.PART2_CHECKBOX, 1, 3)
        elif total_deposit > 0:
            part2 = [self.reportVal(self.deposit_info["Deposit_1"]), self.reportVal(self.deposit_info["Deposit_2"]), self.reportVal(self.deposit_info["Deposit_3"]), self.reportVal(total_deposit)]
            self.setField(MetaDataLoc.PART2_LOC, part2)
            self.setCheckBox(CheckBoxLoc.PART2_CHECKBOX, 2, 3)

    def taxFill(self): 
        if (self.scheduleB == 'y' or self.scheduleB == 'Y'):
            form941sb = Form941sb([self.quarter, self.ein, self.trade_name, self.legal_name, self.deposit_info])
            form941sb.fill()
            total_deposit = form941sb.schedB_total_deposit
        else:
            self.deposit_info = self.deposit_info.fillna(0).astype(float)
            total_deposit = self.deposit_info["Deposit_1"] + self.deposit_info["Deposit_2"] + self.deposit_info["Deposit_3"]
        
        # Line 6
        total_tax = self.totalTax()
        self.setField(LineLoc.LINE6, [self.reportVal(total_tax)])

        # Line 10
        self.setField(LineLoc.LINE10, [self.reportVal(total_tax)])

        # Line 12 & 13a
        self.setField(LineLoc.LINE12, [self.reportVal(total_tax), self.reportVal(total_deposit)])

        # Line 13g
        self.setField(LineLoc.LINE13G, [self.reportVal(total_deposit)])

        # Balance due
        self.balanceDue(total_tax - total_deposit)

        # Part 2
        self.part2(total_tax, total_deposit)

    def totalTax(self):
        wages = self.tax_info["Wages"]
        tips = self.tax_info["Tips"]
        fedW = self.tax_info["Federal Withholding"]

        # Select quarter
        self.setCheckBox(CheckBoxLoc.TAX_QUARTER_CHECKBOX, self.quarter, 4)

        # Tax Info
        self.setField(LineLoc.LINE1, [[self.employee_count], self.reportVal(wages + tips), self.reportVal(fedW)])

        # Social security tax on wages
        wages_ss_tax = wages * Tax.SS_TAX_RATE

        # Social security tax on tips
        tips_ss_tax = tips * Tax.SS_TAX_RATE

        # Medicare tax on tips + wages
        wages_and_tips_med = (wages + tips) * Tax.MED_TAX_RATE

        # Line 5a
        self.setField(LineLoc.LINE5A, [self.reportVal(wages), self.reportVal(wages_ss_tax)])

        # Line 5b & 5c
        self.setField(LineLoc.LINE5B, [self.reportVal(tips), self.reportVal(tips_ss_tax), self.reportVal(wages + tips), self.reportVal(wages_and_tips_med)])

        # Line 5e
        ss_med_tax = wages_ss_tax + tips_ss_tax + wages_and_tips_med
        self.setField(LineLoc.LINE5E, [self.reportVal(ss_med_tax)])

        return ss_med_tax + fedW

    def balanceDue(self, tax_balance):
        tax_balance = 0 if abs(tax_balance) < 0.1 else tax_balance
        address_elements = self.address.split(", ")
        street = address_elements[0]
        other = ", ".join(address_elements[1:])

        if tax_balance > 0: # Create payment voucher
            self.setField(LineLoc.LINE14, [self.reportVal(tax_balance)])

            # adjustment needed when field index doesnt line up with its page number
            self.setField(MetaDataLoc.VOUCHER_LOC, [[self.ein], self.reportVal(tax_balance), [self.legal_name], [street], [other]], 1)
            self.setCheckBox(CheckBoxLoc.PAYMENT_VOUCHER_CHECKBOX, self.quarter, 4, 1)
        elif tax_balance < 0: # Over payment - Send a refund as default option
            self.setField(LineLoc.LINE15, [self.reportVal(abs(tax_balance))])
            self.setCheckBox(CheckBoxLoc.OVERPAYMENT_CHECKBOX, 2, 2)

    def fillMeta(self):        
        # Company - Meta data may span over multiple pages (set mutiplePages flag to true)
        self.setField(MetaDataLoc.COMPANY_LOC, [self.ein.split("-"), [self.legal_name], [self.trade_name], self.address.split(", ")], multiplePages=True)

        # PART 4 - 3rd party designee contact
        if ThirdParty.THIRD_PARTY_DESIGNEE:
            self.setCheckBox(CheckBoxLoc.PART4_THIRD_PARTY_CHECKBOX, 1, 2)
            self.setField(MetaDataLoc.PART4_LOC, ThirdParty.THIRD_PARTY_DESIGNEE)
        else:
            self.setCheckBox(CheckBoxLoc.PART4_THIRD_PARTY_CHECKBOX, 2, 2)

        # PART 5 - Sign
        self.setField(MetaDataLoc.PART5_LOC, [self.sign.split(", ")])

        # PART 5 - Paid Preparer
        if Preparer.PREPARER_INFO:
            pnum, offset = MetaDataLoc.PART5_LOC
            self.setCheckBox(CheckBoxLoc.PART5_PAID_PREPARER_CHECKBOX, 1, 1)
            self.setField([pnum, offset + 3], Preparer.PREPARER_INFO)


