         subroutine  sub_newton_vel (n_atom, &
                             vel_x, vel_y, vel_z, &
                             gradient_x, &
                             gradient_y, &
                             gradient_z, &
                             mass, &
                             dt )



      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom
      double precision, intent(in) :: dt
 
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      gradient_x, &
                                                      gradient_y, &
                                                      gradient_z



      double precision, intent(inout), dimension(n_atom)  :: mass       


      integer ::  i

      double precision :: dt_atom

    
       
       dt_atom= dt

       do i=1, n_atom
        vel_x(i) = vel_x(i) - 0.5d0 * dt_atom * gradient_x(i)/mass(i) 
        vel_y(i) = vel_y(i) - 0.5d0 * dt_atom * gradient_y(i)/mass(i)
        vel_z(i) = vel_z(i) - 0.5d0 * dt_atom * gradient_z(i)/mass(i)
       enddo



       return
 
       end 
