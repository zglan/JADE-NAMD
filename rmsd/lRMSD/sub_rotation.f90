subroutine sub_rotation(natom, xyz1, xyz2, mat_rotate)
implicit none
! ----- argument -----
integer, intent(in):: natom
real(kind=8) xyz1(3,natom), xyz2(3,natom)
real(kind=8) mat_rotate(3,3)

! ----- Local variables -----
integer i, j, n
real(kind=8) :: mat_C(3,3)
real(kind=8) :: d

real(kind=8) :: mat_A(3,3)
integer ::  LDA, LDU, LDVT, LWORK, INFO
real(kind=8) :: arr_S(3)
real(kind=8) :: mat_S(3,3)
real(kind=8) :: mat_U(3,3)
real(kind=8) :: mat_VT(3,3)
real(kind=8), allocatable :: WORK(:)
integer, allocatable :: IWORK(:)

real(kind=8) det_C
integer output_level

output_level=0

mat_C = matmul(xyz1, transpose(xyz2))
mat_A = mat_C

!write(*,*)
!write(*,*)"mat_C:"
!do i=1,3
!  write(*,*)mat_C(i,:)
!enddo


n=3
LDA=3
LDU=3
LDVT=3
LWORK=3*(6+4*3)+3+5
allocate( WORK(LWORK) )
allocate( IWORK(8*3) )


call dgesdd('A', n, n, mat_A, LDA, arr_S, mat_U, LDU, mat_VT, LDVT, WORK, LWORK, IWORK, INFO)

mat_S = 0.d0
do i=1,3
  mat_S(i,i) = arr_S(i)
enddo

mat_A = matmul(mat_U, mat_S)
mat_A = matmul(mat_A, mat_VT)


!write(*,*)
!write(*,*)"mat_C recalculated:"
!do i=1,3
!  write(*,*)mat_A(i,:)
!enddo
deallocate( WORK )
deallocate( IWORK )

call sub_determinant(mat_C, n, det_C, output_level)

d = sign(1.d0,det_C)

mat_A = 0.d0
mat_A(1,1) = 1.d0
mat_A(2,2) = 1.d0
mat_A(3,3) = d

mat_rotate = matmul(transpose(mat_VT), mat_A)
mat_rotate = matmul(mat_rotate, transpose(mat_U))

return
end
