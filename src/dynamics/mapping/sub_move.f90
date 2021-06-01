subroutine sub_move(n, X, delt_X, dt)
implicit none
! --- arguments ---
integer n
real(kind=8), dimension(n) :: X, delt_X
real(kind=8) dt

X = X + delt_X * dt

return
end
