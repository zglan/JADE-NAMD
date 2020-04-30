subroutine sub_random_gau_1d(n,random_gau)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
implicit none

include 'param.def'

! --- arguments ---
integer n
!real(kind=8) mu, sigma
real(kind=8) random_gau(n)

! --- local variabes ---
integer seed
integer i
real(kind=8) random_1(n)
real(kind=8) random_2(n)
integer, parameter :: two_PI = 2.d0 * PI

CALL RANDOM_SEED()
CALL RANDOM_NUMBER(random_1)

seed = random_1(n/2)*6965896

CALL RANDOM_SEED(seed)
CALL RANDOM_NUMBER(random_2)

do i = 1, n
  random_gau(i) = sqrt( - log(random_1(i)) / log(2.718281828) ) &
                * cos(two_PI * random_2(i)) 
enddo


!do i = 1, n
!  random_gau(i) = random_gau(i)*sigma + mu
!enddo

return
end
