# python

import re
import sys
import io
import json
import shutil
import os
import string

# @dulikai
# @ qibebt
# @ 2014.11.14
# $ du
# 
#

class FileMan:

    @staticmethod
    def pygrep(filename, mystr):
        mygrp = []
        for line in open(f).readlines():
            if re.match(mystr, line):
                mygrp.append(line)
            else:
                mygrp = None
        return mygrp

    @staticmethod    
    def pure_mkdir(mydir):
        """
        make a new directory structure
        """
        # make directory
        # @ Check & Remove the old working directory 
        if os.path.exists(mydir):
          shutil.rmtree(mydir)          
        # Create the new HOME working directory 
        else os.path.exists(mydir):
            os.makedirs(mydir)
        return
        
        