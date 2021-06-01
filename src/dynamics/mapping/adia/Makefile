#
# Paths to directories commands
#
include ../../../compiler.mk

INCDIR = ../../include

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
MOD = ../
ifdef LIB
LIB0 = ${LIB}
else
LIB = -L/home/softwares/intel/composer_xe_2013.1.117/mkl/lib/intel64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
endif

#
# Compilers
#
F90C = ifort
F90FLAGS = -I${INCDIR} -I${MOD}

CC = gcc
CFLAGS = -O2 -mcpu=i486 -I. -DLINUX -D__I8=0 -D__ENDIAN=0 

#
# Executable, source and objects
#

%.o: %.mod

F90SRC = \
sub_calc_dV_eff_div_dx_nuc_adia.o \
sub_calc_dV_eff_div_dx_nuc_adia_traj_adjusted.o \
sub_calc_dp_nuc_kin__dij_term_adia.o \
sub_elec_motion_2_aver_PES_1step_adia.o \
sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia.o \
sub_elec_motion_2_aver_PES_adia.o \
sub_motion_2_adia_aver_PES_1step.o \
sub_nuc_get_dHmn_div_dX_adia.o \
sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia.o \
sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia_traj_adjusted.o \
sub_nuc_motion_2_aver_PES_1step_dx_div_dt_adia.o \
sub_nuc_motion_2_aver_PES_adia.o \
sub_p_kin_to_p.o \
sub_p_to_p_kin.o \
sub_write_trj_2_adia.o \
sub_write_trj_2_adia_traj_adjusted.o

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
