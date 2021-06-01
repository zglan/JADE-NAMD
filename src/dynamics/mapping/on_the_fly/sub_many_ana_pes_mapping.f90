subroutine sub_many_ana_pes_mapping(x_nuc_cur, &
                  grad, &
                  dij_cur, &
                  ene_adia_cur, &
                  atom_label, &
                  i_step)
use mod_main
implicit none
include 'var_n_atom.h'
include 'var_n_mode.h'
integer index_state
integer label_no_nac
integer label_ml_pes
integer i_step

label_no_nac = 0
if (label_debug >= 2 ) then
    write(*,*) "sub_many_ana_pes_mapping"
    write(*,*) "qm_method:", qm_method
endif
call sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)
                
file_md_out = 2016
file_save_dipole = 2017
open(file_md_out, file="md_out.dat")
open(file_save_dipole, file="dipole.dat", position="append")
call sub_many_ana_pes  (n_atom, &
                  n_state, md_state, &
                  atom_label, &
                  coor_x, coor_y, coor_z, &
                  label_no_nac, &
                  label_ml_pes, &
                  qm_method, &
                  index_state, &
                  gra_all_x, &
                  gra_all_y, &
                  gra_all_z, &
                  nac_x, &
                  nac_y, &
                  nac_z, &
                  ene_adia_cur, &
                  i_step, &
                  file_md_out, &
                  file_save_dipole )
close(file_md_out)
close(file_save_dipole) 
call sub_reshape_n_atom_to_n_mode(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)


return
end
