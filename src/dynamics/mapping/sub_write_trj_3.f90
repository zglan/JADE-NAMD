subroutine sub_write_trj_3(i_step, &
                           x_cur, p_cur, &
                           x_elec, y_elec, &
                           p_x_elec, p_y_elec, &
                           Ham)
use mod_main, only : n_mode, n_state, ggamma, label_debug
implicit none
! --- arguments ---
integer i_step
real(kind=8), dimension(n_mode) :: x_cur, p_cur
real(kind=8), dimension(n_state) :: x_elec, y_elec
real(kind=8), dimension(n_state) :: p_x_elec, p_y_elec
real(kind=8), dimension(n_state, n_state) :: Ham

! --- local variables ---
real(kind=8), dimension(n_state) :: E_adia, &
                                    pop_dia, &
                                    pop_adia
!complex(kind=8), dimension(n_state, n_state) :: mat_U
real(kind=8), dimension(n_mode) :: x_sq_add_p_sq
real(kind=8), dimension(n_state, n_state) :: mat_U
real(kind=8),dimension(n_state, n_state) :: Ham_adia, &
                                            mat_tmp, &
                                            mat_pop_dia, &
                                            mat_pop_adia
real(kind=8), allocatable, dimension(:) :: work
!complex(kind=8), allocatable, dimension(:,:) :: rwork
integer lwork, info
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
integer i, j


!lwork= n_state*(n_state+1)
lwork= 3*n_state
allocate (work(lwork))
!allocate (rwork(3*n_state-2,3*n_state-2))

mat_U = Ham

!call ZHEEV('V','U', n_state, mat_U, n_state, &
!           E_adia, work, lwork, rwork, info)
call DSYEV('V','U', n_state, mat_U, n_state, &
           E_adia, work, lwork, info)

Ham_adia = 0.d0
do i=1,n_state
  Ham_adia(i,i) = E_adia(i)
enddo

!test
!mat_tmp = matmul( mat_U, Ham_adia)
!mat_tmp = matmul(mat_tmp, transpose(mat_U) )
!write(*,*) i_step
!write(*,*) Ham
!write(*,*) mat_tmp
do i = 1, n_state
  call sub_sum_sq_sum_by4(x_elec(i), &
                            p_y_elec(i), &
                            y_elec(i), &
                            p_x_elec(i), &
                            mat_pop_dia(i,i))
enddo

do i = 1, n_state-1
  do j = i+1, n_state
    mat_pop_dia(i,j) = x_elec(i) * p_y_elec(j) - y_elec(i) * p_x_elec(j)
  enddo
enddo

mat_pop_adia = matmul(transpose(mat_U), mat_pop_dia)
mat_pop_adia = matmul(mat_pop_adia, mat_U)

do i = 1, n_state
  pop_dia(i) = mat_pop_dia(i,i)
  pop_adia(i) = mat_pop_adia(i,i)
enddo


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

open(f_trj_restart, file='trj_restart.input')
open(f_trj_elec_restart, file='trj_elec_restart.input')

if (i_step .eq. 0) then
  if (label_debug >= 2 ) then
    open(f_trj, file='trj.dat')
    open(f_ham, file='ham.dat')
    open(f_x_sq_add_p_sq, file='x_sq_add_p_sq.dat')
    open(f_trj_elec_debug, file='trj_elec_debug.dat')
  endif
  open(f_trj_elec, file='trj_elec.dat')
  open(f_pop_dia, file='pop_dia.dat')
  open(f_pop_adia, file='pop_adia.dat')
!  open(f_ene, file='energy.dat')
else
  if (label_debug >= 2 ) then
    open(f_trj, position='append', file='trj.dat')
    open(f_ham, position='append', file='ham.dat')
    open(f_x_sq_add_p_sq, position='append', file='x_sq_add_p_sq.dat')
    open(f_trj_elec_debug, position='append', file='trj_elec_debug.dat')
  endif
  open(f_trj_elec, position='append', file='trj_elec.dat')
  open(f_pop_dia, position='append', file='pop_dia.dat')
  open(f_pop_adia, position='append', file='pop_adia.dat')
!  open(f_ene, position='append', file='energy.dat')
endif

if (label_debug >= 2 ) then
  write(f_trj, 9999) i_step, x_cur(:), p_cur(:)
  write(f_trj_elec_debug, 9999) i_step, x_elec(:), y_elec(:), p_x_elec(:), p_y_elec(:)
  x_sq_add_p_sq = x_cur**2 + p_cur**2
  write(f_x_sq_add_p_sq, 9999) i_step, x_sq_add_p_sq(:)
!  write(f_ham, *) i_step
  do i = 1, n_state
    write(f_ham, 9999) i_step, Ham(i,:)
  enddo
endif
do i = 1, n_mode
!  write(f_trj, 9999) i_step, x_cur(i), p_cur(i)
  write(f_trj_restart, 9998) x_cur(i), p_cur(i)
enddo

!open(20, file= 'x_p.dat', access='append')

!write(20, 9999) i_step, x_cur(:), p_cur(:)
!close(20)

write(f_pop_dia, 9999) i_step, pop_dia(:)
write(f_pop_adia, 9999) i_step, pop_adia(:)

do i = 1, n_state
  write(f_trj_elec_restart, 9998) x_elec(i), y_elec(i), p_x_elec(i), p_y_elec(i)
  write(f_trj_elec, 9999) i_step, x_elec(i), y_elec(i), p_x_elec(i), p_y_elec(i)
enddo

close(f_trj_restart)
close(f_trj_elec)
close(f_trj_elec_restart)
close(f_pop_dia)
close(f_pop_adia)
!close(f_ene)
if (label_debug >= 2 ) then
  close(f_trj)
  close(f_x_sq_add_p_sq)
  close(f_ham)
endif



9998  format(10(f20.10, 1x))
9999 format(i8,1x,999(f20.10, 1x))
return
end
