from ast import literal_eval
from constantsForm941sb import Input, MetaDataLoc, DepositInfo, CheckBoxLoc
from form import Form
from datetime import date

class Form941sb(Form):
    def __init__(self, data):
        super().__init__(Input.FORM)
        self.quarter, self.ein, self.trade_name, self.legal_name, self.deposit_info = data
        self.schedB_total_deposit = 0

    def fill(self):
        print(f"{self.trade_name} - 941sb ...")
        self.fillMeta()
        self.taxFill()
        self.output(Input.FORM, self.trade_name + "_schedB")

    def fieldFormat(self, pNum, offset):
        return f"f{pNum}_{str(offset).zfill(3)}_0_[0]"

    def checkBoxFormat(self, pNum, offset, index):
        return f"c{pNum}_{offset}_0_[{index}]"

    def taxFill(self): 
        deposit_loc = DepositInfo.FIRST_DEPOSIT_LOC
        for deposit in self.deposit_info:
            deposit_dict = literal_eval(deposit)
            total = 0
            index = 0
            # Update deposit on a given month
            for deposit_date, deposit_value in deposit_dict.items():
                total += deposit_value

                # Deposit 1 fields have different naming convention compared to the rest
                if index == 0:
                    self.setField2([1, deposit_loc + 2 * (deposit_date - 1)], [self.reportVal(deposit_value)])
                else: self.setField([1, deposit_loc + 2 * (deposit_date - 1)], [self.reportVal(deposit_value)])

            # Update total deposit for a given month and move to next
            self.setField([1, deposit_loc + DepositInfo.GAP_TO_TOTAL], [self.reportVal(total)])
            self.schedB_total_deposit += total
            deposit_loc += DepositInfo.GAP_TO_TOTAL + 2
            index+=1

        self.setField([1, deposit_loc], [self.reportVal(self.schedB_total_deposit)])

    def fillMeta(self):        
        # Fill entity data
        ein1, ein2 = self.ein.split("-")
        self.setField(MetaDataLoc.EIN_LOC, [list(ein1), list(ein2), [self.legal_name], list(str(date.today().year))])
        self.setCheckBox(CheckBoxLoc.TAX_QUARTER_CHECKBOX, f"Report{self.quarter}", 4)

    # Redundant function to due with inconsistent field names in the original pdf form
    def setField2(self, loc, dataBlock): 
        pNum, offset = loc
        field_dictionary = dict()
        
        for field in dataBlock:
            for element in field:
                key = f"f{pNum}_{offset}_0_[0]"
                field_dictionary[key] = element
                offset += 1

        self.pdf_writer.update_page_form_field_values(self.pdf_reader.getPage(pNum - 1), field_dictionary)

       

