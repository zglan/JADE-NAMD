#/bin/sh

traj=100

for  ((  m = 1 ;  m <= $traj ;  m++  ))
    do 
        cd $m
        grep "Current state" log | awk '{print $3}' > t0
        echo "done $m"
        cd ..
     done


