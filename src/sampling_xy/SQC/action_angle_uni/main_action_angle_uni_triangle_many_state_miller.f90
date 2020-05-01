program main_action_angle_uni_triangle_many_state_miller
implicit none

include 'param.def'

integer n_state
integer n_traj
character(len=72) filename_ini_n
character(len=72) filename_x_p_traj
real(kind=8), allocatable, dimension(:) :: ini_n
real(kind=8), allocatable, dimension(:,:) :: x, &
                                             p, &
                                             random_1, &
                                             random_2, &
                                             arr_n
real(kind=8) ggamma
real(kind=8) ggamma_half
real(kind=8) sum_n_max

integer i, j, k, seed, nr, i_occ, n
real(kind=8) angle, aaction, sigma, tmp, rran

write(*,*) 'n_state:'
read(*,*) n_state

write(*,*) 'n_traj:'
read(*,*) n_traj

write(*,*) 'filename of initial n(occupation):'
read(*,*) filename_ini_n

write(*,*) 'gamma:'
read(*,*) ggamma
write(*,*) ggamma
write(*,*) 'Acturally, we choose ggamma = 2/3 in triangle window sampling.'
write(*,*) 'If the input value is not the same as it, please check the input. The sampling will go on with ggamma = 2/3.'

ggamma = 2.d0 / 3.d0
ggamma_half = ggamma / 2.d0
sum_n_max = n_state * ggamma
nr = n_traj !*2**n_state

allocate( ini_n(n_state) )
allocate( random_1(n_traj, n_state) )
allocate( random_2(n_traj, n_state) )
allocate( arr_n(n_traj, n_state) )
allocate( x(n_traj, n_state) )
allocate( p(n_traj, n_state) )

open(10, file=filename_ini_n)
do i = 1, n_state
  read(10, *) ini_n(i)
enddo
close(10)

n = 0
do i = 1, n_state
  if ( ini_n(i) == 1) then
    i_occ = i
    n = n + 1
  endif
enddo

if (n .ne. 1) then
  write(*,*) "Wrong initial action input! Please check the file of ", filename_ini_n
  stop
endif

CALL RANDOM_SEED()
CALL RANDOM_NUMBER(random_1)
seed = 1234571
CALL RANDOM_SEED(seed)
do i = 1, n_traj
  call RANDOM_NUMBER(aaction)
  call RANDOM_NUMBER(rran)
  do while( 1 - aaction < rran)
    call RANDOM_NUMBER(aaction)
    call RANDOM_NUMBER(rran)
  enddo
  tmp = aaction
  if ( tmp == 0.d0 ) then
    arr_n(i, i_occ) = tmp  + 1 - ggamma_half + 1.d-9
  else
    arr_n(i, i_occ) = tmp  + 1 - ggamma_half
  endif
  do j = 1, n_state
    if (j == i_occ) cycle
    arr_n(i, j) = random_1(i, j) * (1 - tmp) - ggamma_half
  enddo
enddo

open(10, file='quantum_number.dat')
do i = 1, n_traj
  write(10,*) arr_n(i,:)
enddo
close(10)

do i = 1, n_traj
  do j = 1, n_state
    arr_n(i, j) = sqrt(2.d0*arr_n(i, j) + ggamma)
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
