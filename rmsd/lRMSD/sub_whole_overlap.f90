subroutine sub_whole_overlap(natom, xyz1_org, xyz2_org, &
                              rmsd)

implicit none
! ----- argument -----
integer natom
real(kind=8) xyz1_org(3,natom), xyz2_org(3,natom)
!f2py intent(inplace) xyz2_org
real(kind=8) rmsd(1)
!real(kind=8), intent(out) :: xyz2_rotate(3,natom)

! ----- Local variables -----
real(kind=8) xyz1(3,natom), xyz2(3,natom)
real(kind=8) xyz1_c(3), xyz2_c(3)
real(kind=8) mat_rotate(3,3)
integer i


xyz2 = xyz1_org
xyz1 = xyz2_org

call sub_translation(natom, xyz1, xyz1_c)
!write(*,*) "sub_translation done."

call sub_translation(natom, xyz2, xyz2_c)

!write(*,*)
!write(*,*)"translated xyz1:"
!do i=1, natom
!  write(*,*)xyz1(:,i)
!enddo

!write(*,*)
!write(*,*)"translated xyz2:"
!do i=1, natom
!  write(*,*)xyz2(:,i)
!enddo

call sub_rotation(natom, xyz1, xyz2, mat_rotate)
call sub_write(natom, xyz1, mat_rotate, xyz2_c, xyz2_org)
call sub_rmsd(natom, xyz1, xyz2, rmsd)


!write(*,*) xyz2_org

!write(*,*) 'rmsd:', rmsd
return
end
