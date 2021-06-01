subroutine          sub_zn_hopping   (n_atom, &
                                      mass, &
                                      atom_label, &
                                      label_ZN, &
                                      label_reject_hops, &
                                      hop_e, &
                                      time, &
                                      it, &
                                      dtime, &
                                      n_state, &
                                      md_state, &
                                      index_state, &
                                      ntime_ele, &
                                      pes_all, &
                                      old_pes_all, &
                                      old_2_Pes_all, &
                                      coor_x, &
                                      coor_y, &
                                      coor_z, &
                                      old_coor_x, &
                                      old_coor_y, &
                                      old_coor_z, &
                                      old_2_coor_x, &
                                      old_2_coor_y, &
                                      old_2_coor_z, &
                                      old_vel_x, &
                                      old_vel_y, &
                                      old_vel_z, &
                                      gra_all_x, &
                                      gra_all_y, &
                                      gra_all_z, &
                                      old_gra_all_x, &
                                      old_gra_all_y, &
                                      old_gra_all_z, &
                                      old_2_gra_all_x, &
                                      old_2_gra_all_y, &
                                      old_2_gra_all_z, &
                                      old_nac_x, &
                                      old_nac_y, &
                                      old_nac_z, &
                                      seed_random, &
                                      file_save_ele,&
                                      file_md_out)


      implicit none

!
!     ----- Parameters -----
!
      include 'param.def'
!
!     ----- Argument -----

      integer, intent(in) :: n_atom, n_state, ntime_ele, it, label_ZN, label_reject_hops

      integer, intent(in), dimension(n_state) :: md_state

      integer, intent(inout) :: index_state

      integer, intent(in) :: file_save_ele, file_md_out

      integer, intent(inout) :: seed_random

      double precision, intent(inout), dimension(n_state, n_state, n_atom) :: old_nac_x, old_nac_y, old_nac_z

      double precision, intent(in) :: dtime, time, hop_e

      double precision, intent(in), dimension(n_atom) :: mass

      double precision, dimension(n_state) ::  pes_all, old_pes_all, old_2_pes_all

      double precision, intent(in), dimension(n_atom) ::   &
                                               coor_x, coor_y, coor_z, &  
                                               old_coor_x, old_coor_y, old_coor_z, &  
                                               old_2_coor_x, old_2_coor_y, old_2_coor_z

      double precision, intent(inout), dimension(n_atom) :: old_vel_x, old_vel_y, old_vel_z

      double precision, intent(in), dimension(n_state, n_atom) ::   &
                                                           gra_all_x, gra_all_y, gra_all_z, &
                                                           old_gra_all_x, old_gra_all_y, old_gra_all_z, &
                                                           old_2_gra_all_x, old_2_gra_all_y, old_2_gra_all_z
      
