#! /usr/bin/python

from molpro_log_parser import *


# mndo parser

class molpro_parser():
    def __init__(self, label_ZN, config={}):
        """
        parser mndo log or fort files to extract relevant data.
        """
        self.config = config
        self.label_ZN = label_ZN

        return

    def get_log_dat(self):
        """
        parse one tddft calculation result.
        """
        log = molpro_log_parser(self.label_ZN, self.config);

        # forces
        log.get_energy()
        log.get_gradient()

        if self.label_ZN == 0:
           log.get_nac()

        # other data.
        log.collect_qm()
        #        log.get_other()

        return
