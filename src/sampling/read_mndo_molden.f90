      subroutine  read_mndo_molden (n_atom, atom_label, &
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
      integer :: i, j, k, label_read      
      double precision, allocatable, dimension (:)   :: x, &
                                                        y, &
                                                        z
      
      integer :: test_n_atoms
      double precision, allocatable, dimension (:,:)   :: vx, &
                                                          vy, &
                                                          vz
      character*80 string
      integer  nword, icint
      integer  ieof, isec, iscend
      character*80  word(40)

      isec = 0
      ieof = 0
      iscend = 0
      nword = 0

      label_read = 0


      allocate (x(n_atom))
      allocate (y(n_atom))
      allocate (z(n_atom))

      allocate (vx(n_mode, n_atom))
      allocate (vy(n_mode, n_atom))
      allocate (vz(n_mode, n_atom))

      mass_mode(:) = 1.0

      open(unit=file_molden, file=trim(filename_es_output))

      do while (1) 
         read (file_molden, 8888, end=8887) string
         call readln(string,word,nword,isec,ieof,iscend)
         
         if (word(1)(1:10)  .eq. "[FR-COORD]" ) then
            test_n_atoms = icint(word(2))
            if ( test_n_atoms  .eq. n_atom ) then
              write (*,*) "The number of atoms are", test_n_atoms
            else
              write (*,*) "Check the number of atoms"
              stop
            endif  
            do i=1, n_atom
               read (file_molden,*) atom_label(i), &
                           coor_x(i), &
                           coor_y(i), &
                           coor_z(i)
            enddo
            goto 8887
         endif
       enddo

8888   format(a80)
8887   close (file_molden)
   



 
      write (*,*) "Begin to read frequency of each mode" 
      open(unit=file_molden, file=trim(filename_es_output))
      do while (1)
         read (file_molden, 8886, end=8885) string
         call readln(string,word,nword,isec,ieof,iscend)
         if (word(1)(1:6)  .eq. "[FREQ]" ) then
            do i=1, n_mode
               read (file_molden,*) frequency(i)
               write (*,*) frequency(i)
            enddo
            go to 8885
         endif
       enddo

8886   format(a80)
8885   close (file_molden)


       write (*,*) "The number of normal mode is", n_mode
       do i=1, n_mode
       write (*,*) "Mode", i
       write (*,*) "Frequency:", frequency(i)
       enddo


     





      
      open(unit=file_molden, file=trim(filename_es_output))

      do while (1)
         read (file_molden, 8884, end=8883) string
         call readln(string,word,nword,isec,ieof,iscend)

         if (word(1)(1:15)  .eq. "[FR-NORM-COORD]" ) then
            do i=1, n_mode
               read (file_molden,*)
               do j=1, n_atom
                  read (file_molden,*) vx(i,j), &
                              vy(i,j), &
                              vz(i,j)
               enddo
            enddo
            label_read = 1 
            goto 8883
         endif
       enddo

8884   format(a80)
8883   close (file_molden)


       if (label_read .eq. 0)  then
           write (*,*)  "Please check the normal modes in Molden file !"
           stop
       endif



!       Write down the final transfermation matrix S(n_mode, n_atom)
        do i=1, n_mode
        do j=1, n_atom
        coor_vib(i,(j-1)*3+1) =  vx(i,j) 
        coor_vib(i,(j-1)*3+2) =  vy(i,j)
        coor_vib(i,(j-1)*3+3) =  vz(i,j)
        enddo
        enddo









      return 


      

        
       end subroutine read_mndo_molden
       


