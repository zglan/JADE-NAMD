#
# Paths to directories commands
#
include ../../compiler.mk

INCDIR = ../include

#
# UNIX commands
#
CP    = /bin/cp -f
RM    = /bin/rm -f
MKEXE = /bin/chmod 755
AR    = /usr/bin/ar
ECHO  = echo

#
# Libraries
#
LIB = -mkl
ifdef LIB
LIB0 = ${LIB}
else
LIB = -L/home/softwares/intel/composer_xe_2013.1.117/mkl/lib/intel64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
endif

#
# Compilers
#

F90C = ifort
F90FLAGS = -I${INCDIR}

CC = gcc
CFLAGS = -O2 -mcpu=i486 -I. -DLINUX -D__I8=0 -D__ENDIAN=0 

#
# Executable, source and objects
#

%.o: %.mod

F90SRC = \
mod_main.o \
sub_mapping_ana_nac.o \
sub_read_control.o  \
sub_nuc_motion.o  \
sub_nuc_get_dH_div_dX_or_dP.o  \
sub_nuc_get_dHmn_div_dP.o  \
sub_nuc_get_dHmn_div_dX.o  \
sub_move.o  \
sub_write_trj_1.o  \
sub_write_trj_2.o \
sub_read_parameter.o \
sub_read_ini_trj_1.o \
sub_read_ini_trj_2.o \
sub_elec_get_dH_div_dx_or_dp.o  \
sub_get_dia_Ham_elec.o  \
sub_get_c_n_elec_1.o  \
sub_get_c_n_elec_2.o \
sub_get_c_n_elec_2_traj_adjusted.o \
sub_evolution_1.o  \
sub_evolution_2.o  \
sub_elec_motion_1.o \
sub_elec_motion_2.o \
sub_evolution_3.o \
sub_write_trj_3.o \
sub_elec_motion_3.o  \
sub_sum_sq_sum_by4.o \
sub_elec_motion_3_step1.o \
sub_elec_motion_3_step1_2.o  \
sub_elec_motion_3_step2.o  \
sub_elec_motion_3_step2_2.o  \
sub_elec_get_dH_div_dx_or_dp_3.o  \
sub_get_c_n_elec_3.o  \
sub_elec_get_dH_div_dx_or_dp_aver_PES.o  \
sub_elec_motion_2_aver_PES.o  \
sub_nuc_motion_aver_PES.o  \
sub_nuc_get_dH_div_dX_or_dP_aver_PES.o  \
sub_nuc_get_dH_div_dP_aver_PES.o  \
sub_evolution_mapping_2_Ham_4.o  \
sub_read_parameter_Ham_4.o  \
sub_get_dia_Ham_elec_Ham_4.o  \
sub_get_dia_Ham_elec_Ham_tor.o  \
sub_elec_motion_mapping_2_Ham_4_aver_PES.o  \
sub_nuc_motion_Ham_4_aver_PES.o  \
sub_nuc_get_dHmn_div_dX_Ham_tor.o  \
sub_elec_motion_mapping_1_Ham_4.o  \
sub_evolution_mapping_1_Ham_4.o  \
sub_nuc_motion_Ham_4.o  \
sub_nuc_get_dH_div_dP.o  \
sub_evolution_adia.o  \
sub_dia_to_adia.o  \
sub_diag.o  \
sub_cal_gammas.o 

#
# Dependencies
#

install: ${F90SRC} 

clean:
	${RM} *.o

veryclean:
	${RM} *.a *.o

#
# Suffix rules
#
.SUFFIXES: $(SUFFIXES) .f90
.f90.o:
	${F90C} -c ${F90FLAGS} ${LIB} $*.f90
.f.o:
	${FC} -c ${FFLAGS} $*.f
	
.c.o:
	${CC} -c ${CFLAGS} $*.c
