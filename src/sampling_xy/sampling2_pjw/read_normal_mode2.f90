      subroutine   read_normal_mode2 (n_atom, atom_label, &
                                  coor_x, coor_y, coor_z, &
                                  n_mode, frequency, mass_mode, &
                                  coor_vib, &
                                  label_es_output, &
                                  filename_es_output, &
                                  file_molden)


      implicit none
!     include parameters
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: n_atom, n_mode, file_molden, &
                             label_es_output
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
 
 
      ! Local variable
      character*80 string
      integer :: n_atom_test, n_mode_test
      integer :: i, j, k, label_read

      integer, dimension(n_atom)   ::  atom_number

      ! Read in data
      open(unit=file_molden, file=trim(filename_es_output))

      do while (.true.)
         read (file_molden, 8888, end=8887) string
         ! write(*,*) string
         read (file_molden, *, end=8887) n_atom_test
         ! write(*,*) n_atom_test
         if ( n_atom_test .eq. n_atom) then
            write(*, *) "The number of atoms are", n_atom_test
         else
            write (*, *) "Check the number of atoms"
         endif

         do i = 1, n_atom
            read (file_molden, *) atom_label(i), atom_number(i), &
                 coor_x(i), &
                 coor_y(i), &
                 coor_z(i)
         enddo

         read (file_molden, *, end=8887) n_mode_test, n_atom_test
         if ( n_mode_test .eq. n_mode) then
            write(*,*) "The number of normal mode are", n_mode_test
         else
            write (*,*) "Check the number of normal mode"
         endif
         
         write (*,*) "Begin to read frequency of each mode"
         read (file_molden, 8888, end=8887) string
         do i = 1, n_mode
            read (file_molden,*) frequency(i)
            ! write (*,*) frequency(i)
         enddo
         
         write(*,*) "Begin to read reduced mass"
         read (file_molden, 8888, end=8887) string
         do i = 1, n_mode
            read(file_molden,*) mass_mode(i)
         enddo

         write(*,*) "Begin to Read normal mode"
         read (file_molden, 8888, end=8887) string
         do i = 1, n_mode
            do j = 1, n_atom
            read(file_molden,*) coor_vib(i,(j-1)*3+1), &
                 coor_vib(i,(j-1)*3+2), coor_vib(i,(j-1)*3+3)
            ! write(*,*) coor_vib(i,(j-1)*3+1), &
            !     coor_vib(i,(j-1)*3+2), coor_vib(i,(j-1)*3+3)

            enddo
         enddo
         go to 8887
         enddo

8888  format(a80)
8887  close(file_molden)

      write (*,*) "Finished!!!"

      end subroutine read_normal_mode2
       

