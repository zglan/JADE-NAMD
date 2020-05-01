      subroutine sub_write_current_geom (n_atom, &
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
      
     
      open(unit=100, file="curr_geom.tmp")
      write (100, *) "Geometry and velocity at the current steps"
      write (100, *) "------------------------------"
      write (100, *) "Geometry:"
      write (100, *) n_atom
      write (100, 9998)  "AU", "Step:", it, "Time:", time
      do  i=1, n_atom  
           write (100, 9999) atom_label(i), &
                                        coor_x(i), &
                                        coor_y(i), &
                                        coor_z(i)
      enddo  

      write (100, *) "------------------------------"
      write (100, *) "Velocity:"
      write (100, *) n_atom 
      write (100,  9998)  "AU" , "Step:", it, "Time:", time
      do  i=1, n_atom 

             write (100, 9999) atom_label(i), &
                                         vel_x(i), &
                                         vel_y(i), &
                                         vel_z(i)
      enddo
      write (100, *) "------------------------------"


      write (100, *) "------------------------------"
      write (100, *) "Total number of electron state is", n_state
      write (100, *) "Step and Time:",it, time
      write (100, *) "Density Matrix"
      do i=1, n_state
         do j=1, n_state
            write(100,*), i,j,rho(i,j)
         enddo
      enddo
      write (100, *) "The current state is", index_state
      close(100)





9999   format(a, 1x, 3(f20.10, 1x))
9998   format(a,  1x, a, 1x, i10, 1x, a, f20.10)

       return
 
       end 
