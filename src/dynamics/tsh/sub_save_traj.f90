      subroutine  sub_save_traj (n_atom, &
                            coor_x, coor_y, coor_z, &
                            vel_x, vel_y, vel_z, &
                            atom_label, &
                            it, time, &
                            file_save_traj, file_save_vel )



      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: file_save_traj, file_save_vel
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


      integer ::  i
      
     

      write (file_save_traj, *) n_atom
      write (file_save_vel, *) n_atom 

      write (file_save_traj, 9998)  "ANG", "Step:", it, "Time:", time
      write (file_save_vel,  9998)  "AU" , "Step:", it, "Time:", time


  
      do  i=1, n_atom  
          write (file_save_traj, 9999) atom_label(i), &
                                       coor_x(i)*BOHRTOANG, &
                                       coor_y(i)*BOHRTOANG, &
                                       coor_z(i)*BOHRTOANG
  
          write (file_save_vel, 9999) atom_label(i), &
                                      vel_x(i), &
                                      vel_y(i), &
                                      vel_z(i)
      enddo

      write (900, *) n_atom
      write (900,  9998)  "AU" , "Step:", it, "Time:", time
      do  i=1, n_atom
          write (900, 9999) atom_label(i), &
                                       coor_x(i), &
                                       coor_y(i), &
                                       coor_z(i)
      enddo



9999   format(a, 1x, 3(f20.10, 1x))
9998   format(a,  1x, a, 1x, i10, 1x, a, f20.10)

       return
 
       end 
