#! /bin/python
#! python
import os
# read xyz file serials to output gamess inp files

# first, read xyz model file
# second, read gamess inp template file
# third, output
#
# =============
# Du Likai @ Chem-306 @ Shandong Univ. 
# Jinan, Shandong
# version 1.0 alpha 1
# date & time 2013-01-14 a.m.
# ============
#
# =========================
# Du Likai @ QIBEBT
# Qingdao, Shandong
# version 1 alpha 2
# data & time 2014-4-2 p.m.
# =========================
# 
class mkgms():
	""" build gamess input file, from xyz file """
	def __init__(self):
		""" initialize several internal variable """
		self.model = {'mol':[], 'nmol':0, 'cursor':0}
		# self.model['mol'][i] = {'natom': 0, 'jobname': '', 'info': '', 'atom':[]}
		self.template = {'head':'', 'body':'', 'mol':{}, 'tail':''}
		self.tfile = 'ccsdt.inp'		
		self.xyzfile = 'model.xyz'
		self.jobfile = 'scan.inp'
		self.tmpjobfile = ''
		self.fp = 0
		self.jobnum = 1
		
		# sub gms job
		self.job = {"ncpu":4, "version":"00", "cdir":"gms"}
		
		self.rd_cmd_stream()
		
	def rd_cmd_stream(self):
		"""
		read in command stream
		"""
		print "Gamess gms file generator version 0.2"
		line = raw_input("Enter the Template inp file name (i.e. ccsdt.inp):\n(Enter only if use default value)\n> ")
		str = line.strip()
		if str != "":
			self.tfile = str
			
		line = raw_input("Enter the xyz coord file name (i.e. model.xyz):\n(Enter only if use default value)\n> ")
		str = line.strip()
		if str != "":
			self.modelfile = str
			
		line = raw_input("Enter the output inp file name (i.e. scan.inp):\n(Enter only if use default value)\n> ")
		str = line.strip()
		if str != "":
			self.jobfile = str
			
		line = raw_input("Enter gms job info. (i.e. ncpu, version, dir):\n(DEFAULT:4 00 gms)\n(Enter only if use default value)\n> ")
		str = line.strip()
		if str != "":
			self.job = {"ncpu":int(str[0]), "version":str[1], "cdir":str[2]}
			
		return
		
	def __rd_template_header(self):
		""" read lines before  """
		fp = self.fp
		head = ''
		line = 'STARTER'
		while line.strip() != "":
			line = fp.readline()
			if line.lower().find('$data') == -1:
				head = head+line
			else:	
				break
		self.template['head'] = head
		return
	def __rd_template_geom(self):
		""" 
		read cart. coordinate info 
		mol: natom, info, atom.
		"""
		fp = self.fp
		body = ''
		line = 'STARTER'
		natom = 0
		mol = {'natom': 0, 'info': '', 'atom':[]}
		line = fp.readline()
		body = body + line
		line = fp.readline()
		body = body + line
		mol['title'] = line[:-1]
		line = fp.readline()
		body = body + line
		mol['symmetry'] = line[:-1]
		while line != "":
			line = fp.readline()
			print line
			if line.strip() == "$end":
				break
			items = line.split()
			atomname = items[0]
			atommass = float(items[1])
			frg = 0
			coord = [float(items[2]),float(items[3]),float(items[4])]
			record = {'name':atomname, 'mass': atommass, 'coord':coord, 'frg':frg}
			mol['atom'].append(record)
			natom = natom + 1
			mol['natom'] = natom
			body = body + line		
		self.template['mol'] = mol
		self.template['body'] = body + ' $end'
		return
	
	def __rd_template_tail(self):
		""" read template tail information """
		fp = self.fp
		tlist = []
		tail = ""
		line = 'STARTER'
		while line != "":
			line = fp.readline()
			tlist.append(line)
		for str in reversed(tlist):
			if str.strip() == "":
				tlist.pop()
			else:
				break
		for str in tlist:
			tail = tail + str
		self.template['tail'] = tail
		return
		
	def rd_template(self):
		""" read template file """
		tfile = self.tfile
		fp = open(tfile, 'r')
		self.fp = fp
		# read header
		self.__rd_template_header()
		#geom data
		self.__rd_template_geom()
		# other data
		self.__rd_template_tail()
		return		
		
	def wrt_template_string(self):
		""" wrt template file """
		tfile = 'template-str.txt'
		t = self.template
		fp = open(tfile, 'w')
		print >>fp, "%s%s%s" % (t['head'], t['body'], t['tail'])
		return
		
	def wrt_template(self):
		""" wrt template file """
		tfile = 'template.txt'
		t = self.template
		fp = open(tfile, 'w')
		print >>fp, "%s" % t['head'],
		geom = t['mol']
		print >>fp, "%s" % (geom['title'])
		print >>fp, "%s" % (geom['symmetry'])
		atom = geom['atom']
		natom = geom['natom']
		for i in range(natom):
			record = atom[i]
			atomname = record['name']
			atommass = record['mass']
			coord = record['coord']
			frg = record['frg']
			print >>fp, "%-10s%5.1f%12.7f%12.7f%12.7f%5d" % (atomname, atommass, coord[0], coord[1], coord[2], frg)
		print >>fp, "\n",
		print >>fp, "%s" % t['tail'],
		return

