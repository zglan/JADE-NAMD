#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil 
import copy

#---------------------------------------------------------------------------

#  Creat the coordinates for double-molecule 
def creat_falk_coord (n_atom) :


    fileout1=open('coord_double','w')
    fileout1.write('$coord   \n')

  
    n_line = 0
    filein1=open('coord1','r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein1=open('coord1','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

    for i_line in range(1,n_atom+1) :
        fileout1.write(''+str( line_each[i_line])+' \n')
    
    n_line = 0
    filein1=open('coord2','r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein1=open('coord2','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

    for i_line in range(1,n_atom+1) :
        fileout1.write(''+str( line_each[i_line])+' \n')


    
    fileout1.write('$user-defined bonds \n')
    fileout1.write('$end')
    fileout1.close()
    
    sourceFile = 'coord_double'
    destFile   = 'coord'
    shutil.copyfile("./coord_double", "./coord")

    return

def extend_atom_string(atom_string):
    """
    parse atom_string..
    1-2 ==> [2, 1, 2]
    3   ==> [1, 3]
    """
    if "-" in atom_string:
        x = atom_string.split("-")
        a = int(x[0])
        b = int(x[1])
        atom_number = [2, a, b]
    else:
        x = int(atom_string)
        atom_number = [1, x]

    # print atom_number
    return atom_number
    

def extend_atom_list(line):
    """
    read in atom list: typically one line.
    """
    atom_list = []
    rec = line.split(",")
    for atom_string in rec:
        atom_number = extend_atom_string(atom_string)
        atom_list.append(atom_number)
    # print atom_list
    return atom_list

def strip_atom_list(line):
    """
    deal with atom list and cut header & tail of a line
    """
    myline = line[3:]
    myline = re.sub(r',[\s]+\\', ' ',myline)
    myline = re.sub(r'[\s]+\\', ' ',myline)

    return myline

def extend_atom_section(atom_section):
    """
    read in one element type section
    c  1-6,8,10,14-17,19,21-22,24-28,30,32,35-36,41-46, \
       48,50,54-57,59,61-62,64-68,70,72,75-76   \
       basis =c def2-SVP
       cbas =c def2-SVP
    """
    flag_string = "basis"
    for line in atom_section:
        if 'cbas' in line:
            flag_string = "cbas"
    # print atom_section
    atom_list = []
    # first line
    line = atom_section[0]
    element = line[0:3]    
    basis = ""
    cbas = ""
    for line in atom_section:
        if "basis" in line:
            basis = line.strip()
        elif "cbas" in line:
            cbas = line.strip()
        elif flag_string in line:
            break
        else:
            myline = strip_atom_list(line)        
            atom_list.extend(extend_atom_list(myline))

    atom_section = {'element': element,
                    'basis': basis,
                    'cbas': cbas,
                    'atom_list': atom_list}

    # print atom_section
    return atom_section


def read_atom_basis():
    """
    change to double molecule basis define
    elements: ""
    atom_number: [2, a,b], [1, s]
    basis: ""
    """
    # read $atoms ==> $basis section
    n_line = 0
    filein1 = open("control", "r")
    line_each = filein1.readlines()
    n_line = len(line_each)
    # change $atoms section
    for i_line in xrange(n_line):
        pat1 = re.compile("\$atoms")
        pat2 = re.compile("\$basis")
        m1 = pat1.search(line_each[i_line])
        m2 = pat2.search(line_each[i_line])
        if m1 is not None:
            i_start = i_line
            continue
        if m2 is not None:
            i_end = i_line
            break

    section = []
    content = []
    for i_line in xrange(i_start+1, i_end):
        line = line_each[i_line]
        section.append(line)        
        if "basis" in line:
            content.append(section)
            section = []
 
    return content



def get_atom_basis(atom_dict):
    """
    change to double molecule basis define
    elements: ""
    atom_number: [2, a,b], [1, s]
    basis: ""
    """
    atoms_block = atom_dict['$atoms']
    content = []; section = []
    flag_string = "basis"
    for line in atoms_block:
        if 'cbas' in line:
            flag_string = "cbas"
            break
    for line in atoms_block[1:]:
        section.append(line)
        if flag_string in line:
            content.append(section)
            section = []
    #print content
 
    return content



def extend_atom_basis(content):
    """
    extend double basis
    """
    atom_basis = []
    for section in content:
        sec = extend_atom_section(section)
        
        atom_basis.append(sec)

    #print atom_basis
    return atom_basis

def double_atom_section(basis, n_atom):
    """
    all number + n_atom
    """
    atom_list2 = []
    basis2 = copy.deepcopy(basis)
    atom_list = basis['atom_list']
    for atom_number in atom_list:
        if atom_number[0] == 1:
            atom_number[1] += n_atom
        elif atom_number[0] == 2:
            atom_number[1] += n_atom
            atom_number[2] += n_atom
        else:
            print "no such atom_number ???"
            exit(1)
        atom_list2.append(atom_number)
    basis2['atom_list'] = atom_list2
    
    #print basis2
 
    return basis2

def double_atom_basis(atom_basis, n_atom):
    """
    expand two double molecule basis
    """
    atom_basis2 = copy.deepcopy(atom_basis)
    
    # print atom_basis2
    for basis in atom_basis:
        basis2 = double_atom_section(basis, n_atom)
        atom_basis2.append(basis2)

    return atom_basis2

def contract_atom_number(atom_number):
    """
    contract atom_number to strings
    """
    i_flag = atom_number[0]
    if i_flag == 1:
        mystring = str(atom_number[1])
    elif i_flag == 2:
        mystring = "%s-%s" % (atom_number[1], atom_number[2])
    else:
        print "no such atom_number ???"
        exit(1)
        
    return mystring

def contract_atom_section(typebasis):
    """
    contract list to strings
    """
    atom_list = typebasis['atom_list']
    element = typebasis['element']
    basis = typebasis['basis']
    cbas = typebasis['cbas']
     
    mystr = "%3s" % element
    n_list = len(atom_list)
    i_list = 0
    for atom_number in atom_list:
        i_list += 1
        if i_list == n_list:
            mystr += contract_atom_number(atom_number) + "   \\ \n" + "   "
        else:
            mystr += contract_atom_number(atom_number) + ","            
        if i_list % 10 == 9:
            mystr += "   \\  \n"
            mystr += "   "    
    
    if basis != "":
        extra_string = basis + "\n   "
    if cbas != "":
        extra_string += cbas + "\n"
    
    mystr += extra_string 

    return mystr

def contract_atom_basis(atom_basis):
    """
    change to strings
    """
    basis_string = []
    for basis in atom_basis:
        #print basis['atom_list']
        mystr = contract_atom_section(basis)
        basis_string.append(mystr)

    basis_string.insert(0, "$atoms\n")
    return basis_string

def read_one_block(fp):
    """
    read in one block in control file
    """
    block = []
    title = ""
    line = fp.readline()
    if line.strip() != "":
        title = line.split()[0]
        block.append(line)
    else:
        return title, block

    while line != "":
        pos = fp.tell()
        line = fp.readline()
        if line.strip() == "":
            break
        if line[0] == "$":
            fp.seek(pos)
            break
        block.append(line)
        
    return title, block

def read_control_block():
    """
    read the control file
    """
    fp = open("control", "r")
    title = "haha"
    name_list = []
    name_dict = {}
    while True:
        title, block = read_one_block(fp)
        if title != "":
            # print title, block
            name_dict[title] = block
            name_list.append(title)
        else:
            break

    return name_list, name_dict


def modify_dim_block(dims):
    """
    modify $rundimensions block
    $rundimensions
    dim(fock,dens)=408180
    natoms=80
    nshell=390
    nbf(CAO)=900
    nbf(AO)=850
    dim(trafo[SAO<-->AO/CAO])=1000
    rhfshells=1
    """
    dims2 = []
    for line in dims:
        if 'dim(fock,dens)' in line:
            rec = line.split("=")
            tmp_line = rec[0] + "=" + str(4*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        elif 'natoms' in line:
            rec = line.split("=")
            tmp_line = rec[0] + "=" + str(2*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        elif 'nshell' in line:
            rec = line.split("=")
            tmp_line = rec[0] + "=" + str(2*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        elif 'nbf(CAO)' in line:
            rec = line.split("=")
            tmp_line = rec[0] + "=" + str(2*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        elif 'nbf(AO)' in line:
            rec = line.split("=")
            n_basis_double = 2 * int(rec[1])
            tmp_line = rec[0] + "=" + str(2*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        elif 'dim(trafo[SAO<-->AO/CAO])' in line:
            rec = line.split("=")
            tmp_line = rec[0] + "=" + str(2*int(rec[1])) + "\n"
            dims2.append(tmp_line)
        else:
            dims2.append(line)

    return dims2, n_basis_double


def create_falk_control(n_atom):
    """
    modify the control file
    """
    # read in control
    name_list, name_dict = read_control_block()
    # atoms section
    content = get_atom_basis(name_dict)    
    # double basis define
    atom_basis = extend_atom_basis(content)
    atom_basis2 = double_atom_basis(atom_basis, n_atom)    
    atoms_block = contract_atom_basis(atom_basis2)
    name_dict['$atoms'] = atoms_block

    # $rundimensions
    dim = name_dict['$rundimensions']
    name_dict['$rundimensions'], n_basis_double = modify_dim_block(dim)

    # $scfiterlimit
    name_dict['$scfiterlimit'] = ["$scfiterlimit        0"]

    # Change the states involved
    state = set(["$statistics", "$numprocs", "$exopt", "metastase", "$2e-ints_shell_statistics"])
    name_dict2 = {}
    for key in name_dict:
        if key in state:
            continue
        else:
            name_dict2[key] = name_dict[key]
    name_dict2 = name_dict
    
    name_list2 = []
    for key in name_list:
        if key in state:
            continue
        else:
            name_list2.append(key)

    name_list = name_list2
    # $intsdebug
    n_block = len(name_list) 
    name_list.insert(n_block-2, "$intsdebug")
    name_dict['$intsdebug'] = ["$intsdebug cao \n"]

    # punch it
    fp = open("control_new", "w")
    for key in name_list:
        block = name_dict[key]
        for line in block:
            print >>fp, line,
    fp.close()

    shutil.copyfile("./control_new", "./control")

    return n_basis_double


#############################################################


def create_falk_mos(n_basis_double) :

    fileout3=open('mos_new', 'w')
    fileout3.write('$scfmo   expanded   format(4d20.14) ')
    for i_mo in range(n_basis_double) :
        fileout3.write('\n     '+str(i_mo+1)+'  a      eigenvalue=0.00000000000000D-00   nsaos='+str(n_basis_double)+'')
	for i_ao in range(n_basis_double) :
            if ( (i_ao+1) % 4) == 1 :
               fileout3.write('\n')
            fileout3.write('0.10000000000000D+00')
        
    fileout3.write('\n$end ')
    fileout3.close()
    shutil.copyfile("./mos_new", "./mos")


if __name__ == "__main__":
    atom_lines = """c  1-6,8,10,14-17,19,21-22,24-28,30,32,35-36,41-46, \\
   48,50,54-57,59,61-62,64-68,70,72,75-76   \\
   basis =c def2-SVP"""
    atom_section = atom_lines.split("\n")

#    extend_atom_string("1-6")
#    extend_atom_list("1-6,8,10,14-17,19,21-22,24-28,30,32,35-36,41-46")
    #extend_atom_section(atom_section)

    #name_list, name_dict = read_control_block()
    #content = get_atom_basis(name_dict)

    
    # content = read_atom_basis()

    #atom_basis = extend_atom_basis(content)

    #atom_basis2 = double_atom_basis(atom_basis, 80)
    
    #contract_atom_basis(atom_basis2)

    #modify_control_block(80)

    
    # read_atom_section(atom_lines)
    n_atom = 24
    creat_falk_coord (n_atom)
    n_basis_double = create_falk_control(n_atom)
    create_falk_mos(n_basis_double)
