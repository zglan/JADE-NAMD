#/bin/sh

      

     for  ((  m = 1 ;  m <= 120;  m++  ))

     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"
       

       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run000$m/mndo.inp ./run000$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run000$m/dynvar.in ./run000$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run000$m/hopping.out ./run000$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run000$m/traj.out    ./run000$m/


       fi

       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run00$m/mndo.inp     ./run00$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run00$m/dynvar.in    ./run00$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run00$m/hopping.out  ./run00$m/
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run00$m/traj.out     ./run00$m/


       fi
       fi



       if [ $m -ge 100 ]

       then
       echo "RUN0$m"
     
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run0$m/mndo.inp    ./run0$m/mndo.inp
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run0$m/dynvar.in   ./run0$m/dynvar.in
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run0$m/hopping.out ./run0$m/hopping.out
       cp /ns80th/nas/users/youlue/PUBLIC/LAN/DMN/finished/run0$m/traj.out    ./run0$m/


      fi




     done


