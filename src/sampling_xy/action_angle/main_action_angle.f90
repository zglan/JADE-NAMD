program main_action_angle
implicit none

include 'param.def'

integer n_state
integer n_traj
character(len=72) filename_ini_n
character(len=72) filename_x_p_traj
real(kind=8), allocatable, dimension(:) :: ini_n
real(kind=8), allocatable, dimension(:,:) :: x, &
                                             p, &
                                             random_1
real(kind=8) ggamma

integer i, j
real(kind=8) angle, aaction


write(*,*) 'n_state:'
read(*,*) n_state

write(*,*) 'n_traj:'
read(*,*) n_traj

write(*,*) 'filename of initial n(occupation):'
read(*,*) filename_ini_n

write(*,*) 'gamma:'
read(*,*) ggamma

allocate( ini_n(n_state) )
allocate( x(n_traj, n_state) )
allocate( p(n_traj, n_state) )
allocate( random_1(n_traj, n_state) )

open(10, file=filename_ini_n)
do i = 1, n_state
  read(10, *) ini_n(i)
enddo
close(10)

do i = 1, n_state
  ini_n(i) = sqrt(2.d0 * ini_n(i) + ggamma) 
enddo

CALL RANDOM_SEED()
CALL RANDOM_NUMBER(random_1)

do i = 1, n_traj
  do j = 1, n_state
    angle = 2* PI * random_1(i, j)
    aaction = ini_n(j)
    x(i, j) = aaction * cos(angle)
    p(i, j) = aaction * sin(angle)
  enddo
enddo

do i = 1, n_traj
  write(filename_x_p_traj,*) i
  filename_x_p_traj = 'traj_' // trim(adjustl(filename_x_p_traj))//'.inp'
  open(10, file=filename_x_p_traj)
  do j = 1, n_state
    write(10,9999) x(i, j), p(i, j)
  enddo
  close(10)
enddo



deallocate( ini_n )
deallocate( x )
deallocate( p )

9999 format(2f18.14)

end
