#
# Paths to directories commands
#
include ../compiler.mk

DIR = .
INCDIR = ${DIR}/include
TSHDIR = ${DIR}/tsh
MAPPINGDIR = ${DIR}/mapping
ONTHEFLYDIR = ${DIR}/mapping/on_the_fly
ADIADIR = ${DIR}/mapping/adia

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
EXE  = main_sh.exe
MAIN = main_sh.f90

%.o: %.mod


#
# Dependencies
#

${EXE}:
	$(MAKE) -j2 -C ${TSHDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${MAPPINGDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${ONTHEFLYDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${ADIADIR} $(MAKECMDGOALS) 

	${F90C} -o $@ ${F90FLAGS} ${MAIN} ${TSHO} ${MAPPINGO} ${ONTHEFLYO} ${ADIAO} ${LIB}

TSHO = $(wildcard ./tsh/*o)
MAPPINGO = $(wildcard ./mapping/*o)
ONTHEFLYO = $(wildcard ./mapping/on_the_fly/*o)
ADIAO = $(wildcard ./mapping/adia/*o)

install: ${EXE} 
	mv ${EXE} ../../bin/jade.exe

clean:
	$(MAKE) -j2 -C ${TSHDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${MAPPINGDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${ONTHEFLYDIR} $(MAKECMDGOALS) 
	$(MAKE) -j2 -C ${ADIADIR} $(MAKECMDGOALS) 

#
# Suffix rules
#
.SUFFIXES: $(SUFFIXES) .f90
.f90.o:
	${F90C} -c ${F90FLAGS} $*.f90
.f.o:
	${FC} -c ${FFLAGS} $*.f
	
.c.o:
	${CC} -c ${CFLAGS} $*.c
