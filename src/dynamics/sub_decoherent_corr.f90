    subroutine sub_decoherent_corr (n_atom, &
                                mass,  &
                                vel_x, &
                                vel_y, &
                                vel_z, &
                                n_state, &
                                pes_all, &
                                rho, &
                                dt_dec, &
                                index_state, &
                                cor_dec, &
                                file_md_out )

  implicit none

!
!     ----- Parameters -----
!
        include 'param.def'
!
!     ----- Argument -----


       integer, intent(in) :: n_atom, n_state, file_md_out
       integer, intent(inout) :: index_state
       double precision, intent(in) :: dt_dec, cor_dec

       double precision, intent(in), dimension(n_state) ::  pes_all
       
       double precision, intent(in), dimension(n_atom) :: mass
       double precision, intent(in), dimension(n_atom) ::   &
                                                vel_x, vel_y, vel_z  

       complex (kind=8), intent(inout), dimension(n_state, n_state) :: rho


!      local variables
      
       integer :: i,j,k
       double precision, allocatable, dimension(:) :: time_dec       
       double precision :: kinetic_energy
       complex (kind=8), allocatable, dimension(:, :) :: old_rho, new_rho



       allocate (time_dec(n_state))
       allocate (old_rho(n_state, n_state))
       allocate (new_rho(n_state, n_state))

       old_rho = rho
       new_rho = rho

!      Calculate the kinetic energy
       
       kinetic_energy=0.d0
       do  i=1, n_atom
           kinetic_energy=    kinetic_energy  &
                           + 0.5d0 * mass(i) * (vel_x(i))**2 &
                           + 0.5d0 * mass(i) * (vel_y(i))**2 &
                           + 0.5d0 * mass(i) * (vel_z(i))**2

      enddo

!-------------------------------------------------------------------
!     Decoherence correction
!     Calculate the decay time
!     See Granucci and Perciso's  paper
!     JCP 126, 1334114 (2007).
!    
!     tau (M->K) = \hbar / ( | E_M-E_K | ) * ( 1+  C / E_kin )  

!      write (file_md_out, *) "Perform decoherence corrections." 
      time_dec(:)=0.0      
      do i=1,n_state
         if (i .ne. index_state) then
            if ( ( kinetic_energy .lt.  0.00000001) &
                 .or.      &
                 (abs( pes_all(i)- pes_all(index_state)) .lt. 0.000000001 ) &
               ) then
                   time_dec(i) = 10000000
            else
                   time_dec(i) =  ( 1+ cor_dec/kinetic_energy) / &
                              (abs( pes_all(i)- pes_all(index_state)))
            endif
         endif
      enddo 



!      write (file_md_out, *) "Perform decoherence corrections."
!      write (file_md_out, *) "Decay time constant" 
!      do i=1,n_state
!         if (i .ne. index_state) then
!             write (file_md_out, *),  i, index_state, time_dec(i)
!             write (file_md_out, *),  i, index_state, dexp(-dt_dec/time_dec(i))
!         endif
!      enddo
    


!     M is the current state
!     K is not the current state

!     Make the correction on the diagonal elements rho_ii

!     (1) Corretion for other state K (K \= M) 
!     (rho_KK)' = rho_KK exp (-t/t_dec)       

      do i=1, n_state
         if (i .ne. index_state) then
            new_rho(i,i) =old_rho(i,i) * &
                      dexp(-2*dt_dec/time_dec(i))
         endif
      enddo

!     (2) Correction for the current MD state M
!     Note  (rho_MM)' + sum_K (rho_KK)' = 1 (trace of density matrix should be one)
!     (rho_MM)' = 1- sum_K (rho_KK)'

      new_rho(index_state,index_state) = 1.d0
      do i=1, n_state
         if (i .ne. index_state) then
             new_rho(index_state,index_state) = new_rho(index_state,index_state)  &
                                       -new_rho(i,i)
         endif
      enddo
     
      if ( abs(new_rho(index_state,index_state)) .lt. 0.00001 ) then
        write (*,*) "The population on the current state is near 0 !!!"
        stop
      endif                                  


!     Make the correction on the diagonal elements rho_ij

!     (1) Corretion for rho_K, L (K, L \= M)
!     (rho_KL)' = rho_KL exp (-t/t_dec_K) exp (-t/t_dec_L)

      do i=1, n_state
      do j=1, n_state
         if (i .ne. j) then
         if (  ( i .ne. index_state)  &
               .and.                  &
               ( j .ne. index_state)  &
            )  then
            new_rho(i,j) = old_rho(i,j) * &
                      dexp(-dt_dec/time_dec(i)) * &
                      dexp(-dt_dec/time_dec(j))
         endif
         endif
      enddo
      enddo

!     (2) Corretion for rho_KM (K \= M, M is the current state)
!     (rho_KM)' = rho_KM exp (-t/t_dec_K) * [  ( 1- sum_K (rho_KK)')/ rho_MM  ]^0.5
!             = rho_KM exp (-t/t_dec_K) * [(rho_MM)'/rho_MM]^0.5

              
       do i=1, n_state
          if ( i .ne. index_state ) then
             new_rho(i,index_state) = old_rho(i,index_state) * &
                                  dexp(-dt_dec/time_dec(i)) * &
                           ( new_rho(index_state, index_state) / old_rho(index_state, index_state)  )**0.5d0
          endif
       enddo


!     (2) Corretion for rho_MK (K \= M, M is the current state)
!     (rho_MK)' = rho_MK exp (-t/t_dec_K) * [  ( 1- sum_K (rho_KK)')/ rho_MM  ]^0.5
!             = rho_MK exp (-t/t_dec_K) * [(rho_MM)'/rho_MM]^0.5


       do i=1, n_state
          if ( i .ne. index_state ) then
             new_rho(index_state,i) = old_rho(index_state,i) * &
                                  dexp(-dt_dec/time_dec(i)) * &
                           ( new_rho(index_state, index_state) / old_rho(index_state, index_state)  )**0.5d0
          endif
       enddo


!       print *, old_rho
!       print *, new_rho
!       stop
     
7777   rho=new_rho

       deallocate (time_dec)
       deallocate (old_rho)
       deallocate (new_rho)
       return
       end subroutine sub_decoherent_corr
