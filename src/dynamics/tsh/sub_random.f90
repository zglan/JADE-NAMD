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



subroutine get_random_number(num)
  implicit none
  double precision :: num

  call random_number(num)

end subroutine get_random_number





