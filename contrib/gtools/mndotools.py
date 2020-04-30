#!/usr/bin/python
#
# --------------------
#
#  mndotools.py
#
#  Tom Keal, 2007-2008
#
# --------------------
#

"""mndotools

A set of classes for creating and interpreting MNDO input and output files.

RawFile
InputFile(RawFile)
OutputFile(RawFile)
XYZFile(RawFile)
XYZGeom
XYZPoint
ZMatrixGeom
ZMatrixPoint
VelocityFile(RawFile)
XYZVelocity
PeriodicTable

WARNING: These classes support only MNDO keyword=value input files.
         'Standard input' and 'MOPAC input' are NOT supported.

"""

import math
import string
import sys

class RawFile:
    
    """Hold the contents of an arbitrary file and analyse it."""
    
    def __init__(self, fileName):
        """Load in the entire file as a list."""
        self.fileName = fileName
        try:
            f=open(fileName, 'r')
            self.fileContents = f.readlines()
            f.close()
        except IOError:
            sys.stderr.write("Error: could not read in %s\n" % fileName)
            sys.exit(1)

    def searchForString(self, searchString, findFinal, startLine=-1):
        """Search for a string within the file.

        findFinal - if true, return the last occurence, else find the first
        startLine - start the search from this line (numbered from zero)

        Returns the list index of the matching line (i.e. the line number
        starting from zero),
        Returns -1 if the string wasn't found.

        """
        foundLine = -1
        lineNumber = -1
        for line in self.fileContents:
            lineNumber += 1
            if line.find(searchString) != -1 and lineNumber >= startLine:
                foundLine = lineNumber
                if not findFinal:
                    break
        return foundLine


class InputFile(RawFile):
    
    """Hold an MNDO input file and analyse it."""
    
    def __init__(self, fileName):
        RawFile.__init__(self, fileName)

    def getLastOptionLine(self):
        """Return line number of last line of keyword options.

        The last line of keyword options in an MNDO keyword input file is
        also the first line with no '+' symbol, which is what we search for.

        Return the list index of the last line (line number starting from zero)

        """
        lineNumber = -1
        for line in self.fileContents:
            lineNumber += 1
            if line.find('+') == -1:
                break
        return lineNumber

    def getLastGeomLine(self):
        firstGeomLine = self.getLastOptionLine() + 3
        lineNumber = firstGeomLine
        for line in self.fileContents[firstGeomLine:]:
            rawLine = line.split()
            if rawLine[0] == '0':
                break
            lineNumber += 1
        return lineNumber

    def parseKeywords(self, forceLowerCase=True):
        """Parse standard MNDO keyword=value pairs in the input file.

        Return a tuple containing:
          mndoKeyOrder - an ordered list of keywords (and '+' signs to mark
                         line endings)
          mndoKeyVals  - a dictionary containing keyword=value pairs.
                         All values are stored as strings.

        The order of keywords is not important in an MNDO input, but
        it may be convenient to retain the logical order of the original
        input file.
        
        The special case of keywords that are also MOPAC keywords should also
        be noted (e.g. dmax). These must be kept on the fourth line or later,
        otherwise the input file will be recognised by MNDO as a MOPAC input.

        forceLowerCase - if true (default), convert all keywords to lower case
                         else leave them as they were in the original file.
                         Forcing a change of case prevents accidental multiple
                         storage of the same keyword with different cases.
                         
        WARNING: This routine supports only MNDO keyword=value options.
                 'Standard input' and 'MOPAC input' are NOT supported.
 
        """
        mndoKeyOrder = []
        mndoKeyVals = {}        
        lastOptionLine = self.getLastOptionLine()
        for line in self.fileContents[:lastOptionLine + 1]:
            for rawPair in line.split():
                if rawPair == '+':
                    mndoKeyOrder.append('+')
                    # Like MNDO's own parser, we ignore any text
                    # after a plus symbol
                    break
                kwPair = rawPair.split('=')
                if len(kwPair) != 2 or kwPair[0] == '' or kwPair[1] == '':
                    sys.stderr.write("Warning: badly formatted keyword (%s) "
                                     "ignored.\n" % rawPair)
                    continue
                key = kwPair[0]
                val = kwPair[1]
                if forceLowerCase:
                    key = key.lower()
                if mndoKeyVals.has_key(key):
                    sys.stderr.write("Warning: already defined keyword (%s) "
                                     "ignored.\n" % key)
                else:
                    mndoKeyVals[key] = val
                    mndoKeyOrder.append(key)
        return (mndoKeyOrder, mndoKeyVals)

    def parseCartesianGeometry(self):
        """Parse Cartesian geometry."""
        lastOptionLine = self.getLastOptionLine()
        cartesianGeom = XYZGeom()
        for line in self.fileContents[lastOptionLine + 3:]:
            rawLine = line.split()
            if rawLine[0] == '0':
                break
            cartesianGeom.addAtom(rawLine[0], rawLine[1], rawLine[3],
                                 rawLine[5])
        return cartesianGeom

    def parseInternalGeometry(self):
        """Parse internal geometry."""
        lastOptionLine = self.getLastOptionLine()
        internalGeom = ZMatrixGeom()
        for line in self.fileContents[lastOptionLine + 3:]:
            rawLine = line.split()
            if rawLine[0] == '0':
                break
            internalGeom.addAtom(rawLine[0], rawLine[1], rawLine[3],
                                 rawLine[5], int(rawLine[7])-1,
                                 int(rawLine[8])-1,
                                 int(rawLine[9])-1)
        return internalGeom
            

