     subroutine sub_nac_phase (n_atom, &
                           n_state, &
                              old_nac_x, &
                              old_nac_y, &
                              old_nac_z, &
                              nac_x, &
                              nac_y, &
                              nac_z)
 

  implicit none

!
!     ----- Parameters -----
!
        include 'param.def'
!
!     ----- Argument -----


       integer, intent(in) :: n_atom, n_state

       double precision, intent(inout), dimension(n_state, n_state, n_atom) :: &
                                                nac_x, &
                                                nac_y, &
                                                nac_z

       double precision, intent(in), dimension(n_state, n_state, n_atom) ::   &
                                                old_nac_x, &
                                                old_nac_y, &
                                                old_nac_z

!
!  Local  

  integer :: i, j, k

  double precision :: old_nac_norm, new_nac_norm
  double precision :: nac_doc_product

  double precision :: cos_angle
   
      do i = 1, n_state
      do j=  1, n_state
          if (i .ne. j) then

!            Calculate the norm of old_nac            
             old_nac_norm =0.d0
             do k=1, n_atom
                old_nac_norm = old_nac_norm + &
                               old_nac_x (i, j, k)**2.d0 + &
                               old_nac_y (i, j, k)**2.d0 + &
                               old_nac_z (i, j, k)**2.d0 
             enddo 
             old_nac_norm = old_nac_norm ** 0.5d0

!         Calculate the norm of new_nac
             new_nac_norm =0.d0
             do k=1, n_atom
                new_nac_norm = new_nac_norm + &
                               nac_x (i, j, k)**2.d0 + &
                               nac_y (i, j, k)**2.d0 + &
                               nac_z (i, j, k)**2.d0
             enddo
             new_nac_norm = new_nac_norm ** 0.5d0
             
!     Calculate the dot product of two nac

             nac_doc_product =0.d0             
             do k=1, n_atom
                nac_doc_product = nac_doc_product + &
                              old_nac_x (i, j, k)* nac_x (i, j, k) + &
                              old_nac_y (i, j, k)* nac_y (i, j, k) + &
                              old_nac_z (i, j, k)* nac_z (i, j, k) 
             enddo

             if ( (old_nac_norm .eq. 0)   &
                  .or.                    &
                  (new_nac_norm .eq. 0)   &
                )   then
                 cos_angle = 1.0
             else
                 cos_angle = nac_doc_product / (old_nac_norm*new_nac_norm) 
             endif

             if (cos_angle .ge. 0) then
                 do k=1, n_atom
                    nac_x (i, j, k) =  nac_x (i, j, k)
                    nac_y (i, j, k) =  nac_y (i, j, k)
                    nac_z (i, j, k) =  nac_z (i, j, k)
                 enddo
             else
                 do k=1, n_atom
                    nac_x (i, j, k) = - nac_x (i, j, k)
                    nac_y (i, j, k) = - nac_y (i, j, k)
                    nac_z (i, j, k) = - nac_z (i, j, k)
                 enddo
             endif
             

          endif
      enddo
      enddo 


   end subroutine sub_nac_phase
