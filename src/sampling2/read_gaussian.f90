      subroutine  read_gaussian (n_atom, atom_label, &
                                    coor_x, coor_y, coor_z, &
                                    n_mode, frequency, mass_mode, &
                                    coor_vib, file_molden, &
                                    filename_es_output)



      implicit none
!     include parameters
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: n_atom, n_mode, file_molden
      character*100, intent(in) :: filename_es_output
      double precision, intent(inout), dimension(n_atom)  :: &
                                                    coor_x, &
                                                    coor_y, &
                                                    coor_z
      double precision, intent(inout), dimension(n_mode,3*n_atom)  :: &
                                                    coor_vib
      character*2, intent(inout), dimension(n_atom)   :: & 
                                                    atom_label
      double precision, intent(inout), dimension(n_mode) :: &
                                                    frequency, &
                                                    mass_mode
 
 

!     Local variables
      integer :: i, j, k
      integer :: res_atom, n_line , n_mode_zero, label_read      
!      double precision, allocatable, dimension (:)   :: x, &
!                                                        y, &
!                                                        z
      
      integer :: test_n_atoms
      double precision, allocatable, dimension (:,:)   :: vx_all, &
                                                          vy_all, &
                                                          vz_all
      integer, allocatable, dimension(:)  :: atom_number
      character*80 string, string1, string2, string3,string4, &
                   tmp_atom_label
      integer  n_index, tmp_atom_number
      double precision, allocatable, dimension (:) :: mode_zero, &
                                                      freq_all, &
                                                      mass_all, &
                                                      dis_res




!      allocate (x(n_atom))
!      allocate (y(n_atom))
!      allocate (z(n_atom))

      allocate (vx_all(n_mode, n_atom))
      allocate (vy_all(n_mode, n_atom))
      allocate (vz_all(n_mode, n_atom))
      allocate (freq_all(n_mode))
      allocate (mass_all(n_mode))
      allocate (atom_number(n_atom))


      label_read = 0 

      mass_mode(:) = 1.0

      res_atom = mod (n_mode, 5)
      n_line = (n_mode - res_atom) / 5

      allocate ( dis_res (res_atom) )

      open(unit=file_molden, file=trim(filename_es_output))

      do while (1) 
! if std not found use input ori
         read (file_molden, 8888, end=8887) string
         if ( string(26:46)  .eq. &
             "Standard orientation:" ) then
            write (*,*) "Find Geometry"
            do i=1,4
               read (file_molden,*)
            enddo
            do i=1, n_atom
               read (file_molden,*) n_index, &
                           atom_number(i), &
                           n_index, & 
                           coor_x(i), &
                           coor_y(i), &
                           coor_z(i)
!               write (*,*) coor_x(i), &
!                           coor_y(i), &
!                           coor_z(i)
            enddo
            goto 8887
         endif
      enddo

8888   format(a80)
8887   close (file_molden)
   
      do i=1, n_atom
         tmp_atom_number = atom_number(i)
         call  atom_number_to_label (tmp_atom_number, tmp_atom_label )
         atom_label(i) = tmp_atom_label
      enddo

      coor_x(:) = coor_x(:)*ANSTOBOHR
      coor_y(:) = coor_y(:)*ANSTOBOHR
      coor_z(:) = coor_z(:)*ANSTOBOHR
 
      write (*,*) "Begin to read frequency of each mode" 
      open(unit=file_molden, file=trim(filename_es_output))

      do while (1)
         read (file_molden, 8888, end=8885) string

         if ( string(2:21)  .eq.  &
              "Harmonic frequencies" ) then
            write (*,*)  "Find the normal modes"
            
            do k=1, 3
               read(file_molden,8888) string1
!               write (*,*) "string1", k, string1
            enddo

            do k=1,n_line
                read(file_molden,8888) string1
!                write (*,*) 14, string1
                read(file_molden,8888) string1
!                write (*,*) 15, string1
!                read(file_molden,*)
                read(file_molden,*)   string1, string2, &
                    freq_all(1+(k-1)*5),freq_all(2+(k-1)*5), &
                    freq_all(3+(k-1)*5),freq_all(4+(k-1)*5), &
                    freq_all(5+(k-1)*5)
!                write (*,*) freq_all(1+(k-1)*6),freq_all(2+(k-1)*6), &
!                    freq_all(3+(k-1)*6),freq_all(4+(k-1)*6), &
!                    freq_all(5+(k-1)*6),freq_all(6+(k-1)*6)

                read (file_molden,*)  string1, string2, string3, &
                              mass_all(1+(k-1)*5),mass_all(2+(k-1)*5), &
                              mass_all(3+(k-1)*5),mass_all(4+(k-1)*5), &
                              mass_all(5+(k-1)*5)


                do j=1,6
                   read(file_molden,*)
                enddo 

                do i=1,n_atom
                   read(file_molden,*)   string1, string2, string3, &
                           vx_all(1+(k-1)*5,i),vx_all(2+(k-1)*5,i), &
                           vx_all(3+(k-1)*5,i),vx_all(4+(k-1)*5,i), &
                           vx_all(5+(k-1)*5,i)

