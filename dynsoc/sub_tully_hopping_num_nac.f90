    subroutine sub_tully_hopping_num_nac  (n_atom, &
                                mass, &
                                old_vel_x, &
                                old_vel_y, &
                                old_vel_z, &
                                vel_x, &
                                vel_y, &
                                vel_z, &
                                n_state, &
                                old_pes_all, &
                                pes_all, &
                                pes_ref, &
                                old_nac_time, &
                                nac_time, &
                                rho, &
                                time, &
                                it, &
                                dtime, &
                                ntime_ele, &
                                index_state, &
                                seed_random, & 
                                cor_dec, &
                                file_save_ele, &
                                file_md_out  )

  

  implicit none

!
!     ----- Parameters -----
!
        include 'param.def'
!
!     ----- Argument -----


       integer, intent(in) :: n_atom, n_state, ntime_ele, it
       integer, intent(inout) :: index_state
       integer, intent(in) :: file_save_ele, file_md_out
       integer, intent(inout) :: seed_random
       double precision, intent(in) :: dtime, pes_ref, time, cor_dec

       double precision, intent(in), dimension(n_state) ::  pes_all, & 
                                                old_pes_all
       
       double precision, intent(in), dimension(n_atom) :: mass
       double precision, intent(in), dimension(n_atom) ::   &
                                                vel_x, vel_y, vel_z  
       double precision, intent(in), dimension(n_atom) ::   &
                                                old_vel_x, old_vel_y, old_vel_z

 
       double precision, intent(in), dimension(n_state, n_state) :: &
                                                nac_time

       double precision, intent(in), dimension(n_state, n_state) ::   &
                                                old_nac_time

       complex (kind=8), intent(inout), dimension(n_state, n_state) :: rho



!
!  Local  

  complex (kind=8), allocatable, dimension (:,:) :: h_vv, h_vv_conjg  

  double precision, allocatable, dimension(:) :: pes_all_eff
  double precision, allocatable, dimension(:) :: vel_x_eff, vel_y_eff, vel_z_eff   

  double precision, allocatable, dimension(:,:) ::  nac_time_eff


  integer :: i,j,k,l, it_ele, lwork, info

  complex (kind=8) :: cnorm

  complex (kind=8), allocatable, dimension(:,:) ::  &
                                                 tmp1,tmp2,ematrix

  complex (kind=8), allocatable, dimension(:,:) :: rho_tmp
                                                           
  double precision, allocatable, dimension(:) :: work,ev
  double precision :: delt, num_random
  complex (kind=8), allocatable, dimension(:,:) :: rwork
  integer, allocatable, dimension(:) :: sign_psi(:)    
  double precision, allocatable, dimension(:) :: pro_hop, pro_sum

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   For test purpose
  complex (kind=8), allocatable, dimension(:,:) :: old_rho
  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!
!     ----- Variables in common -----
!




  lwork= n_state*(n_state+1)
  
    

  delt= dtime/ntime_ele 


!         set the denmension of h_theta and rho_tmp_theta
           
           allocate (h_vv(n_state,n_state))
           allocate (h_vv_conjg(n_state,n_state)) 
           allocate (pes_all_eff(n_state))
           allocate (nac_time_eff(n_state, n_state))
           allocate (vel_x_eff(n_atom))
           allocate (vel_y_eff(n_atom))
           allocate (vel_z_eff(n_atom))
           allocate (rho_tmp(n_state,n_state))
           allocate (work(lwork))
           allocate (ematrix(n_state,n_state))
           allocate (tmp1(n_state,n_state))
           allocate (tmp2(n_state,n_state))
           allocate (ev(n_state)) 
           allocate (rwork(3*n_state-2,3*n_state-2))
           allocate (sign_psi(n_state))           
           allocate (pro_hop(n_state))
           allocate (pro_sum(n_state))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   For test purpose
           allocate (old_rho(n_state,n_state))
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
        

                   
           sign_psi(:) = 1


          old_rho = rho 
             


                   
          pro_hop=0.d0

          do it_ele =1, ntime_ele


             pes_all_eff = old_pes_all + &
                           (it_ele-1)*(pes_all-old_pes_all) /ntime_ele
             nac_time_eff   =   old_nac_time + &
                           (it_ele-1)*(nac_time - old_nac_time) /ntime_ele
             vel_x_eff   = old_vel_x + &
                           (it_ele-1)*(vel_x - old_vel_x) /ntime_ele
             vel_y_eff   = old_vel_y + &
                           (it_ele-1)*(vel_y - old_vel_y) /ntime_ele
             vel_z_eff   = old_vel_z + &
                           (it_ele-1)*(vel_z - old_vel_z) /ntime_ele

         
