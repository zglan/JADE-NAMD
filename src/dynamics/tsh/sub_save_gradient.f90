      subroutine  sub_save_gradient (n_atom, &
                                gradient_x, &
                                gradient_y, &
                                gradient_z, &
                                atom_label, &
                                it, time, &
                                file_save_grad )

      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: file_save_grad
      double precision, intent(in) :: time
      double precision, intent(in), dimension(n_atom) ::   &
                                                gradient_x, &
                                                gradient_y, &
                                                gradient_z

      character*2, intent(in), dimension(n_atom)  ::  atom_label

      integer ::  i

      write (file_save_grad, *) n_atom

      write (file_save_grad, 9998)  "AU", "Step:", it, "Time:", time


      do  i=1, n_atom
          write (file_save_grad, 9999) atom_label(i), &
                                       gradient_x(i), &
                                       gradient_y(i), &
                                       gradient_z(i)
      enddo


9999   format(a, 1x, 3(f20.10, 1x))
9998   format(a,  1x, a, 1x, i10, 1x, a, f20.10)

       return

       end
