#/bin/sh



       current=$PWD
       dire=$current

       traj=200

       for  ((  m = 1 ;  m <= $traj ;  m++  ))
       do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"


       echo "run000$m"                       >> test_hop.dat
       tail -n1   run000$m/state.dat         >> test_hop.dat

       fi

       if [ $m -ge 10 ]        
       then
         if  [ $m -lt 100 ]
         then
         
          echo "RUN00$m"
       echo "run00$m"                       >> test_hop.dat
       tail -n1   run00$m/state.dat         >> test_hop.dat

         fi
      fi


        if [ $m -ge 100 ]
        then

          echo "RUN0$m"
       echo "run0$m"                       >> test_hop.dat
       tail -n1   run0$m/state.dat         >> test_hop.dat

       fi


     done


