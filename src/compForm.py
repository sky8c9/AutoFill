import os
import concurrent.futures
import time
import numpy as np
import pandas as pd
from constantsCompForm import Constants
from abc import abstractclassmethod
from multiprocessing import Pool
from PyPDF2 import PdfReader, PdfWriter

class CompForm():
    def __init__(self, fname, cls_consts):
        # class constants
        self.cls_consts = cls_consts

        # read payer sheet
        self.payer_payload = pd.read_excel(f'{fname}', sheet_name=self.cls_consts.PAYER_SHEET, dtype=str).fillna('').to_numpy()

        # read payee sheet
        self.payee_payload = pd.read_excel(f'{fname}', sheet_name=self.cls_consts.PAYEE_SHEET, dtype=str).fillna('').to_numpy()

        # get payer
        self.payer_name, self.payer_field_dictionary = self.getPayer()

    @abstractclassmethod
    def assertPayeeFieldVal(self, payee_name, payee_field_dictionary):
        pass

    def fieldFormat(self, form_id, field_code, offsetX=0, offsetY=0):
        return f'{self.cls_consts.FORM_NAME}[{form_id}]_f[{field_code}][{offsetX}][{offsetY}]'

    def setFormField(self, field_dictionary, field_code, offsetX, offsetY, field_val):
        # gen key and set key, value pair for field
        form_b_key = self.fieldFormat('b', field_code, offsetX, offsetY)
        form_c_key = self.fieldFormat('c', field_code, offsetX, offsetY)
        field_dictionary[form_b_key] = field_dictionary[form_c_key] = field_val

    def getPayer(self):
        # payer field id & value
        payer_boxID = self.payer_payload[0]
        payer = self.payer_payload[1:].flatten()

        # store payer field info to dictionary
        payer_field_dictionary = dict()
        for i in range(len(payer_boxID)):
            self.setFormField(payer_field_dictionary, payer_boxID[i], 0, 0, payer[i])
        
        # get payer name
        cIdx, rIdx = self.cls_consts.NAME_LOC
        payer_name = payer[cIdx].splitlines()[rIdx]

        return payer_name, payer_field_dictionary
    
    def getPayee(self, payee):        
        # Payee field id
        payee_boxID = self.payee_payload[0]

        # store payee field info to dictionary
        payee_field_dictionary = self.payer_field_dictionary.copy()
        for i in range(len(payee_boxID)):
            # read lines
            rows = [payee[i]] if i < self.cls_consts.MULTIPLE_ENTRY_COL_START else payee[i].splitlines()
            
            for j in range(len(rows)):
                # read & store key, value pair to dictionary
                cols = rows[j].split(':')
                for k in range(len(cols)):
                    self.setFormField(payee_field_dictionary, payee_boxID[i], j, k, cols[k])
        
        # Retrieve payee name & assert payee field dictionary
        cIdx, rIdx = self.cls_consts.NAME_LOC
        payee_name = payee[cIdx].splitlines()[rIdx]
        self.assertPayeeFieldVal(payee_name, payee_field_dictionary)

        return payee_name, payee_field_dictionary
      
    def parallelWrite(self, payload):
        # store info to page writer
        payer, payee_name, field_dictionary, writer = payload

        # write to files
        writer.update_page_form_field_values(writer.pages[0], field_dictionary)
        outputStream = open(f'{self.cls_consts.OUT}/{payer}/{payee_name} - {self.cls_consts.FORM_NAME}.pdf', 'wb')
        writer.write(outputStream)
        outputStream.close()

    def build(self):        
        # create output entity directory
        buildPath(f'{self.cls_consts.OUT}/{self.payer_name}')

        # build form field dictionary
        payee_list = self.payee_payload[1:]
        payload = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                # build payload
                for payee_name, field_dictionary in executor.map(self.getPayee, payee_list):      
                    # create reader & writer for each business entity
                    reader = PdfReader(self.cls_consts.FORM)  
                    writer = PdfWriter()
                    writer.clone_document_from_reader(reader)
                    
                    # store info to payload
                    payload.append([self.payer_name, payee_name, field_dictionary, writer])

                # gen files
                executor.map(self.parallelWrite, payload)
            except Exception as e:
                print(str(e))

        return f'Done generating {self.payer_name}s {self.cls_consts.FORM_NAME}s!!!'

class FormW2(CompForm):
    def assertPayeeFieldVal(self, payee_name, payee_field_dictionary):
        # get box1 to box7 values
        box1_7 = [payee_field_dictionary[self.fieldFormat('b', i)] for i in range(1, 8)]
        box1_7 = [0 if val == '' else float(val) for val in box1_7]
        earning, fed_w, ss_wage, ss_tax, med_wage, med_tax, ss_tip = box1_7

        # test amount & cap
        assert fed_w <= earning, f'Error!!! {self.payer_name} - {payee_name}: Federal tax withholding is greater earning'
        assert ss_wage + ss_tip <= self.cls_consts.SS_MAX_22, f'Error!!! {self.payer_name} - {payee_name}: Social wages + tip cant be greater than {self.cls_consts.SS_MAX_22}'
        assert med_wage >= ss_wage, f'Error!!! {self.payer_name} - {payee_name}: Medicare wages cant be smaller than Social security wages'

        # test tax relations & calculations accuracy
        assert ss_wage + ss_tip > ss_tax and abs((ss_wage + ss_tip) * self.cls_consts.SS_RATE_22 - ss_tax) < self.cls_consts.EPSILON, f'Error!!! {self.payer_name} - {payee_name}: Social security tax is incorrect'
        assert med_wage > med_tax and abs(med_wage * self.cls_consts.MC_RATE_22 - med_tax) < self.cls_consts.EPSILON, f'Error!!! {self.payer_name} - {payee_name}: Medicare tax is incorrect'

class Form1099NEC(CompForm):
    pass

def buildPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ioTask(): 
    # menu
    form_list = []
    print('-----------------------------')
    for idx, cls in enumerate(Constants.__subclasses__()):
        print(f'{idx}: Create {cls.FORM_NAME}s')
        form_list.append(cls)
    print('-----------------------------')
    choice = int(input("Select: "))

    # build io path
    form = form_list[choice]
    form_cls = globals()[form.FORM_CLASS]
    buildPath(form.IN)
    buildPath(form.OUT)

    # create task
    tasks = []
    for file in os.listdir(form.IN):
        if not file.startswith('.'):
            tasks.append(form_cls(f'{form.IN}/{file}', form))   
    return tasks

def gen():
    # create w2
    tasks = ioTask()
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        try:  
            for res in executor.map(CompForm.build, tasks): 
                print(res)
        except Exception as e:
            print(str(e))  

if __name__ == "__main__":
    start = time.time()
    gen()
    end = time.time()
    print(end - start)
   
   

