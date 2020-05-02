subroutine sub_write(natom, xyz1, mat_rotate, xyz2_c, xyz)

implicit none

! ----- Parameters -----
!include 'param.def'

! ----- argument -----
integer natom
real(kind=8) xyz1(3,natom)
real(kind=8) xyz2_c(3)
real(kind=8) mat_rotate(3,3)

! ----- Local variables -----
integer i, j
real(kind=8) xyz(3,natom)

!rotated_xyzfile="rotate.xyz"
!mat_rotate_file="mat_rotate.xyz"

xyz=xyz1

xyz = matmul(mat_rotate, xyz)

xyz1 = xyz

do i=1, natom
  do j=1, 3
    xyz(j,i) = xyz(j,i) + xyz2_c(j)
  enddo
enddo



return
end