class DynvarFile(RawFile):

    """Hold an MNDO dynamics input file and analyse it."""

    def __init__(self, fileName):
        RawFile.__init__(self, fileName)

    def parseNamelist(self, forceUpperCase=True):
        """Parse the dynvar namelist.

        Returns a tuple containing:
          dynvarKeyOrder - ordered list of keywords.
          dynvarKeyVals  - dictionary of keyword=value pairs.
                           All values are stored as strings.

        The order of keywords is not important in a dynvar input, but
        it may be convenient to retain the logical order of the original
        input file.

        forceUpperCase - if true (default), convert all keywords to upper case
                         else leave them as they were in the original file.
                         Forcing a change of case prevents accidental multiple
                         storage of the same keyword with different cases.

        """
        dynvarKeyOrder = []
        dynvarKeyVals = {}
        if self.fileContents[0].upper().find('&DYNVAR') == -1:
            sys.stderr.write("Warning: first line of dynvar file does not "
                             "contain '&DYNVAR'.\n")
        if self.fileContents[-1].find('/') == -1:
            sys.stderr.write("Warning: last line of dynvar file does not "
                             "contain '/'.\n")
        for line in self.fileContents[1:-1]:
                kwPair = line.split('=')
                if len(kwPair) != 2:
                    sys.stderr.write("Warning: badly formatted keyword (%s) "
                                     "ignored.\n" % line.strip())
                    continue
                kwPair[0] = kwPair[0].strip()
                kwPair[1] = kwPair[1].strip(string.whitespace + ',')
                if kwPair[0] == '' or kwPair[1] == '':
                    sys.stderr.write("Warning: badly formatted keyword (%s) "
                                     "ignored.\n" % line.strip())
                    continue
                key = kwPair[0]
                val = kwPair[1]
                if forceUpperCase:
                    key = key.upper()
                if dynvarKeyVals.has_key(key):
                    sys.stderr.write("Warning: already defined keyword (%s) "
                                     "ignored.\n" % key)
                else:
                    dynvarKeyVals[key] = val
                    dynvarKeyOrder.append(key)
        return (dynvarKeyOrder, dynvarKeyVals)


