#! /usr/bin/env python

import os
import subprocess
import shutil



class gms_run():
    """
    gamess runner setting..
    """
    def __init__(self, config = {}):
        """
        parameter set.
        """
        self.directory = {"qc": "./QC_TMP", "work": "./QC_TMP/GMS_TMP", \
                          "home": "./QC_TMP" }
        self.files = {"template": "template.json",
                      "job_inp": "gamess.inp",
                      "job_log": "gamess.log",
                      "job_dat": "gamess.dat",
                      "interface": "interface.json"}
        self.config = config
        self.dim = {}
        self.dim['i_state'] = 1
        self.vars = {}
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']
            self.dim = {}
            self.directory = {}
            self.files = {}

            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            if 'userscr' in dirs:
                self.directory['userscr'] = dirs['userscr']

            self.files['template'] = files['template']
            self.files['job_inp'] = files['job_inp']
            self.files['job_log'] = files['job_log']
            self.files['job_dat'] = files['job_dat']
            self.files['interface'] = files['interface']
            
            self.files['job_inp2'] = files['job_inp2']
            self.files['job_log2'] = files['job_log2']
            self.files['job_dat2'] = files['job_dat2']            
            self.dim = {}
            self.dim['i_state'] = config['interface']['parm']['i_state']
            
        return

    def check(self):
        """
        check variable
        """
        # check & use env variable.
        if 'GMS_VERSION_NO' in os.environ:
            verno = os.environ.get('GMS_VERSION_NO')
            print "use gamess value<env>: version-no: ", verno
        elif 'GMS_VERSION_NO' in self.config['command']:
            verno = self.config['command'].get('GMS_VERSION_NO')
            print "use gamess value<cfg>: version-no: ", verno
        else:
            verno = "06"
            print "GMS_VERSION_NO cannot be found ???"
            print "use default value: version-no: 06"
        self.vars['verno'] = verno
        
        if 'GMS_N_CPU' in os.environ:
            n_cpu = os.environ.get('GMS_N_CPU')
            print "use cpu value<env>: n_cpu: ", n_cpu
        elif 'GMS_N_CPU' in self.config['command']:
            n_cpu = self.config['command'].get('GMS_N_CPU')
            print "use cpu value<cfg>: n_cpu: ", n_cpu            
        else:
            n_cpu = 2
            print "GMS_N_CPU cannot be found ???"
            print "use default value: n_cpu: 2"
        self.vars['n_cpu'] = n_cpu
        
        return

    def run(self):
        """
        call the gamess runner
        """
        n_cpu = self.vars['n_cpu']
        verno = self.vars['verno']

        # files..
        datfile = self.files['job_dat']
        datfile2 = self.files['job_dat2']
        
        if 'GMS_USER_SCRATCH' in os.environ:
            userscr = self.directory['userscr']
            print "use gamess value: userscr: ", userscr
        elif 'GMS_USER_SCRATCH' in self.directory:
            userscr = self.directory['userscr']
        else:
            userscr = "./scr"
            print "GMS_USER_SCRATCH cannot be found ???"
            print "use default value: userscr: ./scr" 
        
        # check config-ini variable
        # 1 default variables: version-no.=06 n_cpu=2        
        exec_name = self.config['command']['exec']
        jobfile = self.files['job_inp']
        logfile = self.files['job_log']
        mycmd = "%s %s %s %s >& %s;" % (exec_name, jobfile,
                                        verno, n_cpu, logfile)
        mycmd = mycmd.strip()
        print mycmd,"@", os.getcwd()
        # os.system("rungms gamess.inp 06 2 >& gamess.log")
        subprocess.call(mycmd, shell=True) 
        if os.path.isfile(datfile): 
            shutil.copy2(userscr+"/"+datfile, "./")
            
        # 2 for the case of ground state. run excited state energy calc.
        i_state = self.dim['i_state']
        if i_state == 1:
            jobfile = self.files['job_inp2']
            logfile = self.files['job_log2']
            mycmd = "%s %s %s %s >& %s;" % (exec_name, jobfile,
                                        verno, n_cpu, logfile)
            mycmd = mycmd.strip()
            print "EX FOR GS CALC."
            print mycmd, "@", os.getcwd() 
            subprocess.call(mycmd, shell=True)
            if os.path.isfile(datfile2):
                shutil.copy2(userscr+"/"+datfile2, "./")
                
        return


    
    def caller(self):
        """
        define external variable and run
        """
        # variable useful.
        self.check()
        
        self.run()
        # self.more_work()
        
        return




