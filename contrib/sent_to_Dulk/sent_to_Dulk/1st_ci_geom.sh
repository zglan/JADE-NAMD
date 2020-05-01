#/bin/sh

ci_qm.xyz

       current=$PWD
       dire=$current

       traj=200

       for  ((  m = 1 ;  m <= $traj ;  m++  ))
       do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"

      cp run000$m/ci_qm.xyz first_CI_geom/$m.xyz

       fi

       if [ $m -ge 10 ]        
       then
         if  [ $m -lt 100 ]
         then
         
          echo "RUN00$m"
     cp run00$m/ci_qm.xyz first_CI_geom/$m.xyz    
     fi
      fi


        if [ $m -ge 100 ]
        then

          echo "RUN0$m"
         cp run0$m/ci_qm.xyz first_CI_geom/$m.xyz
       fi


     done


