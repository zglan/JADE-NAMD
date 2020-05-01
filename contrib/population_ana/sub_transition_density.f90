      subroutine  sub_transition_density ( n_atom, &
                                           n_ao, &
                                          tra_density1,  &
                                          s_ao_to_mo, &
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
       double precision, intent (in), dimension(n_ao,n_ao) :: &
                                              tra_density1, &
                                              s_ao_to_mo, &
                                              s_ao_overlap
       integer, intent (in), dimension(n_atom)::  basis

       double precision, intent (inout), dimension(n_ao,n_ao) :: &
                                               tra_density2

!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: tra_lis 
       double precision, allocatable, dimension(:,:) :: tmp_matrix1, &
                                                        tmp_matrix2   

       double precision, allocatable, dimension(:,:) ::  overlap_half, &
                                                      trans_overlap_half
       double precision :: total, total1
                                                  
       integer :: i, j, k, l, i_atom, j_atom, k_basis, l_basis
     
!      local variables
       integer, allocatable, dimension(:) :: IPIV, WORK
       integer :: INFO, LWORK
       



 
       allocate ( tra_lis (n_atom, n_atom))
       allocate ( tmp_matrix1 (n_ao,n_ao))
       allocate ( tmp_matrix2 (n_ao,n_ao))
       allocate ( overlap_half(n_ao, n_ao))
       allocate ( trans_overlap_half(n_ao, n_ao))
 

       LWORK = n_ao
       allocate (IPIV(n_ao))
       allocate (WORK(LWORK))
 
      tra_density2(:,:) = 0.d0
      tra_lis(:,:) = 0.d0

      write (*,*) "Transition density in MO basis"

      do i=1, n_ao
      do j=1, n_ao      
      write (*,*)  i,j,tra_density1(i,j) 
      enddo
      enddo


      write (*,*) "Calculate the transition density in AO basis"

      tmp_matrix1   = MATMUL (TRANSPOSE(s_ao_to_mo),tra_density1)
      tra_density2 = MATMUL ( tmp_matrix1, s_ao_to_mo)


      write (*,*) "Transition density in AO basis"
  
      do i=1, n_ao
      do j=1, n_ao
      write (*,*)  i,j, tra_density2(i,j)
      enddo
      enddo


!     Lischka's way


      write (*,*) "Calculate the transition at each atoms"

      tmp_matrix1 =  MATMUL (tra_density2, s_ao_overlap)
      tmp_matrix2 =  MATMUL (s_ao_overlap, tra_density2)   
 
      do i=1, n_ao
      do j=1, n_ao
      write (*,9998)  i, j, tmp_matrix1(i,j),  tmp_matrix2(i,j)
      enddo
      enddo

9998  format (2(i4), 10(2x, f10.8))

!      write (*,*) "Number of atom", n_atom
      tra_lis= 0.d0
      k_basis = 0
      l_basis = 0 
      do i_atom = 1, n_atom
         l_basis = 0
         do j_atom =1, n_atom 
            tra_lis (i_atom,j_atom) = 0.d0
!            write (*,*)  "Basis", basis(i_atom), basis(j_atom)
            do k = 1, basis(i_atom)
               do l = 1, basis(j_atom)
                  write (*,9999) "ATOM", i_atom, j_atom,    &
                                "   Basis", k_basis+k, l_basis+l, &
                                    tra_density2(k_basis+k,l_basis+l), &
                                    tmp_matrix1 (k_basis+k,l_basis+l), &
                                     tmp_matrix2 (k_basis+k,l_basis+l)
9999   format(a, 2(i4), a, 2(i5), 3x, 20(f10.8) )
                  tra_lis(i_atom,j_atom) = tra_lis(i_atom,j_atom)+ &
                            tmp_matrix1 (k_basis+k,l_basis+l) *        &
                            tmp_matrix2 (k_basis+k,l_basis+l)
               enddo
             enddo
             write (51, *) i_atom, j_atom, &
                           tra_lis(i_atom, j_atom)
          
             l_basis = l_basis + basis(j_atom)
         enddo
         k_basis = k_basis + basis(i_atom)
      enddo


      write (*,*)  "Lischka's way"
      total = 0.d0
      do i_atom = 1, n_atom
         total1 =0.d0
         do j_atom = 1 , n_atom
            total1 = total1 + tra_lis(i_atom, j_atom)
         enddo
         write (*,*) "Total Transion density for Atom:", i_atom, total1
         total = total + total1
      enddo
      write (*,*) "Total Transion density:", total
 

!     Lowdin transformation

      call sub_overlap_half_positive(n_ao, &
                               s_ao_overlap, &
                               overlap_half, &
                               trans_overlap_half )

      tmp_matrix1 =  MATMUL (tra_density2, overlap_half)
      tmp_matrix2 =  MATMUL (overlap_half, tmp_matrix1)
      tmp_matrix1 =  tmp_matrix2
  
      tra_lis= 0.d0
      k_basis = 0
      l_basis = 0
      do i_atom = 1, n_atom
         l_basis = 0 
         do j_atom =1, n_atom
            tra_lis (i_atom,j_atom) = 0.d0
            do k = 1, basis(i_atom)
               do l = 1, basis(j_atom)
                  tra_lis(i_atom,j_atom) = tra_lis(i_atom,j_atom)+ &
                            tmp_matrix1 (k_basis+k,l_basis+l) *        &
                            tmp_matrix2 (k_basis+k,l_basis+l)
               enddo
             enddo
             write (52, *) i_atom, j_atom, &
                           tra_lis(i_atom, j_atom)


             l_basis = l_basis + basis(j_atom)
         enddo
         k_basis = k_basis + basis(i_atom)
      enddo


      write (*,*)  "Lowdin's way"
      total = 0.d0
      do i_atom = 1, n_atom
         total1 =0.d0
         do j_atom = 1 , n_atom
            total1 = total1 + tra_lis(i_atom, j_atom)
         enddo
         write (*,*) "Total Transion density for Atom:", i_atom, total1
         total = total + total1
      enddo
      write (*,*) "Total Transion density:", total

   

      return
      end subroutine  sub_transition_density
     


