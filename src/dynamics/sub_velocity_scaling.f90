       subroutine sub_velocity_scaling ( n_atom, &
                                      n_state, &
                                      mass,    &
                                      pes_all, &
                                      nac_x, &
                                      nac_y, &
                                      nac_z, &
                                      old_index_state, &
                                      new_index_state, &
                                      vel_x, vel_y, vel_z, &
                                      file_md_out)

      
       implicit none
       include 'param.def'
!     common  variables 

      integer, intent(in) :: n_atom, n_state
      double precision,  intent(in), dimension(n_atom) :: mass
      double precision,  intent(in), dimension(n_state) :: pes_all     
      double precision,  intent(in), dimension(n_state, n_state, n_atom) ::   &
                                                nac_x, &
                                                nac_y, &
                                                nac_z

      integer, intent(in) :: old_index_state
      integer, intent(inout) :: new_index_state

      double precision, intent(inout), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      integer, intent(in) :: file_md_out

!     Local variables

      integer :: i, j, k
      double precision :: a_second_equ, b_second_equ, c_second_equ, &
                          judge_second_equ
      double precision :: solu_1_second_equ, solu_2_second_equ, &
                          solu_second_equ     
      double precision :: a_rev, b_rev, solu_rev   
      double precision :: nac_norm

      double precision,  allocatable, dimension(:,:,:) ::   &
                                           nac_unit_x, &
                                           nac_unit_y, &
                                           nac_unit_z 

      allocate (nac_unit_x(n_state, n_state, n_atom))
      allocate (nac_unit_y(n_state, n_state, n_atom))
      allocate (nac_unit_z(n_state, n_state, n_atom))

      
      write (file_md_out,*)  "Check the velocity adjustment"
      write (file_md_out,*)  "Old velocity"
      do i=1,n_atom
          write (file_md_out,9999) i, vel_x(i), vel_y(i), vel_z(i)
      enddo

9999  format(i7, 1x, 3(f20.10, 1x))
 


!      Set up the unit vector to correct the velocity.
!      Please note that the direct use of nonadiabatic coupling or other
!      vectors should also be correct, while the unit vector 
!      should be recommend to use due to the numerical stability.       


       nac_norm = 0.0
       do i=1, n_atom
          nac_norm =  nac_norm + &
                  (  nac_x(new_index_state, old_index_state, i)**2.d0  &
                   + nac_y(new_index_state, old_index_state, i)**2.d0  &
                   + nac_z(new_index_state, old_index_state, i)**2.d0  &
                  )
       enddo
       nac_norm = nac_norm **0.5d0

       nac_unit_x = nac_x / nac_norm
       nac_unit_y = nac_y / nac_norm
       nac_unit_z = nac_z / nac_norm
       


!     "Calculate all terms in the second-order equations"
!     (v_new)_i = (v_old)_i - d * nac(new_state, old_state, i) / m_i
!     a*d^2 - b*d + c =0
!     Calculate a, b, c. Then get d   

      a_second_equ =0.d0
      do i=1,n_atom
        a_second_equ=a_second_equ + &
            (  nac_unit_x(new_index_state, old_index_state, i)**2.d0  &
             + nac_unit_y(new_index_state, old_index_state, i)**2.d0  &
             + nac_unit_z(new_index_state, old_index_state, i)**2.d0  &
             )/mass(i)
      enddo      
      a_second_equ =0.5d0*a_second_equ
      
      if (a_second_equ .eq. 0) then
        write (file_md_out,*)  "a term is zero"
        stop
      endif
     
      b_second_equ =0.d0
      do i=1,n_atom
        b_second_equ =  b_second_equ + &
          (  nac_unit_x(new_index_state, old_index_state, i)*vel_x(i)  &
           + nac_unit_y(new_index_state, old_index_state, i)*vel_y(i)  &
           + nac_unit_z(new_index_state, old_index_state, i)*vel_z(i)  &
          )
      enddo
      b_second_equ = b_second_equ

   
      c_second_equ = pes_all(new_index_state) - pes_all(old_index_state)

     
      judge_second_equ =  b_second_equ**2.d0   &
                         -4.d0*(a_second_equ*c_second_equ) 
      write (file_md_out,*)  &
         "Check whether the kinetic energy is enough to perform the hop"
      write (file_md_out,*)  "b^2-4ac", judge_second_equ 
  
