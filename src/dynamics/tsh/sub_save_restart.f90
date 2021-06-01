
subroutine  sub_save_restart (n_atom, &
     coor_x, coor_y, coor_z, &
     vel_x, vel_y, vel_z, &
     atom_label, &
     n_state, &
     rho, &
     index_state, &
     it, time)

  implicit none
  include 'param.def'
      
  integer, intent(in) :: n_atom, it, n_state
  double precision, intent(in) :: time
 
  double precision, intent(in), dimension(n_atom) ::   &
       coor_x, &
       coor_y, &
       coor_z

  double precision, intent(in), dimension(n_atom) ::   &
           vel_x, &
           vel_y, &
           vel_z
      
  character*2, intent(in), dimension(n_atom)  ::  atom_label
  complex (kind=8), intent(inout), dimension(n_state, n_state) :: rho
  integer, intent(inout) :: index_state

  integer ::  i, j, tmp_i, tmp_j

  tmp_i = 0
  tmp_j = 0
      
  open(unit=100, file="restart_all", status='replace')
  write(100, *) "------------------------------------"
  write(100, *) "RESTART FILE"
  write(100, *) ""
  write(100, *) "------------------------------------"
  write(100, *) n_atom
      
  do i = 1, n_atom
     write (100, *) atom_label(i), &
          coor_x(i), &
          coor_y(i), &
          coor_z(i)
  enddo

  write (100, *) ""
  write (100, *) ""
  write (100, *) ""
  write (100, *) ""
  do i = 1, n_atom
     write(100, *) atom_label(i), &
          vel_x(i), &
          vel_y(i), &
          vel_z(i)
  enddo

  write (100, *) ""
  write (100, *) n_state
  do i = 1, n_state
     do j = 1, n_state
        write (100, *) tmp_i, tmp_j, rho(i,j)
     enddo
  enddo
         
  ! write current state
  write (100, *) "current state"
  write (100, *) ""
  write (100, *) index_state

  close(100)

  return

end subroutine sub_save_restart



  
