####################################################################################


# Author: Yidan Zhang
# Function: Find all the file in the current path. And extract special pre
# Notification:
# 1. Used in Python3 Enviroment, Havn't tried in Python2


#####################################################################################

import nltk
import string
import os
import re 
from os import listdir
from os.path import isfile, join


class FilenameFinder:
    # Used for finding the pdf name in the path
    
    def __init__(self, file_path='.'):
        "Initial Function, file_path is set for finding the filename, default set to '.', which means the current path"
        self.file_path = file_path

    def getFileName(self):
        "Get all the file name in the path"
        os.system('cd '+self.file_path)
        # Entering the path offered
        onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
        return onlyfiles

    def getSpecialSuffix(self, suffix):
        "Extract the special suffix file name from the files found in getFileName()"
        pdfFileName = []
        # Using a list for saving the pdf file name

        for file in self.getFileName():
            if re.match('.+\\'+suffix+'$', file):
            # Match the file end with .pdf
                pdfName = file[:-4]
                pdfFileName.append(pdfName) 
        # Will return the name without the suffix
        return pdfFileName


    def getAllPDFName(self):
        "Extract the pdf name from the files found in getFileName()"
        return self.getSpecialSuffix('.pdf')

    
    def getAllTXTName(self):
        "Extract the txt name from the files found in getFileName()"
        return self.getSpecialSuffix('.txt')
