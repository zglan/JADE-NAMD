#! /usr/bin/python

class py2fortran():
    def __init__(self):

        self.tbfile = "elements.dat"
        self.table = []
        
        return

    def read_table(self):
        """ read in it """
        filename = self.tbfile
        fp = open(filename, "r")
        line = fp.readline()
        line = fp.readline()
        n_type = int(line)
        line = fp.readline()
        for i in xrange(n_type):
            line = fp.readline()
            rec = line.split()
            atom = {'label': rec[0],
                    'std_name': rec[1], 'eng_name': rec[2],
                    'charge': int(rec[3]), 'mass': float(rec[4])}

            self.table.append(atom)

        fp.close()

        return
    
    def write_fortran(self):
        """ wrt """
        filename = "new.f90"
        fp = open(filename, "w")
        print >>fp, \
              """
subroutine   atom_number_to_label (atom_number, label )


    implicit none

    integer, intent(in) :: atom_number
    character*2, intent(inout) :: label
     
      
    label=""

              """
        
        for atom in self.table:            
            print >>fp, '      if (atom_number .eq. ' + str(atom['charge']) + ')' + " then"
            print >>fp, "        label = \""+atom['label']+"\""
            print >>fp, "      endif"
            print >>fp, ""


        print >>fp, \
              """
       if (label .eq. "") then
       write (*,*) "PLEASE CHECK THE ATOMIC NUMBER!!"
       stop
       endif


      return
      end  subroutine   atom_number_to_label
 
              """
       
        fp.close()
        
        return


if __name__ == "__main__":
    pf = py2fortran()
    pf.read_table()
    pf.write_fortran()

