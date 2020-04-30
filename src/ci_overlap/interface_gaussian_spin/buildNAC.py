#!/usr/bin/python
import os
import sys
import re
import shutil

sys.path.append("../tools/")
import tools

class buildNAC():
    """
    calc. SOC value between different spin state.
    """
    def __init__(self, config = {}):
        """
        automatic nac calc.
        """
        self.directory = {'work': "./QC_TMP/GAU_TMP", \
                          'work_prev': "./QC_TMP/GAU_TMP", \
                          "overlap": "./QC_TMP/OVERLAP", \
                          "nac": "./QC_TMP/NAC"  \
                          }
        self.files = {'dimension': "dimension.json", 'interface': 'interface.json'}
        self.results = {}
        self.dim = {}
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']            
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['work_prev'] = self.directory['home'] + "/" + dirs['work_prev']
            self.files["dimension"] = files['dimension']
            self.files["interface"] = files['interface']
            
            # run the job directly
            self.worker()
                        
        return
        

    def prepare(self):
        """
        first, prepare work dir; then, the necessary files.
        """
        # load internal data.
        filename = self.files['interface']
        it = tools.load_data(filename)
        self.dim = it['parm']
        return

    def build(self):
        """
        call another standalone program to deal with SOC
        here, i use constant SOC
        """
        har2cm = 219474.5459784
        n_state = self.dim['n_state']    # Number of states
        val = 100. / har2cm
        
        nac = [[0.0 for j in xrange(n_state)] for i in xrange(n_state)]
        val = 0.0
        for i in xrange(n_state):
            for j in xrange(n_state):
                if i != j:
                    soc[i][j] = val
                    
        self.results['soc'] = soc       

        # overlap_time = 0.d0
        # do j=1, n_state
           # do k=1, n_state
              # read (101, *)   tmp_i, tmp_j, &
                             # overlap_time(j,k)
          # enddo
        # enddo

        # close(101)


        # nac_time =0.d0 
        # do i = 1, n_state
           # do j = 1, i-1
              # nac_time(i,j) = 0.5 * &
                           # (   abs( overlap_time(i,j) ) &
                             # + abs( overlap_time(j,i) ) &
                           # ) 
              # nac_time(j,i) =  - nac_time(i,j) 
           # enddo
        # enddo
        
        return
        
    def dump(self):
        """
        dump necessary data of nac
        """
        n_state = self.dim['n_state']    # Number of states
        soc = self.results['soc']
        fp = open('nac.dat', "w")
        for i in xrange(n_state):
            for j in xrange(n_state):
                print >>fp, "%20.12e" % soc[i][j],
            print >>fp, ""
        fp.close()
        return

    def finilize(self):
        """
        finish the current step & prepare for the following step
        """
        return
        
    def worker(self):
        """
        prepare; run; dump; finilize
        """
        self.prepare()
        self.build()
        self.dump()
        self.finilize()
        
        return
        

# main program.
if __name__ == "__main__":    
    n = buildNAC() 
    n.worker()

   
     
     
      
