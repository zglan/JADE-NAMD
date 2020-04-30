      subroutine  sub_mndo_many   (n_atom, &
                               n_state, &
                               md_state, &
                               atom_label, &
                               coor_x, coor_y, coor_z, &
                               file_md_out)
 

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, n_state
      integer, intent(in) :: file_md_out
      integer, intent(in), dimension(n_state) :: md_state(n_state)
      character*2, intent(in), dimension(n_atom)  ::  atom_label
      double precision, intent(in), dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z



      

      double precision,  dimension(n_state) :: pes_all
      double precision,  dimension(n_state, n_atom) ::   &
                                         gra_all_x, &
                                         gra_all_y, &
                                         gra_all_z
      double precision,  dimension(n_state, n_state, n_atom) ::   &
                                                       nac_x, &
                                                       nac_y, &
                                                       nac_z




!     Local variables

      integer  ::  i, i_state, j_state, k, j
      integer  ::  file_qm_in, file_mndo_in, file_mndo_out

      integer,  dimension(n_atom) :: charge

      character*100   line 
      character*47    line_energy

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
       double precision :: tmp_mass
       integer          :: tmp_charge
       character*2      :: tmp_label

       double precision :: tmp_read_1,  tmp_read_2,  &
                           tmp_read_3,  tmp_read_4, &
                           tmp_read_5

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



  



       write (file_md_out, *)  "Write the MNDO input"

       
     
       file_mndo_in=31
       open(unit=file_mndo_in, file="mn.in")


!      Construct the beginning part of MNDO input
       file_qm_in=32
       open(unit=file_qm_in, file="qm_input.in")                
       do while (.TRUE.) 
         read (file_qm_in, 8001, end=8999) line   
         if (line(1:10) .eq.  "----------"  ) then
           goto 8999 
         endif
!         write (*,8001) line
         write (file_mndo_in, 8001) line 
       enddo
8999   close (file_qm_in)


!      Leave two lines empty (Requirement of MNDO)      
       write (file_mndo_in,*) "Number of atom", n_atom  
       write (file_mndo_in,*)  


!      Get the charge
       do i=1,n_atom
          tmp_label = atom_label(i)
          call sub_get_mass ( tmp_label, tmp_mass, tmp_charge)
          charge(i) = tmp_charge
       enddo

!      Construct the coordinates             


       do i=1,n_atom
         write (file_mndo_in, 8002)  charge(i),  &
                         coor_x(i)*BOHRTOANG, 1,    &
                         coor_y(i)*BOHRTOANG, 1,    &
                         coor_z(i)*BOHRTOANG, 1
       enddo
   


       write (file_mndo_in, 8002)  0,  &
                         0.0, 0,    &
                         0.0, 0,    &
                         0.0, 0

     

8001   format(a100)
8002   format(i3, 1x 3(f20.10, 1x, i1, 1x)) 



!      Add the end part of MNDO

       file_qm_in=32
       open(unit=file_qm_in, file="qm_input.in")
       do while (.TRUE.)
         read (file_qm_in, 8001, end=8998) line
         if (line(1:10) .eq.  "----------"  ) then
           do while (.TRUE.)
              read (file_qm_in, 8001, end=8998) line
              write (file_mndo_in,8001) line
           enddo 
         endif
       enddo
       
       



8998   close (file_qm_in)



       close(file_mndo_in)




       call system ("rm  mn.out")
       write (file_md_out, *)  "Run MNDO calculations"
       call system ("mndo99  < mn.in > mn.out")

  

       write (file_md_out, *)  "Get MNDO results"


       gra_all_x = 0.d0
       gra_all_y = 0.d0
       gra_all_z = 0.d0
       nac_x     = 0.d0
       nac_y     = 0.d0
       nac_z     = 0.d0
       pes_all   = 0.d0
    



!      Read the MNDO gradient
      
       i_state = 1  
       file_mndo_out=33
       open(unit=file_mndo_out, file="mn.out")
       do while (.TRUE.)
         read (file_mndo_out, 8001, end=8997) line
         if ( (line(27:48) .eq. "COORDINATES (ANGSTROM)") &
              .and.                                          &
              (line(64:94) .eq. "GRADIENTS (KCAL/(MOL*ANGSTROM))")  &
            )  then
            write (file_md_out,*) "Read gradient !!!"
            read (file_mndo_out, *)
            read (file_mndo_out, *)
            read (file_mndo_out, *)
            do k=1,n_atom
               read (file_mndo_out, *)  tmp_read_1, tmp_read_2, &
                                        tmp_read_3, tmp_read_4, &
                                        tmp_read_5,             &
                                        gra_all_x(i_state, k),  &
                                        gra_all_y(i_state, k),  &
                                        gra_all_z(i_state, k)
            enddo
            i_state = i_state  + 1 
         endif
         if (i_state .eq. (n_state+1)) then
            goto 8997
         endif
       enddo



