#! /usr/bin/python

import shutil
import os

from bagel_create import *
from bagel_parser import *
sys.path.append("../tools/")
import tools


class bagel_run:
    def __init__(self, config={}):
        """
        common data block, cannot be inherted by subclass automatically
        """
        self.config = config

        root_dir = self.config['root']
        dirs = self.config['dirs']
        files = self.config['files']

        # working directory & files >>>
        self.directory = {}
        self.directory['root'] = root_dir
        self.directory['template'] = root_dir + "/" + dirs['template']
        self.directory['home'] = root_dir + "/" + dirs['home']
        self.directory[
            'work'] = self.directory['home'] + "/" + dirs['work']
        self.files = {}
        self.files["template"] = files['template']
        self.files["interface"] = files['interface']
        self.files["bagel_wfu"] = files['bagel_wfu']
        self.files["bagel_input"] = files['bagel_input']
        self.files["bagel_log"] = files['bagel_log']

        # run the job directly
        self.qm_interface = tools.load_data(self.files["interface"])

        self.i_step = self.qm_interface['parm']['i_time']

        self.worker()


        return

    def initilize(self):
        """
        check interface & determine the implimented module to be called.
        """
        # make directory
        # @ Check & Remove the old working directory for QC calc.
        home_dir = self.directory['home']

        if not os.path.exists(home_dir):
            os.makedirs(home_dir)

        # working directory: such as BAGEL_TMP.
        destPath = self.directory['work']
        tempPath = self.directory['template']

        wfufile_temp = tempPath + '/' + self.files['bagel_wfu']
        wfufile_dyn = home_dir + '/' + self.files['bagel_wfu']

        if os.path.exists(destPath):
            shutil.rmtree(destPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
            wfu_dir = destPath

            if self.i_step == 0:

               if os.path.isfile(wfufile_temp):
                   shutil.copy2(wfufile_temp, wfu_dir)
               else:
                   print "No wavefuncton file, exit!"
                   exit(1)

            if self.i_step > 0:

               if os.path.isfile(wfufile_dyn):
                   shutil.copy2(wfufile_dyn, wfu_dir)

               else:
                   print "No wavefuncton file, exit!"
                   exit(1)

                # copy template & interface
        sourceFile = self.files['template']
        shutil.copy2(sourceFile, destPath)

        sourceFile = self.files['interface']
        if os.path.isfile(sourceFile):
            shutil.copy2(sourceFile, destPath)
        else:
            print 'Check the interface file generated by dynamics code!'
            exit(1)
            #   Enter the QC working directory
        os.chdir(destPath)

        return

    def prepare(self):
        """
        generate bagel input file
        based on template (user) or parameter (auto)
        """
        # read template & create input bagel file
        bagel = bagel_create(self.config)
        bagel.wrt_bagel_input()

        return

    def run(self):
        """
        call the QC code & confirm the running is ok. if not throw error messages.
        """

        exec_name = self.config['command']['bagel']
        jobin = self.files["bagel_input"]
        jobout = self.files["bagel_log"]

       
        NP = int(os.environ['NP'])

        if NP > 1:

           exec_name = "mpirun -np " + str(NP) + ' ' + exec_name + " " + jobin + ' > ' + jobout

        else:

           exec_name = exec_name + " " + jobin + ' > ' + jobout


        print exec_name

        os.system(exec_name)
        return

    def analyze(self):
        """
        extract data used for surface hopping dynamics., 
        the required QC information was extraced.
        """
        bagel = bagel_parser(self.config)
        bagel.get_log_dat()

        return

    def finalize(self):
        """
        simply clean up the tmp dat. and so on.
        """
        #   Go back to directory of dynamics work
        #   Copy results of QM calculations

        #   Go back to directory of dynamics work
        os.chdir(self.directory['root'])

        home_dir = self.directory['home']
        destPath = self.directory['work']
        wfufile = destPath + '/' + self.files['bagel_wfu']
        if os.path.isfile(wfufile):
            shutil.copy2(wfufile, home_dir)

            #   Copy results of QM calculations
        sourcePath = self.directory['work']
        sourceFile = sourcePath + '/' + 'qm_results.dat'
        destPath = './'
        shutil.copy2(sourceFile, destPath)

        print 'Finish QC calculation'

        return

    def worker(self):
        """
        wrap the whole process
        """
        self.initilize()
        self.prepare()
        self.run()
        self.analyze()
        self.finalize()
        return

    # Main Program


if __name__ == "__main__":
    mr = bagel_run()
    mr.worker()
