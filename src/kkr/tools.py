#!/usr/bin/env python

# python

import json
import os
import re
import sys


def interface_converter(filename="qm_interface"):
    """
    $ du
    @ convert 'qm_interface from md' to 'xyz & parm' format file.
    @
    """
    interface_file = filename

    print("--- read whole interface file ---")
    file_in = open(interface_file, 'r')
    line_all = file_in.read()
    file_in.close()
    # split lines
    line_each = line_all.split('\n')
    n_line = len(line_each)

    # read QC related parameters        
    flag = 0
    for cur_line in line_each:
        i_find_geom = re.search('Number of atom', cur_line)
        if i_find_geom is not None:
            n_atom = int(cur_line.split(":")[1])
            flag += 1
            print("Number of atoms", n_atom)

        i_find_state1 = re.search('Number of state', cur_line)
        if i_find_state1 is not None:
            n_state = int(cur_line.split(":")[1])
            print("Number of states", n_state)
            flag += 1

        i_find_state2 = re.search('Current state', cur_line)
        if i_find_state2 is not None:
            i_state = int(cur_line.split(":")[1])
            print("Current state", i_state)
            flag += 1

        i_find_package = re.search('Quan-Chem package:', cur_line)
        if i_find_package is not None:
            useful_dat = cur_line.split(":")[1]
            record = useful_dat.split()
            i_method = int(record[0])
            i_time = int(record[1])
            print("current time ", i_time)
            flag += 1

    if flag < 4:
        print("some data in the interface file cannot be found ???")
        sys.exit(0)
    else:
        parm = {'n_atom': n_atom, 'n_state': n_state, 'i_state': i_state, 'qm_method': i_method, \
                'i_time': i_time}

    # --------------------------------------------------------------------------	
    # read cart. coordinates of atoms from interface_file.
    atoms = []
    # seek to the target line
    for i_line in range(n_line):
        i_find_geom = re.search('Current Geometry', line_each[i_line])
        if i_find_geom is not None:
            i_line = i_line + 3
            break
    # read in coordinates
    for i_atom in range(n_atom):
        rec = {}
        cur_record = line_each[i_line].split()
        rec['name'] = cur_record[0].lower()
        # read in coordinates in string type. to maintain the precise between each.
        rec['coord'] = [cur_record[1], cur_record[2], cur_record[3]]
        atoms.append(rec)
        i_line = i_line + 1
    mol = {'natom': n_atom, 'atoms': atoms}
    data = {'parm': parm, 'mol': mol}
    dump_data('interface.json', data)

    return data


def dump_data(filename, obj):
    """
    dump data in to disk in a special format.
    wrap internal storage method.
    """
    dump_json(filename, obj)

    return


def load_data(filename):
    """
    load data into memory from disk
    wrap internal storage method.
    """
    if os.path.isfile(filename):
        obj = load_json(filename)
    else:
        print("CANNOT FIND file: %s" % filename)
        sys.exit(1)

    return obj


def dump_json(filename, obj):
    """
    dump an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='w')
    my_str = json.dumps(obj, indent=2)
    fp.write(my_str)
    fp.close()

    return


def load_json(filename):
    """
    load an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='r')
    obj = json.load(fp)

    return obj


def make_path(strlist=[], spliter="/"):
    """ path make """
    path = spliter.join(strlist)
    if strlist == []:
        path = "./"
    return path


if __name__ == "__main__":
    self = 0
    interface_converter()
