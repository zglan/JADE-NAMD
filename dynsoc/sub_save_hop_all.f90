      subroutine  sub_save_hop_all (n_atom, n_state, md_state, &
                                it,time, &
                                index_state, &
                                pes_all, &
                                nac_time, &
                                soc_time, &
                                rho, &
                                file_save_all)

 
      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, it
      integer, intent(in) :: n_state, index_state
      integer, intent(in) :: file_save_all
      double precision, intent(in) :: time
 
      double precision, intent(in), dimension(n_state, n_state) ::   &
                                                nac_time, soc_time
      complex (kind=8), dimension(n_state, n_state) :: rho


      double precision,  intent(in), dimension(n_state) :: pes_all
      integer,  intent(in), dimension(n_state) :: md_state


!!!!!!  Local variables

      integer ::  i, j, k
      double precision :: vel_norm
      double precision :: gra_all_norm
      double precision :: nac_time_norm
      double precision, allocatable, dimension(:) :: pop_norm
       
       allocate ( pop_norm (n_state))

       do i=1, n_state
          pop_norm(i) = rho(i,i)
       enddo


        write (file_save_all, * ) "------------------------------------"
        write (file_save_all, 9997) it, time*TOFS, &
                              "current state", md_state(index_state)
        write (file_save_all, 9999) it, time*TOFS, &
                              "Potential energy", pes_all(:)
        write (file_save_all, 9999) it, time*TOFS, &
                              "Current potential energy", pes_all(index_state)
        write (file_save_all, 9999) it, time*TOFS, &
                             "<psi_i| d/dt | psi_j>", nac_time(:,:)    
        write (file_save_all, 9999) it, time*TOFS, &
                             "<psi_i| Hsoc | psi_j>", soc_time(:,:)   
        write (file_save_all, 9999) it, time*TOFS, &
                              "population", pop_norm(:) 
        write (file_save_all, * ) "------------------------------------"
      
9997   format(i10, 1x, f15.8, 3x, a, 1x, i3)
9999   format(i10, 1x, f15.8, 3x, a, 1x, 100(f20.10, 1x))


       deallocate (pop_norm)


       return
 
       end 
