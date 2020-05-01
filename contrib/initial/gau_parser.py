#!python
import os
import re

# 
# =====================================
# Author: LiuFang 
# Address: @ Jinan @ Shandong Univ. @ chem
# Date: 2014.5.12
# =====================================
# 
#
#
#

class gau_parse():
	""" get excitation-energy oscillator-strength """
	def __init__(self):
		self.files = {'log':'scana0x100.log','info':'info.dat'}
		self.dim = {'n_traj':100,'n_state':3}
		self.par_energy = []
		return

	
    
	def rd_log_file(self):
		log_file = self.files['log']
		rec = raw_input("Enter the number of molecule: ")
		n_traj = rec.strip()
		if n_traj == '':
			print "n_traj as the default 100\n!"
			n_traj = self.dim['n_traj']
		else:
			self.dim['n_traj'] = n_traj
		log_file = self.files['log'].split('.')
		log_file = log_file[0]+'0'+'x'+n_traj+'.'+log_file[1]
		# n_traj = __rd_n_traj(logfile)
		fp = open(log_file, 'r')
		line = fp.readline()
#        print line
		n = 0
		par_energy = []
		while 1:
			p= re.compile("Excited State   1:")
			line = fp.readline()
			rec = p.search(line)
			if rec is not None:
				print "Find the normal modes"
				n = n+1
				par_energy.append(line)
				print n
			# print line
			if n == int(n_traj):
				print line
				break
		self.par_energy = par_energy
		print par_energy
		return

	def wrt_par_energy(self):
		info = self.files['info']
		par_energy = self.par_energy
		fp = open(info,'w')
		n_traj = int(self.dim['n_traj'])
		n_state = int(self.dim['n_state'])
		es,os,ho = '','',''
		energy = []
		print >>fp, "# n_traj n_state"
		print >>fp, "%10d%10d" %(n_traj,n_state)
		print >>fp, "# \Delta E(eV); osciallator ho=f/deltaE"
		for i in range(n_traj):
			energy = par_energy[i].split()
			print energy
			es = float(energy[4])
			os = energy[8].split('=')
			# print os
			os = float(os[1])
			# print os
			if es == 0:
				ho = err
				print "err"
			else:
				ho = os/es
			print >>fp, "%15.8f%15.8f%15.8f" %(es,os,ho)
		fp.close()
        
                
if __name__ == "__main__":
	gau = gau_parse()
	gau.rd_log_file()
	gau.wrt_par_energy()
            

            