!     Find the solutions of second-order equation if b**2-4*a*c>=0

      if (judge_second_equ .ge. 0.d0) then
         write (file_md_out,*) "Successful hops!"
         write (file_md_out,*) "Velocity adjustment" 
         solu_1_second_equ = &
                          (b_second_equ + (judge_second_equ)**0.5d0) &
                           / (2.d0*a_second_equ)
         solu_2_second_equ = &
                          (b_second_equ - (judge_second_equ)**0.5d0) &
                            / (2.d0*a_second_equ)
!        Select the d with the smaller absolute value
         if (abs(solu_1_second_equ) .ge. abs(solu_2_second_equ) ) then
             solu_second_equ = solu_2_second_equ
         else
             solu_second_equ = solu_1_second_equ
         endif
         write (file_md_out,*) "Scaling parameter 1:", solu_1_second_equ
         write (file_md_out,*) "Scaling parameter 2:", solu_2_second_equ
         write (file_md_out,*) "Scaling parameter 3:", solu_second_equ


         do i=1,n_atom
            vel_x(i) = vel_x(i) - solu_second_equ * &
                nac_unit_x(new_index_state, old_index_state, i)/mass(i) 
            vel_y(i) = vel_y(i) - solu_second_equ * &
                nac_unit_y(new_index_state, old_index_state, i)/mass(i)
            vel_z(i) = vel_z(i) - solu_second_equ * &
                nac_unit_z(new_index_state, old_index_state, i)/mass(i)
         enddo
       
      endif 

!     If b**2-4*a*c>0, deal with the frustrated hops
!     Please note the velocity correction of frustrated hops can be 
!     derived from the energy conservation
!     sum_i 0.5*m_i*(vnew)_i**2 - sum_i 0.5*m_i*(vold)_i**2 =0   

      if (judge_second_equ .lt. 0.d0) then
         write (file_md_out,*) "Frustrated hops!"
         
         a_rev =0.d0
         do i=1,n_atom
         a_rev =  a_rev + &
                  (  nac_unit_x(new_index_state, old_index_state, i)**2.d0  &
                   + nac_unit_y(new_index_state, old_index_state, i)**2.d0  &
                   + nac_unit_z(new_index_state, old_index_state, i)**2.d0  &
                  )/mass(i)
         enddo

         if (a_rev .eq. 0) then
            write (file_md_out,*)  "a term is zero"
            stop
         endif


         b_rev =0.d0
         do i=1,n_atom
            b_rev =  b_rev + &
             (vel_x(i)*nac_unit_x(new_index_state, old_index_state, i) &
             +vel_y(i)*nac_unit_y(new_index_state, old_index_state, i) &
             +vel_z(i)*nac_unit_z(new_index_state, old_index_state, i) &
          )
         enddo


         solu_rev = 2.d0*b_rev/a_rev


         do i=1,n_atom
            vel_x(i) = vel_x(i) - solu_rev * &
                 nac_unit_x(new_index_state, old_index_state, i)/mass(i)
            vel_y(i) = vel_y(i) - solu_rev * &
                 nac_unit_y(new_index_state, old_index_state, i)/mass(i)
            vel_z(i) = vel_z(i) - solu_rev * &
                 nac_unit_z(new_index_state, old_index_state, i)/mass(i)
         enddo
     
         b_rev =0.d0
         do i=1,n_atom
            b_rev =  b_rev + &
                    (  mass(i)*vel_x(i)*   &
                       nac_unit_x(new_index_state, old_index_state, i) &
                     + mass(i)*vel_y(i)*   &
                       nac_unit_y(new_index_state, old_index_state, i) &
                     + mass(i)*vel_z(i)*   &
                       nac_unit_z(new_index_state, old_index_state, i) &
                    )
         enddo

    
         write (file_md_out,*) "Return back to the current state!"
         write (file_md_out,*) "Back to State", old_index_state
         new_index_state = old_index_state
         write (file_md_out,*) "Reverse the component of momenta"
         write (file_md_out,*) "Rescaling factor", solu_rev


                 
      endif


      write (file_md_out,*)  "New velocity"
      do i=1,n_atom
          write (file_md_out,9999) i, vel_x(i), vel_y(i), vel_z(i)
      enddo



       deallocate (nac_unit_x)
       deallocate (nac_unit_y)
       deallocate (nac_unit_z)


      return 
      end subroutine sub_velocity_scaling
