      subroutine displacement_hand  (n_atom, &
                                     atom_label, &
                                     coor_x, coor_y, coor_z, &
                                     n_mode, &
                                     frequency, &
                                     coor_vib, &
                                     file_stru_au, &
                                     file_stru_ang  )

      implicit none
!     include parameters
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: n_atom, n_mode
      integer, intent(in) :: file_stru_au, file_stru_ang
      double precision, intent(inout), dimension(n_atom)  :: &
                                                    coor_x, &
                                                    coor_y, &
                                                    coor_z
      double precision, intent(inout), dimension(n_mode,3*n_atom)  :: &
                                                    coor_vib
      character*2, intent(inout), dimension(n_atom)   :: & 
                                                    atom_label
      double precision, intent(inout), dimension(n_mode) :: &
                                                    frequency
 
 

!     Local variables
      integer :: i, j, k      
      double precision, allocatable, dimension (:,:) :: Q_normal 
      double precision, allocatable, dimension (:,:) :: Q_xyz
      double precision, allocatable, dimension (:)   :: x, &
                                                        y, &
                                                        z


      allocate (Q_normal(1,n_mode))
      allocate (Q_xyz(1,3*n_atom))
      allocate (x(n_atom))
      allocate (y(n_atom))
      allocate (z(n_atom))




!    Make displacement in [-1,1] !
!    Step is 0.1
      
      Q_normal =0.0
      
      do i=1, n_mode
         
          write (file_stru_au,*) "Mode", i 
!      Calculate the displacement of the normal coordinates
!      Write down the structures for each Q_vib
          do j=1, 21 
            Q_normal(1,i)=-2+(j-1)*0.2           
            Q_xyz = MATMUL (Q_normal, coor_vib)
      
            do k=1, n_atom
               x(k) = coor_x(k) + Q_xyz(1, 3*(k-1)+1)
               y(k) = coor_y(k) + Q_xyz(1, 3*(k-1)+2)
               z(k) = coor_z(k) + Q_xyz(1, 3*(k-1)+3)
            enddo

            write (file_stru_au,*) "Displacement", Q_normal(1,i)
            
            write (file_stru_ang,*) n_atom
            write (file_stru_ang,*) "Displacement, Mode",i,Q_normal(1,i)
            do k=1, n_atom 
               write (file_stru_au,7777) atom_label(k), &
                               x(k), y(k), z(k)
               write (file_stru_ang,7777) atom_label(k), &
                               x(k)*BOHRTOANG, &
                               y(k)*BOHRTOANG, &
                               z(k)*BOHRTOANG

            enddo
            Q_normal(1,i)=0.0
          enddo
      enddo
 

7777  format (a, 1x, 3(f10.5, 2x)  )

      close(60)
      close(61)

      

      deallocate (Q_normal)
      deallocate (Q_xyz)
      deallocate (x)
      deallocate (y)
      deallocate (z)


      return 


      

        
       end subroutine displacement_hand
       


