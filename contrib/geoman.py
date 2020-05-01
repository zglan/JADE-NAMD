#! /usr/bin/env python
#
#
# -------------------------------------
# geoman.py version 2
# This is taken from mndo codes.
# @ dulikai @qibebt @Qingdao
# @ 2014.5.14
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


def geoman(config):
    '''Routine for analysing trajectories.'''

    # Parse command-line options
    parser = config['parser']
    options = config['options']
    arguments = config['arguments']

    filename = config['filename']
    file_handler = open(filename, "w")
    __console__ = sys.stdout
    if 'stdout_mode' not in config.keys():
        sys.stdout = file_handler
    
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
    if options.param == 'length' or options.param == "radius":
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
        elif options.param == 'radius':
            sphereRadius = geom.getSphereRadius() 
            sys.stdout.write('%4i   %14.8f\n' % (reportedStep, sphereRadius))
            
    file_handler.close()
    sys.stdout = __console__
    return


if __name__ == '__main__':
    geoman()
