subroutine sub_elec_get_dH_div_dx_or_dp_3(n_state, Ham, x_elec, dH_div_dx)
implicit none
! --- arguments ---
integer n_state
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_state) :: x_elec
real(kind=8), dimension(n_state) :: dH_div_dx

! --- local variables ---
integer i,j

dH_div_dx = 0.d0
do i = 1, n_state
  do j = 1, n_state
    if (i==j) then
      dH_div_dx(i) = dH_div_dx(i) + 0.5 * Ham(i,j) * x_elec(j)
    else
      dH_div_dx(i) = dH_div_dx(i) +  Ham(i,j) * x_elec(j)
    endif
  enddo
enddo

return
end
