      subroutine   read_normal_mode (n_atom, atom_label, &
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
 
 

!     Local variables

      if ( label_es_output .eq. 1  ) then
         write (*,*)  "Read MOLDEN file generated from MNDO output"
         call  read_mndo_molden (n_atom, atom_label, &
                                    coor_x, coor_y, coor_z, &
                                    n_mode, frequency, mass_mode, &
                                    coor_vib, file_molden, &
                                    filename_es_output)
         write (*,*)  "Finish to Read MOLDEN file (MNDO output)."
      endif


      if ( label_es_output .eq. 2  ) then
         write (*,*) "Read Turbomole output file!"
         call  read_turbomole (n_atom, atom_label, &
                                    coor_x, coor_y, coor_z, &
                                    n_mode, frequency, mass_mode, &
                                    coor_vib, file_molden, &
                                    filename_es_output)
         write (*,*) "Finish to read Turbomole output file!"
      endif

!      write (*,*) frequency(:)
!      write (*,*) mass_mode(:)
!      write (*,*) coor_x 


      if ( label_es_output .eq. 3  ) then
         write (*,*) "Read Gaussian output file!"
         call  read_gaussian (n_atom, atom_label, &
                                    coor_x, coor_y, coor_z, &
                                    n_mode, frequency, mass_mode, &
                                    coor_vib, file_molden, &
                                    filename_es_output)
         write (*,*) "Finish to read Gaussian output file!"
      endif

 

       end subroutine read_normal_mode
       


