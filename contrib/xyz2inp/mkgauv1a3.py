#! /user/bin/env python

import os

# read xyz file serials to output gaussian files

# first, read xyz model file
# second, read gjf model file
# third, output
#
#
# =========================
# Du Likai @ QIBEBT & SDU
# Shandong
# version 1 alpha 3
# date & time 2014.7.14 p.m.
# change the value of xyzfile
#
# =========================
# Du Likai @ QIBEBT & SDU
# Shandong
# version 1 alpha 3
# date & time 2014.5-9 a.m.
# change the output style..
#
# ==========================
# Du Likai @ QIBEBT
# Qingdao, Shandong
# version 1 alpha 2
# data & time 2014-4-2 p.m.
# ===========================
#
# ===================================
# Du Likai @ Chem-306 @ Shandong Univ.
# Jinan, Shandong
# version 1.0 alpha 1
# date & time 2013-01-14 a.m.
# ===================================

print "Gaussian gjf file generator version 1.0 ALPHA 3"
##
#
class mkgau():
    """ build gaussian input file, from xyz file """
    def __init__(self):
        """ initialize several internal variable """
        self.model = {'mol':[], 'nmol':0, 'cursor':0}
        # self.model['mol'][i] = {'natom': 0, 'jobname': '', 'info': '', 'atom':[]}
        self.template = {'link0':{}, 'routine':'', 'title':'','sc':'', 'head':'', 'body':'', 'mol':{}, 'tail':''}
        self.job = {}
        self.tfile = 'gau-template-bsse.gjf'
        self.xyzfile = 'model.xyz'
        self.jobfile = 'scan.gjf'
        self.tmpjobfile = ''
        self.fp = 0
        self.jobnum = 1

        self.rd_cmd_stream()
        return
    def rd_cmd_stream(self):
        """
        read in command stream
        """
        # working directory
        line = raw_input("Enter the working directory(press enter to use default: [default: .]\n>")
        mydir = line.strip()
        if mydir == "":
            mydir = '.'
        os.chdir(mydir)
        print "CURRENT WORKING DIRECTORY:"
        print os.getcwd()
        #
        line = raw_input("Enter the Template gjf file name (i.e. gau-template-bsse.gjf):\n(Enter only if use default value)\n> ")
        str = line.strip()
        if str != "":
            self.tfile = str

        line = raw_input("Enter the xyz coord file name (i.e. model.xyz):\n(Enter only if use default value)\n> ")
        str = line.strip()
        if str != "":
            self.xyzfile = str

        line = raw_input("Enter the output gjf file name (i.e. scan.gjf):\n(Enter only if use default value)\n> ")
        str = line.strip()
        if str != "":
            self.jobfile = str
        return
    def __rd_template_header(self):
        """ read % and # line """
        fp = self.fp
        link0 = {'chk':'', 'mem':'', 'nproc':''}
        head = ''
        routine = ''
        title = ''
        sc = ''
        # read header
        line = 'STARTER'
        while line.strip() != "":
            line = fp.readline()
            if line.lower().find('%chk') == 0:
                items = line.split('=')
                link0['chk'] = items[1][:-1]
                head = head+line
            elif line.lower().find('%mem') == 0:
                items = line.split('=')
                link0['mem'] = items[1][:-1]
                head = head+line
            elif line.lower().find('%nproc') == 0:
                items = line.split('=')
                link0['nproc'] = items[1][:-1]
                head = head+line
            elif line.lower().find('#') == 0:
                routine = line[:-1]
            else:
                head = head+line
                break
        # title, blank line, spin/charge.
        line = fp.readline()
        title = line[:-1]
        head = head+line
        line = fp.readline()
        head = head+line
        line = fp.readline()
        sc = line[:-1]
        head = head+line

        # assign value
        self.template['link0'] = link0
        self.template['routine'] = routine
        self.template['title'] = title
        self.template['sc'] = sc
        self.template['mol']['info'] = sc
        self.template['head'] = head
        return

    def __check_gjf_frg(self, line):
        """
            check gjf fragment type 03 or 09 version, and return records
        """
        frg = 0
        if line.find('=') != -1:
            myline = line.replace('(',' ').replace(')',' ').replace('=',' ')
            items = myline.split()
            atomname = items[0]
            frg = int(items[2])
            coord = [ float(items[3]), float(items[4]), float(items[5]) ]
        else:
            myline = line
            items = myline.split()
            if len(items) > 4:
                frg = int(items[4])
            atomname = items[0]
            coord = [ float(items[1]), float(items[2]), float(items[3]) ]
        rec = {'name': atomname, 'coord': coord, 'frg': frg}
        return rec
    def __rd_template_geom(self):
        """ read coordinate info """
        fp = self.fp
        body = ''
        line = 'STARTER'
        natom = 0
        mol = {'natom': 0, 'jobname': '', 'info': '', 'atom':[]}
        while line != "":
            line = fp.readline()
            if line.strip() == "":
                break
            record = self.__check_gjf_frg(line)

            # items = line.split()
            # atomname = items[0]
            # coord = [float(items[1]),float(items[2]),float(items[3])]
            # if items > 4:
                # frg = int(items[4])
            # else:
                # frg = ''
            # record = {'name':atomname, 'coord':coord, 'frg':frg}

            mol['atom'].append(record)
            natom = natom + 1
            mol['natom'] = natom
            body = body + line
        self.template['mol'] = mol
        self.template['body'] = body + '\n'
        return

    def __rd_template_tail(self):
        """ read template tail information """
        fp = self.fp
        line = 'STARTER'
        tlist = []
        tail = ""
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
        tfile = 'template.txt'
        t = self.template
        fp = open(tfile, 'w')
        print >>fp, "%s%s%s" % (t['head'], t['body'], t['tail'])
        return

    def wrt_template(self):
        """ wrt template file """
        tfile = 'template.txt'
        t = self.template
        fp = open(tfile, 'w')
        # print >>fp, "%s" % t['head'],
        link0 = t['link0']
        print >>fp, "%%chk=%s\n%%mem=%s\n%%nproc=%s" % (link0['chk'], link0['mem'], link0['nproc'])
        print >>fp, "%s\n\n%s\n\n%s\n" % (t['routine'], t['title'], t['sc']),
        geom = t['mol']
        atom = geom['atom']
        natom = geom['natom']
        for i in range(natom):
            record = atom[i]
            atomname = record['name']
            coord = record['coord']
            frg = record['frg']
            print >>fp, "%-10s%12.7f%12.7f%12.7f%5d" % (atomname, coord[0], coord[1], coord[2], frg)
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
        for i in range(nmol):
            # number of atom,
            line = fpin.readline()
            natom = int(line)
            line = fpin.readline()
            # items = line.split()
            # print items
            # sa = items[0]
            # sb = items[1]
            # jobname = "%s %s" % (sa, sb)
            jobname = "%s" % line[:-1]
            atom = []
            tmol = self.template['mol']['atom']
            ntatom = self.template['mol']['natom']
            if ntatom != natom:
                print "geometry data in template file is not consistant with xyz file. check the template."
            for j in range(natom):
                line = fpin.readline()
                items = line.split()
                if items == 5:
                    atomname, x, y, z, imove = items
                elif len(items) == 4:
                    atomname, x, y, z = items
                else:
                    print "nothing to do..."
                    exit(1)
                frg = tmol[j]['frg']
                record = {'name': atomname, 'coord': [float(x),float(y),float(z)], 'frg':frg}
                atom.append(record)
            onemol = {'natom': natom, 'jobname': jobname, 'info': '', 'atom':atom}
            mol.append(onemol)
        self.model['mol'] = mol
        fpin.close()
        return

