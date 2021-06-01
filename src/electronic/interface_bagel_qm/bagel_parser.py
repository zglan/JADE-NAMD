#! /usr/bin/python

from bagel_log_parser import *

# mndo parser


class bagel_parser():
    def __init__(self, config={}):
        """
        parser mndo log or fort files to extract relevant data.
        """
        self.config = config

        return

    def get_log_dat(self):
        """
        parse one tddft calculation result.
        """
        log = bagel_log_parser(self.config)

        # forces
        log.get_energy()
        log.get_gradient()
        log.get_nac()
        log.collect_qm()

        return
