      subroutine sub_wf_overlap   ( n_atom,  &
                             n_ao, &
                             n_ele, &
                             n_ele_alpha, &
                             n_ele_beta,  &
                             n_state,  &
                             n_csf, &
                             s_mo_overlap, &
                             ci_1, ci_2,  &
                             s_wf_overlap, &
                             s_ci_overlap, &
                             output_level  )



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine constructs the wavefunctions overlap!
!      Calculate s_wf_overlap (n_state, n_state)


!     For state i at Geom 1 and state j at Geom 2, 
!     pick up their corresponding CI vector as
!     ci_a and ci_b.
!     Then only compute the overlap between 
!     state i at Geom 1 and state j at Geom 2.     

!     state_overlap:   s_wf_overlap (i,j)
!                      Overlap between state i at Geom 1 and state j at Geom 2. 

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

       integer, intent (in) :: n_atom, n_ao, n_ele, &
                               n_ele_alpha, n_ele_beta, &
                               n_state, n_csf, output_level
       double precision, intent (in), dimension(2*n_ao,2*n_ao) :: &
                                                          s_mo_overlap
       double precision, intent (in), dimension(n_state, n_csf, 3) :: &
                                                         ci_1, ci_2
       double precision, intent (inout), dimension(n_state,n_state) :: &
                                                         s_wf_overlap, &
                                                         s_ci_overlap


!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: ci_a, &
                                                        ci_b 
       double precision ::  s_state_overlap, s_ci_state_overlap
                                                        
       integer :: i, j, k, l
      
       allocate ( ci_a (n_csf,3))
       allocate ( ci_b (n_csf,3))


 

!      do i=1, n_state
!         write (*,*) "State", i
!         do j = 1, n_csf
!            write (*,*) ci_1(i,j,:)
!            write (*,*) ci_2(i,j,:)
!         enddo
!      enddo

      write (*,*) "Calculate the overlap of different electronic states"

      s_wf_overlap(:,:) = 0.d0

      do i = 1, n_state
         do j= 1, n_state

            write (*,*)  "Overlap between state:", i, j

            if ( i .ne. j) then

!        Pick up the CI vector for state i at Geom 1 and state j at Geom 2
                 do k = 1, n_csf
                   do l= 1, 3
                     ci_a (k,l) = ci_1(i,k,l)
                     ci_b (k,l) = ci_2(j,k,l)
                   enddo
                 enddo

                 if (output_level .eq. 2 )  then
                      write (*,*) "Geom1: State", i
                      do k = 1, n_csf
                          write (*,*) "CI component"
                          write (*,9998) ci_a (k,1), ci_a (k,2), ci_a (k,3)
                      enddo

9998                  format (1x, f10.5, ":  ", f20.5, "-->", f20.5)

                      write (*,*) "Geom2: State", j 
                      do k = 1, n_csf
                         write (*,*) "CI components"
                         write (*,9998) ci_b (k,1), ci_b (k,2), ci_b (k,3)
                         enddo
                      endif


!       Compute the overlap between 
!       state i at Geom 1 and state j at Geom 2.                    
                      call sub_state_overlap ( n_atom,  &
                                               n_ao, &
                                               n_ele, &
                                          n_ele_alpha, &
                                          n_ele_beta,  &
                                          n_csf, &
                                          s_mo_overlap, &
                                          ci_a, ci_b, &
                                          s_state_overlap, &
                                          s_ci_state_overlap, &
                                          output_level )
                  
                      s_wf_overlap(i,j) = s_state_overlap
                      s_ci_overlap(i,j) = s_ci_state_overlap
            endif
         enddo
      enddo       

      write (*,*) "Obtain the overlap of different electronic states"


      open (unit=71, file="wavefuction_overlap.dat")
      write (71, *)  "Overlap between S_i and S_j, <psi_i | Psi_j>"
      do i = 1, n_state
         do j= 1, n_state
            write (71,*) i, j, s_wf_overlap(i,j)
         enddo
      enddo
      close (71)

       open (unit=72, file="ci_overlap.dat")
       write (72, *)  "CI Overlap between S_i and S_j"
       do i = 1, n_state
          do j= 1, n_state
             write (72,*) i, j, s_ci_overlap(i,j)
          enddo
       enddo
       close (72)


      deallocate ( ci_a )
      deallocate ( ci_b )



      return
      end subroutine  sub_wf_overlap
     


