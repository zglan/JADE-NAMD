set terminal pngcairo enhanced size 1000, 600
set output "3d.png"

unset x2tics
unset mx2tics
unset y2tics

unset key
set pm3d
set pm3d map
set size square
set pm3d interpolate 0,0
set xrange [138:180]
set yrange [-180:180]
set border 0
set xtics border 10
set ytics border 60
set palette rgbformulae 22,13,-31
splot 'my3d.dat' with im title ""

set output


