subroutine sub_rmsd(natom, xyz1, xyz2, rmsd)
implicit none
! ----- argument -----
integer, intent(in):: natom
real(kind=8) xyz1(3,natom), xyz2(3,natom)
real(kind=8) rmsd

! ----- Local variables -----
integer i,j
real(kind=8) ssum


ssum = 0.d0

do i = 1, natom
  do j = 1, 3
    ssum = ssum + (xyz1(j, i) - xyz2(j, i))**2
  enddo
enddo

ssum = ssum/real(natom)
ssum = sqrt(ssum)

rmsd = ssum

return
end
