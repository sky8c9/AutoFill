import os
import concurrent.futures
from form941 import Form941
from form941x import Form941x
from form940 import Form940
from form import Form
from constantsForm941 import Input as Input941
from constantsForm940 import Input as Input940
from constantsForm941x import Input as Input941x
import pandas as pd

def menu():
    print("-----------------------------")
    print("1: View Template Data")
    print("2: View Form Mapping")
    print("3: AutoFill")
    print("-----------------------------")

def task():
    dict = {"941" : Input941.SHEET, "941x" : Input941x.SHEET, "940" : Input940.SHEET}
    form = input("Enter form: ")

    df = pd.read_excel(dict[form], dtype=str)
    if df.empty:
        print("Empty Data File !!!")
        return

    tasks = []
    for index, rowData in df.iterrows():
        if form == "941":
            tasks.append(Form941(rowData))
        elif form == "940":
            tasks.append(Form940(rowData))
        elif form == "941x":
            tasks.append(Form941x(rowData))

    menu()
    option = int(input("Select: "))
    if (option == 3):
        os.makedirs(Form.report_folder_name)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for idx, task in enumerate(tasks):
                executor.submit(task.fill)
    elif (option == 2):
        tasks[0].viewFormMapping()  
    elif (option == 1):
        print(df)

def main():
    task()

if __name__ == "__main__":
	main()