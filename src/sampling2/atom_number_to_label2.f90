
subroutine atom_number_to_label(atom_number, label )


  implicit none

  integer, intent(in) :: atom_number
  character*2, intent(inout) :: label
           
  label=""

              
      if (atom_number .eq. 1) then
        label = "H"
      endif

      if (atom_number .eq. 2) then
        label = "He"
      endif

      if (atom_number .eq. 3) then
        label = "Li"
      endif

      if (atom_number .eq. 4) then
        label = "Be"
      endif

      if (atom_number .eq. 5) then
        label = "B"
      endif

      if (atom_number .eq. 6) then
        label = "C"
      endif

      if (atom_number .eq. 7) then
        label = "N"
      endif

      if (atom_number .eq. 8) then
        label = "O"
      endif

      if (atom_number .eq. 9) then
        label = "F"
      endif

      if (atom_number .eq. 10) then
        label = "Ne"
      endif

      if (atom_number .eq. 11) then
        label = "Na"
      endif

      if (atom_number .eq. 12) then
        label = "Mg"
      endif

      if (atom_number .eq. 13) then
        label = "Al"
      endif

      if (atom_number .eq. 14) then
        label = "Si"
      endif

      if (atom_number .eq. 15) then
        label = "P"
      endif

      if (atom_number .eq. 16) then
        label = "S"
      endif

      if (atom_number .eq. 17) then
        label = "Cl"
      endif

      if (atom_number .eq. 18) then
        label = "Ar"
      endif

      if (atom_number .eq. 19) then
        label = "K"
      endif

      if (atom_number .eq. 20) then
        label = "Ca"
      endif

      if (atom_number .eq. 21) then
        label = "Sc"
      endif

      if (atom_number .eq. 22) then
        label = "Ti"
      endif

      if (atom_number .eq. 23) then
        label = "V"
      endif

      if (atom_number .eq. 24) then
        label = "Cr"
      endif

      if (atom_number .eq. 25) then
        label = "Mn"
      endif

      if (atom_number .eq. 26) then
        label = "Fe"
      endif

      if (atom_number .eq. 27) then
        label = "Co"
      endif

      if (atom_number .eq. 28) then
        label = "Ni"
      endif

      if (atom_number .eq. 29) then
        label = "Cu"
      endif

      if (atom_number .eq. 30) then
        label = "Zn"
      endif

      if (atom_number .eq. 31) then
        label = "Ga"
      endif

      if (atom_number .eq. 32) then
        label = "Ge"
      endif

      if (atom_number .eq. 33) then
        label = "As"
      endif

      if (atom_number .eq. 34) then
        label = "Se"
      endif

      if (atom_number .eq. 35) then
        label = "Br"
      endif

      if (atom_number .eq. 36) then
        label = "Kr"
      endif

      if (atom_number .eq. 37) then
        label = "Rb"
      endif

      if (atom_number .eq. 38) then
        label = "Sr"
      endif

      if (atom_number .eq. 39) then
        label = "Y"
      endif

      if (atom_number .eq. 40) then
        label = "Zr"
      endif

      if (atom_number .eq. 41) then
        label = "Nb"
      endif

      if (atom_number .eq. 42) then
        label = "Mo"
      endif

      if (atom_number .eq. 43) then
        label = "Tc"
      endif

      if (atom_number .eq. 44) then
        label = "Ru"
      endif

      if (atom_number .eq. 45) then
        label = "Rh"
      endif

      if (atom_number .eq. 46) then
        label = "Pd"
      endif

      if (atom_number .eq. 47) then
        label = "Ag"
      endif

      if (atom_number .eq. 48) then
        label = "Cd"
      endif

      if (atom_number .eq. 49) then
        label = "In"
      endif

      if (atom_number .eq. 50) then
        label = "Sn"
      endif

      if (atom_number .eq. 51) then
        label = "Sb"
      endif

      if (atom_number .eq. 52) then
        label = "Te"
      endif

      if (atom_number .eq. 53) then
        label = "I"
      endif

      if (atom_number .eq. 54) then
        label = "Xe"
      endif

      if (atom_number .eq. 55) then
        label = "Cs"
      endif

      if (atom_number .eq. 56) then
        label = "Ba"
      endif

      if (atom_number .eq. 57) then
        label = "La"
      endif

      if (atom_number .eq. 58) then
        label = "Ce"
      endif

      if (atom_number .eq. 59) then
        label = "Pr"
      endif

      if (atom_number .eq. 60) then
        label = "Nd"
      endif

      if (atom_number .eq. 61) then
        label = "Pm"
      endif

      if (atom_number .eq. 62) then
        label = "Sm"
      endif

      if (atom_number .eq. 63) then
        label = "Eu"
      endif

      if (atom_number .eq. 64) then
        label = "Gd"
      endif

      if (atom_number .eq. 65) then
        label = "Tb"
      endif

      if (atom_number .eq. 66) then
        label = "Dy"
      endif

      if (atom_number .eq. 67) then
        label = "Ho"
      endif

      if (atom_number .eq. 68) then
        label = "Er"
      endif

      if (atom_number .eq. 69) then
        label = "Tm"
      endif

      if (atom_number .eq. 70) then
        label = "Yb"
      endif

      if (atom_number .eq. 71) then
        label = "Lu"
      endif

      if (atom_number .eq. 72) then
        label = "Hf"
      endif

      if (atom_number .eq. 73) then
        label = "Ta"
      endif

      if (atom_number .eq. 74) then
        label = "W"
      endif

      if (atom_number .eq. 75) then
        label = "Re"
      endif

      if (atom_number .eq. 76) then
        label = "Os"
      endif

      if (atom_number .eq. 77) then
        label = "Ir"
      endif

      if (atom_number .eq. 78) then
        label = "Pt"
      endif

      if (atom_number .eq. 79) then
        label = "Au"
      endif

      if (atom_number .eq. 80) then
        label = "Hg"
      endif

      if (atom_number .eq. 81) then
        label = "Tl"
      endif

      if (atom_number .eq. 82) then
        label = "Pb"
      endif

      if (atom_number .eq. 83) then
        label = "Bi"
      endif

      if (atom_number .eq. 84) then
        label = "Po"
      endif

      if (atom_number .eq. 85) then
        label = "At"
      endif

      if (atom_number .eq. 86) then
        label = "Rn"
      endif

      if (atom_number .eq. 87) then
        label = "Fr"
      endif

      if (atom_number .eq. 88) then
        label = "Ra"
      endif

      if (atom_number .eq. 89) then
        label = "Ac"
      endif

      if (atom_number .eq. 90) then
        label = "Th"
      endif

      if (atom_number .eq. 91) then
        label = "Pa"
      endif

      if (atom_number .eq. 92) then
        label = "U"
      endif

      if (atom_number .eq. 93) then
        label = "Np"
      endif

      if (atom_number .eq. 94) then
        label = "Pu"
      endif

      if (atom_number .eq. 95) then
        label = "Am"
      endif

      if (atom_number .eq. 96) then
        label = "Cm"
      endif

      if (atom_number .eq. 97) then
        label = "Bk"
      endif

      if (atom_number .eq. 98) then
        label = "Cf"
      endif

      if (atom_number .eq. 99) then
        label = "Es"
      endif

      if (atom_number .eq. 100) then
        label = "Fm"
      endif

      if (atom_number .eq. 101) then
        label = "Md"
      endif

      if (atom_number .eq. 102) then
        label = "No"
      endif

      if (atom_number .eq. 103) then
        label = "Lr"
      endif

      if (atom_number .eq. 104) then
        label = "Rf"
      endif

      if (atom_number .eq. 105) then
        label = "Db"
      endif

      if (atom_number .eq. 106) then
        label = "Sg"
      endif

      if (atom_number .eq. 107) then
        label = "Bh"
      endif

      if (atom_number .eq. 108) then
        label = "Hs"
      endif

      if (atom_number .eq. 109) then
        label = "Mt"
      endif


      if (label .eq. "") then
         write (*,*) "PLEASE CHECK THE ATOMIC NUMBER!!"
         stop
      endif


      return
    end  subroutine   atom_number_to_label
 
              
