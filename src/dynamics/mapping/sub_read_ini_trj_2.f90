subroutine sub_read_ini_trj_2(x_cur, p_cur, &
           x_elec, p_elec) 
use mod_main
implicit none

include "param.def"

integer :: i_mode,  &
           file_ini_input, &
           file_restart_input

!double precision :: q
double precision, dimension(n_mode) :: x_cur,p_cur
real(kind=8), dimension(n_state) :: x_elec, p_elec

integer i_state




!call RANDOM_NUMBER(q)

!q=q*PI

!ele_coe(1)=cmplx(0.d0,0.d0)
!ele_coe(2)=cmplx(cos(q),sin(q))
!      ele_coe(3)=(0.d0,0.d0)

if (label_restart .eq. 0 ) then

   file_ini_input=11
   open(unit=file_ini_input, file="trj.input")
   do i_mode=1, n_mode
      read (file_ini_input, *)  x_cur(i_mode), p_cur(i_mode)
   enddo
   close(11)

   open(21, file="trj_elec.input")
   do i_state = 1, n_state
     read(21, *) x_elec(i_state), p_elec(i_state)
   enddo
   close(21)

endif


if (label_restart .eq. 1 ) then

   file_restart_input=12
   open(unit=file_restart_input, file="trj_restart.input")
   do i_mode=1, n_mode
      read (file_restart_input, *)  x_cur(i_mode), p_cur(i_mode)
   enddo
   close(12)

   open(21, file="trj_elec_restart.input")
   do i_state = 1, n_state
     read(21, *) x_elec(i_state), p_elec(i_state)
   enddo
   close(21)

endif

end
