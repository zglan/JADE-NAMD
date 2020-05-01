#! /usr/bin/env python

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


class geom_worker():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "mytmp.dat"
        self.params['stdout_mode'] = "yes"
        
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
                  'numbers count back from the last atom/geometry.' + \
                  'Please note the default output filename is mytmp.dat'
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

    def prep_traj(self):
        """
        read all traj...
        """
 
        geoman.geoman(self.params)
 
        return
    
if __name__ == "__main__":
    pw = geom_worker()
    pw.getcmd()
    pw.prep_traj()

