subroutine sub_translation(natom, xyz, xyz_c)
implicit none
! ----- argument -----
integer natom
real(kind=8) xyz(3,natom)
real(kind=8) xyz_c(3)

! ----- Local variables -----
integer i, j

xyz_c=0.d0
!write(*,*) "centroid:"
do j=1, 3
  do i=1, natom
    xyz_c(j) = xyz_c(j) + xyz(j,i)
  enddo
  xyz_c(j) = xyz_c(j)/dble(natom)
!  write(*,*)xyz_c(j)
enddo

do i=1, natom
  do j=1, 3
    xyz(j,i) = xyz(j,i) - xyz_c(j)
  enddo
enddo


return
end
