 
module langevin  
  use randomlib
  implicit none
  ! @ Likai Du 
  ! units
  ! everything in atomic unit
  ! for gamma: for dyn.inp in 1/fs, so convert to amu. by TOFS
  ! for temp: in dyn.inp in 1/K, so convert to amu. by AU2TEMP
  ! see http://en.wikipedia.org/wiki/Atomic_units

  ! in atomic unit, kb is 1.0
  double precision :: kb
  parameter (kb=1.0)

  contains

  subroutine sub_set_langevin_gamma(gamma,n_atom, mass, g0, dtime)
    implicit none
    include "param.def"
    integer, intent(in) :: n_atom
    double precision, intent(in) :: g0, dtime
    double precision, dimension(n_atom), intent(in) :: mass
    double precision, dimension(n_atom), intent(out) :: gamma
    
    if (dabs(dtime) .gt. 1.0d-10) then
       gamma(:) = g0 * TOFS 
    else
       gamma(:) = mass(:) / dtime  ! note other option may also be possible.. here
    endif
  end subroutine sub_set_langevin_gamma



  subroutine sub_langevin_friction(gamma,mass,vel_x,vel_y,vel_z, &
       grad_x, grad_y, grad_z, n_atom)
    implicit none

    integer :: n_atom
    double precision, dimension(n_atom), intent(in) :: gamma, mass, &
         vel_x, vel_y, vel_z
    double precision, dimension(n_atom), intent(out) :: grad_x, grad_y, grad_z
    integer :: i
    double precision :: t

    do i = 1, n_atom
       t = gamma(i) * mass(i)
       ! write(*,*) grad_x(i), grad_y(i), grad_z(i)
       grad_x(i) = grad_x(i) + vel_x(i) * t
       grad_y(i) = grad_y(i) + vel_y(i) * t
       grad_z(i) = grad_z(i) + vel_z(i) * t
       ! write(*,*) grad_x(i), grad_y(i), grad_z(i)
       ! write(*,*) gamma(i), mass(i)
    enddo
  end subroutine sub_langevin_friction


  subroutine sub_langevin_noise(gamma, temp, mass, &
       grad_x, grad_y, grad_z, n_atom)
    implicit none
    include "param.def"
    integer :: n_atom
    double precision :: temp
    double precision, dimension(n_atom), intent(in) :: gamma, mass
    double precision, dimension(n_atom), intent(out) :: grad_x, grad_y, grad_z
    integer :: i, nr
    double precision :: t    
    double precision, dimension(:), allocatable :: ran
    ! double precision :: AU2TEMP = 3.1577464D+5
    ! random number
    nr = n_atom * 3
    allocate(ran(1:nr))
    call get_std_normal(ran, nr)
    ! 2.0 k_b T \gamma M Gauss
    do i = 1, n_atom
       t = 2.0 * kb * temp / AU2TEMP       
       grad_x(i) = grad_x(i) - dsqrt(gamma(i) * mass(i) * t) * ran(i*3+0)
       grad_y(i) = grad_y(i) - dsqrt(gamma(i) * mass(i) * t) * ran(i*3+1)
       grad_z(i) = grad_z(i) - dsqrt(gamma(i) * mass(i) * t) * ran(i*3+2)
 
    enddo
  end subroutine sub_langevin_noise


  subroutine sub_langevin_modify(mass, vel_x, vel_y, vel_z, g0, temp, &
       grad_x, grad_y, grad_z, n_atom, dtime)
    implicit none
    integer :: n_atom
    double precision :: g0, temp
    double precision, dimension(n_atom) :: gamma, mass, &
         vel_x, vel_y, vel_z
    double precision, dimension(n_atom), intent(out) :: grad_x, grad_y, grad_z
    integer :: i, nr
    double precision :: dtime  
    double precision, dimension(:), allocatable :: ran      

    ! suppose grad_* was initialized.
    call sub_set_langevin_gamma(gamma,n_atom, mass, g0, dtime)
    call sub_langevin_friction(gamma,mass,vel_x,vel_y,vel_z, &
         grad_x, grad_y, grad_z, n_atom)
    call sub_langevin_noise(gamma, temp, mass, &
         grad_x, grad_y, grad_z, n_atom)
   
  end subroutine sub_langevin_modify




end module langevin


!!$
!!$program main
!!$  use langevin
!!$  implicit none
!!$
!!$end program main
