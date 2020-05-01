module restart
  implicit none

  type restarter
     integer :: n_atom
     integer :: it
     integer :: n_state


  end type restarter

  contains


    subroutine  sub_write_restart (res)
      implicit none
      include 'param.def'
      type(restarter) :: res
      
      integer :: it, n_atom, n_state
      double precision :: time
      double precision, dimension(n_atom) :: &
           coor_x, &
           coor_y, &
           coor_z

      double precision, dimension(n_atom) :: &
           vel_x, &
           vel_y, &
           vel_z

      character*2, dimension(n_atom) :: atom_label




         
         


    end subroutine sub_write_restart

         coor_x, coor_y, coor_z, &
     vel_x, vel_y, vel_z, &
     atom_label, &
     n_state, &
     rho, &
     index_state, &
     it, time )


         subroutine  sub_read_restart (n_atom, &
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
      complex (kind=8), intent(inout), dimension(n_state, n_state) :: rho
      integer, intent(inout) :: index_state

      integer ::  i, j, tmp_i, tmp_j
      
     
      open(unit=100, file="restart_all")
      read (100, *) 
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
      do i =1 , n_state
         do j=1, n_state
            read (100,*)  tmp_i, tmp_j, rho(i,j)
         enddo
      enddo

      read (100, *)
      read (100, *)
      read (100, *) index_state


      close(100)

       return
 
       end 


    
end module restart








e
