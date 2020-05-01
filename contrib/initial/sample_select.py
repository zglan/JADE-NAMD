#! /usr/bin/env python
import os
import copy
import shutil
import random
import distutils.core


# $$ f = \Delta E |\mu|^2 $$
# $ \frac{f_i}{\Delta E_i} = |\mu_i|^2 = \rho_i $
# $ \rho_i' ~ \frac{\rho_i}{max\{rho_i\}} $
# $ \rho_i' < \zeta ~[0,1] $
#

class sample_select():
    def __init__(self):
        """
        sampling oscillator strength
        """
        self.files = {}
        self.files['input'] = "excitation.dat"
        self.results = {}
        self.dim = {}

        self.par = {}
        
        return

    def read_excitation(self):
        """
        read in excitation data.
        """
        filename = self.files['input']
        fp = open(filename, "r")
        # comments
        line = fp.readline()
        # dimensional info. 
        line = fp.readline(); rec = line.split()
        print line
        n_traj = int(rec[0]); n_state = int(rec[1])
        self.dim['n_traj'] = n_traj; self.dim['n_state'] = n_state
        # comments
        line = fp.readline()
        # excitation info.
        excitation = [[0.0 for i in xrange(0, n_traj)] for j in xrange(0, n_state)]
        for i in xrange(n_traj):
            for j in xrange(n_state):
                line = fp.readline(); rec = line.split()
                excitation[j][i] = float(rec[2])
        self.results['excitation'] = excitation
        # scaling..
        excitation_scaled = copy.deepcopy(excitation)
        for i_state in xrange(n_state):            
            max_val = max(excitation[i_state])
            for j_traj in xrange(n_traj):
                excitation_scaled[i_state][j_traj] /= max_val
        self.results['excitation_scaled'] = excitation_scaled
        
        return


    def random_select_state(self, i_state = 1):
        """
        select geometry for one state
        """
        n_traj = self.dim['n_traj']
        
        this_state = self.results['excitation_scaled'][i_state]
        
        select_traj = []
        for i_traj in xrange(n_traj):
            x = this_state[i_traj]
            ran_num = random.random()
            if x >= ran_num:
                select_traj.append(i_traj+1)

        this_traj = {str(i_state): select_traj}
        self.results['select_traj'].update(this_traj)
        
        return

    
            
    def random_select(self):
        """
        select by random number
        """
        self.results['select_traj'] = {}
        n_state = self.dim['n_state']
        state_list = self.par['state_list']
        
        if state_list == []:
            state_list = range(0,n_state)
        # seeds
        random.seed()
        
        # excitation info        
        for i_state in state_list:            
            self.random_select_state(int(i_state))
                
        return


    def get_cmd(self):
        """
        read in param from cmd line
        """
        self.par['state_list'] = []
        line = raw_input("which state do you want to analysis[default all avaiable]: \n > ")
        if line.strip() == "":
            self.par['state_list'] = []
        else:
            for i_state in line.split():
                self.par['state_list'].append(int(i_state) - 1)
            
        return

    def dump_traj_id(self):
        """
        write done in a file
        """
        fp = open("traj.dat", "w")
        traj_select = self.results['select_traj']
        
        for key in traj_select:
            destPath = "state-" + str(int(key)+1)
            if os.path.exists(destPath):
                os.rmdir(destPath)
                
            os.mkdir(destPath)
            n_traj = len(traj_select[key])            
            print >>fp, "# STATE:%s TRAJ:%d" % (key, n_traj)
            
            for traj_id in traj_select[key]:
                print >>fp, "%10d" % (traj_id)
                this_path = destPath + "/" + str(traj_id)
                # os.system("cp -r " + str(traj_id) + " " + destPath)
                # distutils.dir_util.copy_tree(str(traj_id), destPath)
                os.mkdir(this_path)
                shutil.copy2(str(traj_id)+"/stru_xyz.in", this_path)
                
        fp.close()

        return
        
if __name__ == "__main__":
    ss = sample_select()
    ss.get_cmd()
    ss.read_excitation()
    ss.random_select()
    ss.dump_traj_id()            
        
        

