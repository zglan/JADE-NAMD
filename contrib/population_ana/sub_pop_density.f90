      subroutine    sub_pop_density        ( n_atom, &
                                          n_ao,  &
                                          tra_density1,  &
                                          s_ao_to_mo,  &
                                          tra_density2, &
                                          s_ao_overlap, &
                                          basis &
                                        )


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
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

       integer, intent (in) :: n_atom, n_ao
      
       double precision, intent (in), dimension (n_ao,n_ao) :: &
                                              tra_density1, &
                                              s_ao_to_mo, &
                                              s_ao_overlap
       integer, intent (in), dimension(n_atom)::  basis

       double precision, intent (inout), dimension(n_ao,n_ao) :: &
                                               tra_density2

!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: pop1, pop2 
       double precision, allocatable, dimension(:,:) :: tmp_matrix1, &
                                                        tmp_matrix2   

       double precision, allocatable, dimension(:,:) ::  overlap_half, &
                                                      trans_overlap_half
       double precision, allocatable, dimension(:) :: den1, den2, &
                                        den_sum, den_diff, den_diff_abs
       double precision :: total, total1
                                                  
       integer :: i, j, k, l, i_atom, j_atom, k_basis, l_basis
     
!      local variables
       integer, allocatable, dimension(:) :: IPIV, WORK
       integer :: INFO, LWORK
       



 
       allocate ( pop1 (n_ao, n_atom))
       allocate ( pop2 (n_ao, n_atom))
       allocate ( den1 (n_atom))
       allocate ( den2 (n_atom))
       allocate ( den_sum (n_atom))
       allocate ( den_diff (n_atom))
       allocate ( den_diff_abs (n_atom))


       allocate ( tmp_matrix1 (n_ao,n_ao))
       allocate ( tmp_matrix2 (n_ao,n_ao))
       allocate ( overlap_half(n_ao, n_ao))
       allocate ( trans_overlap_half(n_ao, n_ao))
 

       LWORK = n_ao
       allocate (IPIV(n_ao))
       allocate (WORK(LWORK))
 
      tra_density2(:,:) = 0.d0

      write (*,*) "Transition density in MO basis"

      do i=1, n_ao
      do j=1, n_ao      
      write (*,*)  i,j,tra_density1(i,j) 
      enddo
      enddo


 
      
      do i = 1, n_ao
         k_basis = 0
         l_basis = 0
         do i_atom = 1, n_atom

            pop1 (i,i_atom) = 0.d0

            do k = 1, basis(i_atom)
               do l_basis = 1, n_ao
!                  write (*,*) i_atom, k_basis+k, l_basis
                  pop1 (i,i_atom) = pop1 (i,i_atom) +  &
                        s_ao_to_mo (i, k_basis+k) *   &
                        s_ao_overlap ( k_basis+k, l_basis) * &
                        s_ao_to_mo (i,l_basis)   
               enddo
            enddo
            k_basis = k_basis + basis(i_atom)
         enddo  
      enddo
          
      write (*,*) "pop"
      do i = 1, n_ao
      total = 0.d0
        do k = 1, n_atom
           write (*,*) i, k, pop1(i,k)
           total = total + pop1(i,k)
        enddo
        write (*,*) "Orb ", i, total
      enddo     

      den1 = 0.d0
      den2 = 0.d0
      den_sum = 0.d0
      den_diff = 0.d0
      den_diff_abs = 0.d0
      do i_atom =1, n_atom
         do i = 1, n_ao
         do j = 1, n_ao
             if (tra_density1(i,j) .ne. 0)  then
                den1(i_atom) = den1(i_atom) +  &
                                      (tra_density1(i,j))**2  &
                                    * pop1 (i,i_atom) 
                write (*,*) "TRA, i_atom, i, j "
                write (*,*) i_atom, i,j
                write (*,*) tra_density1(i,j), &
                            ( tra_density1(i,j) )**2 
                write (*,*) pop1 (i,i_atom), pop1 (j,i_atom)
                write (*,*) "Product",  &
                       (tra_density1(i,j))**2  & 
                                    * pop1 (i,i_atom), &
                       (tra_density1(i,j))**2  & 
                                    * pop1 (j,i_atom) 

                den2(i_atom) = den2(i_atom) +  &
                                      (tra_density1(i,j))**2  &
                                   * pop1 (j,i_atom)
  
                den_sum (i_atom)  = den1(i_atom) + den2(i_atom)
                den_diff(i_atom)  = den2(i_atom) - den1(i_atom)
   
                den_diff_abs (i_atom) = den_diff_abs (i_atom) +  &
                                       (tra_density1(i,j))**2  &
                                     * abs(  pop1 (j,i_atom)  &
                                           - pop1 (i,i_atom)  &
                                          )  
             endif
         enddo
         enddo
      enddo


9998  format (1(i4), 10(2x, f15.8))


      write (*,*)  "Barbatti's way"
      do i_atom = 1, n_atom
         write (53, 9998) i_atom, den1(i_atom), &
                               den2(i_atom), &
                               den_sum(i_atom), &
                               den_diff(i_atom), &
                               den_diff_abs (i_atom)
      enddo
 

!     Lowdin transformation

   

      return
      end subroutine  sub_pop_density
     


