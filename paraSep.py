###########################################################################


# Author: Yidan Zhang
# Function: Transfer the pdf file to txt file. and sepearte the txt.
# Notification:
# Used in Python3 Enviroment, Havn't tried in Python2




###########################################################################



import os
import re

from FilenameFinder import FilenameFinder


from nltk.tokenize import RegexpTokenizer
from string import digits
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def remove_punc_num(line):
  tokenizer = RegexpTokenizer(r'\w+')
  result = ""
  for i in tokenizer.tokenize(re.sub(r'\d+', '', line)):
    result += i 
    result += " "
  return result


def notrecord1(line):
  return True if ("..." in line) else False

def notrecord2(line):
  # print("length", len(line))
  return True if len(line) < 8 else False

def condition1(line):
  # print("length", len(line))
  return True if len(line) > 40 else False

NOTRECORD  = [notrecord1, notrecord2]  # THAT WE DONOT WANT TO RECORD THIS INFORMATION

CONDITIONS = [condition1]

def word_modify(file):
  # For some words in the transferring txt file will have some errors. 
  # We modify this transferrring error word here 

  # The first case is that there will have a lot "+" in front of some words
  fileLines = [] # Save the line in the memory, after modifying, write it back
  with open(file, "r") as fr:
    for line in fr.readlines():
      if "+" in line:
        line.replace("+",' ')

  with open(file, "w") as fw:
    for line in fileLines:
      fw.write(line)







class PdfConverter:

  def __init__(self, pdfName, path = './'):
    # pdfName for the pdf that you want to transfer
    # path is the purpose pdffile path. default set to current path

    self.path    = path
    self.pdfName = self.path + pdfName

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

  def createNewFile(self, line, conditions = CONDITIONS):
    result = True
    for condition in conditions:
      result = result & condition(line)
      # print(condition, condition(line))
    return result

  def notrecord(self, line, notrecord = NOTRECORD):
    result = False 
    for notrecord in NOTRECORD:
      result  = result | notrecord(line)
    return result

  def convertTOpara(self):
      pdfName = self.pdfName[:-4]
      with open(pdfName+".txt", "r", encoding="utf8") as f:
        counter, writeFile, returnLine, canReturn = 0, 0, 0, 1# Calculate the number of the txt that we sepereate
        # returnLine decide how many "\n" has calculated. For deside whether create a new file or not
        # canReturn is used for the function createNewFile() which decide whether need create a new file based on the current sentece
        # Eg: I donnot need to create a new file for "123..." Just write it into the fromer file
        for line in f.readlines():
          
          if line == "\n" and returnLine == 0 and canReturn == 0:
              returnLine = returnLine + 1
              writeFile = 0
              continue
          
          elif line == "\n" and returnLine == 1:
            # IF the "\n" occured together, that means the readline will only get "\n" In this line

              if writeFile == 1 and canReturn == 0:
                fr.close()
                writeFile = 0 # Set the write file status back to 0 means we do not have file write para now.
              else:
                continue
              
          else:
            returnLine = 0
            if not self.createNewFile(line):
                canReturn = 1 
            else:
                canReturn = 0
            if self.notrecord(line):
              continue
            else:

              if writeFile == 0:
                counter += 1 # Update the file sequence
                fr = open(pdfName+str(counter)+".txt", "w", encoding="utf8") # Create File 
                writeFile = 1
              fr.write(remove_punc_num(line)) # We can modify the txt here. for recovering the translating error.

      fr.close()


if __name__ == '__main__':
      ff = FilenameFinder()
      print(ff.getAllPDFName())
      for pdfName in ff.getAllPDFName():
          print(pdfName)
          print("********************************************************************************")
          convert = PdfConverter(pdfName = pdfName+'.pdf')
          convert.save_convert_pdf_to_txt()
          convert.convertTOpara()
          print("FINISH Transfer")







