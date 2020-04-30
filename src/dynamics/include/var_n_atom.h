!
!***********************************************************************    

integer  md_state

double precision, dimension(n_atom) ::   &
                                                coor_x, &
                                                coor_y, &
                                                coor_z

double precision, dimension(n_atom) ::   &
                                                vel_x, &
                                                vel_y, &
                                                vel_z

character*2, dimension(n_atom)  ::  atom_label


integer :: file_save_energy, file_save_traj,  &
           file_save_grad, &
           file_save_vel, file_md_out, &
           file_save_state, file_save_all, &
           file_save_ele, file_save_pe, &
           file_save_dipole


double precision, dimension(n_state, n_atom) ::   &
                                         gra_all_x, &
                                         gra_all_y, &
                                         gra_all_z



double precision, dimension(n_state, n_state, n_atom) ::   &
                                         nac_x, &
                                         nac_y, &
                                         nac_z

double precision, dimension(n_state, n_state, n_atom) ::   &
                                         old_nac_x, &
                                         old_nac_y, &
                                         old_nac_z


double precision :: time, pes_ref, pes_current


double precision, dimension(n_state) ::  pes_all,  &
                                         old_pes_all 
complex (kind=8), dimension(n_state, n_state) :: rho 
double precision :: tmp_mass
integer          :: tmp_charge   
character*2      :: tmp_label
