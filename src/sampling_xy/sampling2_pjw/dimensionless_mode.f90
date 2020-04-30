      subroutine dimensionless_mode (n_atom, &
                                     atom_label, &
                                     coor_x, coor_y, coor_z, &
                                     n_mode, &
                                     frequency, &
                                     mass_mode, &
                                     coor_vib, &
                                     file_Q_vib  )

      implicit none
!     include parameters
      include "param.def"     

!     Define the input and output variables

      integer, intent(in) :: n_atom, n_mode, file_Q_vib
      double precision, intent(inout), dimension(n_atom)  :: &
                                                    coor_x, &
                                                    coor_y, &
                                                    coor_z

      character*2, intent(inout), dimension(n_atom)   :: &
                                                    atom_label


      double precision,intent(inout), dimension(n_mode) :: frequency, &
                                                        mass_mode

      double precision,intent(inout), dimension(n_mode,3*n_atom) :: &
                                               coor_vib
 

!     Define the local variables
 
      integer :: i, j, k      

      

      
      do i=1, n_mode
      do j=1, n_atom
      coor_vib (i, (j-1)*3+1) = coor_vib (i, (j-1)*3+1) / &
                                ( sqrt(ATOMMASS*frequency(i)/TOCM) )
      coor_vib (i, (j-1)*3+2) = coor_vib (i, (j-1)*3+2) / &
                                ( sqrt(ATOMMASS*frequency(i)/TOCM) )
      coor_vib (i, (j-1)*3+3) = coor_vib (i, (j-1)*3+3) / &
                                ( sqrt(ATOMMASS*frequency(i)/TOCM) )
      enddo
      enddo




      write (file_Q_vib,*) "Reference geometry"
      do i=1, n_atom
      write (file_Q_vib,7777)  atom_label(i),  &
                        coor_x(i), &
                        coor_y(i), &
                        coor_z(i)

      enddo

      write (file_Q_vib,*) "Dimensionless normal coordinates"
      do i=1, n_mode
      write (file_Q_vib,*) "Mode", i
      write (file_Q_vib,*) "Frequency", frequency(i)
      do j=1, n_atom
      write (file_Q_vib,7777)  atom_label(j),  &
                        coor_vib (i, (j-1)*3+1), &
                        coor_vib (i, (j-1)*3+2), &
                        coor_vib (i, (j-1)*3+3)
      enddo
      enddo


7777  format (a, 1x, 3(f10.5, 2x)  )


      return 


      

        
       end subroutine dimensionless_mode
       


