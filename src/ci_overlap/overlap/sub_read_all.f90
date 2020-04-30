       subroutine sub_read_all (   n_ao, &
                                   n_state, &
                                   n_csf, &
                                   type_input, &
                                   file_input1, &
                                   filename_input1, &
                                   ci_1, &
                                   s1_ao_to_mo_alpha, &
                                   s1_ao_to_mo_beta, &
                                   file_input2, &
                                   filename_input2, &
                                   ci_2, &
                                   s2_ao_to_mo_alpha, &
                                   s2_ao_to_mo_beta, &
                                   file_input3, &
                                   filename_input3, &
                                   s_ao_overlap )


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine reads CI vectors and MOs (for Geom A and Geom B) 
!      and AO overlap of Geom A and Geom B.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!

       integer, intent (in) :: n_ao, n_state, n_csf, type_input
       integer, intent (in) :: file_input1, file_input2, file_input3
       
       character*20, intent (in) :: filename_input1, filename_input2, &
                                    filename_input3

       double precision, intent (inout), dimension(n_ao,n_ao) :: &
                                                 s1_ao_to_mo_alpha, &
                                                 s2_ao_to_mo_alpha, &
                                                 s1_ao_to_mo_beta, &
                                                 s2_ao_to_mo_beta, &
                                                 s_ao_overlap
      double precision, intent (inout), dimension(n_state, n_csf, 3) :: &
                                                 ci_1, ci_2

       !      ---- local variables ---
      integer :: i, j, k
      character*4 :: tmp_i_state 
      integer :: i_state, occ_tmp, vir_tmp, i_tmp, j_tmp  
      double precision :: ci_vec_tmp, contri_tmp
         


          ci_1(:,:,:) =0
          ci_2(:,:,:) =0
          s_ao_overlap (:,:) = 9


!   Read the CI vectors. The final CI vector is 
!   saved at a table
!   ci_1(i,j,k)  
!        i :  Which state
!        j :  which CSF
!        k = 1 : ci vector
!        k = 2 : occupied orbitals involved in the transition
!        k = 3 : virtual orbitals involved in the transition 

!   Construct the first CI vector

!   Set up the groud state CI vector      

          ci_1(1,1,1) = 1
          ci_1(1,1,2) = 0
          ci_1(1,1,3) = 0
  
!    Read the CI vector for excited state
          open (unit=file_input1, file="ci_1.dat")
          read (file_input1, *)
          do  i= 2, n_state
              do j= 1, n_csf          
                 read (file_input1,*) tmp_i_state, ci_vec_tmp, &
                                    occ_tmp, vir_tmp, contri_tmp
                 ci_1(i,j,1) = ci_vec_tmp
                 ci_1(i,j,2) = occ_tmp
                 ci_1(i,j,3) = vir_tmp
              enddo
          enddo
          close(file_input1)


!   Construct the second CI vector

!   Set up the groud state CI vector      
          ci_2(1,1,1) = 1
          ci_2(1,1,2) = 0
          ci_2(1,1,3) = 0


!    Read the CI vector for excited state
          open (unit=file_input2, file="ci_2.dat")
          read (file_input2, *)
          do  i= 2, n_state
              do j= 1, n_csf
                 read (file_input2,*) tmp_i_state, ci_vec_tmp, &
                                    occ_tmp, vir_tmp, contri_tmp
                 ci_2(i,j,1) = ci_vec_tmp
                 ci_2(i,j,2) = occ_tmp
                 ci_2(i,j,3) = vir_tmp
              enddo
          enddo
          close(file_input2)



!    Read the MO coefficient!

!    MO at R
!    
     
          open (unit=file_input1, file="mo_1.dat")
          read (file_input1, *)
          do  i= 1, n_ao
              read (file_input1, *)
              do j= 1, n_ao
                 read (file_input1,*) i_tmp, j_tmp, &
                                      s1_ao_to_mo_alpha(i,j)
                 s1_ao_to_mo_beta(i,j) =  s1_ao_to_mo_alpha(i,j)
              enddo
          enddo
          close(file_input1)

!    MO at R+dR
!    

          open (unit=file_input2, file="mo_2.dat")
          read (file_input2, *)
          do  i= 1, n_ao
              read (file_input2, *)
              do j= 1, n_ao
                 read (file_input2,*) i_tmp, j_tmp, &
                                      s2_ao_to_mo_alpha(i,j)
                 s2_ao_to_mo_beta(i,j) = s2_ao_to_mo_alpha(i,j)
              enddo
          enddo
          close(file_input2)






!    Read the orbital overlap between R and R+dR

          open (unit=file_input3, file="ao_overlap.dat")
          read (file_input3, *)
          do i = 1, n_ao
             do j = 1, n_ao
                read (file_input3, *)  i_tmp, j_tmp, s_ao_overlap(i,j)
             enddo
          enddo
          close(file_input3)      
 

        return 

        end     subroutine sub_read_all                 
