subroutine sub_elec_get_dH_div_dx_or_dp_aver_PES(n_state, Ham, x_elec, dH_div_dx)
implicit none
! --- arguments ---
integer n_state
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_state) :: x_elec
real(kind=8), dimension(n_state) :: dH_div_dx

! --- local variables ---
integer i,j
real(kind=8) H_diag_aver

H_diag_aver = 0.d0
do i = 1, n_state
  H_diag_aver = H_diag_aver + Ham(i,i)
enddo
H_diag_aver = H_diag_aver / dble(n_state)

dH_div_dx = 0.d0
do i = 1, n_state
  do j = 1, n_state
    dH_div_dx(i) = dH_div_dx(i) + Ham(i,j) * x_elec(j)
  enddo
  dH_div_dx(i) = dH_div_dx(i) - H_diag_aver * x_elec(i)
enddo

return
end
