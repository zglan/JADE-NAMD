#! /usr/bin/env python
import os

# this scripts read 'fort.18'
# <mopac internal coordinates> and convert to
# xyz format, then combine it.
# note: babel is required.
class jobcut():
    def __init__(self):
    
        return
        

    def mopac_int_block(self, fp, id):
        filename = str(id) + ".mopin"
        fp_out = open(filename, "w")
        line = fp.readline()
        print >>fp_out, "%s" % line,
        n_atom = int(line)
        
        line = fp.readline()
        print >>fp_out, "%s" % line,
        line = fp.readline()
        print >>fp_out, "%s" % line,
        for i in xrange(n_atom):
            line = fp.readline()
            print >>fp_out, "%s" % line,
        fp_out.close()
        return
        
    def mopac_int(self):
        line = raw_input("number of structure:")
        n_mol = int(line)
        filename = "fort.18"
        fp = open(filename, "r")
        for id in xrange(n_mol):
            self.mopac_int_block(fp, id+1)
            self.xyz_convert(id+1)
        fp.close()
        fp = open("m.xyz", "w")
        for id in xrange(n_mol):
            self.xyz_write(fp, id+1)
        fp.close()
        return
        
    def xyz_convert(self, id):
        mopac = str(id) + ".mopin"
        xyz = str(id) + ".xyz"
        os.system("babel -imopin " + mopac + " -oxyz " + xyz)
        return
        
    def xyz_write(self,fp,id):
        xyz = str(id) + ".xyz"
        file_in = open(xyz, "r")
        fp.write(file_in.read())
        file_in.close()
        return
        
        
        
        
if __name__ =="__main__":
    job = jobcut()
    job.mopac_int()
   
    