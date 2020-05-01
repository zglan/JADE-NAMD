# python

from tools import *


# namelist: for the exchange of data between python/internal(json) & fortran-namelist.

# % read fortran namelist 
#   convert to json format.
# % write fortran namelist
#
# %
#

class namelist():
    """
    model for quantum chemistry calculations.
    """

    def __init__(self, filename=""):

        comment = re.compile(r"^(.*)!(.*)$")
        varname = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
        spaces = r'[\s\t]*'
        namelistname = re.compile(r"^[\s\t]*&(" + varname + r")[\s\t]*$")
        paramname = re.compile(r"[\s\t]*(" + varname + r')[\s\t]*=[\s\t]*(.*)')
        namelistend = re.compile(r"^" + spaces + r"/" + spaces + r"$")
        # namelistend = re.compile(r"^" + spaces + r"&end" + spaces + r"$") 
        self.reg = {"comment": comment, "varname": varname, "spaces": spaces, \
                    "namelistname": namelistname, "paramname": paramname, "namelistend": namelistend}
        self.obj = {}

        if filename != "":
            self.namelist(filename)
        return

    def __remove_comment(self, line):
        """ remove line content after ! """
        # remove comment
        comment = self.reg['comment']
        m_comment = comment.search(line)
        if m_comment is not None:
            line = m_comment.group(1)
        return line

    def __namelist_name(self, fp):
        """ get name of one section """
        namelistname = self.reg['namelistname']
        # locate & section one
        name = ""
        line = "not empty line."
        while line != "":
            line = fp.readline()
            line = self.__remove_comment(line)
            m = namelistname.search(line)

            if m is not None:
                name = m.group(1)
                break
            else:
                name = ""
        return name

    def __namelist_parm(self, fp):
        """ the parameter of each section """
        namelistend = self.reg['namelistend']
        paramname = self.reg['paramname']
        parm = {}
        line = "not empty line."
        while line != "":
            # prepare line
            line = fp.readline().replace("\"", " ").replace(",", " ").strip()
            line = self.__remove_comment(line)
            # end or not
            m = namelistend.search(line)
            if m is not None:
                break
            # parameters
            m = paramname.search(line)
            if m is not None:
                parm[m.group(1)] = m.group(2)
            else:
                continue
        return parm

    def namelist(self, filename="dyn.inp"):
        """
        read namelist at first
        """

        fp = open(filename, "r")

        name = "HAHAHA"
        while 1:
            name = self.__namelist_name(fp)
            if name == "":
                break
            parm = self.__namelist_parm(fp)

            self.obj[name] = parm

        dump_data("inp.json", self.obj)

        return

    def write(self, filename="nma.inp"):
        """
        write down name list from python list
        """
        fp = open(filename, "w")

        for name, parm in self.obj.iteritems():
            print >> fp, "&%s" % name
            for key, value in parm.iteritems():
                print >> fp, "   %s = %s" % (key, value)
            print >> fp, "/"
        fp.close()

        return

    def get(self):
        """ return obj """
        return self.obj


if __name__ == "__main__":
    nma = namelist()
    nma.namelist(filename="dyn.inp")
    nma.write()
