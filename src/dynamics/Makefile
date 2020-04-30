#
# Paths to directories commands
#
include ../compiler.mk

DIR = .
INCDIR = ${DIR}/include

MAPPING = ${DIR}/mapping
ADIA = ${MAPPING}/adia
FLY = ${MAPPING}/on_the_fly
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
#LIB = -llapack -lblas
LIB = -mkl
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
#F90FLAGS = -FR -O3 -I${INCDIR}
# F90FLAGS =    -Mbounds -I${INCDIR}
#F90FLAGS = -FR -fcheck=bounds  -I${INCDIR}
F90FLAGS = -I${INCDIR}
#F90FLAGS = -O3 -stand f03 -check all -traceback -warn all -fstack-protector -assume protect_parens -implicitnone  -I${INCDIR}
#F90FLAGS = -g -Mbounds -I${INCDIR} -fpic
#F90FLAGS =  -fastsse -tp athlonxp -I${INCDIR}
#FC = ifc
#FC = pgf90
#FFLAGS = -g -Mbounds -I${INCDIR} -fpic
#FFLAGS = -l lapack -l f77blas -l atlas
#FFLAGS = -O3   

#CC = ifort
CC = gcc
CFLAGS = -O2 -mcpu=i486 -I. -DLINUX -D__I8=0 -D__ENDIAN=0 
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