!                   write (*,*) "displacement, x"
!                   write (*,*) vx_all(1+(k-1)*6,i),vx_all(2+(k-1)*6,i), &
!                           vx_all(3+(k-1)*6,i),vx_all(4+(k-1)*6,i), &
!                           vx_all(5+(k-1)*6,i),vx_all(6+(k-1)*6,i)

                   read(file_molden,*)   string1, string2, string3, &
                           vy_all(1+(k-1)*5,i),vy_all(2+(k-1)*5,i), &
                           vy_all(3+(k-1)*5,i),vy_all(4+(k-1)*5,i), &
                           vy_all(5+(k-1)*5,i)

!                   write (*,*) "displacement, y"
!                   write (*,*) vy_all(1+(k-1)*6,i),vy_all(2+(k-1)*6,i), &
!                           vy_all(3+(k-1)*6,i),vy_all(4+(k-1)*6,i), &
!                           vy_all(5+(k-1)*6,i),vy_all(6+(k-1)*6,i)

                   read(file_molden,*)   string1, string2, string3, &
                           vz_all(1+(k-1)*5,i),vz_all(2+(k-1)*5,i), &
                           vz_all(3+(k-1)*5,i),vz_all(4+(k-1)*5,i), &
                           vz_all(5+(k-1)*5,i)
                   
!                   write (*,*) "displacement, z"
!                   write (*,*) vz_all(1+(k-1)*6,i),vz_all(2+(k-1)*6,i), &
!                           vz_all(3+(k-1)*6,i),vz_all(4+(k-1)*6,i), &
!                           vz_all(5+(k-1)*6,i),vz_all(6+(k-1)*6,i)
                enddo
            
!                write (*,*) "mass"
!                write (*,*) string1
!                write (*,*) string2
!                write (*,*) string3
!                write (*,*) string4
!                write (*,*) mass_all(1+(k-1)*6),mass_all(2+(k-1)*6), &
!                           mass_all(3+(k-1)*6),mass_all(4+(k-1)*6), &
!                           mass_all(5+(k-1)*6),mass_all(6+(k-1)*6)

!                read(file_molden,*)
!                read(file_molden,*)
            enddo

!            write (*,*) "res_atom", res_atom
            if (res_atom .ge. 1) then
                read(file_molden,*)
                read(file_molden,*)
                read(file_molden,*)   string1, string2, &
                    freq_all(1+(k-1)*5 : res_atom+(k-1)*5)
!                write (*,*) freq_all(1+(k-1)*6 : res_atom+(k-1)*6)
                read (file_molden,*)  string1, string2, string3, &
                              mass_all( 1+(k-1)*5 : res_atom+(k-1)*5 )

                do j=1,6
                   read(file_molden,*)
                enddo

                do i=1,n_atom

                   read(file_molden,*)   string1, string2, string3, &
                           dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vx_all (j+(k-1)*5,i)  = dis_res(j)      
                   enddo
!                   write (*,*) dis_res(:)
                   read(file_molden,*)   string1, string2, string3, &
                           dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vy_all (j+(k-1)*5,i)  = dis_res(j)
                   enddo

                   read(file_molden,*)  string1, string2, string3, &
                             dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vz_all (j+(k-1)*5,i)  = dis_res(j)
                   enddo

                enddo

 
             endif

             label_read = 1
             goto 8885
          endif
      enddo


8885   close (file_molden)


       if (label_read .eq. 0)  then
           write (*,*)  "Please check the Gaussian output file !"
           stop
       endif



!       write (*,*) freq_all(:)
!       write (*,*) mass_all(:)

       write (*,*) "The number of normal mode is", n_mode
       do i=1, n_mode
!          write (*,*) "Mode", i
          frequency(i) = freq_all(i)
!          write (*,*) "Frequency:", frequency(i)
          mass_mode(i) = mass_all(i)
!          write (*,*)  "Mass:",  mass_mode(i)
       enddo



      

!       Write down the final transfermation matrix S(n_mode, n_atom)

        do i=1, n_mode
           do j=1, n_atom
               coor_vib(i,(j-1)*3+1) =  vx_all(i,j)   &
                                          /  (mass_mode(i))**0.5
               coor_vib(i,(j-1)*3+2) =  vy_all(i,j)   &
                                          /  (mass_mode(i))**0.5
               coor_vib(i,(j-1)*3+3) =  vz_all(i,j)   &
                                          /  (mass_mode(i))**0.5
           enddo
        enddo
      
!        do i=1, 3*n_atom
!           write (*,*) "mode", i
!           do j=1, n_atom
!              write (*,*) vx_all(i,j), vy_all(i,j), vz_all(i,j)
!           enddo
!        enddo
        

!        print *, n_mode_zero
!        write (*,*) coor_vib(1,:)


!        deallocate (x)
!        deallocate (y)
!        deallocate (z)

        deallocate (vx_all)
        deallocate (vy_all)
        deallocate (vz_all)
        deallocate (freq_all)
        deallocate (mass_all)





      return 


      

        
       end subroutine read_gaussian
       


