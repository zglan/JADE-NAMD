      subroutine  sub_csf_overlap ( n_atom,  &
                                         n_ao, &
                                         n_ele, &
                                         n_ele_alpha, &
                                         n_ele_beta,  &
                                         s_mo_overlap, &
                                         ci_a_orb, ci_b_orb, &
                                         csf_overlap, &
                                         output_level)


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine constructs the wavefunctions overlap!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      Total_matrix:   the overlap matrix in occupied MO basis.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 


       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!

       integer, intent (in) :: n_atom, n_ao, n_ele, n_ele_alpha, &
                               n_ele_beta, output_level
       double precision, intent (in), dimension(n_ao*2,n_ao*2) :: &
                                                          s_mo_overlap
       double precision, intent (in), dimension(3) :: &
                                                     ci_a_orb, ci_b_orb
       double precision, intent (inout) :: csf_overlap


!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: temp_matrix
       double precision, allocatable, dimension(:,:) :: total_matrix
       double precision :: s_det
                                            
       integer :: i, j, k, l
       integer :: i_occ_a, i_vir_a, i_occ_b, i_vir_b

       allocate (temp_matrix (n_ele_alpha, n_ele_alpha))
       allocate (total_matrix (n_ele, n_ele))


!      Define the occupied and unoccpied orbitals in the transition for 
!      R and R+dR      
 
       i_occ_a = int(ci_a_orb(2))
       i_vir_a = int(ci_a_orb(3)) 
       i_occ_b = int(ci_b_orb(2))
       i_vir_b = int(ci_b_orb(3))

       
!       write (*,*) "For R, Contribution for transition"
!       write (*,*) i_occ_a, i_vir_a
!       write (*,*) "For R+dR, Contribution for transition"
!       write (*,*) i_occ_b, i_vir_b
      

!     -- Calculate the overlap of relavant configurations


       temp_matrix (:,:) = 0.d0

       total_matrix (:,:) = 0.d0
!     -- The overlap between two configurations without excitations

       csf_overlap =0.d0
       s_det =0.d0

       if ( ( i_occ_a  .eq.  0 ) &
            .AND.                   &
            ( i_occ_b  .eq.  0 ) &
          ) then

               write (*,*) "Overlap between two closed configurations"         
!        Alpha part
               total_matrix (:,:) = 0.d0
               temp_matrix (:,:) = 0.d0
               do i=1, n_ele_alpha
                    do j=1, n_ele_alpha
                        temp_matrix (i,j) = s_mo_overlap(i,j) 
                        total_matrix (i,j) = temp_matrix (i,j)
                     enddo
               enddo
!        Beta part
               temp_matrix (:,:) = 0.d0
               do i=1, n_ele_beta
                     do j= 1, n_ele_beta
                        temp_matrix (i,j) = s_mo_overlap(i,j)
                        total_matrix (i+n_ele_alpha, j+n_ele_alpha) = &
                                                       temp_matrix (i,j)
                     enddo
               enddo         
           

               call sub_determinant (total_matrix, n_ele, &
                                     s_det, output_level)
               csf_overlap = s_det
       endif


!      CSF 1 contains no excitation

!      CSF 2 contains the single excitation
!      For CSF2, We only consider the transition of beta electron 
!      from  ci_b_orb(2) --> ci_b_orb(3) here.

       if ( ( i_occ_a  .eq.  0 ) &
            .AND.                   &
            ( i_occ_b  .ne.  0 ) &
          ) then
               
!               write (*,*) "Overlap <close | single >"
!      Alpha part 
               total_matrix (:,:) = 0.d0
               temp_matrix (:,:) = 0.d0
               do i=1, n_ele_alpha
                    do j=1, n_ele_alpha
                       temp_matrix (i,j) = s_mo_overlap(i,j)
                       total_matrix (i,j) = temp_matrix (i,j)
                    enddo
               enddo
!      Beta part
               temp_matrix (:,:) = 0.d0
               do i=1, n_ele_beta
                    do j=1, n_ele_beta
                       if (j .ne. i_occ_b) then
                         temp_matrix (i,j) = s_mo_overlap(i,j)
                       else
                         temp_matrix (i,j) = s_mo_overlap(i,i_vir_b)
                       endif
                       total_matrix (i+n_ele_alpha, j+n_ele_alpha) = &
                                                       temp_matrix (i,j)
                     enddo
                enddo
 

!                write (*,*) "Compute the determinant"
                call sub_determinant (total_matrix, n_ele, &
                                      s_det, output_level)
                csf_overlap = s_det



       endif


!      CSF 1 contains the single excitation
!      For CSF 1, We only consider the transition of beta electron 
!      from  ci_b_orb(2) --> ci_b_orb(3) here.

!      CSF 2 contains no excitation

       if ( ( i_occ_a  .ne.  0 ) &
            .AND.                   &
            ( i_occ_b  .eq.  0 ) &
          ) then
 
!                 write (*,*) "Overlap <close | single >"

!      Alpha part
                 total_matrix (:,:) = 0.d0
                 temp_matrix (:,:) = 0.d0
                 do i=1, n_ele_alpha
                      do j=1, n_ele_alpha
                            temp_matrix (i,j) = s_mo_overlap(i,j)
                            total_matrix (i,j) = temp_matrix (i,j)
                      enddo
                 enddo

