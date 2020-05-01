      subroutine sub_read_ini_vel (n_atom, vel_x, vel_y, vel_z, &
                                atom_label, file_ini_vel)


      implicit none
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: n_atom, file_ini_vel
      
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z

      character*2, intent(in), dimension(n_atom)  ::  atom_label
      
   
!     Define the local variables 
      integer :: i
      character*2, allocatable, dimension(:) :: atom_label_vel


      allocate (atom_label_vel(n_atom))

      read (file_ini_vel, *)
      read (file_ini_vel, *)  


      do i=1, n_atom
      read (file_ini_vel, *)  atom_label_vel(i),  &
                           vel_x (i),     &
                           vel_y (i),     &
                           vel_z (i)
 
      enddo


      deallocate(atom_label_vel)

      return 


      

        
       end subroutine sub_read_ini_vel
       


