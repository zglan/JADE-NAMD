#! /usr/bin/env python

import re

class bIndex():
    def __init__(self, flag = 0):
        """ index split or slab or etc. """
        # atomic index start from ..
        self.flag = flag

        return
        
    def set_flag(self, flag = 0):
        self.flag = flag
        
        return
        
    def ext_frg_ndx(self, frg_ndx):
        """
        extend it in to actual list
        [0-17, 38, 40]
        """
        # fragment start id.
        flag = self.flag
        #
        frg_list = []
        pat = re.compile("([0-9]+)-([0-9]+)")
        r = frg_ndx.split(',')
        for ir in r:
            m = pat.search(ir)
            if m is not None:
                a, b = [int(x) for x in m.group(1,2)]
                for i in xrange(a, b+1):
                    frg_list.append(i-flag)
            else:
                frg_list.append(int(ir)-flag)
        return frg_list
        
        
        
        
        
  
