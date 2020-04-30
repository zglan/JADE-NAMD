      subroutine  sub_read_current_geom (n_atom, &
                            coor_x, coor_y, coor_z, &
                            vel_x, vel_y, vel_z, &
                            atom_label, &
                            n_state, &
                            rho, &
                            index_state, &
                            it, time )



      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it, n_state
      double precision, intent(in) :: time
 
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z

      double precision, intent(inout), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      
      character*2, intent(inout), dimension(n_atom)  ::  atom_label
      complex (kind=8),intent(inout),dimension(n_state, n_state) :: rho
      integer, intent(inout) :: index_state

      integer ::  i, j, tmp_i, tmp_j
      
      character*20 :: string,tmp_string     

      open(unit=100, file="curr_geom.tmp")
      write (*,*) "open curr_geom.tmp"
      read (100, *) string
      write (*,*) string
      read (100, *) 
      read (100, *) 
      read (100, *) 
      read (100, *) 
      do  i=1, n_atom  
           read (100, *) atom_label(i), &
                                        coor_x(i), &
                                        coor_y(i), &
                                        coor_z(i)
      enddo  

      write (*,*)  "Get coordinates"
      read (100, *) 
      read (100, *) 
      read (100, *) 
      read (100, *)  
      do  i=1, n_atom 

          read(100, *) atom_label(i), &
                                         vel_x(i), &
                                         vel_y(i), &
                                         vel_z(i)
      enddo

      read (100, *) 
      read (100, *)
      read (100, *)
      read (100, *)
      read (100, *)
 
      do i =1 , n_state
         do j=1, n_state
            read (100,*)  tmp_i, tmp_j, rho(i,j)
         enddo
      enddo

!     read (100, *)
!     read (100, *)
      read (100, *) tmp_string, tmp_string, tmp_string, &
                    tmp_string, index_state


      close(100)

       return
 
       end 
