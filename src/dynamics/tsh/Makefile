#
# Paths to directories commands
#
include ../../compiler.mk

INCDIR = ../include

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
sub_sh_zn.o \
sub_zn_hopping.o \
constant.o \
sub_random.o \
sub_string.o \
sub_write_current_geom.o \
sub_read_current_geom.o \
sub_save_gradient.o  \
sub_save_grad.o  \
sub_save_hopping_num_nac.o  \
sub_tully_hopping_num_nac.o \
sub_decoherent_corr.o \
sub_nac_phase.o  \
sub_read_ini_vel.o \
sub_save_traj.o \
sub_velocity_scaling.o \
sub_get_mass.o  \
sub_newton_coor.o \
sub_read_restart.o \
sub_sh_ana_nac.o  \
sub_write_current_geom.o \
sub_many_ana_pes.o \
sub_newton_vel.o   \
sub_save_energy.o \
sub_sh_num_nac.o \
sub_many_pes_num_nac.o  \
sub_read_coor.o   \
sub_save_hopping_ana_nac.o \
sub_tully_hopping_ana_nac.o \
sub_save_pe.o \
sub_save_restart.o \
sub_random3.o \
langevin.o \
sub_lang_sh_num_nac.o

#
# Dependencies
#

install: ${F90SRC} 

clean:
	${RM} *.o *mod

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
