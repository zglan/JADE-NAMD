module randomlib
! for langevin dynamics calling 
  implicit none
  private ran_state

  integer, save :: n_seed = 0
  integer, save :: n_seed0 = 0
  integer, save, dimension(100) :: ran_state, ran_state0
  double precision, save, dimension(10000) :: ran_all
  integer, save :: n_ran = 0

contains
  
  subroutine random_gauss2d(X, Y)
    implicit none
    double precision, intent(out) :: X, Y
    double precision :: PI, R1, R2, R
    ! define pi value
    PI=4.D0*DATAN(1.D0)
    call random_number(R1)
    call random_number(R2)
    R1 = DSQRT(-2.0*DLOG(R1))
    R2 = 2.0 * PI * R2
    X  = R1*COS(R2)
    Y  = R1*SIN(R2)
  end subroutine random_gauss2d


  subroutine init_random_seed(iseed)
    implicit none
    integer :: iseed
    integer :: k
    integer, dimension(:), allocatable :: seed
    integer :: values(1:8)

    call random_seed(size=k)
    allocate(seed(1:k))

    if (iseed .eq. -1) then
       call date_and_time(values=values)
       seed(:) = values(8) 
    else
       seed(:) = iseed
    end if

    call random_seed(put=seed)

    deallocate(seed)

  end subroutine init_random_seed


  subroutine get_random_state(iflag)
    implicit none
    integer :: iflag
    if (iflag == 0) then
       call random_seed(size=n_seed)
       call random_seed(get=ran_state)    
    else if (iflag == 1) then
       call random_seed(size=n_seed0)
       call random_seed(get=ran_state0)   
    else
       write(*,*) "no such option"
       stop
    endif
  end subroutine get_random_state

  subroutine set_random_state(iflag)
    implicit none
    integer :: iflag
    if (iflag == 0) then
       call random_seed(put=ran_state(1:n_seed))
    else if (iflag == 1) then
       call random_seed(put=ran_state0(1:n_seed))
    else
       write(*,*) "no such option"
       stop
    endif
  end subroutine set_random_state


  subroutine set_random_state2(seed, n_seed)
    implicit none
    integer :: n_seed
    integer, dimension(:) :: seed
    call random_seed(put=seed(1:n_seed))
  end subroutine set_random_state2


  ! in which \mu is zero, and \deta is 1.
  subroutine get_std_normal(ran, nr)
    implicit none
    integer :: nr
    double precision, dimension(:) :: ran
    integer :: i
    double precision :: num

    call get_random_state(1)
    ! set seed state
    call set_random_state(0)
    
    ! get one gaussian random number
    do i = 1, nr
       call get_std_normal_one(num)
       ran(i) = num
    enddo

    ! get current state
    call get_random_state(0)
    ! eliminate the effect of this subroutine
    call set_random_state(1)

  end subroutine get_std_normal



  subroutine get_std_normal_one(num)
    implicit none
    integer, save :: iset = 0
    double precision, save :: saveY
    double precision, intent(out) :: num
    double precision :: X, Y
    if (iset .eq. 0) then
       call random_gauss2d(X, Y)
       num = X
       saveY = Y
       iset = 1
    else
       num = saveY
       iset = 0
    endif

  end subroutine get_std_normal_one



  ! generate all value at once & store in memory
  subroutine get_std_normal_all(n_ran)
    implicit none
    integer :: i
    integer :: n_ran
    double precision :: X, Y
 
    call get_random_state(0)
    do i = 1, n_ran/2+1
       call random_gauss2d(X, Y)
       ran_all(i) = X
       ran_all(i+1) = Y
    enddo

    call set_random_state(0)

  end subroutine get_std_normal_all


  ! generate all value at once & store in memory
  subroutine dump_std_normal_all(n_ran)
    implicit none
    integer :: i
    integer :: n_ran
    double precision :: X, Y
    !allocate(ran_all(1:n_ran))

    call get_random_state(0)
    write(*,*) n_ran
    do i = 1, n_ran/2+1
       call random_gauss2d(X, Y)
       write(*,*) X
       write(*,*) Y
    enddo

    call set_random_state(0)

  end subroutine dump_std_normal_all


end module randomlib


subroutine read_std_normal(ran_all, n_ran)
  implicit none
  integer :: i, n_ran
  double precision, dimension(:) :: ran_all
  open(unit=100, file='ran.txt')
  read(100,*) n_ran
  do i = 1, n_ran
     read(100,*) ran_all(i)
  enddo

  close(100)

end subroutine read_std_normal

!subroutine get_std_normal(ran, nr)
!  implicit none
!  integer nr
!  double precision, dimension(:) :: ran
!  integer, save :: num = 0

! ran(1:nr) = ran_all(1:nr)
!  num = num + nr
!end subroutine get_std_normal


subroutine write_array(ran, nr)
  implicit none
  integer :: i
  integer :: nr
  double precision, dimension(:) :: ran
  open(unit=100, file='ran.txt')
  do i = 1, nr
     write(100,*) ran(i), i
  enddo
     
  close(100)

end subroutine write_array


!!$program main
!!$  use randomlib
!!$  implicit none
!!$  integer :: nr
!!$  integer :: i
!!$  double precision, dimension(:), allocatable :: ran
!!$  integer :: file_random_gau, file_dis1d
!!$  nr = 1000000
!!$  allocate(ran(1:nr))
!!$
!!$  call init_random_seed(-1)
!!$  call get_random_state(0)
!!$  call get_std_normal(ran, nr)
!!$  open(unit=100, file='ran.txt')
!!$  write(100,*) "# header"
!!$  do i = 1, nr
!!$     write(100,*) i, ran(i)
!!$  enddo
!!$     
!!$  close(100)


!  file_random_gau = 100
!  file_dis1d = 1000
!  open(file_random_gau, file='ran.txt', status='old')
!  open(file_dis1d, file="dis1d.txt")
!  call check_random_1d(file_random_gau, nr, 500, 1, file_dis1d)
 

!!$end program main
!!$

