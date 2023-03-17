import os, shutil
import concurrent.futures
import time
import numpy as np
import pandas as pd
from constantsFormW2 import Input, W2
from form import Form
from PyPDF2 import PdfFileWriter, PdfFileReader
from itertools import repeat
from multiprocessing import Pool
from PyPDF2 import PdfReader, PdfWriter

class FormW2(Form):
    def __init__(self, fname):  
        # read employer sheet
        self.employer_payload = pd.read_excel(f'{fname}', sheet_name=Input.EMPLOYER_SHEET, dtype=str).fillna('').to_numpy()

        # read employee sheet
        self.employee_payload = pd.read_excel(f'{fname}', sheet_name=Input.EMPLOYEE_SHEET, dtype=str).fillna('').to_numpy()

        # get employer
        self.employer_name, self.employer_field_dictionary = self.getEmployer()

    def fieldFormat(self, formId, fieldCode, offsetX=0, offsetY=0):
        return f'w2[{formId}]_f[{fieldCode}][{offsetX}][{offsetY}]'

    def setFormField(self, field_dictionary, fieldCode, offsetX, offsetY, fieldVal):
        # gen key and set key, value pair for w2 field
        w2b_key = self.fieldFormat('b', fieldCode, offsetX, offsetY)
        w2c_key = self.fieldFormat('c', fieldCode, offsetX, offsetY)
        field_dictionary[w2b_key] = field_dictionary[w2c_key] = fieldVal

    def getEmployer(self):
        # employer field id & value
        employer_boxID = self.employer_payload[0]
        employer = self.employer_payload[1:].flatten()

        # store employer field info to dictionary
        employer_field_dictionary = dict()
        for i in range(len(employer_boxID)):
            self.setFormField(employer_field_dictionary, employer_boxID[i], 0, 0, employer[i])
        
        # get employer name
        cIdx, rIdx = W2.EMPLOYER_INFO_META
        employer_name = employer[cIdx].splitlines()[rIdx]

        return employer_name, employer_field_dictionary
    
    def assert_box1_7(self, employee_name, field_dictionary):
        # get box1 to box7 values
        box1_7 = [field_dictionary[self.fieldFormat('b', i)] for i in range(1, 8)]
        box1_7 = [0 if val == '' else float(val) for val in box1_7]
        earning, fed_w, ss_wage, ss_tax, med_wage, med_tax, ss_tip = box1_7

        # test amount & cap
        assert fed_w <= earning, f'Error!!! {self.employer_name} - {employee_name}: Federal tax withholding is greater earning'
        assert ss_wage + ss_tip <= W2.SS_MAX_22, f'Error!!! {self.employer_name} - {employee_name}: Social wages + tip cant be greater than {W2.SS_MAX_22}'
        assert med_wage >= ss_wage, f'Error!!! {self.employer_name} - {employee_name}: Medicare wages cant be smaller than Social security wages'

        # test tax relations & calculations accuracy
        assert ss_wage + ss_tip > ss_tax and abs((ss_wage + ss_tip) * W2.SS_RATE_22 - ss_tax) < W2.EPSILON, f'Error!!! {self.employer_name} - {employee_name}: Social security tax is incorrect'
        assert med_wage + ss_tip > med_tax and abs((med_wage + ss_tip) * W2.MC_RATE_22 - med_tax) < W2.EPSILON, f'Error!!! {self.employer_name} - {employee_name}: Medicare tax is incorrect'

    def getEmployee(self, employee):
        # emmployee field id
        employee_boxID = self.employee_payload[0]

        # store employee field info to dictionary
        employee_field_dictionary = self.employer_field_dictionary.copy()
        for i in range(len(employee_boxID)):
            # read lines
            rows = [employee[i]] if i < W2.MULTIPLE_ENTRY_COL_START else employee[i].splitlines()
            
            for j in range(len(rows)):
                # read & store key, value pair to dictionary
                cols = rows[j].split(':')
                for k in range(len(cols)):
                    self.setFormField(employee_field_dictionary, employee_boxID[i], j, k, cols[k])
        
        # assert box1 to 7 values of employee w2
        cIdx, rIdx = W2.EMPLOYEE_INFO_META
        employee_name = employee[cIdx].splitlines()[rIdx]
        self.assert_box1_7(employee_name, employee_field_dictionary)

        return employee_name, employee_field_dictionary
      
    def parallelWrite(self, w2_payload):
        # store info to page writer
        employer, employee_name, field_dictionary, writer = w2_payload

        # write to files
        writer.update_page_form_field_values(writer.pages[0], field_dictionary)
        outputStream = open(f'{Input.W2_OUT}/{employer}/{employee_name} - w2.pdf', 'wb')
        writer.write(outputStream)
        outputStream.close()

    def buildW2(self):        
        # create output entity directory
        buildPath(f'{Input.W2_OUT}/{self.employer_name}')

        # build w2 field dictionary
        employee_list = self.employee_payload[1:]
        w2_payload = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                # build w2 payload
                for employee_name, employee_w2 in executor.map(self.getEmployee, employee_list):      
                    # create reader & writer for each business entity
                    reader = PdfReader(Input.FORM)  
                    writer = PdfWriter()
                    writer.clone_document_from_reader(reader)
                    
                    # store info to w2 payload array
                    w2_payload.append([self.employer_name, employee_name, employee_w2, writer])

                # gen w2 files
                executor.map(self.parallelWrite, w2_payload)
            except Exception as e:
                print(str(e))

        return f'Done generating {self.employer_name}s W2s!!!'

def buildPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def gen():
    buildPath(Input.W2_IN)
    buildPath(Input.W2_OUT)

    tasks = []
    for file in os.listdir(Input.W2_IN):
        if not file.startswith('.'):
            tasks.append(FormW2(f'{Input.W2_IN}/{file}'))
    
    # create w2
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        try:  
            for res in executor.map(FormW2.buildW2, tasks): 
                print(res)
        except Exception as e:
            print(str(e))  

if __name__ == "__main__":
    start = time.time()
    gen()
    end = time.time()
    print(end - start)
   
   

