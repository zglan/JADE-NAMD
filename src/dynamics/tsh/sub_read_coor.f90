      subroutine sub_read_coor ( n_atom, coor_x, coor_y, coor_z, &
                       atom_label, file_coor)


      implicit none
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: n_atom, file_coor
      
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z

      character*2, intent(inout), dimension(n_atom)  ::  atom_label
      
   
!     Define the local variables 
      integer :: i
      character*3 :: coor_unit 


      read (file_coor, *)
      read (file_coor, *)  coor_unit


      do i=1, n_atom
      read (file_coor, *)  atom_label(i),  &
                           coor_x (i),     &
                           coor_y (i),     &
                           coor_z (i)
 
      enddo


!     Change to the atomic unit for all coordinates
      if ( coor_unit .eq. "ANG") then      
        do i=1, n_atom 
           coor_x (i) = coor_x(i) / BOHRTOANG 
           coor_y (i) = coor_y(i) / BOHRTOANG
           coor_z (i) = coor_z(i) / BOHRTOANG
        enddo
      endif



      return 


      

        
       end subroutine sub_read_coor
       


