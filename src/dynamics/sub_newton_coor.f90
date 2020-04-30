         subroutine  sub_newton_coor (n_atom, &
                             coor_x, coor_y, coor_z, &
                             vel_x, vel_y, vel_z, &
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
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z




      integer ::  i
      double precision :: dt_atom



       dt_atom= dt

       do i=1, n_atom
        coor_x(i) = coor_x(i) + vel_x(i) * dt_atom
        coor_y(i) = coor_y(i) + vel_y(i) * dt_atom
        coor_z(i) = coor_z(i) + vel_z(i) * dt_atom
       enddo


       return
 
       end 