# output nw file
    def wrt_gau_geom_once(self):
        """ write out geom content once """
        fp = self.fp
        model = self.model
        template = self.template
        cursor = model['cursor']
        mol = model['mol']
        onemol = mol[cursor]
        natom = onemol['natom']
        for atom in onemol['atom']:
            atomname = atom['name']
            coord = atom['coord']
            frg = atom['frg']
            print >>fp, "%-5s%12.6f%12.6f%12.6f%5d" % (atomname, coord[0], coord[1], coord[2], frg)
        print >>fp, "\n",
        return

    def wrt_gau_onejob(self):
        """ wrt one gaussian job , one link """
        fp = self.fp
        t = self.template
        link0 = t['link0']
        print >>fp, "%%chk=%s\n%%mem=%s\n%%nproc=%s" % (link0['chk'], link0['mem'], link0['nproc'])
        print >>fp, "%s\n\n%s\n\n%s\n" % (t['routine'], t['title'], t['sc']),
        self.wrt_gau_geom_once()
        print >>fp, "%s" % t['tail'],
        self.model['cursor'] = self.model['cursor'] + 1
        return
    def wrt_gau_onejob_extra(self, ijob):
        """ wrt one gaussian job , one link """
        fp = self.fp
        t = self.template
        link0 = t['link0']
        routine = t['routine']
        if ijob > 0:
            routine = routine.strip() + " Guess=read"
        else:
            routine = t['routine']
        print >>fp, "%%chk=%s\n%%mem=%s\n%%nproc=%s" % (link0['chk'], link0['mem'], link0['nproc'])
        print >>fp, "%s\n\n%s\n\n%s\n" % (routine, t['title'], t['sc']),
        self.wrt_gau_geom_once()
        print >>fp, "%s" % t['tail'],
        self.model['cursor'] = self.model['cursor'] + 1
        return
    def __gen_jobfile(self):
        """ generate job fiel name """
        jobfile = self.jobfile
        items = jobfile.split('.')
        jobname = items[0]
        jobapp = items[1]
        return jobname, jobapp
    def wrt_gau_onefile(self, type='normal'):
        """ write one gau structure """
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
        self.template['link0']['chk'] = purename +".chk"
        fp = open(filename, "w")
        self.fp = fp
        for i in range(ijobnum):
            if type == "normal":
                self.wrt_gau_onejob()
            elif type == "extra":
                self.wrt_gau_onejob_extra(i)
            else:
                print "No other job type"
            if ijobnum - i > 1:
                self.wrt_link()
            else:
                print >>fp, ""
        fp.close()
        return

    def wrt_link(self):
        """ link info """
        fp = self.fp
        link = "--Link1--"
        print >>fp, "\n%s\n"  % (link)
        return

    def wrt_gau_input(self, type='normal'):
        """ wrt gau file """
        nmol = self.model['nmol']
        subfile = "subshell"
        fp = open(subfile, "w")
        while self.model['cursor'] < nmol:
            self.wrt_gau_onefile(type)
            # print >>fp, "subg09 %s Gridxe%d" %(self.tmpjobfile, self.model['cursor'])
            print >>fp, "g09 %s " %(self.tmpjobfile)
        fp.close()
        return


# Main Program

# working
gau = mkgau()
gau.rd_template()
gau.wrt_template()
gau.rd_xyz()
# if you do not want set guess=read, set type='normal' else set type='extra'
gau.wrt_gau_input(type='normal')