8997   if (i_state .eq. (n_state+1)) then
          write (file_md_out,*) "Read gradient successfully!!!"
       else
          write (file_md_out,*) "Do not read gradient successfully!!!"
          write (file_md_out,*) "Check the MNDO output"
       endif
       




         i_state = 1
         j_state = i_state + 1
         do while (.TRUE.)
            read (file_mndo_out, 8001, end=8996) line
            if ( (line(27:48) .eq. "COORDINATES (ANGSTROM)") &
                  .and.                                          &
                (line(64:94) .eq. "GRADIENTS (KCAL/(MOL*ANGSTROM))")  &
               )  then
                 write (file_md_out,*) "Read nonadiabatic_couplings !!!"
                 read (file_mndo_out, *)
                 read (file_mndo_out, *)
                 read (file_mndo_out, *)
                 do k=1,n_atom
                    read (file_mndo_out, *)  tmp_read_1, tmp_read_2, &
                                             tmp_read_3, tmp_read_4, &
                                             tmp_read_5,             &
                                        nac_x(i_state, j_state, k),  &
                                        nac_y(i_state, j_state, k),  &
                                        nac_z(i_state, j_state, k)
              
!              print *, i_state, j_state, k  
!              print *, nac_x(i_state, j_state, k)
!              print *, nac_y(i_state, j_state, k)
!              print *, nac_z(i_state, j_state, k)

                enddo
                j_state = j_state  + 1
                if (j_state  .eq. (n_state+1)) then
                    i_state = i_state + 1
                    j_state = i_state + 1              
                endif
            endif
            if ( i_state .eq. (n_state) ) then
               goto 8996
            endif
         enddo



8996    if (i_state .eq. (n_state)) then
          write (file_md_out,*) &
          "Read nonadiabatic couplings successfully!!!"
       else
          write (file_md_out,*) &
          "Do not read nonadiabatic couplings successfully!!!"
          write (file_md_out,*) "Check the MNDO output"
          STOP
       endif


       close (file_mndo_out)
 
       

       
       
       do i_state = 1, n_state
       do j_state = 1, i_state
           nac_x(i_state, j_state, :) = - nac_x(j_state, i_state, :)
           nac_y(i_state, j_state, :) = - nac_y(j_state, i_state, :)
           nac_z(i_state, j_state, :) = - nac_z(j_state, i_state, :)
       enddo
       enddo
 
       


       gra_all_x=gra_all_x*KCANGTOEV/(TOEV*ANSTOBOHR)
       gra_all_y=gra_all_y*KCANGTOEV/(TOEV*ANSTOBOHR)
       gra_all_z=gra_all_z*KCANGTOEV/(TOEV*ANSTOBOHR)


!       do i_state = 1, n_state
!       do j_state = 1, n_state
!       do k= 1, n_atom
!          print *, i_state, j_state, k
!          print *, nac_x(i_state, j_state, k)
!          print *, nac_y(i_state, j_state, k)
!          print *, nac_z(i_state, j_state, k)
!       enddo
!       enddo
!       enddo

       nac_x = nac_x/ ANSTOBOHR
       nac_y = nac_y/ ANSTOBOHR
       nac_z = nac_z/ ANSTOBOHR
       


!      Read the MNDO PES


       pes_all=0.0
       file_mndo_out=33
       i_state = 1
       open(unit=file_mndo_out, file="mn.out")
       do while (.TRUE.)
         read (file_mndo_out, 8001, end=8995) line
         if (line(2:36) .eq.  "SUMMARY OF MULTIPLE CI CALCULATIONS"  ) then
            read (file_mndo_out, *)
            read (file_mndo_out, *)
            read (file_mndo_out, *)
            read (file_mndo_out, *)
            do i =1, n_state  
            read (file_mndo_out, *)  tmp_read_1, tmp_read_2, &
                                        pes_all(i)
            enddo 
            if (i .eq. (n_state+1)) then 
                goto 8995
            endif
         endif
       enddo

8995   if (i .eq. (n_state+1)) then
          write (file_md_out,*) &
          "Read energies successfully!!!"
       else
          write (file_md_out,*) &
          "Do not read energies successfully!!!"
          write (file_md_out,*) "Check the MNDO output"
          STOP
       endif


       close (file_mndo_out)
       
       pes_all(:)=pes_all(:)*KCANGTOEV/TOEV   



        open(unit=101, file="qm_results.dat")
        write (101,*) n_atom
        write (101,*) "The coordinates"
        do i=1,n_atom
           write (101, 9999)  atom_label(i),  &
                          coor_x(i),      &
                          coor_y(i),      &
                          coor_z(i)
        enddo
        write (101,*) "Energy of electronic states"

        do j=1,n_state
           write (101, *) pes_all(j)
        enddo

        Write (101,*)  "Gradient of electronic states"
        do j=1,n_state
           write (101,*) "State:", j
           do i=1,n_atom
              write (101, *)    &
                             gra_all_x(j,i),      &
                             gra_all_y(j,i),      &
                             gra_all_z(j,i)
           enddo
        enddo

        write (101,*) "Nonadiabatic couplings"
        do j=1, n_state
           do k=1, n_state
               write (101,*) "State:", j, k
               do i=1,n_atom
                  write (101, *)   &
                             nac_x(j,k,i),      &
                             nac_y(j,k,i),      &
                             nac_z(j,k,i)
               enddo
           enddo
        enddo

       close(101)
9999   format(a, 1x, 3(f20.10, 1x))


       return
 
       end 
