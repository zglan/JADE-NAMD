#! /usr/bin/env python2

import os
import shutil
import optparse
import sys

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/gtools/")

import geoman

# 
# notes:
# in pe_time.out file
# i_step&i_time&pe_all(1:n)&pe_index
# time in fs. & pe in a.u.
#
#



def callbackParam(option, opt_str, value, parser):
    '''Prevent multiple geometrical parameters being selected.'''
    if parser.values.param:
        raise optparse.OptionValueError('cannot use %s option with --%s' %
                                        (opt_str, parser.values.param))
    parser.values.param = option.dest
    parser.values.atomList = value


class geom_time():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "mytmp.dat"
        self.params['resfilename'] = "geom_aver.dat"
        self.params['mydir'] = "tmpdirs"
        return


    def getcmd(self):
        """
        parameters
        """
        # Parse command-line options
        usage = 'usage: %prog [options] file'
        description = 'Extracts XYZ geometries or geometrical parameters from ' + \
                  'a Molden or XYZ trajectory file. By default, atoms and ' + \
                  'geometries are numbered starting from one. Negative ' + \
                  'numbers count back from the last atom/geometry.'
        parser = optparse.OptionParser(usage=usage, description=description)
        parser.set_defaults(param=None, range=[], atomList=[], scaleIndex=1,
                            countStart=1)
        parser.add_option('--range', '-r', action='store', type='int', nargs=2, 
                          dest='range', metavar='R1 R2',
                          help='limit output to geometry range from R1 to R2')
        parser.add_option('--length', '-l', action='callback', type='int', nargs=2,
                          callback=callbackParam, dest='length', metavar='A1 A2',
                          help='calculate bond length (magnitude of A1-A2)')
        parser.add_option('--angle', '-a', action='callback', type='int', nargs=3,
                          callback=callbackParam, dest='angle', metavar='A1 A2 A3',
                          help='calculate bond angle (angle between vectors '
                          'A1-A2 and A2-A3)')
        parser.add_option('--dihedral', '-d', action='callback', type='int',
                          nargs=4, callback=callbackParam, dest='dihedral',
                          metavar='A1 A2 A3 A4',
                          help='calculate dihedral angle (angle between planes '
                          'A1-A2-A3 and A2-A3-A4)')
        parser.add_option('--outofplane', '-o', action='callback', type='int',
                          nargs=4, callback=callbackParam, dest='outofplane',
                          metavar='A1 A2 A3 A4',
                          help='calculate out of plane angle (angle between '
                          'plane A1-A2-A3 and vector A2-A4)')
        parser.add_option('--sphereradius', '-x', action='callback', type='int',
                          nargs=0, callback=callbackParam, dest='radius',
                          metavar='',
                          help='calculate radius of a sphere..')        
        parser.add_option('--scale-index', '-s', action='store', type='int',
                          dest='scaleIndex', metavar='N',
                          help='scale output of step numbers by a factor N')
        parser.add_option('--zero-based', '-z', action='store_const', const=0,
                          dest='countStart',
                          help='count atoms/geometries starting from zero instead '
                          'of one')
    
        (options, arguments) = parser.parse_args()
        if len(arguments) != 1:
            parser.error('incorrect number of arguments')
      
        self.params['parser'] = parser
        self.params['options'] = options
        self.params['arguments'] = arguments
        
        return


    def get_status(self):
        """
        read in prepare.dat
        """
        filename = "prepare.dat"
        fp = open(filename, "r")
        line = fp.readline()
        rec = line.split()
        n_traj = int(rec[0]); n_step = int(rec[1])
        line = fp.readline()
        traj = {}
        for i in xrange(n_traj):
            line = fp.readline()
            rec = line.split()
            key = rec[0]
            traj[key] = {'complete': int(rec[1]), 'n_step': int(rec[2]),
                         'n_active': int(rec[3]), 'ratio': float(rec[4])
            }

        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        steps = [0 for i in xrange(n_step)]
        for i in xrange(n_step):
            line = fp.readline()
            rec = line.split()
            steps[i] = int(rec[1])
        self.status = {'n_step': n_step, 'n_traj': n_traj,
                       'traj': traj, 'steps': steps  
        }
        return        


    def __one_traj(self, sid):
        """
        read in one traj.
        """
        this_traj = self.status['traj'][sid]
        n_step = this_traj['n_active']
        
        filename = self.params['filename']
        fp = open(filename, "r")
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        for i_step in xrange(n_step):            
            line = fp.readline()
            rec = line.split()            
            mystep = int(rec[0])
            val = float(rec[1])
            
            self.results[i_step][0] = mystep
            self.results[i_step][1] += val
        fp.close()

        return


    def read_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        n_step = self.status['n_step']
         
        self.results = [[] for i in xrange(n_step)]
        for i_step in xrange(n_step):
            self.results[i_step] = [0 for i in xrange(2)]

        
        for sid in traj:
            os.chdir(sid)
            self.__one_traj(sid)            
            os.chdir("../")
            
        return


    def prep_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        filename = "myplot.plt"
        fp = open(filename, "w")
        print >>fp, "plot ",
        # backup mygeom.dat in one-directory
        mydir = self.params['mydir']
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
        os.mkdir(mydir)
        jobfilename = self.params['filename']
        for sid in traj:
            os.chdir(sid)
            print "running <%s> job.." % sid
            geoman.geoman(self.params)
            shutil.copy2(jobfilename, "../"+mydir+"/"+sid+".dat")
            os.chdir("../")
            print >>fp, "'./" + sid+ ".dat" +  "'" + " u 1:2,",
        fp.close()

        return



    def aver_traj(self):
        """
        add values
        """
        n_step = self.status['n_step']
        steps = self.status['steps']
         
        for i_step in xrange(n_step):
            self.results[i_step][1] /= steps[i_step]

        return



    def dump(self):
        """
        dump pe results
        """
        res = self.results
        filename = self.params['resfilename']
        mydir = self.params['mydir']
        fp = open(filename, "w")
        for mystep in res:
            print >>fp, "%10d %12.6f" % (mystep[0], mystep[1]),
            for val in mystep[2:]:
                print >>fp, "%15.8f" % (val),
            print >>fp, ""
        fp.close()
        
        shutil.copy2(filename, mydir)

        return

    
if __name__ == "__main__":
    pe = geom_time()
    pe.getcmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        
