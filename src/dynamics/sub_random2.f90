module random_qibebt
  implicit none
  private ran_state
  integer, dimension(:), allocatable :: ran_state

 

  contains

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





! get normal random number distrition; gaussian distribution; [a,b]
  subroutine get_gauss_number(ran, nr)
    implicit none
    integer :: i, nr
    double precision, dimension(:) :: ran
    integer :: file_random_gau
    file_random_gau = 100
    open(file_random_gau, file="ran.txt")
    call random_seed()
    call random_number(ran)
    
    write (file_random_gau, *) "# gaussian distribution"
    do i = 1, nr
       ran(i) =  (-   log( ran(i))    &
                        / log(2.718281828)    &
                     ) ** 0.5d0
       write (file_random_gau, *) ran(i), i
    enddo
    close(file_random_gau)
 
  end subroutine get_gauss_number


! generate nr random number
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

  


  subroutine random_gauss(ran, nr)
    implicit none
    double precision, dimension(:), intent(out) :: ran
    integer :: nr
    integer :: n2d, ires, i
    double precision :: X, Y
    
    ires = MOD(nr, 2)
    n2d = nr / 2
    do i = 1, n2d
       call random_gauss2d(X, Y)
       write (*,*) X, 1
       write (*,*) Y, 1
    enddo
    if (ires == 1) then
       write (*,*) X, 1
    endif

  end subroutine random_gauss


end module random_qibebt






program main

  use random_qibebt
  implicit none
  integer :: nr
  double precision, dimension(:), allocatable :: ran
  integer :: file_random_gau, file_dis1d
  nr = 10000
  allocate(ran(1:nr))
  
 ! call get_gauss_number(ran, n)
  !ran_min = minval(ran)
  !ran_max = maxval(ran)
  
  call random_gauss(ran, nr)

!  write(*,*) ran_min, ran_max
  file_random_gau = 100
  file_dis1d = 1000
  open(file_random_gau, file='ran.txt', status='old')
  write(*,*) file_random_gau
  open(file_dis1d, file="dis1d.txt")
!  call check_random_1d(file_random_gau, n, 100, 1, file_dis1d)





end program main