F90SRC = sub_sh_zn.o sub_zn_hopping.o constant.o sub_random.o sub_string.o sub_write_current_geom.o      sub_mndo_many.o    sub_read_current_geom.o sub_save_gradient.o  sub_save_grad.o  sub_save_hopping_num_nac.o   sub_tully_hopping_num_nac.o sub_decoherent_corr.o   sub_nac_phase.o   sub_read_ini_vel.o          sub_save_traj.o              sub_velocity_scaling.o sub_get_mass.o  sub_newton_coor.o  sub_read_restart.o sub_sh_ana_nac.o  sub_write_current_geom.o sub_many_ana_pes.o      sub_newton_vel.o   sub_save_energy.o sub_sh_num_nac.o sub_many_pes_num_nac.o  sub_read_coor.o    sub_save_hopping_ana_nac.o  sub_tully_hopping_ana_nac.o sub_save_pe.o sub_save_restart.o sub_random3.o langevin.o sub_lang_sh_num_nac.o \
# ${MAPPING}/mod_main.o \
# ${MAPPING}/sub_mapping_ana_nac.o \
# ${MAPPING}/sub_read_control.o  ${MAPPING}/sub_nuc_motion.o  \
# ${MAPPING}/sub_nuc_get_dH_div_dX_or_dP.o  ${MAPPING}/sub_nuc_get_dHmn_div_dP.o  \
# ${MAPPING}/sub_nuc_get_dHmn_div_dX.o  ${MAPPING}/sub_move.o  \
# ${MAPPING}/sub_write_trj_1.o  ${MAPPING}/sub_write_trj_2.o \
# ${MAPPING}/sub_read_parameter.o  ${MAPPING}/sub_read_ini_trj_1.o  ${MAPPING}/sub_read_ini_trj_2.o \
# ${MAPPING}/sub_elec_get_dH_div_dx_or_dp.o  \
# ${MAPPING}/sub_get_dia_Ham_elec.o  ${MAPPING}/sub_get_c_n_elec_1.o  ${MAPPING}/sub_get_c_n_elec_2.o \
# ${MAPPING}/sub_get_c_n_elec_2_traj_adjusted.o \
# ${MAPPING}/sub_evolution_1.o  ${MAPPING}/sub_evolution_2.o  ${MAPPING}/sub_elec_motion_1.o  ${MAPPING}/sub_elec_motion_2.o \
# ${MAPPING}/sub_read_ini_trj_1.o  ${MAPPING}/sub_read_ini_trj_2.o  \
# ${MAPPING}/sub_evolution_3.o  ${MAPPING}/sub_write_trj_3.o ${MAPPING}/sub_elec_motion_3.o  \
# ${MAPPING}/sub_sum_sq_sum_by4.o  ${MAPPING}/sub_elec_motion_3_step1.o  ${MAPPING}/sub_elec_motion_3_step1_2.o  \
# ${MAPPING}/sub_elec_motion_3_step2.o  ${MAPPING}/sub_elec_motion_3_step2_2.o  \
# ${MAPPING}/sub_elec_get_dH_div_dx_or_dp_3.o  ${MAPPING}/sub_get_c_n_elec_3.o  \
# ${MAPPING}/sub_elec_get_dH_div_dx_or_dp_aver_PES.o  \
# ${MAPPING}/sub_elec_motion_2_aver_PES.o  \
# ${MAPPING}/sub_nuc_motion_aver_PES.o  \
# ${MAPPING}/sub_nuc_get_dH_div_dX_or_dP_aver_PES.o  \
# ${MAPPING}/sub_nuc_get_dH_div_dP_aver_PES.o  \
# ${MAPPING}/sub_evolution_mapping_2_Ham_4.o  \
# ${MAPPING}/sub_read_parameter_Ham_4.o  \
# ${MAPPING}/sub_get_dia_Ham_elec_Ham_4.o  \
# ${MAPPING}/sub_get_dia_Ham_elec_Ham_tor.o  \
# ${MAPPING}/sub_elec_motion_mapping_2_Ham_4_aver_PES.o  \
# ${MAPPING}/sub_nuc_motion_Ham_4_aver_PES.o  \
# ${MAPPING}/sub_nuc_get_dHmn_div_dX_Ham_tor.o  \
# ${MAPPING}/sub_elec_motion_mapping_1_Ham_4.o  \
# ${MAPPING}/sub_evolution_mapping_1_Ham_4.o  \
# ${MAPPING}/sub_nuc_motion_Ham_4.o  \
# ${MAPPING}/sub_nuc_get_dH_div_dP.o  \
# ${MAPPING}/sub_evolution_adia.o  \
# ${MAPPING}/sub_dia_to_adia.o  \
# ${MAPPING}/sub_diag.o  \
# ${MAPPING}/sub_cal_gammas.o  \
# ${FLY}/sub_read_parameter_on_the_fly.o  \
# ${FLY}/sub_evolution_mapping_2_on_the_fly.o  \
# ${FLY}/sub_read_parameter_on_the_fly.o  \
# ${FLY}/sub_many_ana_pes_mapping.o  \
# ${FLY}/sub_reshape_n_mode_to_n_atom.o  \
# ${FLY}/sub_reshape_n_atom_to_n_mode.o  \
# ${FLY}/sub_nac_phase_mapping.o  \
# ${FLY}/sub_read_current_geom_mapping.o  \
# ${FLY}/sub_write_current_geom_mapping.o  \
# ${FLY}/sub_write_geom_mapping.o  \
# ${FLY}/sub_write_geom.o  \
# ${FLY}/sub_test.o  \
# ${FLY}/sub_evolution_mapping_2_on_the_fly_traj_adjusted.o  \
# ${FLY}/sub_write_geom_mapping_traj_adjusted.o  \
# ${ADIA}/sub_nuc_get_dHmn_div_dX_adia.o  \
# ${ADIA}/sub_motion_2_adia_aver_PES_1step.o  \
# ${ADIA}/sub_p_to_p_kin.o  \
# ${ADIA}/sub_p_kin_to_p.o  \
# ${ADIA}/sub_elec_motion_2_aver_PES_adia.o  \
# ${ADIA}/sub_elec_motion_2_aver_PES_1step_adia.o  \
# ${ADIA}/sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia.o  \
# ${ADIA}/sub_nuc_motion_2_aver_PES_adia.o  \
# ${ADIA}/sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia.o  \
# ${ADIA}/sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia_traj_adjusted.o  \
# ${ADIA}/sub_calc_dV_eff_div_dx_nuc_adia.o  \
# ${ADIA}/sub_calc_dV_eff_div_dx_nuc_adia_traj_adjusted.o  \
# ${ADIA}/sub_calc_dp_nuc_kin__dij_term_adia.o  \
# ${ADIA}/sub_write_trj_2_adia.o  \
# ${ADIA}/sub_nuc_motion_2_aver_PES_1step_dx_div_dt_adia.o


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
