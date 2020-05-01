#! /usr/bin/env python

import numpy as np

# frequency domain analysis
# suppose we have the time domained data
# such as the bond length vibration along with time
#
#

class FreqDomain():
    """
    try to perform frequency domain analysis
    """
    def __init__(self):
        self.config = {}
        
        return

    def read_cmd(self):
        """ read in control parameters
        """
        line = raw_input("Enter the actual number of sampling points: \n > ")
        self.config['n_sampling_points'] = int(line)
        # file list
        sampling_files = []
        print "Set up analysis files"
        while True:
            line = raw_input("Enter the list of filename to be analyzed: \n > ")
            if line.strip() == "":
                break
            sampling_files.extend(line.split())
        self.config['sampling_files'] = sampling_files
        self.config['n_sampling_files'] = len(sampling_files)

        return

    
    def do_fft(self, filename = '10.dat'):
        """
        fft action on a set of data
        x, y
        """
        #
        nx = self.config['n_sampling_points']
        # #
        fp = open(filename, "r")
        # ignore the first three lines
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        y = []
        for i in xrange(nx):
            line = fp.readline()
            if line.strip() == "":
                print "too many sampling points ???"
                exit(10)
            rec = [float(d) for d in line.split()]
            y.append(rec[1])
        fp.close()
        # fft 
        yf = np.fft.fft(y)
        T = 1.0 / nx
        xf = np.linspace(0.0, 1.0/(2.0*T), nx/2)
        yft = 2.0/nx * np.abs(yf[0:nx/2])
        # dump freq.
        freqfile = "freq-" + filename
        fp = open(freqfile, 'w')
        for dx, dy in zip(xf, yft):
            print >>fp, "%12.6f%12.6f" % (dx, dy)
        fp.close()
    
        return xf, yft

    def collect(self, filelist = []):
        """
        do fft for a series of files
        """
        N = self.config['n_sampling_points']
        filelist = self.config['sampling_files']
        n_filelist = self.config['n_sampling_files']
        #
        ave_xf = np.zeros(N/2)
        ave_yf = np.zeros(N/2)
        fp = open("collect.dat", 'w')
        for filename in filelist:
            xf, yf = self.do_fft(filename)
            ave_xf += xf / n_filelist
            ave_yf += yf / n_filelist
        for dx, dy in zip(ave_xf, ave_yf):
            print >>fp, "%12.6f%12.6f" % (dx, dy)
        fp.close()
        
        return
 

if __name__ == "__main__":
    fd =  FreqDomain()
    fd.read_cmd()
    fd.collect()
    
    

