      subroutine  sub_save_grad (n_atom, nstate, index_state, &
                                gra_all_x, &
                                gra_all_y, &
                                gra_all_z, &
                                atom_label, &
                                it, time, &
                                file_save_grad )

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it, nstate, index_state
      integer, intent(in) :: file_save_grad
      double precision, intent(in) :: time
      double precision, intent(in), dimension(nstate,n_atom) ::   &
                                                gra_all_x, &
                                                gra_all_y, &
                                                gra_all_z
                                                
      character*2, intent(in), dimension(n_atom)  ::  atom_label

      integer ::  i,j
     
      do j=1, nstate
      write (file_save_grad, *) n_atom

      write (file_save_grad, 9998)  "AU", "Step:", it, "State:", j, &
                                     "Time:", time

      do  i=1, n_atom  
          write (file_save_grad, 9999) atom_label(i), &
                                       gra_all_x(j,i), &
                                       gra_all_y(j,i), &
                                       gra_all_z(j,i)
      enddo
      enddo


9999   format(a, 1x, 3(f20.10, 1x))
9998   format(a, 1x, a,  1x, i10, 1x, a, 1x, i10, 1x, a, f20.10)

       return
 
       end 

