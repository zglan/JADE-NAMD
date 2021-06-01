      subroutine  sub_save_hopping_ana_nac (n_atom, n_state, md_state, &
                                it,time, &
                                index_state, &
                                pes_all, &
                                gra_all_x, &
                                gra_all_y, &
                                gra_all_z, &
                                nac_x, &
                                nac_y, &
                                nac_z, &
                                vel_x, vel_y, vel_z, &
                                rho, &
                                file_save_state, &
                                file_save_all)

 

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: n_state, index_state
      integer, intent(in) :: file_save_state, file_save_all
      double precision, intent(in) :: time
 
      double precision, intent(in), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      double precision, dimension(n_state, n_atom) ::   &
                                                gra_all_x, &
                                                gra_all_y, &
                                                gra_all_z
      double precision, dimension(n_state, n_state, n_atom) ::   &
                                                nac_x, &
                                                nac_y, &
                                                nac_z
      complex (kind=8), dimension(n_state, n_state) :: rho


      double precision,  intent(in), dimension(n_state) :: pes_all
      integer,  intent(in), dimension(n_state) :: md_state


!!!!!!  Local variables

      integer ::  i, j, k
      double precision :: vel_norm
      double precision, allocatable, dimension(:) :: gra_all_norm
      double precision, allocatable, dimension(:, :) :: &
                                               nac_all_norm, &
                                               nac_time_norm
      double precision, allocatable, dimension(:) :: pop_norm
       
       allocate (gra_all_norm(n_state))
       allocate (nac_all_norm (n_state, n_state))
       allocate (nac_time_norm (n_state, n_state))
       allocate ( pop_norm (n_state))



       do i=1, n_state
          pop_norm(i) = rho(i,i)
       enddo

       do i=1, n_state
          gra_all_norm(i) = 0.d0
          do k=1, n_atom
              gra_all_norm(i) = gra_all_norm(i) + gra_all_x(i,k)**2.d0 &
                                                + gra_all_y(i,k)**2.d0 &
                                                + gra_all_z(i,k)**2.d0  
          enddo
          gra_all_norm(i) = gra_all_norm(i) ** 0.5d0
       enddo  

!       do i = 1, n_state
!       do j = 1, n_state
!       do k= 1, n_atom
!          print *, i, j, k
!          print *, nac_x(i, j, k)
!          print *, nac_y(i, j, k)
!          print *, nac_z(i, j, k)
!       enddo
!       enddo
!       enddo




       do i=1, n_state
       do j=1, n_state
          nac_all_norm(i,j) = 0.d0
          do k=1, n_atom
              nac_all_norm(i, j) = nac_all_norm(i, j)+ nac_x(i,j,k)**2.d0 &
                                                     + nac_y(i,j,k)**2.d0 &
                                                     + nac_z(i,j,k)**2.d0
          enddo
          nac_all_norm(i,j) = nac_all_norm(i,j) ** 0.5d0
!          print *, i,j, nac_all_norm(i,j)
       enddo
       enddo

!       do i=1, n_state
!       do j=1, n_state
!         print *, i,j, nac_all_norm(i,j)
!       enddo
!       enddo


      
       vel_norm =0.d0
       do k=1, n_atom
          vel_norm = vel_norm + vel_x(k) **2.d0 &
                              + vel_y(k) **2.d0 &
                              + vel_z(k) **2.d0 
       enddo
       vel_norm = vel_norm ** 0.5d0      

       do i=1, n_state
       do j=1, n_state
          nac_time_norm(i,j) = 0.d0
          do k=1, n_atom
              nac_time_norm(i, j) =   nac_time_norm(i, j)   &
                                    + nac_x(i,j,k)*vel_x(k) &
                                    + nac_y(i,j,k)*vel_y(k) &
                                    + nac_z(i,j,k)*vel_z(k)
          enddo
       enddo
       enddo
       
!       do i=1, n_state
!       do j=1, n_state
!         print *, nac_time_norm(i,j)
!       enddo
!       enddo

       write (file_save_state, 9998) it, time*TOFS, &
                                md_state(index_state), &
                                pes_all(index_state), &
                                vel_norm, &
                                gra_all_norm(index_state)
                                

9998    format(i10, 1x, f15.8, 3x, i3, 1x,100(f20.10, 1x))






        write (file_save_all, * ) "------------------------------------"
        write (file_save_all, 9997) it, time*TOFS, &
                              "current state", md_state(index_state)
        write (file_save_all, 9999) it, time*TOFS, &
                              "Potential energy", pes_all(:)
         write (file_save_all, 9999) it, time*TOFS, &
                              "Current potential energy", pes_all(index_state)
        write (file_save_all, 9999) it, time*TOFS, &
                              "Gradient", gra_all_norm(:)
        write (file_save_all, 9999) it, time*TOFS, &
                              "<psi_i| d/dr | psi_j>", nac_all_norm(:,:)
        write (file_save_all, 9999) it, time*TOFS, &
                              "Velocity", vel_norm
        write (file_save_all, 9999) it, time*TOFS, &
                             "<psi_i| d/dt | psi_j>", nac_time_norm(:,:)        
        write (file_save_all, 9999) it, time*TOFS, &
                              "population", pop_norm(:) 
        write (file_save_all, * ) "------------------------------------"
      
9997   format(i10, 1x, f15.8, 3x, a, 1x, i3)
9999   format(i10, 1x, f15.8, 3x, a, 1x, 100(f20.10, 1x))




       deallocate (gra_all_norm )
       deallocate (nac_all_norm )
       deallocate (nac_time_norm )
       deallocate (pop_norm)


       return
 
       end 