class OutputFile(RawFile):
    
    """Hold an MNDO output file and analyse it."""
    
    def __init__(self, fileName):
        RawFile.__init__(self, fileName)

    def getMappingInfo(self, findFinal):
        """Extract information about active space mapping.

        NB: The keywords imomap=1, ioutci>0 must be specified for this
        information to be printed

        findFinal - if true, find the last occurence of active space mapping,
                    otherwise find the first occurence.

        Return a tuple containing:
         - activeOrbitals - a list of the active molecular orbitals
         - mapOverlap - a list of the 'overlaps' with previous MOs
                        (0.0 if mapping failed)

        The active orbitals are determined from the ACTIVE column of the
        eigenvalue table (as orbitals that failed to map do not appear in the
        MATCHED ACTIVE ORBITALS table)

        Overlap values are taken from the MATCHED ACTIVE ORBITALS table, or
        set to 0.0 if the corresponding orbital is missing

        Return None if the information could not be found

        """
        # Find where the information is
        header = 'MATCHED ACTIVE ORBITALS (OVERLAP OVER 0.5):'
        mapLineNo = self.searchForString(header, findFinal)
        if mapLineNo == -1:
            sys.stderr.write("Warning: could not find orbital mapping "
                             + "header.\n")
            return None
        # skip to the real data
        mapLineNo += 4
        # Find the nearest eigenvalue info afterwards
        header = 'MO     EIGENVALUE     LABEL   NSYM  IMOSYM   OCC.  ACTIVE' 
        eigenvalueLineNo = self.searchForString(header, False, mapLineNo)
        if eigenvalueLineNo == -1:
            sys.stderr.write("Warning: could not find eigenvalue "
                             + "header.\n")
            return None
        # skip to the real data
        eigenvalueLineNo += 2
        # Check which orbitals really were active
        activeOrbitals = []
        mapOverlap = []
        line = self.fileContents[eigenvalueLineNo].split()
        mo = 1
        dataLineCols = 7
        if len(line) == 0:
            sys.stderr.write("Warning: could not recognise eigenvalue "
                             + "information formatting (missing?).\n")
            return None            
        while len(line) > 0:
            # Test our assumptions about formatting
            if int(line[0]) != mo:
                sys.stderr.write("Warning: could not recognise eigenvalue "
                             + "information formatting (MO).\n")
                return None                
            if len(line) != dataLineCols:
                sys.stderr.write("Warning: could not recognise eigenvalue "
                             + "information formatting (no. of cols).\n")
                return None          
            # If active, add to list of active orbitals
            if str(line[6]) != '-':
                activeOrbitals.append(mo)
            mo += 1
            eigenvalueLineNo += 1
            line = self.fileContents[eigenvalueLineNo].split()            
        # Now get overlap information
        dataLineCols = 4
        line = self.fileContents[mapLineNo].split()
        if len(line) == 0:
            sys.stderr.write("Warning: could not recognise matched active "
                             + "orbital info formatting (missing?).\n")
            return None                    
        orb = 0
        while len(line) > 0 and orb < len(activeOrbitals):
            if len(line) != dataLineCols:
                sys.stderr.write("Warning: could not recognise matched active "
                             + "orbital info formatting (no. of cols).\n")
            if int(line[2]) != activeOrbitals[orb]:
                mapOverlap.append(0.0)
                orb += 1
            else:
                mapOverlap.append(float(line[3]))
                orb += 1
                mapLineNo += 1
                line = self.fileContents[mapLineNo].split()                
        while orb < len(activeOrbitals):
            mapOverlap.append(0.0)
            orb += 1 
        return (activeOrbitals, mapOverlap)
                
        
    def getTransitionProperties(self, formalism, findFinal):
        """Extract transition properties.

        NB: The keyword iuvcd=2 must be specified for this information to be
        printed.

        formalism - specifies the oscillator strength formalism
                    0 = f_r, 1 = f_p, 2 = f_rp
        findFinal - if true, find the last occurence of transition property
                    print out, else find the first occurence

        Return a tuple containing:
         - excitedStates - a list of the calculated electronic states
         - excitedStateEnergies - a dictionary of state energies
         - oscillatorStrengths - a dictionary of oscillator strengths according
                                 to the chosen formalism
        The dictionary keys are the states in excitedStates

        Return None if the information could not be found

        """
        excitedStates = []
        excitedStateEnergies = {}
        oscillatorStrengths = {}
        # To navigate the MNDO output file
        header = 'Properties of transitions   1 -> #:'
        linesToSkip = 3
        currentState = 2  # first state with data
        dataLineCols = 10
        # Note that energies here are in eV, relative to ground state = 0
        ESEdataColumn = 3
        # Formalism: 0 = r, 1 = p, 2 = rp
        OSdataColumn = 6 + formalism
        # Find the header
        OSLineNo = self.searchForString(header, findFinal)
        if OSLineNo == -1:
            sys.stderr.write("Warning: could not find transition properties "
                             + "header.\n")
            return None
        OSLineNo += linesToSkip
        OSLine = self.fileContents[OSLineNo].split()
        if len(OSLine) == 0:
            sys.stderr.write("Warning: could not recognise transition "
                             + "properties formatting (missing?).\n")
            return None
        # Loop over the states
        while len(OSLine) > 0:
            # Test our assumptions about the formatting
            if int(OSLine[0]) != currentState:
                sys.stderr.write("Warning: could not recognise transition "
                                 + "properties formatting (state no).\n")
                return None
            if len(OSLine) !=  dataLineCols:
                sys.stderr.write("Warning: could not recognise transition " +
                                 "properties formatting (no of cols).\n")
                return None
            # Extract the properties and move on to the next state
            excitedStates.append(currentState)
            excitedStateEnergies[currentState] = float(OSLine[ESEdataColumn])
            oscillatorStrengths[currentState] = float(OSLine[OSdataColumn])
            currentState += 1
            OSLineNo += 1
            OSLine = self.fileContents[OSLineNo].split()
        return (excitedStates, excitedStateEnergies, oscillatorStrengths)


