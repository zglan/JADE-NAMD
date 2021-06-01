#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil
import cre_tur_input_tool
from cre_tur_input_tool import *
import cre_tur_overlap_tool
from cre_tur_overlap_tool import *
import read_tur_overlap_tool
from read_tur_overlap_tool import *





#  ---------------------------------------------------------------------
#  Calculate the AO overlap between R and R+dr
#-----------------------------------------------------------------------------------------   



def tur_double_mole () :


    n_atom = 0
    index_state = 0 
    n_state = 0 
    n_all = read_coord ()
    n_atom = int(n_all[0])


#   Create the working directory for Turbomole
    dir="./QC_TMP/OVERLAP"
    if os.path.exists(dir):
	shutil.rmtree(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)


#   Copy all input files

    sourceFile = 'QC_TMP/TUR_TMP/coord'
    destFile =   'QC_TMP/OVERLAP/coord1'
    shutil.copy2(sourceFile, destFile)

    sourceFile = 'QC_TMP/TUR_TMP_PREV/coord'
    destFile =   'QC_TMP/OVERLAP/coord2'
    shutil.copy2(sourceFile, destFile)


    sourcePath = 'TUR_EXAM'
    destPath =   'QC_TMP/OVERLAP'
    sourcePath_files = os.listdir(sourcePath)
    for file_name in sourcePath_files:
        full_file_name = os.path.join(sourcePath, file_name)
        if (os.path.isfile(full_file_name)):
           shutil.copy(full_file_name, destPath)



    
#   Enter the Turbomole working directory
    os.chdir("./QC_TMP/OVERLAP")

#   Create the falk coordinates for double molecules
    creat_falk_coord(n_atom)
   


#   Modify the control file
    n_basis_double=create_falk_control (n_atom)



#  Create the falk mos file
    create_falk_mos(n_basis_double) 


#   Run Turbomole Work
    os.system("dscf > dscf.out" )

#    sys.exit()

#   Read AO overlap
    read_ao_overlap ()

#   Go back to directory of dynamics work
    os.chdir("../../")

if __name__ == "__main__":
    tur_double_mole ()




