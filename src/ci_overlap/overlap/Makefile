#
# Paths to directories commands
#
include ../../compiler.mk

DIR = ./
INCDIR = ${DIR}/include
#
# UNIX commands
#
CP    = /bin/cp -f
RM    = /bin/rm -f
MKEXE = /bin/chmod 755
AR    = /usr/bin/ar
#
# Libraries
#
# LIB = -lblas
# for intel ifort and mkl
ifdef LIB
LIB0 = ${LIB}
else
LIB = -L/home/softwares/intel/composer_xe_2013.1.117/mkl/lib/intel64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
endif
# for gfortran and lapack
#LIB = -L../lapack/lib -llapack -lrefblas
#
#LIB = -L/opt/intel/Compiler/11.1/064/mkl/lib/em64t -lmkl_lapack -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
#LIB =   -llapack -lblas
#
# Compilers
#
F90C = ifort
#F90C = gfortran
#F90C = pgf90
#F90FLAGS = -FR -O3 -I${INCDIR} -check all -check bounds 

# for gfortran
F90FLAGS = -O3 

# for ifort
#F90FLAGS = -O3 -stand f03 -check all -traceback -warn all -fstack-protector -assume protect_parens -implicitnone

#F90FLAGS =    -Mbounds -I${INCDIR}
#F90FLAGS = -g -Mbounds -I${INCDIR} -fpic
#F90FLAGS =  -fastsse -tp athlonxp -I${INCDIR}

FC = ifort
#FC = gfortran
#FC = pgf90
#FFLAGS = -g -Mbounds -I${INCDIR} -fpic
#FFLAGS = -l lapack -l f77blas -l atlas
#FFLAGS = -O3   

 CC = gcc
#CFLAGS = -O3    
RUNAR = ar rv
#
# Executable, source and objects
#
EXE  = main_overlap_slater.exe
#EXE = testfft.exe
ARCHI = ${DIR}/${EXE:.exe=.a}
MAIN = ${EXE:.exe=.f90}

#FSRC = read_tool.o



F90SRC =  sub_csf_overlap.o    sub_determinant.o    sub_orbital_overlap.o    sub_read_all.o    sub_state_overlap.o    sub_wf_overlap.o

CSRC = 

#
# Dependencies
#
${ARCHI}: ${FSRC} ${F90SRC} ${CSRC}
	${AR} rv ${ARCHI} *.o

${EXE}: ${ARCHI} ${MAIN}
	${AR} rv ${ARCHI} *.o
	${F90C}  -o  $@ ${F90FLAGS} ${MAIN} ${ARCHI} ${LIB}  

install: ${EXE} clean
	
#   cp ${EXE} main_overlap_slater.exe
	${RM} *.o

clean:
	${RM} *.o

veryclean:
	${RM} ${EXE} *.o ${ARCHI}

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
