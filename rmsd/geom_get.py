#! /usr/bin/env python
import numpy as np
import shutil
import sub_geo as geo
import os
import sub_split_coord as spl

# input file is 'input.xyz' in which some traj geoms are saved
# 'geo.inp' is required
# after run this script a 'geom.dat' file will generate

def get_single():
    fp = open('geo.inp','r')
    num = 0
    save_list = []
    for line in fp:
        val = line.strip().split()
        if val[0] == "distance":
            dis = geo.get_dist(int(val[1]),int(val[2]))
        if val[0] == "angle":
            dis = geo.get_angle(int(val[1]),int(val[2]),int(val[3]))
        if val[0] == "dihedral":
            dis = geo.get_dihedral(int(val[1]),int(val[2]),int(val[3]),int(val[4]))
        save_list.append(dis)
        num = num+1
    return save_list

def get_many():
    dir = os.getcwd()
    m = 0
    save_block = []

    spl.make()

    for parentdir,dirname,filenames in os.walk(dir):
        for filename in filenames:
            if 'all_sample' in filename :
                m=m+1
    for i in range(m):
        filename = 'all_sample.xyz_' + str(i+1)
        command = 'cp ' + filename + ' geo.xyz'
        os.system(command)
        lis = get_single()
        save_block.append(lis)
    np.savetxt('geom.dat', save_block)


def get_all():
    curr_path = os.getcwd()
    work_path = curr_path + '/all'
    job_path = work_path + '/job_path'
    save_file = curr_path + '/geom_save'
    
    if os.path.exists(save_file):
        shutil.rmtree(save_file)
    os.mkdir(save_file)
    os.chdir(work_path)
#   read the block num
    workfile = 'split.dat'
    if os.path.exists(workfile):
        fp = open(workfile,"r")
        line = fp.readline()
        line = fp.readline()
        xmin,xmax,ymin,ymax,xnum,ynum = line.split()
    else:
        print "Error: There is not a file named split.dat \n\tMaybe you should run plot_mds.py first"
    os.chdir(curr_path)

    for i in range(int(xnum)):
        for j in range(int(ynum)):
            filename = work_path + '/geom_rmsd_' + str(i+1) + '_' + str(j+1) + '.xyz'
            print "%s_%s work is doing....." % (str(i+1),str(j+1))
            if os.path.isfile(filename):
                if os.path.exists(job_path):
                    shutil.rmtree(job_path)
                os.mkdir(job_path)
                command1 = 'cp geo.inp ' + job_path
                command2 = 'cp ' +  filename + ' ' + job_path + '/input.xyz'
                os.system(command1)
                os.system(command2)
                os.chdir(job_path)
                get_many()
                command3 = 'cp geom.dat ' + save_file + '/' + 'geom_' + str(i+1) + '_' + str(j+1) + '.dat'
                os.system(command3)
                os.chdir(curr_path) 
                shutil.rmtree(job_path)


if __name__ == "__main__":
    get_all()

