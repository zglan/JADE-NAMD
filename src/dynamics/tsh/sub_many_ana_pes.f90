       subroutine    sub_many_ana_pes (n_atom, &
                                n_state, md_state, &
                                atom_label, &
                                coor_x, coor_y, coor_z, &
                                label_no_nac, &
                                label_ml_pes, &
                                qm_method, &
                                index_state, &
                                gra_all_x, &
                                gra_all_y, &
                                gra_all_z, &
                                nac_x, &
                                nac_y, &
                                nac_z, &
                                pes_all, &
                                it, &
                                file_md_out, &
                                file_save_dipole )
 

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, qm_method, n_state, label_no_nac, label_ml_pes
      integer, intent(in) :: file_md_out, file_save_dipole, &
                             index_state, it
      integer, intent(in), dimension(n_state) :: md_state(n_state)
      character*2, intent(in), dimension(n_atom)  ::  atom_label 
      double precision, intent(in), dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z


      double precision, intent(inout), dimension(n_state) :: pes_all
      double precision, intent(inout), dimension(n_state, n_atom) ::   &
                                                       gra_all_x, &
                                                       gra_all_y, &
                                                       gra_all_z
 
      double precision, intent(inout), dimension(n_state, n_state, n_atom) ::   &
                                                       nac_x, &
                                                       nac_y, &
                                                       nac_z




      integer  ::  i, j, k, i_status, system
      integer  ::  file_coor
      character*200 :: string

    


        file_coor=22
        open(unit=file_coor, file="coor_temp.xyz")
        write (file_coor, *)  n_atom
        write (file_coor, *)
        do i=1,n_atom
        write (file_coor, 9999)  atom_label(i),  &
                         coor_x(i),      &
                         coor_y(i),      &
                         coor_z(i)
        enddo
        close(file_coor)



9999   format (a2,1x, 3(f24.14,1x))



       gra_all_x = 0.d0
       gra_all_y = 0.d0
       gra_all_z = 0.d0
       nac_x     = 0.d0
       nac_y     = 0.d0
       nac_z     = 0.d0
       pes_all   = 0.d0



!     Write the interface for QC calculations
        !write(*,*) "qm_method:", qm_method
        open(unit=102, file="qm_interface")
        write (102,*)  "The interface between Fortran and Python"

        if ( qm_method .ne. 3 ) then 
           write (file_md_out, *) "Quan-Chem Theory:", qm_method
           write (102,*)  "Quan-Chem package: ", qm_method, it
        else if ( qm_method .eq. 3 ) then

           if (label_ml_pes .eq. 1) then
              write (file_md_out, *) "kkr regression", qm_method
              write (102,*)  "Quan-Chem package: ", qm_method, it
           else if (label_ml_pes .eq. 0) then
              write (file_md_out, *) "Quan-Chem Theory:", qm_method
              write (102,*)  "Quan-Chem package: ", qm_method, it
           endif

        endif    

        write (102,*)  "-----------------------------------"
        write (102,*)  "Current Geometry"
        write (102, *)  n_atom
        write (102, *)  "UNIT(au)"
        do i=1,n_atom
           write (102, 9999)  atom_label(i),  &
                      coor_x(i),      &
                      coor_y(i),      &
                      coor_z(i)
        enddo
        write (102,*)  "-----------------------------------"
        write (102,*)  "Number of atom:", n_atom
        write (102,*)  "Number of states involved in the dynamics:", n_state
        write (102,*)  "Current state:", index_state

        close(102)
  
        ! start electronic structure calculation.
        i_status = 0
        
        if ( qm_method .ne. 3 ) then 
           i_status=system ("quantum.py")
        else if ( qm_method .eq. 3 ) then
           if ( label_ml_pes .eq. 1) then
              i_status=system ("jade_kkr.py")

              if (i_status  .ne. 0) then
                  write (file_md_out, *) "kkr2qm"
                  i_status=system ("quantum.py")
              endif  

           else if ( label_ml_pes .eq. 0) then
              i_status=system ("quantum.py")
           endif

        endif

        if (i_status  .ne. 0) then
            write (*,*) "The interface errors!", i_status
            write (*,*) "Check QM calculations at t=0!"     
            stop   
        endif  


        ! direct read qm results dat & dump.
        
        open(unit=101, file="qm_results.dat")
        read (101,*)
        read (101,*)  
        do i=1,n_atom
           read (101, *)
        enddo
        read (101,*)


        do j=1,n_state
           read (101, *) pes_all(j)
        enddo

        read (101,*)
        do j=1,n_state
           read (101,*)
           do i=1,n_atom
              read (101, *)    &
                             gra_all_x(j,i),      &
                             gra_all_y(j,i),      &
                             gra_all_z(j,i)
           enddo
        enddo


        if (label_no_nac .eq. 0) then
           read (101,*)
           do j=1, n_state
              do k=1, n_state
                 read (101,*)
                 do i=1,n_atom
                    read (101, *)   &
                                nac_x(j,k,i),      &
                                nac_y(j,k,i),      &
                                nac_z(j,k,i)
                 enddo
             enddo
           enddo

        endif

        close(101)

        write (file_save_dipole, *) "----------------------------------"
        write (file_save_dipole, *) "----------------------------------"
        write (file_save_dipole, *)  "STEP",  it 
        write (file_save_dipole, *) "----------------------------------"
        open(unit=103, file="qm_other.dat")
        do while (.TRUE.)
           read (103, 8001, end=8998) string
           write (file_save_dipole, 8001) string
        enddo
8998    close(103)
        write (file_save_dipole, *) "----------------------------------"

8001    format(a100)


       return
 
       end 
