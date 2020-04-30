      subroutine   sub_save_energy( n_atom, &
                                pes, &
                                vel_x, vel_y, vel_z, &
                                mass, &
                                it,time, &
                                file_save_energy )


      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: file_save_energy
      double precision, intent(in) :: time
 
      double precision, intent(inout), dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z
      double precision, intent(in), dimension(n_atom) ::   &
                                                      mass     
      double precision :: pes


!!!!!!  Local variables

      integer ::  i
           
      double precision :: kinetic_energy, total_energy
      double precision :: linear_momenta_x, &
                          linear_momenta_y, &
                          linear_momenta_z 


      kinetic_energy=0.d0
      
      do  i=1, n_atom  
       kinetic_energy=    kinetic_energy + 0.5d0 * mass(i) * & 
                        ( vel_x(i)**2.d0 + &
                         vel_y(i)**2.d0 + &
                         vel_z(i)**2.d0 )
      
                          
      enddo
       

!      kb = 1.0
!      temperature = kinetic_energy * (2.0/3.0) / kb
      total_energy = pes+kinetic_energy


       linear_momenta_x=0.d0
       linear_momenta_y=0.d0
       linear_momenta_z=0.d0   


       do  i=1, n_atom
        linear_momenta_x =    linear_momenta_x  &
                            + mass(i) * (vel_x(i)) 
        linear_momenta_y =    linear_momenta_y  &
                            + mass(i) * (vel_y(i))
        linear_momenta_z =    linear_momenta_z  &
                            + mass(i) * (vel_z(i))

      enddo


       write (file_save_energy, 9999) it, time*TOFS, &
                                      pes, &
                                      kinetic_energy, &
                                      total_energy, &
                                      linear_momenta_x, &
                                      linear_momenta_y, &
                                      linear_momenta_z
  




9999   format(i10, 1x, 10(f20.10, 1x))

       return
 
       end 