# xyz file		
	def __rd_xyz_nmol(self):
		""" """
		fpin = open(self.xyzfile, "r")
		nmol = 0
		# read number of atom
		line = "STARTER"		
		line = fpin.readline()		
		while line.strip() != "":
			natom = int(line.split()[0])		
			line = fpin.readline()
			# read a mol
			for i in range(natom):
				line = fpin.readline()
			nmol = nmol + 1			
			line = fpin.readline()
		fpin.close()		
		self.model['nmol'] = nmol		
		return nmol		
	def rd_xyz(self):
		""" read xyz file format """		
		nmol = self.__rd_xyz_nmol()
		fpin = open(self.xyzfile, "r")
		mol = []		
		tmol = self.template['mol']['atom']
		ntatom = self.template['mol']['natom']
		for i in range(nmol):
			# number of atom, 
			line = fpin.readline()
			natom = int(line)
			line = fpin.readline()
			jobname = "%s" % line[:-1]
			atom = []
			if ntatom != natom:
				print "geometry data in template file is not consistant with xyz file. check the template."
				exit()
			for j in range(natom):
				line = fpin.readline()
				rec = line.split()
				atomname, x, y, z, imove = rec
				frg = tmol[j]['frg']
				atommass = tmol[j]['mass']
				record = {'name': atomname, 'mass':atommass, 'coord': [float(x),float(y),float(z)], 'frg':frg}
				atom.append(record)
			onemol = {'natom': natom, 'jobname': jobname, 'info': '', 'atom':atom}
			mol.append(onemol)			
		self.model['mol'] = mol
		fpin.close()		
		return 
	
# output gamess inp file
	def wrt_gms_geom_once(self):
		""" write out geom content once """
		fp = self.fp
		model = self.model
		t = self.template
		cursor = model['cursor']
		mol = model['mol']
		onemol = mol[cursor]
		natom = onemol['natom']
		print >>fp, " $data"
		print >>fp, "%s" % t['mol']['title']
		print >>fp, "%s" % t['mol']['symmetry']
		for atom in onemol['atom']:
			atomname = atom['name']
			coord = atom['coord']
			atommass = atom['mass']
			frg = atom['frg']
			print >>fp, "%-5s%5.1f%12.6f%12.6f%12.6f" % (atomname, atommass, coord[0], coord[1], coord[2])
		print >>fp, " $end"
		return		
	def wrt_gms_onejob(self):
		""" wrt one gms job , one link """
		fp = self.fp
		t = self.template		
		print >>fp, "%s" % t['head'],
		self.wrt_gms_geom_once()
		print >>fp, "%s" % t['tail']
		self.model['cursor'] = self.model['cursor'] + 1		
		return
	# print nothing done	
	def wrt_gms_onejob_extra(self):
		""" wrt one gms job , one link """
		fp = self.fp
		t = self.template		
		print >>fp, "%s" % t['head']
		self.wrt_gms_geom_once()
		print >>fp, "%s" % t['tail']
		self.model['cursor'] = self.model['cursor'] + 1		
		return
		
	def __gen_jobfile(self):
		""" generate job fiel name """
		jobfile = self.jobfile
		items = jobfile.split('.')
		jobname = items[0]
		jobapp = items[1]
		return jobname, jobapp
	def wrt_gms_onefile(self, type='normal'):
		""" write one gms structure """
		nmol = self.model['nmol']
		cursor = self.model['cursor']
		jobnum = self.jobnum
		if nmol-cursor < jobnum:
			ijobnum = nmol - cursor
		else:
			ijobnum = jobnum	
		jobname, jobapp = self.__gen_jobfile()		
		purename = jobname+"a"+str(cursor)+"x"+str(ijobnum)
		filename = purename +"."+jobapp
		self.tmpjobfile = filename
		fp = open(filename, "w")
		self.fp = fp		
		for i in range(ijobnum):
			if type == "normal":
				self.wrt_gms_onejob()
			elif type == "extra":
				self.wrt_gms_onejob_extra(i)
			else:
				print "No other job type"
		fp.close()
		return		
		
	def wrt_gms_input(self, type='normal'):
		""" wrt gms file """
		nmol = self.model['nmol']
		job = self.job
		subfile = "subshell"
		os.system("mkdir "+job['cdir'])
		os.chdir(job['cdir'])
		fp = open(subfile, "w")
		while self.model['cursor'] < nmol:
			self.wrt_gms_onefile(type)
			str = (self.tmpjobfile).split(".")
			filename = "".join(str[0:-1])
			print >>fp, "rungms %s %s %d >& log.%s;" %(filename, job['version'], job['ncpu'], filename)	
		fp.close()
		return
		

		
# Main Program		
		
gms = mkgms()
gms.rd_template()
# gms.wrt_template_string()
gms.wrt_template()
gms.rd_xyz()
# if you do not want set 
gms.wrt_gms_input(type='normal')

line = raw_input("press any key to continue\n")
