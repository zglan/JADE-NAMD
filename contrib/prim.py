
    def get_atom_coord(self, i_mol, j_atom):
        """
        return record of ith mol jth atom
        """
        mol = self.model['mol']
        one_mol = mol[i_mol]
        one_atom = one_mol[j_atom]
        coord = one_atom['coord']
        return coord


    def get_bondlength(self, pa, pb):
        """
        calculate the distance of two points
        """
        ab = np.subtract(pa, pb)
        length = np.linalg.norm(ab)
        return length
    def get_bondangle(self, pa, pb, pc):
        """
        calculate the bond-angle of three point
        (a,b,c)
        """
        ba = np.subtract(pa, pb)
        bc = np.subtract(pc, pb)
        sabc = np.dot(ba, bc)
        lba = np.linalg.norm(ba)
        lbc = np.linalg.norm(bc)
        costh = sab / (lba * lbc)
        angle = math.acos(costh)
        return angle
    def get_dihedral(self, pa, pb, pc, pd):
        """
        calc. dihedral of four points
        (a,b,c,d)
        """
        vab = np.subtract(pa, pb)
        vbc = np.subtract(pb, pc)
        vcd = np.subtract(pc, pd)

        vm = np.cross(vab, vbc)
        vn = np.cross(vbc, vcd)
        dvm = np.linalg.norm(vm)
        dvn = np.linalg.norm(vn)
        dvmn = np.dot(vm, vn)

        smallvalue = 1.0e-10
        if dvm < smallvalue or dvn < smallvalue:
            costh = 1.0
        else:
            costh = dvmn / ( dvm * dvn )
            
        vflag = np.cross(vm, vn)
        dflag = np.dot(vbc, v)
        if dflag > 0.0:
            dsign = 1.0
        else:
            dsign = -1.0

        theta = math.acos(costh) * dsign
        
        return theta

