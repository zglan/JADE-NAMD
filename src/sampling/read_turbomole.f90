      subroutine  read_turbomole (n_atom, atom_label, &
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
      integer :: res_atom, n_line , n_mode_zero      
      double precision, allocatable, dimension (:)   :: x, &
                                                        y, &
                                                        z
      
      integer :: test_n_atoms, label_read
      double precision, allocatable, dimension (:,:)   :: vx_all, &
                                                          vy_all, &
                                                          vz_all
      character*80 string, tmp_string, string1, string2, string3,string4
      integer  nword, icint
      integer  ieof, isec, iscend
      character*80  word(40)
      double precision, allocatable, dimension (:) :: mode_zero, &
                                                      freq_all, &
                                                      mass_all, &
                                                      dis_res

      isec = 0
      ieof = 0
      iscend = 0
      nword = 0

      label_read = 0


!      allocate (x(n_atom))
!      allocate (y(n_atom))
!      allocate (z(n_atom))

      allocate (vx_all(3*n_atom, n_atom))
      allocate (vy_all(3*n_atom, n_atom))
      allocate (vz_all(3*n_atom, n_atom))
      allocate (freq_all(3*n_atom))
      allocate (mass_all(3*n_atom))


      mass_mode(:) = 1.0

      res_atom = mod (3*n_atom, 6)
      n_line = (3*n_atom - res_atom) / 6
      n_mode_zero = 3*n_atom - n_mode

      allocate (mode_zero (n_mode_zero))
      allocate ( dis_res (res_atom) )

      open(unit=file_molden, file=trim(filename_es_output))

      do while (1) 
         read (file_molden, 8888, end=8887) string
         if ( string(15:66)  .eq. &
             "| Atomic coordinate, charge and isotop information |" ) then
            write (*,*) "Find Geometry"
            do i=1,4
               read (file_molden,*)
            enddo
            do i=1, n_atom
               read (file_molden,*) &
                           coor_x(i), &
                           coor_y(i), &
                           coor_z(i), &
                           atom_label(i)
!               write (*,*) coor_x(i), &
!                           coor_y(i), &
!                           coor_z(i)
            enddo
            goto 8887
         endif
      enddo

8888   format(a80)
8887   close (file_molden)
   



 
      write (*,*) "Begin to read frequency of each mode" 
      open(unit=file_molden, file=trim(filename_es_output))

      do while (1)
         read (file_molden, 8888, end=8885) string

         if ( string(11:50)  .eq.  &
              "NORMAL MODES and VIBRATIONAL FREQUENCIES" ) then
            write (*,*)  "Find the normal modes"
            
            do k=1, 13
               read(file_molden,8888) string1
!               write (*,*) "string1", k, string1
            enddo

            do k=1,n_line
                read(file_molden,8888) string1
!                 write (*,*) 14, string1
                read(file_molden,8888) string1
!                write (*,*) 15, string1
!                read(file_molden,*)
                read(file_molden,*)   string1, &
                    freq_all(1+(k-1)*6),freq_all(2+(k-1)*6), &
                    freq_all(3+(k-1)*6),freq_all(4+(k-1)*6), &
                    freq_all(5+(k-1)*6),freq_all(6+(k-1)*6)
!                write (*,*) freq_all(1+(k-1)*6),freq_all(2+(k-1)*6), &
!                    freq_all(3+(k-1)*6),freq_all(4+(k-1)*6), &
!                    freq_all(5+(k-1)*6),freq_all(6+(k-1)*6)

                do j=1,10
                   read(file_molden,*)
                enddo 

                do i=1,n_atom
                   read(file_molden,*)   string1, string2, string3, &
                           vx_all(1+(k-1)*6,i),vx_all(2+(k-1)*6,i), &
                           vx_all(3+(k-1)*6,i),vx_all(4+(k-1)*6,i), &
                           vx_all(5+(k-1)*6,i),vx_all(6+(k-1)*6,i)

!                   write (*,*) "displacement, x"
!                   write (*,*) vx_all(1+(k-1)*6,i),vx_all(2+(k-1)*6,i), &
!                           vx_all(3+(k-1)*6,i),vx_all(4+(k-1)*6,i), &
!                           vx_all(5+(k-1)*6,i),vx_all(6+(k-1)*6,i)

                   read(file_molden,*)   string3, &
                           vy_all(1+(k-1)*6,i),vy_all(2+(k-1)*6,i), &
                           vy_all(3+(k-1)*6,i),vy_all(4+(k-1)*6,i), &
                           vy_all(5+(k-1)*6,i),vy_all(6+(k-1)*6,i)

!                   write (*,*) "displacement, y"
!                   write (*,*) vy_all(1+(k-1)*6,i),vy_all(2+(k-1)*6,i), &
!                           vy_all(3+(k-1)*6,i),vy_all(4+(k-1)*6,i), &
!                           vy_all(5+(k-1)*6,i),vy_all(6+(k-1)*6,i)

                   read(file_molden,*)   string3, &
                           vz_all(1+(k-1)*6,i),vz_all(2+(k-1)*6,i), &
                           vz_all(3+(k-1)*6,i),vz_all(4+(k-1)*6,i), &
                           vz_all(5+(k-1)*6,i),vz_all(6+(k-1)*6,i)
                   
!                   write (*,*) "displacement, z"
!                   write (*,*) vz_all(1+(k-1)*6,i),vz_all(2+(k-1)*6,i), &
!                           vz_all(3+(k-1)*6,i),vz_all(4+(k-1)*6,i), &
!                           vz_all(5+(k-1)*6,i),vz_all(6+(k-1)*6,i)
                enddo
            
                read(file_molden,*)
                 
                read(file_molden,8888) string1
                open(unit=100, file="fort.100")
                write (100, *) string1(21:80)
                close(100)
                open(unit=100, file="fort.100")          
                read (100,*)  mass_all(1+(k-1)*6),mass_all(2+(k-1)*6), &
                              mass_all(3+(k-1)*6),mass_all(4+(k-1)*6), &
                              mass_all(5+(k-1)*6),mass_all(6+(k-1)*6)
                close(100)

!                write (*,*) "mass"
!                write (*,*) string1
!                write (*,*) string2
!                write (*,*) string3
!                write (*,*) string4
!                write (*,*) mass_all(1+(k-1)*6),mass_all(2+(k-1)*6), &
!                           mass_all(3+(k-1)*6),mass_all(4+(k-1)*6), &
!                           mass_all(5+(k-1)*6),mass_all(6+(k-1)*6)

                read(file_molden,*)
                read(file_molden,*)
            enddo

!            write (*,*) "res_atom", res_atom
            if (res_atom .ge. 1) then
                read(file_molden,*)
                read(file_molden,*)
                read(file_molden,*)   string1, &
                    freq_all(1+(k-1)*6 : res_atom+(k-1)*6)
!                write (*,*) freq_all(1+(k-1)*6 : res_atom+(k-1)*6)
                do j=1,10
                   read(file_molden,*)
                enddo

                do i=1,n_atom

                   read(file_molden,*)   string1, string2, string3, &
                           dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vx_all (j+(k-1)*6,i)  = dis_res(j)      
                   enddo
!                   write (*,*) dis_res(:)
                   read(file_molden,*)   string3, &
                           dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vy_all (j+(k-1)*6,i)  = dis_res(j)
                   enddo

                   read(file_molden,*)  string3, &
                             dis_res(1 : res_atom)
                   do j = 1, res_atom
                      vz_all (j+(k-1)*6,i)  = dis_res(j)
                   enddo

                enddo

                read(file_molden,*)

                read(file_molden,8888) string1
                open(unit=100, file="fort.100")
                write (100, *) string1(21:80)
                close(100)
                open(unit=100, file="fort.100")
                read (100,*)  mass_all( 1+(k-1)*6 : res_atom+(k-1)*6 )
                close(100)
                read(file_molden,*)
                read(file_molden,*)

             endif

             label_read = 1
             goto 8885
          endif
      enddo


8885   close (file_molden)


        if (label_read .eq. 0)  then
           write (*,*)  "Please check the Turbomole output !"
           stop
       endif




!       write (*,*) freq_all(:)
!       write (*,*) mass_all(:)

       write (*,*) "The number of normal mode is", n_mode
       do i=1, n_mode
!          write (*,*) "Mode", i
          frequency(i) = freq_all(i+n_mode_zero)
!          write (*,*) "Frequency:", frequency(i)
          mass_mode(i) = mass_all(i+n_mode_zero)
!          write (*,*)  "Mass:",  mass_mode(i)
       enddo



      

!       Write down the final transfermation matrix S(n_mode, n_atom)

        do i=1, n_mode
           do j=1, n_atom
               coor_vib(i,(j-1)*3+1) =  vx_all(i+n_mode_zero,j)   &
                                          /  (mass_mode(i))**0.5
               coor_vib(i,(j-1)*3+2) =  vy_all(i+n_mode_zero,j)   &
                                          /  (mass_mode(i))**0.5
               coor_vib(i,(j-1)*3+3) =  vz_all(i+n_mode_zero,j)   &
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


      

        
       end subroutine read_turbomole
       


