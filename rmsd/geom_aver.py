#! /usr/bin/env python
import os
import numpy as np

def aver_single(filename):
    savefile = filename + '_aver'    
    xx = np.loadtxt(filename)
    savelist = []
    try :
        for i in range(np.shape(xx)[1]):
            aver = np.mean(xx[:,i])
#            if aver > 90:
#                aver = 180 - aver
            savelist.append(aver)
            np.savetxt(savefile,savelist)
    except:
        np.savetxt(savefile,xx) 
def aver_many(xnum,ynum):
    for i in range(xnum):
        for j in range(ynum):
            filename = "geom_" + str(i+1) + "_" + str(j+1) + ".dat"
            if os.path.isfile(filename):
                aver_single(filename)
def paste_aver(lis):
    savelis = []
    for name in lis:
        savelis.append(np.loadtxt(name))
    np.savetxt('result.dat',savelis)

if __name__ == "__main__":
    xnum = 60
    ynum = 30
    lis = ['geom_2_1.dat_aver','geom_3_1.dat_aver','geom_4_1.dat_aver','geom_5_1.dat_aver','geom_6_1.dat_aver','geom_7_1.dat_aver','geom_8_1.dat_aver','geom_9_1.dat_aver']
    aver_many(xnum,ynum)
    paste_aver(lis)
