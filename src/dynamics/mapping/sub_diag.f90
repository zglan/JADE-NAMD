subroutine sub_diag(n, mat_nondiag, mat_U, eig)
implicit none
! --- arguments ---
integer n
real(kind=8), dimension(n,n) :: mat_nondiag, mat_U
real(kind=8), dimension(n) :: eig
!complex(kind=8), dimension(n, n) :: mat_U

! --- local variables ---
real(kind=8), allocatable, dimension(:) :: work
!complex(kind=8), allocatable, dimension(:,:) :: rwork
integer lwork, info

!lwork= n*(n+1)
lwork= 3*n
allocate (work(lwork))
!allocate (rwork(3*n-2,3*n-2))

mat_U = mat_nondiag

!call ZHEEV('V','U', n, mat_U, n, &
!           E_adia, work, lwork, rwork, info)
call DSYEV('V','U', n, mat_U, n, &
           eig, work, lwork, info)


9998  format(10(f20.10, 1x))
9999 format(i8,1x,999(f20.10, 1x))
return
end
