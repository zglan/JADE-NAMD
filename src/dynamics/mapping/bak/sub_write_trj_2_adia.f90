subroutine sub_write_trj_2_adia(i_step, &
                         x_elec, p_elec, &
                         x_nuc, p_nuc, &
                         mat_U)
use mod_main
implicit none
! --- arguments ---
integer i_step
real(kind=8), dimension(n_state) :: x_elec, p_elec
real(kind=8), dimension(n_mode) :: x_nuc, p_nuc
real(kind=8) mat_U(n_state,n_state)

! --- local variables ---
real(kind=8), dimension(n_state) :: pop_dia, &
                                    pop_adia
real(kind=8),dimension(n_state, n_state) :: mat_pop_dia, &
                                            mat_pop_adia
integer f_trj
integer f_trj_restart
integer f_trj_elec
integer f_trj_elec_debug
integer f_trj_elec_restart
integer f_ene
integer f_pop_dia
integer f_pop_adia
integer f_x_sq_add_p_sq
integer f_ham
integer i, j, i_state

f_trj = 10
f_trj_restart = 11
f_trj_elec = 12
f_trj_elec_restart = 13
f_ene = 14
f_pop_dia = 15
f_pop_adia = 16
f_x_sq_add_p_sq = 17
f_ham = 18
f_trj_elec_debug = 19


do i = 1, n_state
  mat_pop_adia(i,i) = 0.5 * ( x_elec(i)**2 + p_elec(i)**2 - ggamma)
enddo

do i = 1, n_state-1
  do j = i+1, n_state
    mat_pop_adia(i,j) = 0.5 * ( x_elec(i) * x_elec(j) + p_elec(i) * p_elec(j) )
    mat_pop_adia(j,i) = mat_pop_adia(i,j)
  enddo
enddo

if(label_debug > 1) then
  write(*,*) 'sub_write_trj_2_adia'
  write(*,*) 'x_elec, p_elec, pop_adia'
  do i = 1, n_state
    write(*,*) x_elec(i), p_elec(i), mat_pop_adia(i,i)
  enddo
  write(*,*)
endif
mat_pop_dia = matmul(transpose(mat_U), mat_pop_adia)
mat_pop_dia = matmul(mat_pop_dia, mat_U)

do i = 1, n_state
  pop_dia(i) = mat_pop_dia(i,i)
  pop_adia(i) = mat_pop_adia(i,i)
enddo

if (i_step .eq. 0) then
  if(label_debug >= 1) then
    open(f_trj, file='trj.dat')
  endif
  open(f_trj_elec, file='trj_elec.dat')
  open(f_pop_dia, file='pop_dia.dat')
  open(f_pop_adia, file='pop_adia.dat')
else
  if(label_debug >= 1) then
    open(f_trj, position='append', file='trj.dat')
  endif
  open(f_trj_elec, position='append', file='trj_elec.dat')
  open(f_pop_dia, position='append', file='pop_dia.dat')
  open(f_pop_adia, position='append', file='pop_adia.dat')
endif

do i = 1, n_state
  write(f_trj_elec, 9999) i_step, x_elec(i), p_elec(i)
enddo
write(f_pop_dia, 9999) i_step, pop_dia(:)
write(f_pop_adia, 9999) i_step, pop_adia(:)
do i = 1, n_mode
  write(f_trj, 9999) i_step, x_nuc(i), p_nuc(i)
enddo

close(f_trj_elec)
close(f_pop_dia)
close(f_pop_adia)
if(label_debug >= 1) then
  close(f_trj)
endif

9998  format(10(f20.10, 1x))
9999 format(i8,1x,999(f20.10, 1x))

return
end
