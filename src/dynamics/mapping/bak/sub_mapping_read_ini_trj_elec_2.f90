subroutine sub_mapping_read_ini_trj_elec_2(x_elec, p_elec) 
use mod_main
implicit none

include "param.def"

integer :: i_mode,  &
           file_ini_input, &
           file_restart_input

!double precision :: q
real(kind=8), dimension(n_state) :: x_elec, p_elec

integer i_state




!call RANDOM_NUMBER(q)

!q=q*PI

!ele_coe(1)=cmplx(0.d0,0.d0)
!ele_coe(2)=cmplx(cos(q),sin(q))
!      ele_coe(3)=(0.d0,0.d0)

if (label_restart .eq. 0 ) then


   open(21, file="trj_elec.input")
   do i_state = 1, n_state
     read(21, *) x_elec(i_state), p_elec(i_state)
   enddo
   close(21)

endif


if (label_restart .eq. 1 ) then

   open(21, file="trj_elec_restart.input")
   do i_state = 1, n_state
     read(21, *) x_elec(i_state), p_elec(i_state)
   enddo
   close(21)

endif

end
