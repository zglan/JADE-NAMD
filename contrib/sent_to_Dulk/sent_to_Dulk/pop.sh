#/bin/sh



       traj=123

       present_dir=$PWD

       rm ./hopping_info

       for  ((  m = 1 ;  m <= $traj ;  m++  ))
       do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"
         echo "1 2"   >    ./pop/state.dat_$m
         cp ./run000$m/MD_data/state.dat  ./pop/state.dat_$m

       fi

       if [ $m -ge 10 ]        
       then
         if  [ $m -lt 100 ]
         then
         
          echo "RUN00$m"
            echo "1 2"   >    ./pop/state.dat_$m
            cp ./run00$m/MD_data/state.dat   ./pop/state.dat_$m

         fi
      fi


        if [ $m -ge 100 ]
        then

          echo "# RUN0$m"
          echo "1 2"   >    ./pop/state.dat_$m
          cp ./run0$m/MD_data/state.dat  ./pop/state.dat_$m

       fi


     done