class XYZFile(RawFile):
    
    """Hold an XYZ file containing one or more XYZ structures.

    XYZFile can also be initialised with the filename of a Molden trajectory.
    The XYZ information in the Molden file will be automatically extracted.

    """
    
    def __init__(self, fileName):
        RawFile.__init__(self, fileName)
        # Load in periodic table for future use
        self.pt = PeriodicTable()
        # Check if the file is a Molden file, and if so, remove everything
        # before the XYZ information
        moldenFile = False
        if self.fileContents[0].find('[Molden Format]') != -1:
            moldenFile = True
            startOfGeoms = self.searchForString('[GEOMETRIES] XYZ', False)
            if startOfGeoms == -1:
                sys.stderr.write("Error: could not find XYZ geometries in "
                                 "Molden file.\n")
                sys.exit(1)
            self.fileContents = self.fileContents[startOfGeoms + 1:]
        # Some useful information and very basic checks
        firstAtomLine = self.fileContents[0].split()
        try:
            self.noOfAtoms = int(firstAtomLine[0])
        except ValueError:
            sys.stderr.write("Error: could not read no. of atoms from first "
                             + "line of XYZ file.\n")
            sys.exit(1)
        if self.noOfAtoms <= 0:
            sys.stderr.write("Error: claimed no. of atoms on first line of " +
                             "XYZ file is <= 0.\n")
        # Remove any information after the XYZ geometries in a Molden file
        if moldenFile:
            atomLine = self.noOfAtoms + 2  
            while atomLine < len(self.fileContents):
                if self.fileContents[atomLine].find('[') != -1:
                    # New Molden section found
                    break
                atomLine += (self.noOfAtoms + 2)
            if atomLine < len(self.fileContents):
                self.fileContents = self.fileContents[:atomLine]
        # Cursory check of contents
        if len(self.fileContents) % (self.noOfAtoms + 2) == 0:
            self.noOfGeoms = len(self.fileContents) / (self.noOfAtoms + 2)
        else:
            sys.stderr.write("Error: XYZ file length is not an integer " +
                             "multiple of claimed individual size.\n")
            sys.exit(1)

    def getGeom(self, geomNumber):
        """Return an XYZGeom object containing a Cartesian geometry.

        geomNumber - specifies which geometry in the file should be parsed
                     (numbered from 0)
        
        Return None if the XYZ data could not be parsed.

        """
        xyzGeom = XYZGeom()
        # We calculate first line assuming that geomNumber is numbered from 0
        lineNo = geomNumber * (self.noOfAtoms + 2)
        claimedAtoms = int(self.fileContents[lineNo].split()[0])
        if claimedAtoms != self.noOfAtoms:
            sys.stderr.write("Error: claimed no. of atoms is inconsistent.\n")
            return None
        # Ignore the title line
        lineNo += 2
        for i in range(self.noOfAtoms):
            XYZLine = self.fileContents[lineNo].split()
            try:
                an = int(XYZLine[0])
            except ValueError:
                an = self.pt.getZ(XYZLine[0])
                if an is None:
                    sys.stderr.write("Error: first xyz column should be an "
                                     "atomic number or symbol.\n")
                    return None
            try:
                x = float(XYZLine[1])
                y = float(XYZLine[2])
                z = float(XYZLine[3])
            except ValueError:
                sys.stderr.write("Error: columns 2-4 should contain xyz " +
                                 "data separated by spaces.\n")
                return None
            xyzGeom.addAtom(an, x, y, z)
            lineNo += 1
        return xyzGeom

    def writeSnapshots(self, snapshots, fileName):
        """Write a new XYZ file containing snapshots from the original file.

        snapshots - list of geometries to be written (numbered from 0)
        fileName - name of the output file containing the snapshots

        The file is copied as-is, with no further checking beyond that when
        the object was initialised.

        Return -1 if unsuccessful

        Usage note: snapshots at regular intervals can be taken using 'range'
          i.e.. snapshots = range([1st snapshot], [total geoms], [interval])

        """
        try:
            f=open(fileName, 'w')
        except IOError:
            sys.stderr.write("Error: could not open %s" +
                             "for writing.\n" % fileName)
            return -1
        for snap in snapshots:
            if snap > self.noOfGeoms - 1:
                sys.stderr.write("Warning: requested snapshot %i is too "
                                 "large - ignored.\n" % snap)
                continue
            startLine = snap * (self.noOfAtoms + 2)
            for i in range(self.noOfAtoms + 2):
                f.write(self.fileContents[startLine + i])
        f.close()

            
