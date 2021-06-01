      subroutine   sub_state_overlap ( n_atom,  &
                                     n_ao, &
                                     n_ele, &
                                     n_ele_alpha, &
                                     n_ele_beta,  &
                                     n_csf, &
                                     s_mo_overlap, &
                                     ci_a, ci_b, &
                                     state_overlap, &
                                     ci_overlap, &
                                     output_level )



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine constructs the wavefunctions overlap
!      for any two given states. 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
!     s_csf_overlap: Overlap matrix of two CSFs.
!     csf_overlap:  s_csf_overlap(i,j) 

       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!

       integer, intent (in) :: n_atom, n_ao, &
                               n_ele, n_ele_alpha, n_ele_beta,  &
                               n_csf, output_level
       double precision, intent (in), dimension(n_ao*2,n_ao*2) :: &
                                                          s_mo_overlap
       double precision, intent (in), dimension(n_csf, 3) :: &
                                                         ci_a, ci_b
       double precision, intent (inout) :: state_overlap,  &
                                           ci_overlap


!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: s_csf_overlap
       double precision, allocatable, dimension(:) :: ci_a_orb,  &
                                                      ci_b_orb
       double precision :: ci_product, csf_overlap, s_state_overlap, &
                                                    s_ci_overlap       
       integer :: i, j, k

       double precision :: normal_factor, overlap_factor

      
       allocate (s_csf_overlap (n_csf, n_csf))
       allocate (ci_a_orb(3))
       allocate (ci_b_orb(3)) 
        
!     -- Calculate the overlap of relavant configurations
 
!     When  ci_product= ci_a(i, 1) *  ci_b(j, 1) is very small, 
!     the final product should be close to zero.
!     In such case, we do not need to compute the s_csf_overlap. 



      


       
       s_state_overlap=0.d0

       do i= 1, n_csf 
          do j=1, n_csf

!           Pick up the orbital transition information for particilar CSF.
             do k=1, 3
                   ci_a_orb(k) =  ci_a(i, k)
                   ci_b_orb(k) =  ci_b(j, k)
             enddo
       
 
!     -- The CI products between two configurations without excitations

             if ( ( ci_a_orb(2)  .eq.  0 ) &
                  .AND.                    &
                  ( ci_b_orb(2)  .eq.  0 ) &
                ) then
                  
                  ci_product = abs(ci_a_orb(1) * ci_b_orb(1))
                  normal_factor = 1
             endif


!      -- The CI products between two configurations---
!      CSF 1 contains no excitation
!      CSF 2 contains the single excitation
!      For CSF2, We only consider the transition of beta electron 
!      from  ci_b_orb(2) --> ci_b_orb(3) here.

             if ( ( ci_a_orb(2)  .eq.  0 ) &
                   .AND.                   &
                  ( ci_b_orb(2)  .ne.  0 ) &
                ) then
                  
                  ci_product = abs(               &
                                    ci_a_orb(1) * &
                                    ci_b_orb(1)   &
                                  )
                  normal_factor = 2 / 2**0.5

             endif


!      -- The CI products between two configurations---
!      CSF 1 contains the single excitation
!      For CSF2, We only consider the transition of beta electron 
!      from  ci_b_orb(2) --> ci_b_orb(3) here.
!      CSF 2 contains no excitation
             if ( ( ci_a_orb(2)  .ne.  0 ) &
                   .AND.                   &
                  ( ci_b_orb(2)  .eq.  0 ) &
                ) then
                  
                  ci_product = abs(               &
                                    ci_a_orb(1) * &
                                    ci_b_orb(1)   &
                                  )
                  normal_factor = 2 / 2**0.5

             endif



!      -- The CI products between two configurations---
!      CSF 1 contains the single excitation
!      CSF 2 contains the single excitation
!      Please note that we totally have four terms.
!      These can be devided into two group.
!      Each group has two terms.
!      Two terms in the same  group are same.
!      Two terms from different group may be similar.
!      Therefore we have factor of four here.
             if ( ( ci_a_orb(2)  .ne.  0 ) &
                   .AND.                   &
                  ( ci_b_orb(2)  .ne.  0 ) &
                ) then

                  ci_product = abs(  &
                                    ci_a_orb(1)  * &
                                    ci_b_orb(1)    &
                                  )
                  normal_factor = 2 * (1/2**0.5) * (1/2**0.5)
            endif


!             if ( output_level .eq. 2 ) then
!                write (*,*) "CI products"                
!                write (*,*) ci_product
!             endif


             if ( ci_product .le. 0.01 ) then
                s_csf_overlap (i,j) = 0.d0
             endif

             if ( ci_product .gt. 0.01 )  then

!           Compute the overlap between two CSFs.

                if ( output_level .eq. 2 ) then
                    write (*,*) "Compute CI product between CSF", i,j
                    write (*,*) ci_product
                endif

                call   sub_csf_overlap ( n_atom,  &
                                         n_ao, &
                                         n_ele, &
                                         n_ele_alpha, &
                                         n_ele_beta,  &
                                         s_mo_overlap, &
                                         ci_a_orb, ci_b_orb, &
                                         csf_overlap, &
                                         output_level )
                                         
                s_csf_overlap(i,j) = csf_overlap

             endif

             if ( output_level .eq. 2 ) then
                if (s_csf_overlap(i,j)  .ne. 0 ) then
                   write (*,*) "CSF index at R and R+dR:" ,i, j  
                   write (*,*) "SCF overlap calculations"
                   write (*,*) "CI vector for a:", ci_a(i, 1), &
                                                   ci_a_orb(1) 
                   write (*,*) "CI vector for b:", ci_b(j, 1), &
                                                   ci_b_orb(1)
                   write (*,*) "Normalization factor:", &
                                                   normal_factor
                   write (*,*) "CSF overlap:", s_csf_overlap(i,j)
                   write (*,*) "C_1* CSF_OVERLAP * C_2:",  &
                               ci_a_orb(1)* s_csf_overlap(i,j)* &
                               ci_b_orb(1) * normal_factor
                endif
             endif


!      Please note here that CI vector has been modified according to 
!      their normalization factor.

             s_state_overlap  = s_state_overlap +    &
                         ci_a_orb(1)* s_csf_overlap(i,j)* ci_b_orb(1) &
                           *  normal_factor
             
          enddo
       enddo          

       write (*,*) "s_state_overlap", s_state_overlap 
       state_overlap = s_state_overlap




!     Compute the CI overlap directly. This is rather easily.
!      Pick up the correspondence CI coefficient and make product.


      s_ci_overlap = 0.d0

      do i= 1, n_csf
          do j=1, n_csf
               overlap_factor = 0.0
               if ( ( ci_a(i, 2) .eq. ci_b(j, 2) )  &
                    .AND.                                   &
                    ( ci_a(i, 3) .eq. ci_b(j, 3) )  &
                  ) then
                  overlap_factor = 1.0   
               endif     
               s_ci_overlap = s_ci_overlap +  &
                              ci_a(i, 1) * ci_b(j, 1) &
                              * overlap_factor * normal_factor
!               write (200, *)  i, j              
!               write (200, *)  ci_a(i, 1), ci_b(j, 1), overlap_factor
!               write (200, *)  s_ci_overlap
                            
           enddo
      enddo
      ci_overlap = s_ci_overlap      
 
            
      deallocate (s_csf_overlap )
      deallocate (ci_a_orb)
      deallocate (ci_b_orb)


      return
      end subroutine  sub_state_overlap

     


