       subroutine      sub_many_pes_num_nac  (n_atom, &
                                n_state, md_state, &
                                atom_label, &
                                coor_x, coor_y, coor_z, &
                                qm_method, &
                                index_state, &
                                gradient_x, &
                                gradient_y, &
                                gradient_z, &
                                nac_time, &
                                pes_all, &
                                it, &
                                file_md_out, &
                                file_save_dipole )



      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, qm_method, n_state
      integer, intent(in) :: file_md_out, file_save_dipole, &
                             index_state,it
      integer, intent(in), dimension(n_state) :: md_state
      character*2, intent(in), dimension(n_atom)  ::  atom_label 
      double precision, intent(in), dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z


      double precision, intent(inout), dimension(n_state) :: pes_all
      double precision, intent(inout), dimension(n_atom) ::   &
                                                       gradient_x, &
                                                       gradient_y, &
                                                       gradient_z
 
      double precision, intent(inout), dimension(n_state, n_state) ::  &
                                                       nac_time




      integer  ::  i, j, k, i_status, system, i_other
      integer  ::  file_coor
      character*5 ::  tmp_i, tmp_j
      character*200 :: string
    
      double precision, allocatable, dimension(:,:) :: &
                                                  overlap_time


        
        allocate (overlap_time (n_state, n_state)) 


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



9999   format (a2,1x, 3(f20.10,1x))



       gradient_x = 0.d0
       gradient_y = 0.d0
       gradient_z = 0.d0
       nac_time     = 0.d0
       pes_all   = 0.d0

!     Write the interface for QC calculations

        open(unit=102, file="qm_interface")
        write (102,*)  "The interface between Fortran and Python"

        if ( ( qm_method .eq. 11 ) &
             .or.                  & 
             ( qm_method .eq. 12 ) &
           ) then 
           write (file_md_out, *) "Quan-Chem Theory:", qm_method
           write (102,*)  "Quan-Chem package: ", qm_method, it
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
        i_status=system ("quantum.py")
        if (i_status  .ne. 0) then
            write (*,*) "The interface errors!", i_status
            write (*,*) "Check QM calculations at t=0!"     
            stop   
        endif  

        ! direct read qm results dat & dump.
        
        open(unit=101, file="qm_results.dat")
        do i = 1, 7
           read (101,*)
        enddo
        
        read (101,*)
        read (101,*)
        do i=1,n_atom
           read (101, *)
        enddo

        do i = 1, 10
           read (101,*)
        enddo
      
        do i = 1, 5
           read (101,*)
        enddo


        do j=1,n_state
           read (101, *) tmp_i, pes_all(j)
        enddo

        read (101,*)
        read (101,*)
        do i=1, n_atom
             read (101, *)    &
                             gradient_x(i),      &
                             gradient_y(i),      &
                             gradient_z(i)
        enddo

        read (101,*)
        read (101,*)
    
        overlap_time = 0.d0
        do j=1, n_state
           do k=1, n_state
              read (101, *)   tmp_i, tmp_j, &
                             overlap_time(j,k)
          enddo
        enddo

        close(101)


        nac_time =0.d0 
        do i = 1, n_state
           do j = 1, i-1
              nac_time(i,j) = 0.5d0 * &
                           (   abs( overlap_time(i,j) ) &
                             + abs( overlap_time(j,i) ) &
                           ) 
              nac_time(j,i) =  - nac_time(i,j) 
           enddo
        enddo
       
        write (file_save_dipole, *) "----------------------------------"
        write (file_save_dipole, *) "----------------------------------"
        write (file_save_dipole, *)  "STEP",  it 
        write (file_save_dipole, *) "----------------------------------"
        open(unit=102, file="qm_other.dat")
        do while (.TRUE.)
           read (102, 8001, end=8998) string
           write (file_save_dipole, 8001) string
        enddo
8998    close(102)
        write (file_save_dipole, *) "----------------------------------"

8001    format(a100)

        deallocate (overlap_time)

       return
 
       end 
