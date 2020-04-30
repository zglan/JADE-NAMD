#!/usr/bin/python
#
# --------------------------------------
#
# geoman.py
#
# Tom Keal, October 2007
#
# Based on the original Fortran program
# geoman.f90 by Eduardo Fabiano
#
# --------------------------------------
#
import sys
import optparse
import math
import mndotools

def main():
    '''Routine for analysing trajectories.'''

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

    # Load in the trajectory
    traj = mndotools.XYZFile(arguments[0])

    # Check that specified atoms/geometries are in range
    for i in options.range:
        if (abs(i) < options.countStart or i < -traj.noOfGeoms or
            i > traj.noOfGeoms - (1 - options.countStart)):
            parser.error('invalid geometry number: %i' % i)
    for i in options.atomList:
        if (abs(i) < options.countStart or i < -traj.noOfAtoms or
            i > traj.noOfAtoms - (1 - options.countStart)):
            parser.error('invalid atom number: %i' % i)        

    # Determine the range of geometries, taking into account:
    #  - User-supplied range includes final value, python ranges don't
    #  - User-supplied range may be one or zero based, python is zero-based.
    # The final values of start/stop follow python conventions
    if options.range:
        start = options.range[0]
        stop = options.range[1]
        # Negative numbers count back from the end, like a python list
        # This should be invariant to whether the user counts from 0 or 1,
        # so we need to correct for countStart here
        if start < 0:
            start += (traj.noOfGeoms + options.countStart)
        if stop < 0:
            stop += (traj.noOfGeoms + options.countStart)
        # Convert to python conventions
        #  - User range is inclusive of the last number, unlike a python range
        stop += 1
        #  - Convert to zero-based if not already
        start -= options.countStart
        stop -= options.countStart
    else:
        start = 0
        stop = traj.noOfGeoms

    # If no parameter is specified, just print out the XYZ geometries in range
    if not options.param:
        startLine = start * (traj.noOfAtoms + 2)
        stopLine = stop * (traj.noOfAtoms + 2)
        for i in range(startLine, stopLine):
            sys.stdout.write(traj.fileContents[i])
        sys.exit(0)

    # A parameter is specified
    sys.stdout.write('# %s: %s - %i-based counting\n' %
                     (options.param, options.atomList, options.countStart))
    if options.param == 'length':
        sys.stdout.write('#\n#step      distance\n') 
    else:
        sys.stdout.write('#\n#step     angle [deg]       angle [rad]\n')
    for i in range(start, stop):
        geom = traj.getGeom(i)
        reportedStep = (i + options.countStart) * options.scaleIndex
        # mndotools counts from zero internally, so correct by countStart here
        if options.param == 'length':
            bondLength = geom.getBondLength(
                options.atomList[0] - options.countStart,
                options.atomList[1] - options.countStart)
            sys.stdout.write('%4i   %14.8f\n' % (reportedStep, bondLength))
        elif options.param == 'angle':
            bondAngleRad = geom.getBondAngle(
                options.atomList[0] - options.countStart,
                options.atomList[1] - options.countStart,
                options.atomList[2] - options.countStart,
                False)
            bondAngleDeg = bondAngleRad * (180.0 / math.pi)
            sys.stdout.write('%4i   %14.8f   %14.8f\n' %
                             (reportedStep, bondAngleDeg, bondAngleRad))
        elif options.param == 'dihedral':
            dihedralRad = geom.getDihedralAngle(
                options.atomList[0] - options.countStart,
                options.atomList[1] - options.countStart,
                options.atomList[2] - options.countStart,
                options.atomList[3] - options.countStart,
                False)
            dihedralDeg = dihedralRad * (180.0 / math.pi)
            sys.stdout.write('%4i   %14.8f   %14.8f\n' %
                             (reportedStep, dihedralDeg, dihedralRad))
        elif options.param == 'outofplane':
            outOfPlaneRad = geom.getOutOfPlaneAngle(
                options.atomList[0] - options.countStart,
                options.atomList[1] - options.countStart,
                options.atomList[2] - options.countStart,
                options.atomList[3] - options.countStart,
                False)
            outOfPlaneDeg = outOfPlaneRad * (180.0 / math.pi)
            sys.stdout.write('%4i   %14.8f   %14.8f\n' %
                             (reportedStep, outOfPlaneDeg, outOfPlaneRad))
        

def callbackParam(option, opt_str, value, parser):
    '''Prevent multiple geometrical parameters being selected.'''
    if parser.values.param:
        raise optparse.OptionValueError('cannot use %s option with --%s' %
                                        (opt_str, parser.values.param))
    parser.values.param = option.dest
    parser.values.atomList = value


if __name__ == '__main__':
    main()
