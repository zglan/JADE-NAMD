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
If anyone wishes to add new features, please do not hesitate to contact with Prof. Zhenggang Lan. (Zhenggang.lan@gmail.com). 

# Bug Reports:
If you find any problem in our code, please send email to Prof. Zhenggang Lan. (Zhenggang.lan@gmail.com)


# JADE-NAMD package references 
Method Development
1.	Likai Du, Zhenggang Lan*; An on-the-fly surface-hopping program JADE for nonadiabatic molecular dynamics of poly-atomic systems: implementation and applications; J. Chem. Theory Comput. 11, 1360-1374 (2015).
2.	Deping Hu, Yan Fang Liu, Andrzej L. Sobolewski, Zhenggang Lan*; Nonadiabatic dynamics simulation of keto isocytosine: a comparison of dynamical performance of different electronic-structure methods; Phys. Chem. Chem. Phys., 19, 19168-19177, (2017).
3． D. Hu, Y. Xie, X Li, L. Li, Z Lan*, Inclusion of Machine Learning Kernel Ridge Regression Potential Energy Surfaces in On-the-Fly Nonadiabatic Molecular Dynamics Simulation. J. Phys. Chem. Lett., 9, 2725-2732 (2018).
4. X.Li, D. Hu, Y. Xie, Z. Lan*, Analysis of trajectory similarity and configuration similarity in on-the-fly surface-hopping simulation on multi-channel nonadiabatic photoisomerization dynamics, J. Chem. Phys., 149, 244104 (2018).
5. X. Li, Y. Xie, D. Hu, Z. Lan*. Analysis of the Geometrical Evolution in On-the-Fly Surface-Hopping Nonadiabatic Dynamics with Machine Learning Dimensionality Reduction Approaches: Classical Multidimensional Scaling and Isometric Feature Mapping, J. Chem. Theory Comput., 13, 4611-4623 (2017).

Application
6. F. Liu, L. Du, Z. Lan and J. Gao. Liu. Hydrogen Bond Dynamics Governs the Effective Photoprotection Mechanism of Plant Phenolic Sunscreens. Photoch. Photobio. Sci., 16, 211-219 (2017).
7. L. Du, and Z. Lan*, Ultrafast Structural Flattening Motion in Photoinduced Excited State Dynamics of a Bis(dimine) Copper(I) Complex, Phys. Chem. Chem. Phys., 18, 7641-7650 (2016).
8. D. Hu, J. Huang, Y. Xie, L. Yue, X. Zhuang, Z. Lan*, Nonadiabatic Dynamics and Photoisomerization of Biomimetic Photoswitches, Chem. Phys., 463, 95-105 (2015).
9. J. Wang, J. Huang, L. Du, Z. Lan*, Photoinduced Ultrafast Intramolecular Excited-State Energy Transfer in the Silylene-Bridged Biphenyl and Stilbene (SBS) System: A Nonadiabatic Dynamics Point of View, J. Phys. Chem. A, 119, 6937-6948 (2015).
10. J. Huang, L. Du, J. Wang, Z. Lan*, Photoinduced Excited-State Energy-Transfer Dynamics of a Nitrogen-Cored Symmetric Dendrimer: From the Perspective of the Jahn-Teller Effect, J. Phys. Chem. C, 119, 7578-7589 (2015).
