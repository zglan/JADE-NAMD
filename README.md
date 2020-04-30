# JADE-NAMD
JADE-NAMD: An package for the on-the-fly nonadiabatic molecular dynamics simulation 

# Outline
Welcome to the newest version of JADE-NAMD page!

The JADE-NAMD package is mainly developed for the simulation of the nonadiabatic dynamics of polyatomic systems. Particularly, the on-the-fly nonadiabatic molecular dynamics simulation is performed based on different dynamical approaches at various electronic-structure levels. We wish to provide an small but easy program for the nonadiabatic dynamics simulation.

# History and Old Version
The development of the JADE code starts from several years ago. This code is initialized in the year of 2014-2015 in the group of Prof. Zhenggang Lan when he was in QIBEBT, Qingdao, China. The first version is mainly developed by Dr. Likai Du and Dr. Zhenggang Lan, which is found also in Github (https://github.com/jade-package/JADE). In these years, several people also made some important contributions, which include Dr. Yu Xie, Dr. Deping Hu, Dr. Jing Huang, Dr. Xusong Li and Ms. Jiawei Peng.

Since Sept 2018, Prof. Zhenggang Lan moved to Souch China Normal University. In these years, many new features are implemented. Thus we decide to release a new version of JADE. Also we noticed that many packages are named as "JADE". To avoid confusing, the new package is namded "JADE-NAMD".

We will try to make this code more formal in the future. For instance, we will try to update this code more often than previous time. The more features will be added and the more turtorials are given.

We add the GNU licences to this code. If someone wishes to join us for the development of this package, we will be happy.

# Main features
The main part of the JADE-NAMD code contains the on-the-fly surface-hopping dynamics at different electronic levels.

1. The module of the initial sampling of the nuclear part include
   * Wigner sampling at zero and finite temperature
   * Action-angle sampling at zero and finite temperature
   * Action-angle sampling when the particular mode is excited
   * Sampling with freezing mode
   * Sampling at the transition state

2. The dynamics module include different nonadiabatic dynamics methods
   * Tully's surface hopping dynamics
   * Zhu-Nakamura surface hopping dynamics
   * Others (under development)
   
3.	We also introduce machine learning in nonadiabatic dynamics
    * Supervised learning approaches: Kernel Ridge regression for PES fitting
    * Unsupervised learning approaches in data analysis: multidimensional scaling, ISOMAP
    * Trajectory similarity analysis: Frechet distance
    
4.	The current available interface for the electronic-struture calculations include:
    * TDDFT, ADC(2), CC(2) and CIS in Turbomole
    * TDDFT In Gamess
    * TDDFT in Gaussian
    * CASSCF in Molpro
    * OM2/MRCI in MNDO
    
5.	The numerical nonadiabatic coupling is also available when the analytical one is not available. This module supports
    * TDDFT, ADC(2), CC(2) and CIS in Turbomole  
    * TDDFT in Gaussian

# Contributors:
Zhenggang Lan, Likai Du, Deping Hu, Yu Xie, Jiawei Peng, Jing Huang, Xusong Li.

# Bug reports:
If you find any problem in our code, please send email to Prof. Zhenggang Lan. (Zhenggang.lan@gmail.com)


# JADE-NAMD package references
1.	Likai Du, Zhenggang Lan*; An on-the-fly surface-hopping program JADE for nonadiabatic molecular dynamics of poly-atomic systems: implementation and applications; J. Chem. Theory Comput. 2015, 11, 1360-1374
2.	Deping Hu, Yan Fang Liu, Andrzej L. Sobolewski, Zhenggang Lan*; Nonadiabatic dynamics simulation of keto isocytosine: a comparison of dynamical performance of different electronic-structure methods; Phys. Chem. Chem. Phys., 2017, 19, 19168-19177



