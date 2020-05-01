       subroutine label_to_mass ( tmp_label, tmp_mass)   

      implicit none
      include 'param.def'

      character*2 , intent(in) :: tmp_label
!      integer, intent(inout) ::  charge
      double precision, intent(inout) :: tmp_mass

      integer :: charge

             
             tmp_mass = 0
             charge = 0
          
             if ( (tmp_label .eq. "H") &
                   .or.  &
                   (tmp_label .eq. "h") &
                ) then 
                 tmp_mass=1.0079d0
                 charge=1
             endif        
          
             if ( (tmp_label .eq. "HE") &
                   .or.  &
                   (tmp_label .eq. "He") &
                   .or.  &
                   (tmp_label .eq. "he") &
                ) then
                 tmp_mass=4.0026
                 charge=2
             endif

             if ( (tmp_label .eq. "LI") &
                   .or.  &
                   (tmp_label .eq. "Li") &
                   .or.  &
                   (tmp_label .eq. "li") &
                ) then
                 tmp_mass=6.94d0
                 charge=3
             endif


             if ( (tmp_label .eq. "BE") &
                   .or.  &
                   (tmp_label .eq. "Be") &
                   .or.  &
                   (tmp_label .eq. "be") &
                ) then
                 tmp_mass=9.0122
                 charge=4
             endif

             if ( (tmp_label .eq. "B") &
                   .or.  &
                   (tmp_label .eq. "b") &
                ) then
                 tmp_mass=10.81d0
                 charge=5
             endif


             if ( (tmp_label .eq. "C") &
                   .or.  &
                  (tmp_label .eq. "c") &
                ) then
                tmp_mass=12.01115d0
                charge=6
             endif

             if ( (tmp_label .eq. "N") &
                   .or.  &
                  (tmp_label .eq. "n") &
                )  then
                tmp_mass=14.0067d0
                charge=7
             endif

             if ( (tmp_label .eq. "O") &
                   .or.  &
                  (tmp_label .eq. "o") &
                ) then
                tmp_mass=15.9994d0
                charge=8
             endif

              if ( (tmp_label .eq. "F") &
                   .or.  &
                  (tmp_label .eq. "f") &
                ) then
                tmp_mass=18.988d0
                charge=9
             endif

             if ( (tmp_label .eq. "NE") &
                   .or.  &
                  (tmp_label .eq. "Ne") &
                   .or.  &
                  (tmp_label .eq. "ne") &
                ) then
                tmp_mass=20.180d0
                charge=10
             endif

             if ( (tmp_label .eq. "NA") &
                   .or.  &
                  (tmp_label .eq. "Na") &
                   .or.  &
                  (tmp_label .eq. "na") &
                ) then
                tmp_mass=22.990
                charge=11
             endif
 
             if ( (tmp_label .eq. "MG") &
                   .or.  &
                  (tmp_label .eq. "Mg") &
                   .or.  &
                  (tmp_label .eq. "mg") &
                ) then
                tmp_mass=24.305d0
                charge=12
             endif

             if ( (tmp_label .eq. "AL") &
                   .or.  &
                  (tmp_label .eq. "Al") &
                   .or.  &
                  (tmp_label .eq. "al") &
                ) then
                tmp_mass=26.982d0
                charge=13
             endif



             if ( (tmp_label .eq. "SI") &
                   .or.  &
                  (tmp_label .eq. "Si") &
                   .or.  &
                  (tmp_label .eq. "si") &
                ) then
                tmp_mass=28.0855d0
                charge=14
             endif

         
             if ( (tmp_label .eq. "P") &
                   .or.  &
                  (tmp_label .eq. "p") &
                ) then
                tmp_mass=30.974d0
                charge=15
             endif


             if ( (tmp_label .eq. "S") &
                   .or.  &
                  (tmp_label .eq. "s") &
                ) then
                tmp_mass=32.065d0
                charge=16
             endif

             if ( (tmp_label .eq. "CL") &
                   .or.  &
                  (tmp_label .eq. "Cl") &
                   .or.  &
                  (tmp_label .eq. "cl") &
                ) then
                tmp_mass=35.45d0
                charge=17
             endif

             if ( (tmp_label .eq. "AR") &
                   .or.  &
                  (tmp_label .eq. "Ar") &
                   .or.  &
                  (tmp_label .eq. "ar") &
                ) then
                tmp_mass=39.948d0
                charge=18
             endif
 
             if ( (tmp_label .eq. "K") &
                   .or.  &
                  (tmp_label .eq. "k") &
                ) then
                tmp_mass=39.098d0
                charge=19
             endif

             if ( (tmp_label .eq. "CA") &
                   .or.  &
                  (tmp_label .eq. "Ca") &
                   .or.  &
                  (tmp_label .eq. "ca") &
                ) then
                tmp_mass=40.078d0
                charge=20
             endif

             if ( (tmp_label .eq. "SC") &
                   .or.  &
                  (tmp_label .eq. "Sc") &
                   .or.  &
                  (tmp_label .eq. "sc") &
                ) then
                tmp_mass=44.956d0
                charge=21
             endif


             if ( (tmp_label .eq. "TI") &
                   .or.  &
                  (tmp_label .eq. "Ti") &
                   .or.  &
                  (tmp_label .eq. "ti") &
                ) then
                tmp_mass=47.88d0
                charge=22
             endif


             if ( (tmp_label .eq. "V") &
                   .or.  &
                  (tmp_label .eq. "v") &
                ) then
                tmp_mass=50.942d0
                charge=23
             endif

             if ( (tmp_label .eq. "CR") &
                   .or.  &
                  (tmp_label .eq. "Cr") &
                   .or.  &
                  (tmp_label .eq. "cr") &
                ) then
                tmp_mass=51.996d0
                charge=24
             endif

            if ( (tmp_label .eq. "MN") &
                   .or.  &
                  (tmp_label .eq. "Mn") &
                   .or.  &
                  (tmp_label .eq. "mn") &
                ) then
                tmp_mass=54.938d0
                charge=25
             endif


             if ( (tmp_label .eq. "FE") &
                   .or.  &
                  (tmp_label .eq. "Fe") &
                   .or.  &
                  (tmp_label .eq. "fe") &
                ) then
                tmp_mass=55.845d0
                charge=26
             endif



             if ( (tmp_label .eq. "CO") &
                   .or.  &
                  (tmp_label .eq. "Co") &
                  .or.   &
                  (tmp_label .eq. "co") &
                ) then
                tmp_mass=58.933195d0
                charge=27
             endif

             if ( (tmp_label .eq. "NI") &
                   .or.  &
                  (tmp_label .eq. "Ni") &
                  .or.   &
                  (tmp_label .eq. "ni") &
                ) then
                tmp_mass=58.693d0
                charge=28
             endif


             if ( (tmp_label .eq. "CU") &
                   .or.  &
                  (tmp_label .eq. "Cu") &
                  .or.   &
                  (tmp_label .eq. "cu") &
                ) then
                tmp_mass=63.546d0
                charge=29
             endif


             if ( (tmp_label .eq. "ZN") &
                   .or.  &
                  (tmp_label .eq. "Zn") &
                  .or.   &
                  (tmp_label .eq. "zn") &
                ) then
                tmp_mass=65.38d0
                charge=30
             endif

             if ( (tmp_label .eq. "GA") &
                   .or.  &
                  (tmp_label .eq. "Ga") &
                  .or.   &
                  (tmp_label .eq. "ga") &
                ) then
                tmp_mass=69.723d0
                charge=31
             endif

             if ( (tmp_label .eq. "GE") &
                   .or.  &
                  (tmp_label .eq. "Ge") &
                  .or.   &
                  (tmp_label .eq. "ge") &
                ) then
                tmp_mass=72.63d0
                charge=32
             endif

             if ( (tmp_label .eq. "AS") &
                   .or.  &
                  (tmp_label .eq. "As") &
                  .or.   &
                  (tmp_label .eq. "as") &
                ) then
                tmp_mass=74.922d0
                charge=33
             endif

             if ( (tmp_label .eq. "SE") &
                   .or.  &
                  (tmp_label .eq. "Se") &
                  .or.   &
                  (tmp_label .eq. "se") &
                ) then
                tmp_mass=78.96d0
                charge=34
             endif

             if ( (tmp_label .eq. "BR") &
                   .or.  &
                  (tmp_label .eq. "Br") &
                  .or.   &
                  (tmp_label .eq. "br") &
                ) then
                tmp_mass=79.904d0
                charge=35
             endif


             if ( (tmp_label .eq. "KR") &
                   .or.  &
                  (tmp_label .eq. "Kr") &
                  .or.   &
                  (tmp_label .eq. "kr") &
                ) then
                tmp_mass=83.798d0
                charge=36
             endif

             if ( (tmp_label .eq. "W") &
                   .or.  &
                  (tmp_label .eq. "w") &
                ) then
                tmp_mass=183.84
                charge=74
             endif



             if ( ( tmp_mass .eq. 0 ) &
                  .or.              &
                  (charge .eq. "0") &
                ) then
                  write (*,*)  "-------------------------------"
                  write (*,*)  "ERROR !"
                  write (*,*)  "Please check the atomic labels!"
           write (*,*)  "Or some used atoms are not in the atomic list!"
                  stop


             endif 

       return
       end 
