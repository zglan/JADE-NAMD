#/bin/sh



      export FSHOME=/ns80th/nas/users/lan

       traj=120

      rm -r ./*/MD_data*

 
      for  ((  m = 1 ;  m <= $traj ;  m++  ))
     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"

       cd ./run000$m 
    
       qsub $FSHOME/bin/mndo/extr

       cd ..

       fi

       if [ $m -ge 10 ]       
       then
       if [ $m -lt 100 ] 
       then
       echo "RUN00$m"

       cd ./run00$m

       qsub $FSHOME/bin/mndo/extr

       cd ..
       
       fi
       fi




        if [ $m -ge 100 ]

       then
       echo "RUN0$m"

       cd ./run0$m

        qsub $FSHOME/bin/mndo/extr

       cd ..

       fi


     done
