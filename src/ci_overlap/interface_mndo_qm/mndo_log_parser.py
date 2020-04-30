# python
import os
import sys
import re
import copy
import math
from operator import itemgetter
import shutil

sys.path.append("../tools/")
import tools


class mndo_log_parser():
    """
    parse mndo log file
    """
    def __init__(self, label_ZN, config = {}):
        """ init """

        self.files = {'interface': 'interface.json', 'mo': 'mndo.log', 'fort': 'fort.15'}
        self.label_ZN = label_ZN
        
      
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files'] 
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            
            self.files = {}
            self.files["interface"] = self.directory['work'] + "/" + files['interface'] 
            self.files["mo"] = self.directory['work'] + "/" + files['mndo_log'] 
            self.files["fort"] = self.directory['work'] + "/" + files['mndo_fort'] 
        
 
        self.load()
        return

# -------------------------------------------------------------------------

    def load(self):
        """
        load interface.json
        """
        filename = self.files['interface']
        obj = tools.load_data(filename)
        self.interface = copy.deepcopy(obj)
        

    def collect_qm(self):
        """
        wrt down in one file
        """
        fileout3 = open('qm_results.dat', 'w')

        qm_interface = tools.load_data("interface.json")
        n_atom = qm_interface['parm']['n_atom']
        geom = qm_interface['mol']
        atoms = geom['atoms']
        
        fileout3.write('     ' + str(n_atom)+ '\n')  
        fileout3.write(' The coordinates' + '\n')  
        for i in  range(n_atom):
           record = atoms[i]
           atomname = record['name']
           coord = record['coord']
           fileout3.write(str(atomname) +'   '+str(coord[0])+'   '+str(coord[1])+'   '+str(coord[2])+ '\n')  


        filein4=open('qm_energy.dat','r')
        fileout3.write(filein4.read())  
        filein4.close()

        filein4=open('qm_gradient.dat','r')
        fileout3.write(filein4.read())  
        filein4.close()    
     
        if self.label_ZN == 0:
           sourceFile = 'qm_nac.dat'
           if os.path.isfile(sourceFile):
               filein4=open('qm_nac.dat','r')
               fileout3.write(filein4.read())
               filein4.close()
           else : 
               for i_state in range(n_state):
                   for j_state in range(n_state):
                       fileout3.write('S'+str(i_state)+'    S'+str(j_state)+'   0.00000   \n')

        fileout3.close()         
            
        return



# ---------------------------------------------------------------------------    

#   %%% Read the energy
#   qm_energy.dat
#   Attention:

    def get_energy(self):
        """ read energy and punch out """
        fortfile = self.files['fort']
        file_in = open(fortfile, "r")
        file_out = open("qm_energy.dat", "w")

        file_out.write(' Energy of electronic states'+ '\n')

        pattern = re.compile(" STATES, ENERGIES, CARTESIAN AND INTERNAL GRADIENT NORMS") 

        KCANGTOEV=0.0433641
        TOEV= 27.2113961
        ANSTOBOHR=1.8897261328856432

        line = "NOT EMPTY LINE"
        while line != "":
           while line != "":
               line = file_in.readline()
               m = pattern.search(line)
               if m is not None:    
                   break
           
           while line != "": 
               line = file_in.readline()           
               if line.strip() == "":
                  break
            
               record = line.split()

               energy = float(record[1])*KCANGTOEV/TOEV

               file_out.write(''+str( energy )+'   '+ '\n')

        file_in.close() 
        file_out.close()       
        
        return


    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['mo']
        fortfile = self.files['fort']
        file_in = open(fortfile, "r")
        file_out = open("qm_gradient.dat", "w")

        file_out.write(' Gradient of electronic states'+ '\n')

        pattern = re.compile("CARTESIAN GRADIENT FOR STATE") 

        KCANGTOEV=0.0433641
        TOEV= 27.2113961
        ANSTOBOHR=1.8897261328856432

        line = "NOT EMPTY LINE"
        while line != "":
           while line != "":
               line = file_in.readline()
               m = pattern.search(line)
               if m is not None:    
                   file_out.write(' State:           '+ line.split()[-1]+ '\n')
                   break
           
           while line != "": 
               line = file_in.readline()           
               if line.strip() == "":
                  break
            
               record = line.split()

               grad_x = float(record[2])*KCANGTOEV/(TOEV*ANSTOBOHR)
               grad_y = float(record[3])*KCANGTOEV/(TOEV*ANSTOBOHR)
               grad_z = float(record[4])*KCANGTOEV/(TOEV*ANSTOBOHR)

               file_out.write(''+str( grad_x )+'   '+ \
                               str( grad_y )+'   '+str( grad_z )+'  \n')            
        file_in.close() 
        file_out.close()       
        
        return
        
