#
# Paths to directories commands
#
include ../src/compiler.mk

DIR = .
INCDIR = ${DIR}/numerical_nac
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
# LIB = -lblas
ifdef LIB
LIB0 = ${LIB}
else
LIB = -L/home/softwares/intel/composer_xe_2013.1.117/mkl/lib/intel64 -lmkl_lapack95_lp64 -lmkl_blas95_lp64 -lmkl_core -lmkl_sequential -lmkl_intel_lp64
endif

#LIB = -L./lapack/lib -llapack -lrefblas
#LIB =   -llapack -lblas

#AUXLIB = -L./aux -lstr_man
#
# Compilers
#
#F90C = ifc
F90C = ifort
#F90C = gfortran 
F90FLAGS = -FR -O3 -I${INCDIR}
# F90FLAGS =    -Mbounds -I${INCDIR}

#F90FLAGS = -O3 -stand f03 -check all -traceback -warn all -fstack-protector -assume protect_parens -implicitnone  -I${INCDIR}
#F90FLAGS = -g -Mbounds -I${INCDIR} -fpic
#F90FLAGS =  -fastsse -tp athlonxp -I${INCDIR}
#FC = ifc
#FC = pgf90
#FFLAGS = -g -Mbounds -I${INCDIR} -fpic
#FFLAGS = -l lapack -l f77blas -l atlas
#FFLAGS = -O3   

CC = ifort
# CC = gcc
#CFLAGS = -O3    
RUNAR = ar rv
#
# Executable, source and objects
#
EXE  = main_sh.exe
#EXE = testfft.exe
ARCHI = ${DIR}/${EXE:.exe=.a}
MAIN = ${EXE:.exe=.f90}

%.o: %.mod

#FSRC = read_tool.o

# F90SRC = dynamics.o newton_vel.o  read_coor.o  save_energy.o dynamics_single_pes.o newton_coor.o save_traj.o single_pes.o mndo_single.o get_mass.o surface_hopping.o tully_hopping.o many_pes.o mndo_many.o save_hopping.o velocity_scaling.o decoherent_corr.o read_ini_vel.o nac_phase.o

F90SRC = constant.o sub_random.o sub_string.o sub_write_current_geom.o      sub_mndo_many.o    sub_read_current_geom.o   sub_save_grad.o  sub_save_hopping_num_nac.o   sub_tully_hopping_num_nac.o sub_decoherent_corr.o   sub_nac_phase.o   sub_read_ini_vel.o          sub_save_traj.o              sub_velocity_scaling.o sub_get_mass.o  sub_newton_coor.o  sub_read_restart.o sub_sh_ana_nac.o  sub_write_current_geom.o sub_many_ana_pes.o      sub_newton_vel.o   sub_save_energy.o sub_sh_num_nac.o sub_many_pes_num_nac.o  sub_read_coor.o    sub_save_hopping_ana_nac.o  sub_tully_hopping_ana_nac.o sub_save_pe.o sub_save_restart.o sub_random3.o langevin.o sub_lang_sh_num_nac.o sub_sh_soc_gs.o sub_many_pes_soc.o sub_save_state.o sub_save_hop_all.o sub_tully_hopping_num_soc.o


CSRC = 

#
# Dependencies
#
${ARCHI}: ${FSRC} ${F90SRC} ${CSRC}
	${AR} rv ${ARCHI} *.o

${EXE}: ${ARCHI} ${MAIN}
	${AR} rv ${ARCHI} *.o
	${F90C}  -o  $@ ${F90FLAGS} ${MAIN} ${ARCHI} ${LIB} ${AUXLIB} 

install: ${EXE} 
	mv ${EXE} ../../bin/jade.exe
	${RM} *.o *.mod

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
