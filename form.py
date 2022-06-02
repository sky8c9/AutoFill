from abc import abstractclassmethod
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject
from pytz import timezone
from datetime import datetime

class Form():
    report_folder_name = datetime.now(timezone('US/Pacific')).strftime("%m-%d-%y_%H_%M_%S")

    def __init__(self, form):
        self.pdf_reader = PdfFileReader(open(form, "rb"))
        self.pdf_writer = PdfFileWriter()

        for page in self.pdf_reader.pages:
            self.pdf_writer.addPage(page)

    @abstractclassmethod
    def fill(self):
        pass

    def output(self, form, entity):
        outputStream = open(f"{Form.report_folder_name}/{entity} - {form}.pdf", "wb")
        self.pdf_writer.write(outputStream)
        outputStream.close()
        print(f"{entity} Done!!!")

    def reportVal(self, val):
        return str(format(float(val), ".2f")).split(".")

    def setField(self, loc, dataBlock, adjustment=0):
        pNum, offset = loc
        field_dictionary = dict()
        
        for field in dataBlock:
            for element in field:
                field_dictionary[f"f{pNum}_{offset}[0]"] = element
                offset += 1

        self.pdf_writer.updatePageFormFieldValues(self.pdf_writer.getPage(pNum - 1 + adjustment), field_dictionary)

    def setCheckBox(self, loc, choice, num_choices, adjustment=0):
        pNum, offset = loc
        field_dict = dict()

        for i in range(num_choices):
            field_dict[f"c{pNum}_{offset}[{i}]"] = f"/{choice}"

        page = self.pdf_reader.getPage(pNum - 1 + adjustment)
        for i in range(0, len(page["/Annots"])):
            writer_annot = page["/Annots"][i].getObject()

            for field in field_dict:
                if writer_annot.get("/T") == field:
                    writer_annot.update({
                        NameObject("/V"): NameObject(field_dict[field])
                    })

    def viewFormMapping(self):
        formfields = self.pdf_reader.getFields()
        for field in formfields:
            if "/V" in formfields[field] :
                print(formfields[field]["/T"], formfields[field]["/V"])
            else:
                print(formfields[field]["/T"], "NULL")