# -------------------------------------------------------------------------
#   %%% Read the nac
#   qm_nac.dat
#   Attention:
# ---------------------------------------------------------------------------    
    def get_nac(self):

        n_state = self.interface['parm']['n_state']
        n_atom = self.interface['parm']['n_atom']
        n_dime = 3

        nac = []
        for i in range(n_state):
           nac.append([])
           for j in range(n_state):
              nac[i].append([])
              for k in range(n_atom):
                 nac[i][j].append([])
                 for l in range(n_dime):
                    nac[i][j][k].append(0.0)
             

        """ read nac and punch out """
        logfile = self.files['mo']
        fortfile = self.files['fort']

        file_in = open(fortfile, "r")

        pattern = re.compile(" CARTESIAN INTERSTATE COUPLING GRADIENT FOR STATES") 

        KCANGTOEV=0.0433641
        TOEV= 27.2113961
        ANSTOBOHR=1.8897261328856432

        line = "NOT EMPTY LINE"
        while line != "":
           while line != "":
               line = file_in.readline()
               m = pattern.search(line)
               if m is not None:    
                   i = int(line.split()[-2]) - 1
                   j = int(line.split()[-1]) - 1
                   break
           k = 0  
           while line != "": 
               line = file_in.readline()           
               if line.strip() == "":
                  break
            
               record = line.split()

               nac[i][j][k][0] = -float(record[2])/ANSTOBOHR
               nac[i][j][k][1] = -float(record[3])/ANSTOBOHR
               nac[i][j][k][2] = -float(record[4])/ANSTOBOHR
               
               nac[j][i][k][0] = - nac[i][j][k][0]
               nac[j][i][k][1] = - nac[i][j][k][1]
               nac[j][i][k][2] = - nac[i][j][k][2]
             
               k = k+1

        file_in.close() 

        file_out = open("qm_nac.dat", "w")

        file_out.write('Nonadiabatic couplings'+ '\n')
        for i in range(n_state):
           for j in range(n_state):
              file_out.write(' State:           '+ str(i+1) + '        '+ str(j+1) +'\n')
              for k in range(n_atom):
                 file_out.write( str( nac[i][j][k][0] )+'   '+str( nac[i][j][k][1])+'    '+str(nac[i][j][k][2]) + '  \n')            


        file_out.close()       
        
        return

        
# -------------------------------------------------------------------------
#   %%% Read all other important information of QM output
#   mndo.log file is required.
#   For example: Transition dipole moment and so on 
# ---------------------------------------------------------------------------
    def get_other(self):
        """
        Write other important information in QM output 
        """
        es = []
        gs = []
        pat1e = re.compile("Excited states from <AA,BB:AA,BB> singles matrix")
        pat2e = re.compile("Excitation energies and oscillator strengths")
        float_number = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        pat1g = re.compile("Charge=(\s)+" + float_number + "(\s)+electrons")
        pat2g = re.compile("XXYZ=(.*)YYXZ=(.*)ZZXY=(.*)")
                
        # read all
        file_energy = self.files['mo']
        filein = open(file_energy,'r')        
        
        line = "empty"
        # Excited states from <AA,BB:AA,BB> singles matrix
        while line != "":
            line = filein.readline()
            m1 = pat1e.search(line)
            if m1 is not None:
                break            
        line = filein.readline()
        line = filein.readline() 

        while line != "":
            line = filein.readline()   
            m2 = pat2e.search(line)
            if m2 is not None:
                break
            es.append(line)             

        # ground state.
        while line != "":
            line = filein.readline()
            m1 = pat1g.search(line)
            if m1 is not None:
                break            
        gs.append(line)
        while line != "":
            line = filein.readline()   
            gs.append(line) 
            m2 = pat2g.search(line)
            if m2 is not None:
                break
        filein.close()
        
        fileout = open('qm_other.dat', 'w')  
        for line in gs:
            fileout.write(line)
        fileout.write('------------------------------------------------------------- \n')           
        for line in es:
            fileout.write(line) 
        fileout.write('------------------------------------------------------------- \n')       
        fileout.close()

        return

        
    
### main program
if __name__ == "__main__":
    ao = mndo_log_parser()
    
    ao.get_gradient()
    ao.get_nac()
#    ao.get_other()