class XYZGeom:
    
    """Hold a cartesian geometry.

    This class provides methods to calculate useful structural quantities
    such as bond lengths, bond angles, dihedral angles.

    The geometry can be written out in XYZ or MNDO formats.

    """

    def __init__(self):
        self.noOfAtoms = 0
        self.atomicNumbers = []
        self.atomCoords = []

    def addAtom(self, atomicNumber, x, y, z):
        """Adds an atom and cartesian coordinates to the geometry."""
        self.noOfAtoms += 1
        self.atomicNumbers.append(int(atomicNumber))
        newCoord = XYZPoint(float(x), float(y), float(z))
        self.atomCoords.append(newCoord)

    def getBondLength(self, a1, a2):
        """Return the distance between atom numbers a1 and a2.

        Atoms are numbered from zero.

        """
        diff = self.atomCoords[a1] - self.atomCoords[a2]
        return diff.getNorm()

    def getBondAngle(self, a1, a2, a3, degrees=True):
        """Return the bond angle a1-a2-a3.

        The angle is defined by the vectors a1-a2 and a2-a3.
        Atoms are numbered from zero.

        degrees - if true, return angle in degrees, else radians.

        """
        # Based on the bond angle routine from geoman.f90 by Eduardo Fabiano
        # vector 1 = 1->2
        v1 = self.atomCoords[a2] - self.atomCoords[a1]
        v1 = v1.normalise()

        # vector 2 = 2->3
        v2 = self.atomCoords[a3] - self.atomCoords[a2]
        v2 = v2.normalise()

        # dot product
        dotp = v1.dotProduct(v2)
 
        # angle in radians
        ang = math.pi - math.acos(dotp)
        if degrees:
            ang *= (180.0 / math.pi)
        return ang

    def getOutOfPlaneAngle(self, a1, a2, a3, a4, degrees=True):
        """Return the out of plane angle a1-a2(-a4)-a3.

        The angle is defined between the plane a1-a2-a3 and the vector a2-a4.
        Atoms are numbered from zero.

        degrees - if true, return angle in degrees, else radians.

        """
        # vector 2->1
        v21 = self.atomCoords[a1] - self.atomCoords[a2]
        v21 = v21.normalise()

        # vector 2->3
        v23 = self.atomCoords[a3] - self.atomCoords[a2]
        v23 = v23.normalise()

        # vector 2->4
        v24 = self.atomCoords[a2] - self.atomCoords[a4]
        v24 = v24.normalise()

        # vector product v21^v23
        w = v21.crossProduct(v23)
        w = w.normalise()

        # dot product
        dotp = w.dotProduct(v24)

        # angle in radians
        # using sin as we are actually calculating the angle
        # to the normal of the plane rather than the plane itself.
        ang = math.asin(dotp)        

        if degrees:
            ang *= (180.0 / math.pi)
        return ang   
                   
    def getDihedralAngle(self, a1, a2, a3, a4, degrees=True, signed=True):
        """Return the dihedral angle a1-a2-a3-a4.

        The angle is defined between the planes a1-a2-a3 and a2-a3-a4.
        Atoms are numbered from zero.

        degrees - if true, return angle in degrees, else radians.

        signed - if true, return a signed dihedral angle according to
                 MNDO conventions

        """
        # Based on the dihedral routine from geoman.f90 by Eduardo Fabiano
        # vector 1 = 1->2
        v1 = self.atomCoords[a2] - self.atomCoords[a1]
        v1 = v1.normalise()

        # vector 2 = 2->3
        v2 = self.atomCoords[a3] - self.atomCoords[a2]
        v2 = v2.normalise()

        # vector 3 = 3->4
        v3 = self.atomCoords[a4] - self.atomCoords[a3]
        v3 = v3.normalise()

        # vector product 1 = v1^v2
        w1 = v1.crossProduct(v2)
        w1 = w1.normalise()

        # vector product 2 = v3^v2
        w2 = v3.crossProduct(v2)
        w2 = w2.normalise()

        # dot product
        dotp = w1.dotProduct(w2)

        # angle in radians
        ang = math.pi - math.acos(dotp)
        if signed:
            # the dot product between the 1->2 bond and the normal to
            # the plane 2-3-4 is used to determine whether the dihedral
            # angle is clockwise or anti-clockwise
            # if the dot product is positive, the rotation is clockwise
            #
            # Taken from ChemShell FRAG_dihedral in interface.c
            #
            rotdir = v1.dotProduct(w2)
            if rotdir > 0:
                ang = -ang
        if degrees:
            ang *= (180.0 / math.pi)
        return ang        


    def getSphereRadius(self):
        """Return the radius of fullerene-like molecules and et al..

        Atoms are numbered from zero.

        """
        noOfAtoms = self.noOfAtoms
        averCoord = XYZPoint(0.0, 0.0, 0.0)
        for i in xrange(noOfAtoms):
            averCoord = averCoord + self.atomCoords[i]
        averCoord = averCoord.scale(1.0/noOfAtoms)

        radius = 0.0
        for i in xrange(noOfAtoms):
            diff = self.atomCoords[i] - averCoord
            radius += diff.getNorm()
        radius /= noOfAtoms 

        return radius


    def writeXYZGeom(self, title='', symbols=False):
        """Return the geometry in XYZ format

        title: sets title line
        symbols: if True, write atomic symbols instead of numbers

        Return a list containing the XYZ formatted geometry

        """
        if symbols:
            p = PeriodicTable()
        xyzGeom = []
        xyzGeom.append("%5s" % self.noOfAtoms)
        xyzGeom.append(title)
        for i in range(self.noOfAtoms):
            if symbols:
                atom = p.getSymbol(self.atomicNumbers[i])
            else:
                atom = self.atomicNumbers[i]
            geomLine = "%3s %20.10f %20.10f %20.10f" % (atom,
                                                        self.atomCoords[i].x,
                                                        self.atomCoords[i].y,
                                                        self.atomCoords[i].z)
            xyzGeom.append(geomLine)
        return xyzGeom

    def writeMNDOGeom(self, optimise):
        """Return the geometry in MNDO input format.

        The geometry will be in free format (iform > 0) because a formatted
        geometry would lose accuracy. Coords will be written f20.10

        optimise: If true, set MNDO optimisation flags to 1, otherwise 0

        Return a list containing the MNDO formatted geometry

        """
        if optimise:
            opt = "1"
        else:
            opt = "0"
        inputGeom = []
        for i in range(self.noOfAtoms):
            geomLine = "%3s %20.10f  %s %20.10f  %s %20.10f  %s" % \
                       (self.atomicNumbers[i], self.atomCoords[i].x, opt,
                        self.atomCoords[i].y, opt, self.atomCoords[i].z, opt)
            inputGeom.append(geomLine)
        inputGeom.append("  0         " +
                         "0.0           0         " +
                         "0.0           0         " +
                         "0.0           0")
        return inputGeom

    def buildZMatrixGeom(self, relations):
        """Return a ZMatrixGeom object equivalent to the XYZGeom object.

        relations: A list of lists specifying the Z-Matrix atom relationships
                   (zero-indexed)

        """
        internalGeom = ZMatrixGeom()
        for i in range(self.noOfAtoms):
            length = 0.0
            angle = 0.0
            dihedral = 0.0
            lconn = -1
            aconn = -1
            dconn = -1
            if i > 0:
                lconn = relations[i][0]
                length = self.getBondLength(lconn, i)
            if i > 1:
                aconn = relations[i][1]
                angle = self.getBondAngle(aconn, lconn, i)
            if i > 2:
                dconn = relations[i][2]
                # Note signed dihedral angle here
                dihedral = self.getDihedralAngle(dconn, aconn, lconn, i,
                                                 True, True)
            internalGeom.addAtom(self.atomicNumbers[i], length, angle,
                                 dihedral, lconn, aconn, dconn)
        return internalGeom


