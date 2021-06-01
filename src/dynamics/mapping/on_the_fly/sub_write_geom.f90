subroutine sub_write_geom (n_atom, &
                          coor_x, coor_y, coor_z, &
                          vel_x, vel_y, vel_z, &
                          atom_label, &
                          n_state, &
                          rho, &
                          index_state, &
                          it, time )

implicit none
include 'param.def'

integer, intent(in) :: n_atom, it, n_state, index_state
!      integer, intent(in) :: file_save_traj, file_save_vel
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

complex (kind=8), intent(in), dimension(n_state, n_state) :: rho



integer ::  i, j
      
     
if (it .eq. 0) then     
  open(unit=100, file="geom.xyz")
else
  open(unit=100, position='append', file='geom.xyz')
endif
write (100, *) n_atom
write (100, 9998)  "ANG", "Step:", it, "Time:", time
do  i=1, n_atom  
     write (100, 9999) atom_label(i), &
                                  coor_x(i)*BOHRTOANG, &
                                  coor_y(i)*BOHRTOANG, &
                                  coor_z(i)*BOHRTOANG
enddo  
close(100)



9999   format(a, 1x, 3(f20.10, 1x))
9998   format(a,  1x, a, 1x, i10, 1x, a, f20.10)
9997   format(i10, 1x, 20(f20.10, 1x))

return

end 
