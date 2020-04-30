#
# Paths to directories commands
#
DIR = ./
INCDIR = ${DIR}/include
#
# UNIX commands
#
CP	  = /bin/cp -f
RM	  = /bin/rm -f
MKEXE = /bin/chmod 755
AR	  = /usr/bin/ar
#
# Libraries
#
# LIB = -lblas
#LIB = -L/home/softwares/intel/composer_xe_2013.1.117/mkl/lib/intel64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
#
LIB = -mkl
#LIB = -L/opt/intel/Compiler/11.1/064/mkl/lib/em64t -lmkl_lapack -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
#LIB =	 -llapack -lblas
#
# Compilers
#
F90C = ifort
#F90C = pgf90
#F90FLAGS = -FR -O3 -I${INCDIR} -check all -check bounds 
F90FLAGS = -O3 -stand f03 -check all -traceback -warn all -fstack-protector -assume protect_parens -implicitnone

#F90FLAGS =    -Mbounds -I${INCDIR}
#F90FLAGS = -g -Mbounds -I${INCDIR} -fpic
#F90FLAGS =  -fastsse -tp athlonxp -I${INCDIR}

FC = ifort
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
EXE  = main_pop.exe
ARCHI = ${DIR}/${EXE:.exe=.a}
MAIN = ${EXE:.exe=.f90}

#FSRC = read_tool.o

F90SRC = sub_inverse_matrix.o	sub_overlap_half.o	sub_read_all.o	sub_transition_density.o  sub_pop_density.o



CSRC = 


PARSER = pop_parser.exe
PARSRC = pop_parser.f90 sub_fragit.f90 sub_contour.f90

#
# Dependencies
#
${ARCHI}: ${FSRC} ${F90SRC} ${CSRC}
	${AR} rv ${ARCHI} *.o

${EXE}: ${ARCHI} ${MAIN}
	${AR} rv ${ARCHI} *.o
	${F90C}  -o  $@ ${F90FLAGS} ${MAIN} ${ARCHI} ${LIB}  
	${F90C}  -o ${PARSER} ${PARSRC}	 
	mv main_pop.exe pop_main.exe



install: ${EXE} ${PARSER} clean

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