!  Local  

      character*2, dimension(n_atom)  ::  atom_label 

      integer :: i, j, k, l, it_ele, ZN_method, old_index_state, new_index_state


      double precision, dimension(n_state) ::  pes_zn1, pes_zn2, pes_zn3, &
                                               pro_hop, pro_sum
      double precision, dimension(n_state,n_state) ::  ZN_EK_PAL, ZN_EK_PER

      double precision, dimension(n_atom,3) ::   coor_zn1, coor_zn2, coor_zn3, vel_zn2, &
                                                 ZN_F1, ZN_F2, ZN_S, ZN_S_NORM, ZN_P_PAL, &
                                                 ZN_P_PER

      double precision, dimension(n_state, n_atom, 3) ::   gra_zn1, &
                                                           gra_zn2, &
                                                           gra_zn3
      double precision, dimension(n_state, n_state, n_atom, 3) ::   ZN_V_PAL, ZN_V_PER

      double precision, dimension(n_atom) ::   ZN_PS

      double precision :: ZN_a2, ZN_b2, ZN_EX, ZN_ET, ZN_F1_F2, &
                          ZN_F1F2, ZN_V12, tmp, tmp_1, tmp_2,  &
                          tmp_ZN_F1F2, ZN_DELTA_E_zn3, ZN_DELTA_E_zn2, &
                          ZN_DELTA_E_zn1, delt, num_random, ZN_SUM_F1, ZN_SUM_F2, &
                          ZN_E_HOP, ZN_DELTA_E, ZN_K_SCAL


      old_index_state = index_state
      new_index_state = index_state

      delt= dtime/ntime_ele 

         pes_zn3 = pes_all
         pes_zn2 = old_pes_all
         pes_zn1 = old_2_pes_all
         
         do i = 1, n_atom

            coor_zn3(i,1) = coor_x(i)
            coor_zn3(i,2) = coor_y(i)
            coor_zn3(i,3) = coor_z(i)

            coor_zn2(i,1) = old_coor_x(i)
            coor_zn2(i,2) = old_coor_y(i)
            coor_zn2(i,3) = old_coor_z(i)

            coor_zn1(i,1) = old_2_coor_x(i)
            coor_zn1(i,2) = old_2_coor_y(i)
            coor_zn1(i,3) = old_2_coor_z(i)

            vel_zn2(i,1) = old_vel_x(i)
            vel_zn2(i,2) = old_vel_y(i)
            vel_zn2(i,3) = old_vel_z(i)


            gra_zn3(:,i,1) = gra_all_x(:,i)
            gra_zn3(:,i,2) = gra_all_y(:,i)
            gra_zn3(:,i,3) = gra_all_z(:,i)

            gra_zn2(:,i,1) = old_gra_all_x(:,i)
            gra_zn2(:,i,2) = old_gra_all_y(:,i)
            gra_zn2(:,i,3) = old_gra_all_z(:,i)

            gra_zn1(:,i,1) = old_2_gra_all_x(:,i)
            gra_zn1(:,i,2) = old_2_gra_all_y(:,i)
            gra_zn1(:,i,3) = old_2_gra_all_z(:,i)

         enddo

      ZN_EK_PAL = 0.d0
      ZN_EK_PER = 0.d0

      i = index_state

      do j =1, n_state

         pro_hop(j) = 0.d0

         if (i .ne. j) then
            
            ZN_DELTA_E_zn3 = abs(pes_zn3(j) - pes_zn3(i))
            ZN_DELTA_E_zn2 = abs(pes_zn2(j) - pes_zn2(i))
            ZN_DELTA_E_zn1 = abs(pes_zn1(j) - pes_zn1(i))

            if ((ZN_DELTA_E_zn2 .lt. ZN_DELTA_E_zn3) .and. &
                (ZN_DELTA_E_zn2 .lt. ZN_DELTA_E_zn1) ) then

               tmp = 0.d0

               do k = 1, n_atom

                  do l = 1, 3

                     if (abs((coor_zn3(k,l) - coor_zn1(k,l))) .lt. 0.00005) then
                       ZN_F1(k,l) = 0.d0
                       ZN_F2(k,l) = 0.d0
                     else

                       ZN_F1(k,l) = -1 / (coor_zn3(k,l) - coor_zn1(k,l)) * &
                                  (gra_zn3(j,k,l) * (coor_zn2(k,l) - coor_zn1(k,l)) -  &
                                   gra_zn1(i,k,l) * (coor_zn2(k,l) - coor_zn3(k,l)))


                       ZN_F2(k,l) = -1 / (coor_zn3(k,l) - coor_zn1(k,l)) * &
                                  (gra_zn3(i,k,l) * (coor_zn2(k,l)-coor_zn1(k,l)) -  &
                                   gra_zn1(j,k,l) * (coor_zn2(k,l) - coor_zn3(k,l)))
                     endif


                     ZN_S(k,l) = (ZN_F2(k,l) - ZN_F1(k,l)) / sqrt(mass(k))
                     tmp = tmp + ZN_S(k,l)**2

                  enddo
                 
                  old_nac_x(i,j,k) = ZN_S(k,1)
                  old_nac_y(i,j,k) = ZN_S(k,2)
                  old_nac_z(i,j,k) = ZN_S(k,3)

                  old_nac_x(j,i,k) = -old_nac_x(i,j,k)
                  old_nac_y(j,i,k) = -old_nac_y(i,j,k)
                  old_nac_z(j,i,k) = -old_nac_z(i,j,k)
                  

               enddo



               tmp = sqrt(tmp)

               do k = 1, n_atom
                   do l = 1, 3
                      ZN_S_NORM(k,l) = ZN_S(k,l) / tmp
                   enddo
               enddo

              do k = 1, n_atom
                  tmp = 0.d0
                  do l = 1, 3
                      tmp = tmp + ZN_S_NORM(k,l)**2
                  enddo

                  tmp = sqrt(tmp)

                  if (tmp .eq. 0.d0) then

                     ZN_S_NORM(k,:) = 0.d0
                  
                  else

                     do l = 1, 3
                         ZN_S_NORM(k,l) = ZN_S_NORM(k,l) / tmp
                     enddo
                  endif
              enddo




               ZN_SUM_F1 = 0.d0
               ZN_SUM_F2 = 0.d0

               do k = 1, n_atom
                  do l = 1, 3
                    ZN_SUM_F1 = ZN_SUM_F1 + ZN_F1(k,l)**2
                    ZN_SUM_F2 = ZN_SUM_F2 + ZN_F2(k,l)**2
                  enddo
               enddo


               if ((sqrt(ZN_SUM_F1) .lt. 0.001) .or. (sqrt(ZN_SUM_F2) .lt. 0.001) ) then
                  ZN_method = 1
               else
                  ZN_method = label_ZN
               endif




               ZN_F1_F2 = 0.d0
               ZN_F1F2 = 0.d0

               do k = 1, n_atom
                  do l = 1, 3
                     
                     ZN_F1_F2 = ZN_F1_F2 + (1/mass(k))*(ZN_F1(k,l) - ZN_F2(k,l))**2                  
                     ZN_F1F2 = ZN_F1F2 + (1/mass(k))*ZN_F1(k,l)*ZN_F2(k,l) 

                  enddo
               enddo

               tmp_ZN_F1F2 = ZN_F1F2

               ZN_F1_F2 = sqrt(ZN_F1_F2)
               ZN_F1F2 = sqrt(abs(ZN_F1F2))
 

               
               ZN_V12 = abs(pes_zn2(i) - pes_zn2(j)) / 2


               do k = 1, n_atom

                  ZN_PS(k) = 0.d0

                  do l = 1, 3
                     ZN_PS(k) = ZN_PS(k) + vel_zn2(k,l)* ZN_S_NORM(k,l)*mass(k)
                  enddo

                  do l = 1, 3
                     ZN_P_PAL(k,l) = ZN_PS(k) * ZN_S_NORM(k,l)
                     ZN_V_PAL(i,j,k,l) = ZN_P_PAL(k,l)
                     ZN_P_PER(k,l) = vel_zn2(k,l)*mass(k) - ZN_P_PAL(k,l)
                     ZN_V_PER(i,j,k,l) = ZN_P_PER(k,l)
                  enddo

               enddo

               do k = 1, n_atom
                  do l = 1, 3
                     ZN_EK_PAL(i,j) = ZN_EK_PAL(i,j) + ZN_P_PAL(k,l)**2 / (2*mass(k))
                     ZN_EK_PER(i,j) = ZN_EK_PER(i,j) + ZN_P_PER(k,l)**2 / (2*mass(k))
                  enddo
               enddo

               ZN_ET = pes_zn2(i)

               do k = 1, n_atom
                  do l = 1, 3
                     ZN_ET = ZN_ET + ZN_P_PAL(k,l)**2 / (2.d0 * mass(k))
                  enddo
               enddo

               

               ZN_EX = (pes_zn2(i) + pes_zn2(j)) / 2.d0

               if (ZN_method .eq. 1) then
                  ZN_a2  = ZN_F1_F2**2 / (16.d0 * ZN_V12**3)
                  ZN_b2 = (ZN_ET - ZN_EX) / (2*ZN_V12)
               else
                  ZN_a2  = ZN_F1_F2 * ZN_F1F2 / (16.d0 * ZN_V12**3)
                  ZN_b2 = (ZN_ET - ZN_EX) * ZN_F1_F2 / (ZN_F1F2*2*ZN_V12)

               endif

               
               if (tmp_ZN_F1F2 .gt. 0.d0 ) then           

                  pro_hop(j) = exp(-pi / (4 * sqrt(ZN_a2)) * sqrt(2 / (ZN_b2 + sqrt(ZN_b2**2 + 1))))
               else
                  pro_hop(j) = exp(-pi / (4 * sqrt(ZN_a2)) * sqrt(2 / (ZN_b2 + sqrt(ZN_b2**2 - 1))))

               endif

               if ( ZN_a2 .lt. 0.001) then
                  pro_hop(j) = 0.d0
               endif

               if ( ZN_a2 .gt. 1000) then
                  pro_hop(j) = 1.d0
               endif

            endif

         endif
          
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

      write (file_save_ele, 9996) it, it*dtime*TOFS, &
                            "The current state", index_state
      write (file_save_ele, 9997) it, it*dtime*TOFS, &
                            "Hopping probability", pro_hop(:)
      write (file_save_ele, 9997) it, it*dtime*TOFS, &
                             "Area for hopping", pro_sum(:)



