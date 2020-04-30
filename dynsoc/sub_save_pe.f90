      subroutine   sub_save_pe (  it,time, &
                              n_state, &
                              index_state, &
                              pes_all, &
                              file_save_pe )


      implicit none
      include 'param.def'

      integer, intent(in) :: it, n_state, index_state
      integer, intent(in) :: file_save_pe
      double precision, intent(in) :: time
 
      double precision, intent(in), dimension(n_state) ::   &
                                                      pes_all    


!!!!!!  Local variables

       write (file_save_pe, 9999) it, time*TOFS, &
                                      pes_all(:), &
                                      pes_all(index_state)




9999   format(i10, 1x, 20(f20.10, 1x))

       return
 
       end subroutine sub_save_pe
