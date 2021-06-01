subroutine   sub_mapping_ana_nac
use mod_main
implicit none


integer file_dyn_in


write(*,*) '************************************************************************'
write(*,*) 
write(*,*) 'hamilton_type:'
write(*,*) '1. constant Vij; '
write(*,*) '2. LVC; '
write(*,*) '3. V_aa = E_a_0 + 0.5 * w_a_i * Q_i**2 + k_a_i * Q_i,'
write(*,*) '   V_ab = la_ab_0_i + la_ab_1_i * Q_i'
write(*,*) '4. M Type-3 modes, N torsional modes'
write(*,*) 'torsional potential: '
write(*,*) '0.5 * I_inverse * P_i **2 + 0.5 * V_i_n * ( 1 - cos(A) ) * c_n'
write(*,*) 
write(*,*) 'mapping_model: Please see JCP, 145, 204105(2016).'
write(*,*) 'The sequence is the same as that in the paper.'
write(*,*) 'Model 1. '
write(*,*) '    c_nn = x * p_y - y * p_x = 1 (occupied) or 0 (unoccupied)'
write(*,*) '    c_nm = x_n * p_y_m - y_m * p_x_n'
write(*,*)
write(*,*) 'Model 2. MM model'
write(*,*)
write(*,*) 'Model 3. '
write(*,*) '    c_nn = [(x_n + p_y_n)**2 + (y_n-p_x_n)**2]/4'
write(*,*) '    c_nm = x_n * p_y_m - y_m * p_x_n'
write(*,*) 

call sub_read_control
!write(*,*) 'sub_read_control done!'
write(*,*) 'mapping_model: ', mapping_model
if (hamilton_type == 3) then
  if (mapping_model == 1) then
    call sub_evolution_1
  elseif (mapping_model == 2) then
    call sub_evolution_2
  elseif (mapping_model == 3) then
    call sub_evolution_3
  elseif (mapping_model == 0) then
    call sub_evolution_adia
  ! 10 for "on the fly", 2 for MM model
  elseif (mapping_model == 102) then
    call sub_evolution_mapping_2_on_the_fly
  elseif (mapping_model == 1021) then  
    call sub_evolution_mapping_2_on_the_fly_traj_adjusted
  else
    write(*,*) 'mapping_model label error', mapping_model
    stop
  endif
elseif (hamilton_type == 4) then
  if (mapping_model == 1) then
    call sub_evolution_mapping_1_ham_4
    !stop "sub_evolution_mapping_1_ham_4.f90 is not available!"
  elseif (mapping_model == 2) then
    if (label_debug >= 2) write(*,*) 'sub_evolution_mapping_2_Ham_4 starts!'
    call sub_evolution_mapping_2_Ham_4
  elseif (mapping_model == 3) then
    !call sub_evolution_mapping_3_ham_4
    stop "sub_evolution_mapping_3_ham_4.f90 is not available!"
  else
    write(*,*) 'mapping_model label error', mapping_model
    stop
  endif
elseif (hamilton_type == 0) then
  !stop "Mapping on-the-fly programing!"
  call sub_evolution_mapping_2_on_the_fly()
else
  write(*,*) '------------------------------------------------------------------------'
  write(*,*) 'The function dealing with the Hamiltonian type'
  write(*,*) '    ', hamilton_type
  write(*,*) 'is not avialable now!'
  write(*,*) '------------------------------------------------------------------------'
endif

write(*,*) '************************************************************************'
write(*,*) 

return
end 
