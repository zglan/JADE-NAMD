       subroutine    sub_many_ana_pes (n_atom, &
                                n_state, md_state, &
                                atom_label, &
                                coor_x, coor_y, coor_z, &
                                qm_method, &
                                gra_all_x, &
                                gra_all_y, &
                                gra_all_z, &
                                nac_x, &
                                nac_y, &
                                nac_z, &
                                pes_all, &
                                file_md_out, &
                                file_save_dipole )
 

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, qm_method, n_state
      integer, intent(in) :: file_md_out, file_save_dipole
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




      integer  ::  i, j, k
      integer  ::  file_coor

    


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



       gra_all_x = 0.d0
       gra_all_y = 0.d0
       gra_all_z = 0.d0
       nac_x     = 0.d0
       nac_y     = 0.d0
       nac_z     = 0.d0
       pes_all   = 0.d0




        if ( qm_method .eq. 1 ) then 
           write (file_md_out, *) "MNDO calculations"
           call sub_mndo_many   (n_atom, &
                          n_state, &
                          md_state, &
                          atom_label, &
                          coor_x, coor_y, coor_z, &
                          file_md_out)

        endif



        
        open(unit=101, file="qm_results.dat")
        read (101,*)
        read (101,*)  
        do i=1,n_atom
           read (101, *)
!           read (101, *)  atom_label(i),  &
!                          coor_x(i),      &
!                          coor_y(i),      &
!                          coor_z(i)
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

        close(101)





       return
 
       end 
