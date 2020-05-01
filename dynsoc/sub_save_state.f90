      subroutine  sub_save_state (n_atom, n_state, md_state, &
                                it,time, &
                                index_state, &
                                pes_all, &
                                gradient_x, &
                                gradient_y, &
                                gradient_z, &
                                vel_x, vel_y, vel_z, &
                                rho, &
                                file_save_state)

 

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: n_state, index_state
      integer, intent(in) :: file_save_state
      double precision, intent(in) :: time
 
      double precision, intent(in), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      double precision, intent(in), dimension(n_atom) ::   &
                                                gradient_x, &
                                                gradient_y, &
                                                gradient_z
      complex (kind=8), dimension(n_state, n_state) :: rho


      double precision,  intent(in), dimension(n_state) :: pes_all
      integer,  intent(in), dimension(n_state) :: md_state


!!!!!!  Local variables

      integer ::  i, j, k
      double precision :: vel_norm
      double precision :: gra_all_norm
      double precision :: nac_time_norm
       
       ! gradient norm
       gra_all_norm = 0.d0
       do k=1, n_atom
          gra_all_norm = gra_all_norm + gradient_x(k)**2.d0 &
                                      + gradient_y(k)**2.d0 &
                                      + gradient_z(k)**2.d0  
       enddo
       gra_all_norm = gra_all_norm ** 0.5d0

       ! velocity norm
       vel_norm =0.d0
       do k=1, n_atom
          vel_norm = vel_norm + vel_x(k) **2.d0 &
                              + vel_y(k) **2.d0 &
                              + vel_z(k) **2.d0 
       enddo
       vel_norm = vel_norm ** 0.5d0      

       write (file_save_state, 9998) it, time*TOFS, &
                                md_state(index_state), &
                                rho(index_state, index_state), &
                                pes_all(index_state), &
                                vel_norm, &
                                gra_all_norm


       return

9998    format(i10, 1x, f15.8, 3x, i3, 1x,100(f20.10, 1x))

 
       end 
