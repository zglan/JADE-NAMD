      subroutine   check_kinetic         (n_geom, &
                                          n_atom, &
                                          file_v_V_au, &
                                          file_p_P_au )


      implicit none
      include "param.def"     

      integer, intent(in) :: n_geom, n_atom, &
                            file_v_V_au, file_p_p_au




      double precision, allocatable, dimension (:) :: px, py, pz
      double precision, allocatable, dimension (:) :: m_atom, kinetic

      character*2, allocatable,dimension(:) ::   atom_1, atom_2
      character*80 :: string1, string2
      integer :: i, j ,k      
      double precision :: charge_tmp


      

       allocate (px(n_atom))
       allocate (py(n_atom))
       allocate (pz(n_atom))

       allocate (m_atom(n_atom))

       allocate (atom_1(n_atom))
       allocate (atom_2(n_atom))


       allocate (kinetic(n_geom))
 


       write (*,*)
       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
       write (*,*) "The average kinetic energy in Catersian coordinates"
       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"




           do j=1, n_geom
              read  (file_p_P_au,9997) string1  
              read  (file_p_P_au,9997) string2
              
              kinetic(j) =0.0              
              do k=1, n_atom
                 read (file_p_P_au,*) atom_1(k), &
                             px(k), &  
                             py(k), &  
                             pz(k)  

                 call sub_get_mass ( atom_1(k), m_atom(k), charge_tmp)          

                 kinetic(j) =  kinetic(j) + &
                               ( px(k)**2  & 
                               + py(k)**2  &
                               + pz(k)**2  &
                               ) / (2 * m_atom(k) )
             enddo
          enddo


             write (*,*) "Check the kinetic energy from monmenta"
             write (*,*) " Average of Kinetic Energy (au) " &
                          , sum(kinetic)/(n_geom) 
             write (*,*) " Average of Kinetic Energy (eV) " &
                          , sum(kinetic)/(n_geom)*TOEV 
 





            
           do j=1, n_geom
              read  (file_v_V_au,9997) string1
              read  (file_v_V_au,9997) string2

              kinetic(j) =0

              do k=1, n_atom
                 read (file_v_V_au,*) atom_1(k), &
                             px(k), &
                             py(k), &
                             pz(k)

                 call sub_get_mass ( atom_1(k), m_atom(k), charge_tmp)

                 kinetic(j) = kinetic(j) + &
                               0.5 * m_atom(k) * &
                               ( px(k)**2  &
                               + py(k)**2  &
                               + pz(k)**2  &
                               ) 
!                print *, i, k
!                print *, kinetic(j)
             enddo
          enddo


             
             write (*,*) "Check the kinetic energy from velocity"
             write (*,*) " Average of Kinetic Energy (au) " &
                          , sum(kinetic)/(n_geom)
             write (*,*) " Average of Kinetic Energy (eV) " &
                          , sum(kinetic)/(n_geom)*TOEV



      
9997  format(a80)
9996  format(1x,i3, 3(1x, f15.8, 1x, i2))
       
        
       end subroutine   check_kinetic
       


