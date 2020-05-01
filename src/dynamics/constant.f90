!
!***********************************************************************
!     ----- Param.def : Size Parameters definitions -----
!=======================================================================
!     ----- If needed these parameters can be increased       -----
!     ----- An extensive description of the various variables -----
!     ----- is provided in the user manual epciso.ps          -----
!-----------------------------------------------------------------------
!     written by:  Z. Lan TU Munich
!***********************************************************************
! @ dulikai @ 2014.4 @ extended to modular

module constant
      implicit none
      double precision :: ZERO,ONE,TWO,THREE,SMALL,HBAR,HBAR2,AMU,TOEV, &
                       TOFS,TOCM,PI, ATOMMASS, ANSTOBOHR, BOHRTOANG, &
                       KCANGTOEV, AU2TEMP
      complex (kind=8) :: c1

      parameter (ZERO=0.0D+00,ONE=1.0D+00,TWO=2.0D+00,THREE=3.0D+00, &
                 SMALL = 1.0D+03, &
                 HBAR=1.0D+00,HBAR2=HBAR**2,AMU=1/1822.88851633D+00, &
                 ATOMMASS=1822.88851633D+00, &
                 TOEV= 27.2113961D+00,TOCM=219474.0D+00, &
                 TOFS=2.418918299D-02, &
                 PI=3.14159265358979323846, &
                 ANSTOBOHR=1.8897261328856432D+00, &
                 BOHRTOANG=0.52917720859D+00, &
                 KCANGTOEV=0.0433641D+00, &
                 c1 = (0.0D+00,1.0D+00),  &
                 AU2TEMP = 3.1577464D+5 &
                 )

    end module constant
