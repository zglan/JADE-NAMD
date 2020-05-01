program main_action_angle_uni_angular_triangle
implicit none

include 'param.def'

integer n_state
integer n_traj
character(len=72) filename_ini_n
character(len=72) filename_x_p_traj
real(kind=8), allocatable, dimension(:) :: ini_n
real(kind=8), allocatable, dimension(:,:) :: x, &
                                             y, &
                                             p_x, &
                                             p_y, &
                                             random_1, &
                                             random_2, &
                                             arr_n
real(kind=8) ggamma
real(kind=8) ggamma_half
real(kind=8) sum_n_max

integer i, j, k, seed, nr
real(kind=8) angle, aaction, sigma, tmp

write(*,*) 'n_state:'
read(*,*) n_state

write(*,*) 'n_traj:'
read(*,*) n_traj

write(*,*) 'filename of initial n(occupation):'
read(*,*) filename_ini_n

write(*,*) 'gamma:'
read(*,*) ggamma
write(*,*) ggamma
write(*,*) 'Acturally, we choose ggamma = 1/3 in triangle window sampling.'
write(*,*) 'If the input value is not the same as it, please check the input. The sampling will go on with ggamma = 1/3.'

ggamma = 2.d0 / 3.d0 ! This is actually the window width. For convinience, it is not modified.
ggamma_half = ggamma / 2.d0
sum_n_max = n_state * ggamma
nr = n_traj*2**n_state

allocate( ini_n(n_state) )
allocate( random_1(nr, n_state) )
allocate( random_2(n_traj, n_state) )
allocate( arr_n(n_traj, n_state) )
allocate( x(n_traj, n_state) )
allocate( y(n_traj, n_state) )
allocate( p_x(n_traj, n_state) )
allocate( p_y(n_traj, n_state) )

open(10, file=filename_ini_n)
do i = 1, n_state
  read(10, *) ini_n(i)
enddo
close(10)

CALL RANDOM_SEED()
CALL RANDOM_NUMBER(random_1)

i = 1
do k = 1, nr
  do j = 1, n_state
    if (ini_n(j) == 0) then
      arr_n(i, j) = random_1(k, j) - ggamma_half
    elseif (ini_n(j) == 1) then
      if ( random_1(k, j) == 0.d0 ) then
        arr_n(i, j) = random_1(k, j) + ggamma + 1.d-9
      else
        arr_n(i, j) = random_1(k, j) + ggamma
      endif
    else
      write(*,*) 'Wrong "action" input! N = 1 or 0 and it cannot be the other values'
    endif
  enddo
  tmp = 0.d0
  do j = 1, n_state
    tmp = tmp + arr_n(i, j)
  enddo
  if ( tmp > sum_n_max ) then
    cycle
  else
    i = i + 1
  endif
  if (i > n_traj) exit
enddo

open(10, file='quantum_number.dat')
do i = 1, n_traj
  write(10,*) arr_n(i,:)
enddo
close(10)

do i = 1, n_traj
  do j = 1, n_state
    arr_n(i, j) = sqrt(arr_n(i, j) + ggamma_half)
  enddo
enddo


seed = 1234567
CALL RANDOM_SEED(seed)
CALL RANDOM_NUMBER(random_2)


!do i = 1, n_state
!  ini_n(i) = ini_n(i) + (random_2(i) - 0.5) * 2.d0 * ggamma
!  ini_n(i) = sqrt(2.d0 * ini_n(i) + ggamma)
!enddo

do i = 1, n_traj
  do j = 1, n_state
    angle = 2* PI * random_2(i, j)
    !aaction = ini_n(j)
    aaction = arr_n(i, j)
    x(i, j) = aaction * cos(angle)
    y(i, j) = - aaction * sin(angle)
    p_x(i, j) = aaction * sin(angle)
    p_y(i, j) = aaction * cos(angle)
  enddo
enddo

do i = 1, n_traj
  write(filename_x_p_traj,*) i
  filename_x_p_traj = 'traj_' // trim(adjustl(filename_x_p_traj))//'.inp'
  open(10, file=filename_x_p_traj)
  do j = 1, n_state
    write(10,9999) x(i, j), y(i, j), p_x(i, j), p_y(i, j)
  enddo
  close(10)
enddo


deallocate( ini_n )
deallocate( x )
deallocate( y )
deallocate( p_x )
deallocate( p_y )

9999 format(4f18.14)

end
