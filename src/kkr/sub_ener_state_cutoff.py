#!/usr/bin/env python

import numpy as np


class ener_state_cutoff():
    def __init__(self, n_atom, Total_E_change, Time_after_jump_back):
        self.n_atom = n_atom
        self.n_step = 0
        self.n_geom_stop = 0
        self.n_geom = 0
        self.Total_E_change = Total_E_change
        self.Time_after_jump_back = Time_after_jump_back

    def read_energy(self):
        energy_pe = np.loadtxt('all_in_one.dat')
        self.n_step = energy_pe.shape[0]
        self.n_state = energy_pe.shape[1] - 2
        Total_energy = energy_pe[:, -1]
        current_state = energy_pe[:, -2]
        dt = energy_pe[1, 1]

        n_dt_after_jump = self.Time_after_jump_back / dt

        if n_dt_after_jump >= self.n_step:
            n_dt_after_jump = self.n_step

        n_energy_step = self.n_step
        n_time_step = self.n_step
        self.useful_n_step = self.n_step

        for i in range(self.n_step - 1):
            if abs(Total_energy[i + 1] - Total_energy[i]) > self.Total_E_change:
                n_energy_step = i + 1
                break

        for i in range(int(self.n_step - n_dt_after_jump)):
            if sum(current_state[i:int(i + n_dt_after_jump)] - 1) == 0:
                n_time_step = i + n_dt_after_jump
                break

        if n_energy_step <= n_time_step:
            self.useful_n_step = n_energy_step
        else:
            self.useful_n_step = n_time_step
        return self.useful_n_step


def make(n_atom, Total_E_change, Time_after_jump_back):
    jobs = ener_state_cutoff(n_atom, Total_E_change, Time_after_jump_back)
    a = jobs.read_energy()
    return a


if __name__ == '__main__':
    n_atom = 6
    Total_E_change = 1000
    Time_after_jump_back = 50
    jobs = ener_state_cutoff(n_atom, Total_E_change, Time_after_jump_back)
    a = jobs.read_energy()
    print(a)
