
subroutine sub_get_mass ( tmp_label, tmp_mass, charge)   

  implicit none
  include 'param.def'

  character*2 , intent(in) :: tmp_label
  integer, intent(inout) ::  charge
  double precision, intent(inout) :: tmp_mass

  character*2 :: mylabel
              
  mylabel = tmp_label
  call lower_case(mylabel)

  tmp_mass = 0.0D+00
  charge = 0

  if (mylabel .eq. "h") then
    tmp_mass = 1.007825037/AMU
    charge =  1
  endif

  if (mylabel .eq. "hd") then
    tmp_mass = 2.274246/AMU
    charge =  1
  endif


  if (mylabel .eq. "he") then
    tmp_mass = 4.0026/AMU
    charge =  2
  endif

  if (mylabel .eq. "li") then
    tmp_mass = 6.941/AMU
    charge =  3
  endif

  if (mylabel .eq. "be") then
    tmp_mass = 9.0122/AMU
    charge =  4
  endif

  if (mylabel .eq. "b") then
    tmp_mass = 10.811/AMU
    charge =  5
  endif

  if (mylabel .eq. "c") then
    tmp_mass = 12.0/AMU
    charge =  6
  endif

  if (mylabel .eq. "n") then
    tmp_mass = 14.003074008d0/AMU
    charge =  7
  endif

  if (mylabel .eq. "o") then
    tmp_mass = 15.99491464/AMU
    charge =  8
  endif

  if (mylabel .eq. "f") then
    tmp_mass = 18.9984/AMU
    charge =  9
  endif

  if (mylabel .eq. "ne") then
    tmp_mass = 20.1797/AMU
    charge =  10
  endif

  if (mylabel .eq. "na") then
    tmp_mass = 22.9897/AMU
    charge =  11
  endif

  if (mylabel .eq. "mg") then
    tmp_mass = 24.305/AMU
    charge =  12
  endif

  if (mylabel .eq. "al") then
    tmp_mass = 26.9815/AMU
    charge =  13
  endif

  if (mylabel .eq. "si") then
    tmp_mass = 28.0855/AMU
    charge =  14
  endif

  if (mylabel .eq. "p") then
    tmp_mass = 30.9738/AMU
    charge =  15
  endif

  if (mylabel .eq. "s") then
    tmp_mass = 32.065/AMU
    charge =  16
  endif

  if (mylabel .eq. "cl") then
    tmp_mass = 35.453/AMU
    charge =  17
  endif

  if (mylabel .eq. "ar") then
    tmp_mass = 39.948/AMU
    charge =  18
  endif

  if (mylabel .eq. "k") then
    tmp_mass = 39.0983/AMU
    charge =  19
  endif

  if (mylabel .eq. "ca") then
    tmp_mass = 40.078/AMU
    charge =  20
  endif

  if (mylabel .eq. "sc") then
    tmp_mass = 44.9559/AMU
    charge =  21
  endif

  if (mylabel .eq. "ti") then
    tmp_mass = 47.867/AMU
    charge =  22
  endif

  if (mylabel .eq. "v") then
    tmp_mass = 50.9415/AMU
    charge =  23
  endif

  if (mylabel .eq. "cr") then
    tmp_mass = 51.9961/AMU
    charge =  24
  endif

  if (mylabel .eq. "mn") then
    tmp_mass = 54.938/AMU
    charge =  25
  endif

  if (mylabel .eq. "fe") then
    tmp_mass = 55.845/AMU
    charge =  26
  endif

  if (mylabel .eq. "co") then
    tmp_mass = 58.9332/AMU
    charge =  27
  endif

  if (mylabel .eq. "ni") then
    tmp_mass = 58.6934/AMU
    charge =  28
  endif

  if (mylabel .eq. "cu") then
    tmp_mass = 63.546/AMU
    charge =  29
  endif

  if (mylabel .eq. "zn") then
    tmp_mass = 65.39/AMU
    charge =  30
  endif

  if (mylabel .eq. "ga") then
    tmp_mass = 69.723/AMU
    charge =  31
  endif

  if (mylabel .eq. "ge") then
    tmp_mass = 72.64/AMU
    charge =  32
  endif

  if (mylabel .eq. "as") then
    tmp_mass = 74.9216/AMU
    charge =  33
  endif

  if (mylabel .eq. "se") then
    tmp_mass = 78.96/AMU
    charge =  34
  endif

  if (mylabel .eq. "br") then
    tmp_mass = 79.904/AMU
    charge =  35
  endif

  if (mylabel .eq. "kr") then
    tmp_mass = 83.8/AMU
    charge =  36
  endif

  if (mylabel .eq. "rb") then
    tmp_mass = 85.4678/AMU
    charge =  37
  endif

  if (mylabel .eq. "sr") then
    tmp_mass = 87.62/AMU
    charge =  38
  endif

  if (mylabel .eq. "y") then
    tmp_mass = 88.9059/AMU
    charge =  39
  endif

  if (mylabel .eq. "zr") then
    tmp_mass = 91.224/AMU
    charge =  40
  endif

  if (mylabel .eq. "nb") then
    tmp_mass = 92.9064/AMU
    charge =  41
  endif

  if (mylabel .eq. "mo") then
    tmp_mass = 95.94/AMU
    charge =  42
  endif

  if (mylabel .eq. "tc") then
    tmp_mass = 98.0/AMU
    charge =  43
  endif

  if (mylabel .eq. "ru") then
    tmp_mass = 101.07/AMU
    charge =  44
  endif

  if (mylabel .eq. "rh") then
    tmp_mass = 102.9055/AMU
    charge =  45
  endif

  if (mylabel .eq. "pd") then
    tmp_mass = 106.42/AMU
    charge =  46
  endif

  if (mylabel .eq. "ag") then
    tmp_mass = 107.8682/AMU
    charge =  47
  endif

  if (mylabel .eq. "cd") then
    tmp_mass = 112.411/AMU
    charge =  48
  endif

  if (mylabel .eq. "in") then
    tmp_mass = 114.818/AMU
    charge =  49
  endif

  if (mylabel .eq. "sn") then
    tmp_mass = 118.71/AMU
    charge =  50
  endif

  if (mylabel .eq. "sb") then
    tmp_mass = 121.76/AMU
    charge =  51
  endif

  if (mylabel .eq. "te") then
    tmp_mass = 127.6/AMU
    charge =  52
  endif

  if (mylabel .eq. "i") then
    tmp_mass = 126.9045/AMU
    charge =  53
  endif

  if (mylabel .eq. "xe") then
    tmp_mass = 131.293/AMU
    charge =  54
  endif

  if (mylabel .eq. "cs") then
    tmp_mass = 132.9055/AMU
    charge =  55
  endif

  if (mylabel .eq. "ba") then
    tmp_mass = 137.327/AMU
    charge =  56
  endif

  if (mylabel .eq. "la") then
    tmp_mass = 138.9055/AMU
    charge =  57
  endif

  if (mylabel .eq. "ce") then
    tmp_mass = 140.116/AMU
    charge =  58
  endif

  if (mylabel .eq. "pr") then
    tmp_mass = 140.9077/AMU
    charge =  59
  endif

  if (mylabel .eq. "nd") then
    tmp_mass = 144.24/AMU
    charge =  60
  endif

  if (mylabel .eq. "pm") then
    tmp_mass = 145.0/AMU
    charge =  61
  endif

  if (mylabel .eq. "sm") then
    tmp_mass = 150.36/AMU
    charge =  62
  endif

  if (mylabel .eq. "eu") then
    tmp_mass = 151.964/AMU
    charge =  63
  endif

  if (mylabel .eq. "gd") then
    tmp_mass = 157.25/AMU
    charge =  64
  endif

  if (mylabel .eq. "tb") then
    tmp_mass = 158.9253/AMU
    charge =  65
  endif

  if (mylabel .eq. "dy") then
    tmp_mass = 162.5/AMU
    charge =  66
  endif

  if (mylabel .eq. "ho") then
    tmp_mass = 164.9303/AMU
    charge =  67
  endif

  if (mylabel .eq. "er") then
    tmp_mass = 167.259/AMU
    charge =  68
  endif

  if (mylabel .eq. "tm") then
    tmp_mass = 168.9342/AMU
    charge =  69
  endif

  if (mylabel .eq. "yb") then
    tmp_mass = 173.04/AMU
    charge =  70
  endif

  if (mylabel .eq. "lu") then
    tmp_mass = 174.967/AMU
    charge =  71
  endif

  if (mylabel .eq. "hf") then
    tmp_mass = 178.49/AMU
    charge =  72
  endif

  if (mylabel .eq. "ta") then
    tmp_mass = 180.9479/AMU
    charge =  73
  endif

  if (mylabel .eq. "w") then
    tmp_mass = 183.84/AMU
    charge =  74
  endif

  if (mylabel .eq. "re") then
    tmp_mass = 186.207/AMU
    charge =  75
  endif

  if (mylabel .eq. "os") then
    tmp_mass = 190.23/AMU
    charge =  76
  endif

  if (mylabel .eq. "ir") then
    tmp_mass = 192.217/AMU
    charge =  77
  endif

  if (mylabel .eq. "pt") then
    tmp_mass = 195.078/AMU
    charge =  78
  endif

  if (mylabel .eq. "au") then
    tmp_mass = 196.9665/AMU
    charge =  79
  endif

  if (mylabel .eq. "hg") then
    tmp_mass = 200.59/AMU
    charge =  80
  endif

  if (mylabel .eq. "tl") then
    tmp_mass = 204.3833/AMU
    charge =  81
  endif

  if (mylabel .eq. "pb") then
    tmp_mass = 207.2/AMU
    charge =  82
  endif

  if (mylabel .eq. "bi") then
    tmp_mass = 208.9804/AMU
    charge =  83
  endif

  if (mylabel .eq. "po") then
    tmp_mass = 209.0/AMU
    charge =  84
  endif

  if (mylabel .eq. "at") then
    tmp_mass = 210.0/AMU
    charge =  85
  endif

  if (mylabel .eq. "rn") then
    tmp_mass = 222.0/AMU
    charge =  86
  endif

  if (mylabel .eq. "fr") then
    tmp_mass = 223.0/AMU
    charge =  87
  endif

  if (mylabel .eq. "ra") then
    tmp_mass = 226.0/AMU
    charge =  88
  endif

  if (mylabel .eq. "ac") then
    tmp_mass = 227.0/AMU
    charge =  89
  endif

  if (mylabel .eq. "th") then
    tmp_mass = 232.0381/AMU
    charge =  90
  endif

  if (mylabel .eq. "pa") then
    tmp_mass = 231.0359/AMU
    charge =  91
  endif

  if (mylabel .eq. "u") then
    tmp_mass = 238.0289/AMU
    charge =  92
  endif

  if (mylabel .eq. "np") then
    tmp_mass = 237.0/AMU
    charge =  93
  endif

  if (mylabel .eq. "pu") then
    tmp_mass = 244.0/AMU
    charge =  94
  endif

  if (mylabel .eq. "am") then
    tmp_mass = 243.0/AMU
    charge =  95
  endif

  if (mylabel .eq. "cm") then
    tmp_mass = 247.0/AMU
    charge =  96
  endif

  if (mylabel .eq. "bk") then
    tmp_mass = 247.0/AMU
    charge =  97
  endif

  if (mylabel .eq. "cf") then
    tmp_mass = 251.0/AMU
    charge =  98
  endif

  if (mylabel .eq. "es") then
    tmp_mass = 252.0/AMU
    charge =  99
  endif

  if (mylabel .eq. "fm") then
    tmp_mass = 257.0/AMU
    charge =  100
  endif

  if (mylabel .eq. "md") then
    tmp_mass = 258.0/AMU
    charge =  101
  endif

  if (mylabel .eq. "no") then
    tmp_mass = 259.0/AMU
    charge =  102
  endif

  if (mylabel .eq. "lr") then
    tmp_mass = 262.0/AMU
    charge =  103
  endif

  if (mylabel .eq. "rf") then
    tmp_mass = 261.0/AMU
    charge =  104
  endif

  if (mylabel .eq. "db") then
    tmp_mass = 262.0/AMU
    charge =  105
  endif

  if (mylabel .eq. "sg") then
    tmp_mass = 266.0/AMU
    charge =  106
  endif

  if (mylabel .eq. "bh") then
    tmp_mass = 264.0/AMU
    charge =  107
  endif

  if (mylabel .eq. "hs") then
    tmp_mass = 277.0/AMU
    charge =  108
  endif

  if (mylabel .eq. "mt") then
    tmp_mass = 268.0/AMU
    charge =  109
  endif



  if ( tmp_mass .eq. 0 ) then

     write (*,*)  "-------------------------------"
     write (*,*)  "ERROR !"
     write (*,*)  "Please check the atomic labels!"
     write (*,*)  "Or some used atoms are not in the atomic list!"
     stop


  endif

  return
end subroutine sub_get_mass

              
