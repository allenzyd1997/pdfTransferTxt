# Author: Yidan Zhang
# Function: Transfering all the PDF File in a path To the Text File.
# Notification:
# 1. Used in Python3 Enviroment, Havn't tried in Python2
# 2. Used in Linux or OSX, If you want to use in Windows, Changed the getFileName() in FilenameFinder. 
#    It should use Windows command to enter the path and get the list result.






import os
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class FilenameFinder:
    # Used for finding the pdf name in the path
    
    def __init__(self, file_path='.'):
        "Initial Function, file_path is set for finding the filename, default set to '.', which means the current path"
        self.file_path = file_path

    def getFileName(self):
        "Get all the file name in the path"
        os.system('cd '+self.file_path)
        # Entering the path offered
        str = os.popen("ls").read()
        # Execute the ls in command and read the result
        files = str.split("\n")
        # Seperate the result by '\n'
        return files

    def getPDFName(self):
        "Extract the pdf name from the files found in getFileName()"

        pdfFileName = []
        # Using a list for saving the pdf file name

        for file in self.getFileName():
            if re.match('.+\.pdf$', file):
            # Match the file end with .pdf
                pdfName = file[:-4]
                pdfFileName.append(pdfName) 

        return pdfFileName



class PdfConverter:

   def __init__(self, pdfName):
       self.pdfName = pdfName
# convert pdf file to a string which has space among words 

   def convert_pdf_to_txt(self):
       rsrcmgr = PDFResourceManager()
       retstr = StringIO()
       codec = 'utf-8'  # 'utf16','utf-8'
       laparams = LAParams()
       device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
       fp = open(self.pdfName, 'rb')
       interpreter = PDFPageInterpreter(rsrcmgr, device)
       password = ""
       maxpages = 0
       caching = True
       pagenos = set()
       for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
           interpreter.process_page(page)
       fp.close()
       device.close()
       str = retstr.getvalue()
       retstr.close()
       return str
# convert pdf file text to string and save as a text_pdf.txt file
   
   def save_convert_pdf_to_txt(self):
       content = self.convert_pdf_to_txt()
       txt_pdf = open(pdfName+'.txt', 'wb')
       txt_pdf.write(content.encode('utf-8'))
       txt_pdf.close()

if __name__ == '__main__':
      ff = FilenameFinder()
      print(ff.getPDFName())
      for pdfName in ff.getPDFName():
          print(pdfName)
          print("***")
          PdfConverter(pdfName = pdfName+'.pdf').save_convert_pdf_to_txt()