!!        Construct the effective Hamiltonian 

        

             h_vv(:,:) = cmplx(0.d0, 0.d0)
             do i=1,n_state
             do j=1,n_state
               if (i .eq. j) then
                 h_vv(i,j) =  pes_all_eff(i)
                 h_vv(i,j) = h_vv(i,j) - pes_ref 
               endif
             enddo
             enddo
             
             do i=1,n_state
             do j=1,n_state
                 if (i .ne. j) then
                    h_vv(i,j) = 0.d0
                    h_vv(i,j) =  h_vv(i,j)  &
                                   + nac_time_eff (i,j) 
                    h_vv(i,j) = - c1* h_vv(i,j) 
                endif
             enddo
             enddo

!             write (*,*) "The whole H"
!             do i=1,n_state
!             do j=1,n_state
!               write (*,*) i ,j, h_vv(i,j)
!             enddo
!             enddo


      
              call  ZHEEV('V','U', n_state,  h_vv, n_state,  &
                           ev, work, lwork, rwork, info)                                                                                                
!              print *, 'ev'
!              do k=1,n_state
!              print *, ev(k)
!              enddo


!              print *, 'h_vv'
!              do k=1,nx
!              print *, h_vv(k,:)
!             enddo


              do k=1,n_state
              do l=1,n_state
                 ematrix(k,l)=0.d0
              enddo
              enddo
   
              do k=1,n_state        
                   ematrix(k,k)=cdexp(-c1*ev(k)*delt)
!               print *, -c1*ev(k)*delt 
!               ematrix(k,k) = ev(k) 
              enddo

!              print *, 'ematrix'
!              do k=1,nx
!              print *, ematrix(k,:)
!              enddo

 
              
              
              tmp1=MATMUL(h_vv, ematrix)
!              print *, 'tmp1'
!              do k=1,nx
!              print *, tmp1(k,:)
!              enddo            

               




              do i=1,n_state
              do j=1,n_state
                 h_vv_conjg(i,j) = conjg(h_vv(j,i))  
              enddo
              enddo

               
              tmp2=MATMUL(tmp1, h_vv_conjg)

!              print *, 'tmp2'
!              do k=1,nx
!              print *, tmp2(k,:)
!              enddo
              
              rho_tmp =MATMUL(tmp2,rho)

!              print *, 'rho_tmp'
!              do k=1,nx
!              print *, rho_tmp(k,:)
!              enddo

                            
!              stop

              do k=1,n_state
                  ematrix(k,k)=cdexp(c1*ev(k)*delt)
              enddo

!              stop

              tmp1=MATMUL(h_vv, ematrix)
              tmp2=MATMUL(tmp1, h_vv_conjg)

              rho = MATMUL(rho_tmp, tmp2) 


!            Decoherence corrections
             if (cor_dec .gt. 0) then
                call  sub_decoherent_corr (n_atom, &
                                mass,  &
                                vel_x, &
                                vel_y, &
                                vel_z, &
                                n_state, &
                                pes_all, &
                                rho, &
                                delt, &
                                index_state, &
                                cor_dec, &
                                file_md_out )

             endif


!            Calculate  the hopping probability


             do i=1,n_state
             do j=1,n_state
               if (i .eq. j) then
                   h_vv(i,j) =  pes_all_eff(i)
                   h_vv(i,i) = h_vv(i,j) - pes_ref
               endif
             enddo
             enddo

             do i=1,n_state
             do j=1,n_state
                 h_vv(i,j) = 0.d0
                 h_vv(i,j) = h_vv(i,j)  &
                             + nac_time_eff (i,j) 
                 h_vv(i,j) = - c1* h_vv(i,j)
             enddo
             enddo





              do i=1,n_state
                 if (index_state .ne. i) then
                    h_vv(i, index_state) = 0.d0
                    h_vv(i, index_state) = h_vv(i, index_state)  &
                                + nac_time_eff (i,index_state) 
                    pro_hop(i) = pro_hop(i)   & 
                                 - ( 2 * delt *             &
                                     real(conjg(rho(i,index_state)))  &
                                     * h_vv(i, index_state)   &
                                   ) / real(rho(index_state, index_state))       
                 endif
              enddo
             

         enddo



         do i=1,n_state
            if (pro_hop(i) .lt. 0.d0) then
                pro_hop(i)=0.d0
            endif
         enddo



         pro_hop(index_state) = 1.d0
         do i=1,n_state
            if (index_state .ne. i) then   
            pro_hop(index_state) = pro_hop(index_state) - pro_hop(i)  
            endif
         enddo 
         
        
         pro_sum=0.d0
         do  i=1,n_state
             do j =1, i
                pro_sum(i) = pro_sum(i) + pro_hop(j)
             enddo
         enddo    
           



   

        write (file_save_ele, * ) "------------------------------------"