!      Beta part
                 temp_matrix (:,:) = 0.d0
                 do i=1, n_ele_beta
                    do j=1, n_ele_beta
                       if (i .ne. i_occ_a) then
                          temp_matrix (i,j) = s_mo_overlap(i,j)
                       else
                          temp_matrix (i,j) = s_mo_overlap(i_vir_a, j)
                       endif
                       total_matrix (i+n_ele_alpha, j+n_ele_alpha) = &
                                                       temp_matrix (i,j)
                    enddo
                 enddo
 

                 call sub_determinant (total_matrix, n_ele, &
                                       s_det, output_level)
                 csf_overlap = s_det
              

       endif



!      Both CSF 1 and CSF 2 contains single excitation. 
!      Now we have two different cases:
!      For CSF 1, we only consider the transition of beta electron 
!      from  ci_b_orb(2) --> ci_b_orb(3) here.

!      For CSF 2, we need to consider the transition of 
!      beta electron  from  ci_b_orb(2) --> ci_b_orb(3)
!      or
!      alpha electron  from  ci_b_orb(2) --> ci_b_orb(3) 
!      we need to sum over these two cases.


           
        if ( ( i_occ_a  .ne.  0 ) &
            .AND.                    &
             ( i_occ_b  .ne.  0 ) &
           ) then

!                  write (*,*) "Overlap <single | single >"
!      Alpha part of the first component
!      For CSF 1 alpha electron remain on occupied orbitals
!      For CSF 2 alpha electron remain on occupied orbitals

                  total_matrix (:,:) = 0.d0
                  temp_matrix (:,:) = 0.d0
                  do i=1, n_ele_alpha
                       do j=1, n_ele_alpha
                            temp_matrix (i,j) = s_mo_overlap(i,j)
                            total_matrix (i,j) = temp_matrix (i,j)
                       enddo
                  enddo

!      Beta part of the first component
!      For CSF 1 beta electron from ci_a_orb(2) --> ci_a_orb(3)
!      For CSF 2 beta electron from ci_b_orb(2) --> ci_b_orb(3)
                  temp_matrix (:,:) = 0.d0
                  do i=1, n_ele_beta
                       do j=1, n_ele_beta

                          if ( ( i .ne. i_occ_a )  &
                                .AND.               &
                               ( j .ne. i_occ_b )   &
                              ) then
                                 temp_matrix (i,j) = s_mo_overlap(i,j)
                          endif

                          if ( (i .eq. i_occ_a )   &
                               .AND.               &
                               (j .ne. i_occ_b )   &
                             ) then
                                 temp_matrix (i,j) = &
                                          s_mo_overlap(i_vir_a , j)
                          endif

                          if ( (i .ne. i_occ_a)   &
                               .AND.               &
                               (j .eq. i_occ_b)    &
                             ) then
                                 temp_matrix (i,j) = &
                                          s_mo_overlap(i, i_vir_b )
                          endif
 
                          if ( (i .eq. i_occ_a)  &
                               .AND.               &
                               (j .eq. i_occ_b)   &
                             ) then
                                  temp_matrix (i,j) = &
                                s_mo_overlap(i_vir_a, i_vir_b )
                          endif
                 


                          total_matrix (i+n_ele_alpha, j+n_ele_alpha)= &
                                                       temp_matrix (i,j)

 
                       enddo
                  enddo

                  if ( output_level .eq. 2 ) then 
                       do i=1, n_ele
                              write (*,*)  "MO_overlap", &
                                      i, &
                                      total_matrix (i,i)
                       enddo
                  endif

                  call sub_determinant (total_matrix, n_ele, &
                                        s_det, output_level)
                  csf_overlap = s_det



                   
!      Alpha part of the second component
!      For CSF 1 alpha electron remain on occupied orbitals
!      For CSF 2 alpha electron from ci_b_orb(2) --> ci_b_orb(3)

                 total_matrix(:,:) =0.d0
                 temp_matrix (:,:) = 0.d0
                 do i=1, n_ele_alpha
                       do j=1, n_ele_alpha
                            if (j .ne. i_occ_b ) then
                               temp_matrix (i,j) = s_mo_overlap(i,j)
                            else
                               temp_matrix (i,j) = &
                                             s_mo_overlap(i, i_vir_b)
                            endif
                            total_matrix (i, j) = temp_matrix (i,j)
                       enddo
                 enddo


!      Beta part of the second component
!      For CSF 1 beta electron from ci_a_orb(2) --> ci_a_orb(3)
!      For CSF 2 beta electron remain on occupied orbitals
                  temp_matrix (:,:) = 0.d0
                  do i=1, n_ele_beta
                      do j=1, n_ele_beta
                           if (i .ne. i_occ_a) then
                               temp_matrix (i,j) = s_mo_overlap(i,j)
                           else
                               temp_matrix (i,j) = &
                                           s_mo_overlap(i_vir_a, j)
                           endif
                          total_matrix (i+n_ele_alpha, j+n_ele_alpha) &
                                                   = temp_matrix (i,j)
                     enddo
                 enddo

                 call sub_determinant ( total_matrix, &
                                        n_ele,        &
                                        s_det,        &
                                        output_level &
                                      )
                 csf_overlap = csf_overlap + s_det


       endif
          

       if (output_level  .eq.  2) then
!           write (*,*) "CSF ovelap matrix"
!           do i=1,n_ele
!              do j=1, n_ele
!                 write (*,*) total_matrix(i,j)
!              enddo
!           enddo
           write (*,*) "Deterimant of CSF ovelap matrix:", s_det
       endif
       



      return
      end subroutine  sub_csf_overlap

     