class XYZPoint:
    """Hold a 3 dimensional Cartesian coordinate vector."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initialise coordinates."""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        """Print complete string representation of vector."""
        return 'XYZPoint(' + repr(self.x) + ', ' + repr(self.y) + ', ' + \
               repr(self.z) + ')'

    def __str__(self):
        """Return simple string representation of vector to 5dp."""
        return '(%.6f, %.6f, %.6f)' % (self.x, self.y, self.z)

    def __add__(self, other):
        """Overloads the '+' operator to add two vectors."""
        newX = self.x + other.x
        newY = self.y + other.y
        newZ = self.z + other.z
        return XYZPoint(newX, newY, newZ)

    def __iadd__(self, other):
        """Overloads the '+=' operator to add other to self in place."""
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __sub__(self, other):
        """Overloads the '-' operator to subtract two vectors."""
        newX = self.x - other.x
        newY = self.y - other.y
        newZ = self.z - other.z        
        return XYZPoint(newX, newY, newZ)

    def __isub__(self, other):
        """Overloads the '-=' operator to subtract other from self in place."""
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z        

    def scale(self, factor):
        """Return the vector multiplied by a scalar factor."""
        factor = float(factor)
        newX = self.x * factor
        newY = self.y * factor
        newZ = self.z * factor
        return XYZPoint(newX, newY, newZ)        

    def dotProduct(self, other):
        """Returns the dot (scalar) product of two vectors."""
        dotp = (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
        return dotp

    def crossProduct(self, other):
        """Returns the cross (vector) product of two vectors."""
        newX = (self.y * other.z) - (self.z * other.y)
        newY = (self.z * other.x) - (self.x * other.z)
        newZ = (self.x * other.y) - (self.y * other.x)
        return XYZPoint(newX, newY, newZ)   

    def getNorm(self):
        """Return the euclidean norm of the vector."""
        norm = math.sqrt(self.dotProduct(self))
        return norm

    def normalise(self):
        """Return the vector after normalisation.

        If the normalisation factor is zero, the original (zero-)vector is
        returned unchanged.

        """
        try:
            normFactor = 1.0 / self.getNorm()
        except ZeroDivisionError:
            normFactor = 1.0
        return self.scale(normFactor)
        

class ZMatrixGeom:

    """Holds a Z-matrix geometry."""

    def __init__(self):
        self.noOfAtoms = 0
        self.atomicNumbers = []
        self.atomCoords = []

    def addAtom(self, atomicNumber, length, angle, dihedral,
                lconn, aconn, dconn):
        """Adds an atom and Z Matrix coordinates to the geometry."""
        self.noOfAtoms += 1
        self.atomicNumbers.append(int(atomicNumber))
        newCoord = ZMatrixPoint(float(length), float(angle), float(dihedral),
                                int(lconn), int(aconn), int(dconn))
        self.atomCoords.append(newCoord)

    def getRelations(self):
        """Return a list of lists of Z-Matrix atom relationships.

        Zero-indexed, suitable for passing to XYZGeom.buildZMatrixGeom

        """
        relations = []
        for i in range(self.noOfAtoms):
            rel = [self.atomCoords[i].lconn,
                   self.atomCoords[i].aconn,
                   self.atomCoords[i].dconn]
            relations.append(rel)
        return relations

    def writeMNDOGeom(self, optimise):
        """Return the geometry in MNDO input format."""
        if optimise:
            opt = "1"
        else:
            opt = "0"
        inputGeom = []
        for i in range(self.noOfAtoms):
            geomLine = "%3s %20.10f  %s %20.10f  %s %20.10f  %s  %s  %s  %s" % \
                       (self.atomicNumbers[i], self.atomCoords[i].length, opt,
                        self.atomCoords[i].angle, opt,
                        self.atomCoords[i].dihedral, opt,
                        self.atomCoords[i].lconn + 1,
                        self.atomCoords[i].aconn + 1,
                        self.atomCoords[i].dconn + 1)
            inputGeom.append(geomLine)
        inputGeom.append("  0         " +
                         "0.0           0         " +
                         "0.0           0         " +
                         "0.0           0   0   0   0")
        return inputGeom            

    def buildXYZGeom(self):
        """Return an XYZGeom object equivalent to the ZMatrixGeom object.

        First atom is at the origin.
        Orientation of second atom is along X-axis.
        Orientation of third atom is in XY plane.

        Routine adapted from ChemShell zmatrix.c - calc_zatom_vector/ziccd
        Note orientation has been changed to be consistent with MNDO

        """
        deg = (180.0 / math.pi)
        cartesianGeom = XYZGeom()
        for i in range(self.noOfAtoms):
            # These defaults correspond to Atom 0
            r = 0.0
            theta = 0.0
            phi = 0.0
            v1 = XYZPoint(0.0, 0.0, 0.0)
            v2 = XYZPoint(0.0, 0.0, 1.0)
            v3 = XYZPoint(1.0, 1.0, 1.0)
            # Z-matrix atom numbers
            z1 = self.atomCoords[i].lconn
            z2 = self.atomCoords[i].aconn
            z3 = self.atomCoords[i].dconn
            if i == 1:
                v1 = cartesianGeom.atomCoords[z1]
                v2 = cartesianGeom.atomCoords[z1] + XYZPoint(1.0, 0.0, 0.0)
                # Arbitrary vector
                v3 = cartesianGeom.atomCoords[z1] + XYZPoint(0.0, 1.0, 0.0)
                r = self.atomCoords[i].length
            elif i == 2:
                v1 = cartesianGeom.atomCoords[z1]
                v2 = cartesianGeom.atomCoords[z2]
                v3 = cartesianGeom.atomCoords[z1] + XYZPoint(0.0, 1.0, 0.0)
                r = self.atomCoords[i].length
                theta = self.atomCoords[i].angle / deg
            elif i > 2:
                v1 = cartesianGeom.atomCoords[z1]
                v2 = cartesianGeom.atomCoords[z2]
                v3 = cartesianGeom.atomCoords[z3]
                r = self.atomCoords[i].length
                theta = self.atomCoords[i].angle / deg
                phi = self.atomCoords[i].dihedral / deg
            # Construct the new atom position, given v1-3, r, theta, phi
            # v3--v2--v1--x
            # r = r(x--v1), theta = ang(x--v1--v2), phi = tor(x--v1--v2--v3)
            # Normalised v2->v1 vector
            v21 = (v1 - v2).normalise()
            # Vector perpendicular to v3--v2--v1 plane
            vpa = (v21.crossProduct(v3 - v2)).normalise()
            # Another perpendicular vector
            vpb = vpa.crossProduct(v21)
            # Torsion angle vector
            vtor = vpa.scale(math.sin(phi)) + vpb.scale(math.cos(phi))
            # Atom position
            apos = v1 + v21.scale(r * math.cos(math.pi - theta)) + \
                        vtor.scale(r * math.sin(math.pi - theta))
            cartesianGeom.addAtom(self.atomicNumbers[i], apos.x, apos.y, apos.z)
        return cartesianGeom


class ZMatrixPoint:
    """Hold a Z matrix coordinate."""

    def __init__(self, length=0.0, angle=0.0, dihedral=0.0,
                 lconn=-1, aconn=-1, dconn=-1):
        """Initialise coordinates."""
        self.length = float(length)
        self.angle = float(angle)
        self.dihedral = float(dihedral)
        self.lconn = int(lconn)
        self.aconn = int(aconn)
        self.dconn = int(dconn)       


class VelocityFile(RawFile):
    
    """Hold a velocity file containing one or more velocities
       in XYZ format.

    """
    
    def __init__(self, fileName):
        RawFile.__init__(self, fileName)
        noOfAtoms = 0
        # Determine number of atoms from first entry
        for i in self.fileContents:
            if len(i.split()) != 3:
                break
            noOfAtoms += 1
        self.noOfAtoms = noOfAtoms
        # Cursory check of contents
        if len(self.fileContents) % (self.noOfAtoms + 1) == 0:
            self.noOfGeoms = len(self.fileContents) / (self.noOfAtoms + 1)
        else:
            sys.stderr.write("Error: velocity file length is not an integer " +
                             "multiple of the first entry.\n")
            sys.exit(1)

    def getVelocity(self, velNumber):
        """Return an XYZVelocity object containing a set of Cartesian atom velocities.

        velNumber - specifies which velocity set in the file should be parsed
                     (numbered from 0)
        
        Return None if the XYZ data could not be parsed.

        """
        xyzVel = XYZVelocity()
        # We calculate first line assuming that velNumber is numbered from 0
        lineNo = velNumber * (self.noOfAtoms + 1)
        for i in range(self.noOfAtoms):
            XYZLine = self.fileContents[lineNo].split()
            try:
                x = float(XYZLine[0])
                y = float(XYZLine[1])
                z = float(XYZLine[2])
            except ValueError:
                sys.stderr.write("Error: columns 1-3 should contain xyz " +
                                 "data separated by spaces.\n")
                return None
            xyzVel.addAtom(x, y, z)
            lineNo += 1
        return xyzVel

    def writeSnapshots(self, snapshots, fileName):
        """Write a new XYZ file containing snapshots from the original file.

        snapshots - list of geometries to be written (numbered from 0)
        fileName - name of the output file containing the snapshots

        The file is copied as-is, with no further checking beyond that when
        the object was initialised.

        Return -1 if unsuccessful

        Usage note: snapshots at regular intervals can be taken using 'range'
          i.e.. snapshots = range([1st snapshot], [total geoms], [interval])

        """
        try:
            f=open(fileName, 'w')
        except IOError:
            sys.stderr.write("Error: could not open %s" +
                             "for writing.\n" % fileName)
            return -1
        for snap in snapshots:
            if snap > self.noOfGeoms - 1:
                sys.stderr.write("Warning: requested snapshot %i is too "
                                 "large - ignored.\n" % snap)
                continue
            startLine = snap * (self.noOfAtoms + 1)
            for i in range(self.noOfAtoms + 1):
                f.write(self.fileContents[startLine + i])
        f.close()


class XYZVelocity:
    
    """Hold a set of atom velocities in Cartesian coordinates."""

    def __init__(self):
        self.noOfAtoms = 0
        self.atomVelocities = []

    def addAtom(self, x, y, z):
        """Add cartesian velocity for an atom."""
        self.noOfAtoms += 1
        newVelocity = XYZPoint(float(x), float(y), float(z))
        self.atomVelocities.append(newVelocity)

    def writeXYZVelocity(self):
        """Return the set of velocities in vel.out format

        Return a list containing the XYZ formatted velocities.

        """
        xyzVel = []
        for i in range(self.noOfAtoms):
            velLine = "%20.10f %20.10f %20.10f" % (
                                                    self.atomVelocities[i].x,
                                                    self.atomVelocities[i].y,
                                                    self.atomVelocities[i].z)
            xyzVel.append(velLine)
        xyzVel.append('')
        return xyzVel


class PeriodicTable:
    
    """Hold a list of element names and a dictionary of atomic numbers."""

    def __init__(self):
        self.symbols = ["-", "H", "He",
                        "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
                        "K", "Ca",
                        "Sc", "Ti", "V", "Cr", "Mn",
                        "Fe", "Co", "Ni", "Cu", "Zn",
                        "Ga", "Ge", "As", "Se", "Br", "Kr",
                        "Rb", "Sr",
                        "Y", "Zr", "Nb", "Mo", "Tc",
                        "Ru", "Rh", "Pd", "Ag", "Cd",
                        "In", "Sn", "Sb", "Te", "I", "Xe",
                        "Cs", "Ba",
                        "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",
                        "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
                        "Hf", "Ta", "W", "Re",
                        "Os", "Ir", "Pt", "Au", "Hg",
                        "Tl", "Pb", "Bi", "Po", "At", "Rn",
                        "Fr", "Ra",
                        "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
                        "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
                        "Rf", "Db", "Sg", "Bh",
                        "Hs", "Mt", "Ds", "Rg"]
        self.atomicNumbers = {}
        for i in range(1, len(self.symbols)):
            self.atomicNumbers[self.symbols[i].lower()] = i

    def getSymbol(self, atomicNumber):
        """Return an atomic symbol given an atomic number"""
        if atomicNumber < 1 or atomicNumber >= len(self.symbols):
            return None
        else:
            return self.symbols[atomicNumber]

    def getZ(self, symbol):
        """Return an atomic number given an atomic symbol"""
        mysymbol = symbol.lower()
        if self.atomicNumbers.has_key(mysymbol):
            return self.atomicNumbers[mysymbol]
        else:
            return None