!        do i=1, n_state
!        do j=1, n_state
!             write (file_save_ele, 9999), it, time*TOFS, &
!                                          "Effective H", i, j, &
!                                    REAL(h_vv(i,j)), '+i',AIMAG(h_vv(i,j))
!        enddo
!        enddo
!
!        do j=1, n_state
!             write (file_save_ele, 9997), it, time*TOFS, &
!                                          "Eigenvalues", &
!                                          ev(:) 
!        enddo

        do i=1, n_state
        do j=1, n_state
             write (file_save_ele, 9999) it, time*TOFS, &
                                          "rho", i, j, &
                                    REAL(rho(i,j)), '+i',AIMAG(rho(i,j))
        enddo
        enddo

        write (file_save_ele, 9996) it, time*TOFS, &
                              "The current state", index_state
        write (file_save_ele, 9997) it, time*TOFS, &
                              "Hopping probability", pro_hop(:)
        write (file_save_ele, 9997) it, time*TOFS, &
                               "Area for hopping", pro_sum(:)






!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   For testing purpose: different way to calculate hopping probability
!
!
!
             do i=1,n_state
                 if (index_state .ne. i) then
                    h_vv(i, index_state) = 0.d0
                    h_vv(i, index_state) = h_vv(i, index_state)  &
                                   + old_nac_time (i,index_state) 
                    pro_hop(i) = - ( 2 * dtime *             &
                                      real(conjg(old_rho(i,index_state)))  &
                                      * h_vv(i, index_state) &
                                     ) / real(old_rho(index_state, index_state))     
                     h_vv(i, index_state) = 0.d0                           
                     do k =1, n_atom
                        h_vv(i, index_state) = h_vv(i, index_state)  &
                                   + nac_time (i,index_state) 
                     enddo
                     pro_hop(i) =  pro_hop(i) &
                                   -( 2 * dtime *             &
                                      real(conjg(rho(i,index_state)))  &
                                      * h_vv(i, index_state) &
                                     ) / real(rho(index_state, index_state))
                     pro_hop(i) = pro_hop(i) /2.d0 
                 endif
             enddo


             do i=1,n_state
                if (pro_hop(i) .lt. 0.d0) then
!                    pro_hop(i)=0.d0
                endif
             enddo



!             pro_hop(index_state) = 1
!!             do i=1,n_state
!!               if (index_state .ne. i) then
!!                   pro_hop(index_state) = pro_hop(index_state) - pro_hop(i)
!!               endif
!!             enddo



!             pro_sum=0.d0
!             do  i=1,n_state
!                 do j =1, i
!                    pro_sum(i) = pro_sum(i) + pro_hop(j)
!                 enddo
!             enddo



!             write (file_save_ele, 9997) it, time*TOFS, &
!                              "Hopping probability (averaged)", pro_hop(:)
!
!
!
!
!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1






!       generate random number
!       the init_random_seed may be set before the dynamic cycle.
        call get_random_number(num_random)
!       write (*,*) "RANDOM", seed_random, num_random


!       Surface-hopping check

        if ( (0 .le. num_random) &
             .and.               &
             (num_random .lt. pro_sum(1) ) &
           )  then
              index_state = 1
              goto  7000
        else
           do  i= 2, n_state
               if ( (pro_sum(i-1) .le. num_random)  &
                    .and.               &
                    (num_random .lt. pro_sum(i) ) &
                  )  then
                     index_state = i
                     goto 7000
              endif
           enddo
        endif


7000    write (file_save_ele, 9997) it, time*TOFS, &
                              "Random number",  num_random
        write (file_save_ele, 9996) it, time*TOFS, &
                              "The new state", index_state
        write (file_save_ele, * ) "------------------------------------"

9996   format(i10, 1x, f15.8, 3x, a, 1x, i3)
9997   format(i10, 1x, f15.8, 3x, a, 1x, 10(f15.8, 1x))
9999   format(i10, 1x, f15.8, 3x, a, 1x, i3, 1x, i3, 1x, f10.7, a, f10.7)





           deallocate (h_vv)
           deallocate (h_vv_conjg)
           deallocate (pes_all_eff)
           deallocate (nac_time_eff)
           deallocate (rho_tmp)
           deallocate (work)
           deallocate (ematrix)
           deallocate (tmp1)
           deallocate (tmp2)
           deallocate (ev)
           deallocate (rwork)
           deallocate (sign_psi)
           deallocate (pro_hop)
           deallocate (pro_sum)


  
  end 
