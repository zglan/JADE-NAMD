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
sub_evolution_mapping_2_on_the_fly.o \
sub_evolution_mapping_2_on_the_fly_traj_adjusted.o \
sub_many_ana_pes_mapping.o \
sub_nac_phase_mapping.o \
sub_read_current_geom_mapping.o \
sub_read_parameter_on_the_fly.o \
sub_reshape_n_atom_to_n_mode.o \
sub_reshape_n_mode_to_n_atom.o \
sub_test.o \
sub_write_current_geom_mapping.o \
sub_write_geom.o \
sub_write_geom_mapping.o \
sub_write_geom_mapping_traj_adjusted.o

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
