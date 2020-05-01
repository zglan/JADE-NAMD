#! python

from  gaussian_parser import gaussian_parser
from  turbomole_parser import turbomole_parser
from  molden_parser import molden_parser

# read in different type of log file and dump normal mode data.

class normal_mode_parser():
    def __init__(self, config = {}):
        """
        define different log
        """
        self.config = {}

        if config == {}:
            self.prepare()
        else:
            self.config['log_type'] = config['log_type']
            self.config['log'] = config['log']
            self.config['newlog'] = config['newlog']
            self.config['n_atom'] = config['n_atom']
            self.config['n_mode'] = config['n_mode']          
        
        return

    def prepare(self):
        """
        info. about how to read log file & kind of log file
        """
        self.config['log_type'] = raw_input("LOG TYPE (avaiable): \
gaussian/turbomole/mndo \n>> ")
        n_atom = raw_input("Number of Atoms: ")
        n_mode = raw_input("Number of Normal Mode: ")
        self.config['log'] = raw_input("LOG file name: >> ")
        self.config['newlog'] = raw_input("output file name: >> ")
        self.config['n_atom'] = int(n_atom)
        self.config['n_mode'] = int(n_mode)
        
        return


    def running(self):
        """
        read log
        """
        log_type = self.config['log_type']
        if log_type == "gaussian":
            parser = gaussian_parser(self.config)
        elif log_type == "turbomole":
            parser = turbomole_parser(self.config)
        elif log_type == "mndo":
            parser = molden_parser(self.config)
        else:
            print "no other interface implemented!!!"
            exit(1)
            
        parser.read_log()
        
        return


    def finalize(self):


        return

    def done(self):
        """
        done
        """
        print "Extract NORMAL MODE data."
        print "gaussian case, n_atom&n_mode is useless"
        
        # self.prepare()
        self.running()
        self.finalize()

        return

### main program
if __name__ == "__main__":
    nm = normal_mode_parser()
    nm.done()



