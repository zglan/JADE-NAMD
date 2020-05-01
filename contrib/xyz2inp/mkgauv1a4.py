#! /usr/bin/env python

import os

#------------------------------------------------
# this code was initially written for FF development..
# read xyz file serials to output gaussian files
# ===========================================
# initial with parameter. user control..
# first, read xyz model file
# second, read gjf template file
# third, output
# ============================================
#
# =========================================
# Du Likai @ QIBEBT
# Shandong
# version 1 alpha 4
# date & time 2014.7.24 p.m.
# total remove the tedious section
# remove the link1 section to shell scripts
# require linux shell is active.
# change the user interface.
# rewrite the template reader..
# provide the ability to select which xyz model to be punch out.
# and how many single job in one gjf file.
# ========================================
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

# -----------------------------------------------------
print "Gaussian gjf file generator version 1.0 ALPHA 4"
# -----------------------------------------------------
#
#
class mkgau():
    """ build gaussian input file, from xyz file """
    def __init__(self):
        """ initialize several internal variable """
        self.model = {'mol':[], 'nmol':0}
        self.template = {} 
        self.config = {}
        self.config['tfile'] = 'gau-template-bsse.gjf'
        self.config['xyzfile'] = 'model.xyz'
        self.config['jobfile'] = 'gau.gjf'
        self.config['job_prefix'] = self.config['jobfile'].split(".")[0]
        self.config['incr'] = 1
        
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
        mystr = line.strip()
        if mystr != "":
            self.config['tfile'] = mystr

        line = raw_input("Enter the xyz coord file name (i.e. model.xyz):\n(Enter only if use default value)\n> ")
        mystr = line.strip()
        if mystr != "":
            self.config['xyzfile'] = mystr

        line = raw_input("Enter the output gjf file name (i.e. gau_*.gjf):\n(Enter only if use default value)\n> ")
        mystr = line.strip()
        if mystr != "":
            self.config['jobfile'] = mystr
        line = raw_input("Enter how many step to dump the xyz struct..(default: 1)\n> ")
        myincr = line.strip()
        if myincr != "":
            self.config['incr'] = int(myincr)
            
        return


    def __rd_tpl_link0(self, fp):
        """
        read in link 0 section
        most case include: %chk %mem %nproc ...
        """
        link0 = {}
        while True:
            this_pos = fp.tell()
            line = fp.readline()
            if line[0] != '%':
                fp.seek(this_pos)
                break
            else:
                record = line.split("=")
                if len(record) != 2:
                    print "LINK 0 in template NO =.."
                    key = record[0]
                    content = ""
                else:
                    key = record[0]
                    content = record[1]
                link0[key] = content
        self.template['link0'] = link0
        return
        
    def __rd_tpl_route(self, fp):
        """
        read in routine section
        #p/t xxx xxx xxx
        xxx xxx
        """
        line = fp.readline()
        if line[0] != '#':
            print "ROUTE section in template ERROR.."
            exit(1)
        route = line
        while True:
            this_pos = fp.tell()
            line = fp.readline()
            if line.strip() == "":
                fp.seek(this_pos)
                break
            route += line
        self.template['route'] = route
        return
    def __rd_tpl_title(self, fp):
        """
        read in title section
        may be empty line
        """
        line = fp.readline() # empty line..
        line = fp.readline()
        title = line[:-1]
        self.template['title'] = title
        line = fp.readline() # another empty line.
        return

    def __rd_tpl_molspec(self, fp):
        """
        read in spin/charge section
        and cart. coord.
        """
        atoms = []
        # at first spin/charge
        line = fp.readline()
        spin_charge = line[:-1]
        # cart. coord.
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            record = self.__split_line_in_molspec(line)
            atoms.append(record)
        n_atoms= len(atoms)

        molspec = {'spin_charge': spin_charge, 'n_atoms': n_atoms,
                   'atoms': atoms}

        self.template['molspec'] = molspec
        return


    def __split_line_in_molspec(self, line):
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

    def __rd_tpl_tail(self, fp):
        """
        read extra info. in the template
        """
        tlist = []
        tail = ""
        while True:
            line = fp.readline()
            if line == "":
                break
            tlist.append(line)
        for line in reversed(tlist):
            if line.strip() == "":
                tlist.pop()
            else:
                break
        for line in tlist:
            tail += line
        self.template['tail'] = tail
        return



    def rd_template(self):
        """
        read template file
        """
        tfile = self.config['tfile']
        fp = open(tfile, 'r')
        # link0
        self.__rd_tpl_link0(fp)
        # route
        self.__rd_tpl_route(fp)
        # title
        self.__rd_tpl_title(fp)
        # mol-spec
        self.__rd_tpl_molspec(fp)
        # other data
        self.__rd_tpl_tail(fp)
        return


    def wrt_template_string(self):
        """ wrt template file """
        fp = open("dump.txt", 'w')
        print >>fp, self.template
        fp.close()
        return


    def wrt_template(self):
        """ wrt template file """
        fp = open("template.txt", 'w')
        t = self.template
        link0 = t['link0']
        for key in link0:
            if link0[key] != "":
                print >>fp, "%s=%s" % (key, link0[key]),
            else:
                print >>fp, "%s" % (key),
        print >>fp, "%s" % t['route'],
        print >>fp, ""
        print >>fp, "%s" % t['title']
        print >>fp, ""

        molspec = t['molspec']
        print >>fp, "%s" % molspec['spin_charge']
        atoms = molspec['atoms']
        n_atoms = molspec['n_atoms']
        for i in xrange(n_atoms):
            record = atoms[i]
            atomname = record['name']
            coord = record['coord']
            frg = record['frg']
            print >>fp, "%-10s%12.7f%12.7f%12.7f%5d" % (atomname, coord[0], coord[1], coord[2], frg)
        print >>fp, "\n",
        print >>fp, "%s" % t['tail'],            
        fp.close()
        return

    #################################################
    ########## XYZ #########
    #################################################
    # xyz file handling ...
    def __rd_xyz_nmol(self):
        """ number of model in the xyz file, maybe larger than 1. """
        fpin = open(self.config['xyzfile'], "r")
        content = fpin.readlines()
        fpin.close()
        first_line = content[0]
        n_line = len(content)
        n_atom = int(first_line.split()[0])
        nmol = n_line / (n_atom + 2)
        self.model['nmol'] = nmol
        return nmol
    
    def rd_xyz(self):
        """ read xyz file format """
        nmol = self.__rd_xyz_nmol()
        fpin = open(self.config['xyzfile'], "r")
        tmol = self.template['molspec']['atoms']
        ntatom = self.template['molspec']['n_atoms']
        mol = []
        for i in range(nmol):
            # number of atom,
            line = fpin.readline().strip()
            natom = int(line)
            line = fpin.readline()

            jobname = "%s" % line[:-1]
            atom = []

            if ntatom != natom:
                print "geometry data in template file is not consistant with xyz file. check the template."
            for j in range(natom):
                line = fpin.readline()
                rec = line.split()
                if len(rec) == 5:
                    atomname, x, y, z, imove = rec
                elif len(rec) == 4:
                    atomname, x, y, z = rec
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
    # PUNCH OUT GAUSSIAN INPUT FILES

    def wrt_gau_input(self):
        """
        write all gaussian input files
        """
        fp = open("myfiles.dat", "w")        
        nmol = self.model['nmol']
        prefix = self.config['job_prefix']
        incr = self.config['incr']
        for i in xrange(0, nmol, incr):
            self.wrt_gau_input_once(i)
            print >>fp, "%sx%s.gjf" % (prefix, i)
        fp.close()
        
        # extra jobs
        fp = open("link.sh", "w")
        print >>fp, "#! /bin/bash"
        print >>fp, "# sampling shell input"
        print >>fp, "rm linking.gjf"
        print >>fp, "myfiles=`more myfiles.dat`"
        print >>fp, """
        for onefile in $myfiles;
        do cat $onefile >> linking.gjf;
        echo -e '\\n--Link1--\\n' >> linking.gjf;
        done
        """
        fp.close()
        return


    def __build_gau_atom(self, atom):
        """ output a string """
        frg = atom['frg']
        atomname = atom['name']
        coord = atom['coord']
        if frg > 0:
            line = "%-5s%12.6f%12.6f%12.6f%5d" % (atomname, coord[0], coord[1], coord[2], frg)
        else:
            line = "%-5s%12.6f%12.6f%12.6f" % (atomname, coord[0], coord[1], coord[2])
        return line
    
    def wrt_gau_input_once(self, imol):
        """
        write the id-th xyz model to gaussian inp
        """
        prefix = self.config['job_prefix'] 
        inpfile = prefix + "x" +str(imol) + ".gjf"
        t = self.template
        fp = open(inpfile, "w")
        link0 = t['link0']
        link0['%chk'] = prefix + "x" + str(imol) + ".chk\n"
        for key in link0:
            if link0[key] != "":
                print >>fp, "%s=%s" % (key, link0[key]),
            else:
                print >>fp, "%s" % (key),
        print >>fp, "%s" % t['route'],
        print >>fp, ""
        print >>fp, "%s" % t['title']
        print >>fp, ""

        molspec = t['molspec']
        print >>fp, "%s" % molspec['spin_charge']
        
        onemol = self.model['mol'][imol]
        natom = onemol['natom']
        for atom in onemol['atom']:
            line = self.__build_gau_atom(atom)
            print >>fp, "%s" % line
 
        print >>fp, ""
        print >>fp, "%s" % t['tail'],
           
        fp.close()
        return        
 

# Main Program
if __name__ == "__main__":
    gau = mkgau()
    gau.rd_template()
    gau.wrt_template()
    gau.rd_xyz()
    # if you do not want set guess=read, set type='normal' else set type='extra'
    gau.wrt_gau_input()

