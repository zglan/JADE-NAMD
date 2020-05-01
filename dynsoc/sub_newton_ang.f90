         subroutine  sub_newton_ang (n_atom, &
                             coor_x, coor_y, coor_z, &
                             vel_x, vel_y, vel_z, &
                             dt )

      ! integrate euler angle

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




!       print *, "Old coordinate"
!       do i=1, n_atom
!        print *, coor_x(i), vel_x(i) 
!        print *, coor_y(i), vel_y(i)
!        print *, coor_z(i), vel_z(i)
!       enddo

!       dt_atom=0.1


       do i=1, n_atom
        coor_x(i) = coor_x(i) + vel_x(i) * dt_atom
        coor_y(i) = coor_y(i) + vel_y(i) * dt_atom
        coor_z(i) = coor_z(i) + vel_z(i) * dt_atom
       enddo


!        print *, "New coordinate"
!       do i=1, n_atom
!        print *, coor_x(i), vel_x(i)
!        print *, coor_y(i), vel_y(i)
!        print *, coor_z(i), vel_z(i)
!       enddo



       return
 
       end 
