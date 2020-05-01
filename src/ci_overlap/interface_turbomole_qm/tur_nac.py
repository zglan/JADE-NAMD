#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil
import tur_nac_tool
from tur_nac_tool import *





#  ---------------------------------------------------------------------
#  Calculate the AO overlap between R and R+dr
#-----------------------------------------------------------------------------------------   



def tur_nac () :


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#   Compute NAC
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#   Create the working directory for NAC

    dir="./QC_TMP/NAC"
    if os.path.exists(dir):
	shutil.rmtree(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

   
    sourceFile = './QC_TMP/TUR_TMP_PREV/mo.dat'
    destFile =   './QC_TMP/NAC/mo_1.dat'
    shutil.copy2(sourceFile, destFile)
 
    sourceFile = './QC_TMP/TUR_TMP_PREV/ci.dat'
    destFile =   './QC_TMP/NAC/ci_1.dat'
    shutil.copy2(sourceFile, destFile)
 
 
    sourceFile = './QC_TMP/TUR_TMP/mo.dat'
    destFile =   './QC_TMP/NAC/mo_2.dat'
    shutil.copy2(sourceFile, destFile)

    sourceFile = './QC_TMP/TUR_TMP/ci.dat'
    destFile =   './QC_TMP/NAC/ci_2.dat'
    shutil.copy2(sourceFile, destFile)

    sourceFile = './QC_TMP/TUR_TMP/qm_results.dat'
    destFile =   './QC_TMP/NAC/qm_results.dat'
    shutil.copy2(sourceFile, destFile)

    sourceFile = './QC_TMP/OVERLAP/ao_overlap.dat'
    destFile =   './QC_TMP/NAC/ao_overlap.dat'
    shutil.copy2(sourceFile, destFile)
    

    os.chdir(dir)

    create_nac_input()

    run_nac()
    read_nac () 
    

#   Go back to directory of dynamics work
    os.chdir("../../")

    

if __name__ == "__main__":
    tur_nac ()




