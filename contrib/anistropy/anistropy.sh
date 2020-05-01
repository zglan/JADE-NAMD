#!/bin/sh
#for mydir in *
#do  
#cd $mydir
#cp ../ana_tur_tool.py .
#python ana_tur_tool.py
#cd ..
#done
num=`ls ./*/anistropy.dat | wc -l`
ls ./*/anistropy.dat | xargs paste > anix.dat
cat << EOF > plot.awk
{  \$$[2*$num+1] = 0;
   for (i=1;i<=$num;i++)
   \$$[2*$num+1] = \$$[2*$num+1] + \$(2*i);
   \$$[2*$num+1] = \$$[2*$num+1]/$num
   print;
}
EOF

awk -f plot.awk anix.dat > ani.dat
gnuplot << EOF


set terminal jpeg  enhanced 
set output "anistropy.jpg"

set xtics nomirror
unset x2tics 
set ytics nomirror
unset y2tics 
set xlabel 'Time (fs)'
set ylabel 'Anistropy'
set xtics 30


#set terminal postscript color  enhanced
#set output "anix.eps"

plot "ani.dat" u 1:$[2*$num+1] w l
set output
quit
EOF

