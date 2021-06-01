subroutine sub_p_kin_to_p(p_nuc, p_nuc_kin, &
                    dij, &
                    x_elec, p_elec) 
use mod_main
implicit none
include "param.def"
! arguments
real(kind=8), dimension(n_mode) :: p_nuc, p_nuc_kin
real(kind=8), dimension(n_state, n_state, n_mode) :: dij
real(kind=8), dimension(n_state) :: x_elec, p_elec

! local variables
real(kind=8), dimension(n_mode) :: delt_p_nuc
integer i_state, j_state, i_mode, itmp
real(kind=8) dtmp
character(len=72) ctmp

delt_p_nuc = 0.d0
if(label_debug>=1) then
  write(*,*) 'sub_p_kin_to_p'
  write(*,*) 'i_mode, i_state, j_state, dij'
  do i_mode = 1, n_mode
    do i_state = 1, n_state
      do j_state = 1, n_state
        write(*,*) i_mode, i_state, j_state, dij(i_state, j_state, i_mode)
      enddo
    enddo
  enddo
  write(*,*)
  write(*,*) 'i_state, x_elec, p_elec'
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state)
  enddo
  write(*,*) 'sub_p_kin_to_p'
  write(*,*) 'p_nuc_kin'
  do i_mode = 1, n_mode
    write(*,*) i_mode, p_nuc_kin(i_mode)
  enddo
endif
do i_mode = 1, n_mode
  dtmp = 0.d0
  do i_state = 1, n_state
    do j_state = 1, n_state
      if(i_state == j_state) cycle
      dtmp = dtmp + x_elec(i_state) * p_elec(j_state) &
             * dij(i_state, j_state, i_mode)
      if(label_debug>=2) write(*,*) "i_state, j_state, dtmp"
      if(label_debug>=2) write(*,*) i_state, j_state, dtmp
    enddo
  enddo
  delt_p_nuc(i_mode) = dtmp
enddo

do i_mode = 1, n_mode
  p_nuc(i_mode) = p_nuc_kin(i_mode) - delt_p_nuc(i_mode)
enddo

if(label_debug>=1) then
  write(*,*) 'sub_p_kin_to_p'
  write(*,*) 'delt_p_nuc'
  do i_mode = 1, n_mode
    write(*,*) i_mode, delt_p_nuc(i_mode)
  enddo
  write(*,*)
  write(*,*) 'p_nuc'
  do i_mode = 1, n_mode
    write(*,*) i_mode, p_nuc(i_mode)
  enddo
  write(*,*)
endif
return
end