!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

!       generate random number
!       the init_random_seed may be set before the dynamic cycle.
        call get_random_number(num_random)
        call get_random_number(num_random)

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
        


7000    write (file_save_ele, 9997) it, it*dtime*TOFS, &
                              "Random number",  num_random
        write (file_save_ele, 9996) it, it*dtime*TOFS, &
                              "The new state", index_state
        write (file_save_ele, * ) "------------------------------------"

        new_index_state = index_state

!       Reject all hops when the energy gap is large than hop_e if necessary

         if (  label_reject_hops .ne. 0 ) then
            if (old_index_state .ne. new_index_state) then
               if ( abs( old_pes_all(old_index_state) - old_pes_all(new_index_state) )  &
                    .ge.  &
                    (hop_e/TOEV) &
                  )  then
                   write (file_md_out, *)  "energy gap is larger than hop_e, hop is rejected"
                   index_state = old_index_state
                   new_index_state = old_index_state
               endif
            endif
         endif

         if (old_index_state .ne. new_index_state) then

               write (file_md_out, *)  "Possible hop happens at Step", &
                                       it
               write (file_md_out, *)  md_state(old_index_state), &
                                       "-->", &
                                       md_state(new_index_state)
!!!! velocity_scaling
               ZN_E_HOP = old_pes_all(old_index_state) + ZN_EK_PAL(old_index_state, new_index_state) - old_pes_all(new_index_state)
               ZN_DELTA_E = old_pes_all(old_index_state) - old_pes_all(new_index_state)

               if (ZN_E_HOP .lt. 0.d0) then
                  write (file_md_out, *)  "kinetic energy is smaller than then energy gap, hop is rejected"
                  index_state = old_index_state
                  new_index_state = old_index_state
               else
                    write (file_md_out,*)  "Check the velocity adjustment"
                    write (file_md_out,*)  "Old velocity"
                    do k=1,n_atom
                        write (file_md_out,9998) k, old_vel_x(k), old_vel_y(k), old_vel_z(k)
                    enddo



                  ZN_K_SCAL = sqrt(1.d0 + ZN_DELTA_E/ZN_EK_PAL(old_index_state, new_index_state))

                  write (*,*) "ZN_DELTA_E", ZN_DELTA_E

                  write (*,*) "ZN_K_PAL", ZN_EK_PAL(old_index_state, new_index_state)
                  write (*,*) "ZN_K_SCAL", ZN_K_SCAL

                  do k =1, n_atom

                     old_vel_x(k) = ( ZN_V_PER(old_index_state,new_index_state,k,1) + &
                     ZN_K_SCAL * ZN_V_PAL(old_index_state,new_index_state,k,1)) / mass (k)

                     old_vel_y(k) = ( ZN_V_PER(old_index_state,new_index_state,k,2) + &
                     ZN_K_SCAL * ZN_V_PAL(old_index_state,new_index_state,k,2)) / mass (k)

                     old_vel_z(k) = ( ZN_V_PER(old_index_state,new_index_state,k,3) + &
                     ZN_K_SCAL * ZN_V_PAL(old_index_state,new_index_state,k,3)) / mass (k)
                  enddo

                  write (file_md_out,*)  "New velocity"
                  do k=1,n_atom
                      write (file_md_out,9998) k, old_vel_x(k), old_vel_y(k), old_vel_z(k)
                  enddo

               endif
       


          endif



9995   format(i10, 1x, 3(f15.8, 3x))
9996   format(i10, 1x, f15.8, 3x, a, 1x, i3)
9997   format(i10, 1x, f15.8, 3x, a, 1x, 10(f15.8, 1x))
9998  format(i7, 1x, 3(f20.10, 1x))
9999   format(i10, 1x, f15.8, 3x, a, 1x, i3, 1x, i3, 1x, f10.7, a, f10.7)

  
  end 
