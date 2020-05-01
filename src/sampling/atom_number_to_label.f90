       subroutine   atom_number_to_label (atom_number, label )


      implicit none

      integer, intent(in) :: atom_number
      character*2, intent(inout) :: label
     
      
      label=""

                 If ( atom_number  .eq.  1)  then
                    label="H"
                 endif
                 If ( atom_number  .eq.  2)  then
                    label="He"
                 endif                 
                 If ( atom_number  .eq.  3)  then
                    label="Li"
                 endif
                 If ( atom_number  .eq.  4)  then
                    label="Be"
                 endif
                 If ( atom_number  .eq.  5)  then
                    label="B"
                 endif
                 If ( atom_number  .eq.  6)  then
                    label="C"
                 endif
                 If ( atom_number  .eq.  7)  then
                    label="N"
                 endif
                 If ( atom_number  .eq.  8)  then
                    label="O"
                 endif
                 If ( atom_number  .eq.  9)  then
                    label="F"
                 endif
                 If ( atom_number  .eq.  10)  then
                    label="Ne"
                 endif
                 If ( atom_number  .eq.  11)  then
                    label="Na"
                 endif
                 If ( atom_number  .eq.  12)  then
                    label="Mg"
                 endif
                 If ( atom_number  .eq.  13)  then
                    label="Al"
                 endif
                 If ( atom_number  .eq.  14)  then
                    label="Si"
                 endif
                 If ( atom_number  .eq.  15)  then
                    label="P"
                 endif
                 If ( atom_number  .eq.  16)  then
                    label="S"
                 endif
                 If ( atom_number  .eq.  17)  then
                    label="Cl"
                 endif
                 If ( atom_number  .eq.  18)  then
                    label="Ar"
                 endif
                 If ( atom_number  .eq.  19)  then
                    label="K"
                 endif
                 If ( atom_number  .eq.  20)  then
                    label="Ca"
                 endif
                 If ( atom_number  .eq.  21)  then
                    label="Sc"
                 endif
                 If ( atom_number  .eq.  22)  then
                    label="Ti"
                 endif
                 If ( atom_number  .eq.  23)  then
                    label="V"
                 endif
                 If ( atom_number  .eq.  24)  then
                    label="Cr"
                 endif
                 If ( atom_number  .eq.  25)  then
                    label="Mn"
                 endif
                 If ( atom_number  .eq.  26)  then
                    label="Fe"
                 endif
                 If ( atom_number  .eq.  27)  then
                    label="Co"
                 endif
                 If ( atom_number  .eq.  28)  then
                    label="Ni"
                 endif
                 If ( atom_number  .eq.  29)  then
                    label="Cu"
                 endif
                 If ( atom_number  .eq.  30)  then
                    label="Zn"
                 endif
                 If ( atom_number  .eq.  31)  then
                    label="Ga"
                 endif
                 If ( atom_number  .eq.  32)  then
                    label="Ge"
                 endif
                 If ( atom_number  .eq.  33)  then
                    label="As"
                 endif
                 If ( atom_number  .eq.  34)  then
                    label="Se"
                 endif
                 If ( atom_number  .eq.  35)  then
                    label="Br"
                 endif
                 If ( atom_number  .eq.  36)  then
                    label="Kr"
                 endif




       if (label .eq. "") then
       write (*,*) "PLEASE CHECK THE ATOMIC NUMBER!!"
       stop
       endif


      return
      end  subroutine   atom_number_to_label
