#/bin/sh


  traj=200


      rm ./internal/angle_ci.dat
      rm ./internal/ci_all.xyz
      rm ./*/ci_qm.xyz
      for  ((  m = 1 ;  m <= $traj ;  m++  ))
   


     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"


        
       cp ./ci_stru.exe   ./run000$m/ci_stru.exe
       cd ./run000$m/
       cp ./MD_data/state.dat state.dat
       ./ci_stru.exe 
       cd ..
     
#       ./geoman.py -d 1 9 10 11  ./run000$m/ci_qm.xyz >>   ./run000$m/angle_ci.dat


#       echo "#   traj000$m"            >>  ./internal/angle_ci.dat
#        head -n2 ./run000$m/ci_qm.xyz >  ./internal/tmp
#        tail -n1 ./internal/tmp       >>  ./internal/angle_ci.dat
#        tail -n1 ./run000$m/angle_ci.dat >>  ./internal/angle_ci.dat 
# 
#        cat ./run000$m/ci_qm.xyz   >> ./internal/ci_all.xyz


       fi

       if [ $m -ge 10  ]
       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"

       cp ./ci_stru.exe   ./run00$m/ci_stru.exe 
       cd ./run00$m/
       cp ./MD_data/state.dat state.dat
       ./ci_stru.exe
       cd ..

#      ./geoman.py -d 1 9 10 11  ./run00$m/ci_qm.xyz >>   ./run00$m/angle_ci.dat
# 
#        echo "#   traj00$m"            >>  ./internal/angle_ci.dat
#        head -n2 ./run00$m/ci_qm.xyz >  ./internal/tmp
#        tail -n1 ./internal/tmp       >>  ./internal/angle_ci.dat
#        tail -n1 ./run00$m/angle_ci.dat >>  ./internal/angle_ci.dat
#
#        cat ./run00$m/ci_qm.xyz   >> ./internal/ci_all.xyz



       fi
       fi



       if [ $m -ge 100  ]
       then
       echo "RUN0$m"

       cp ./ci_stru.exe   ./run0$m/ci_stru.exe
       cd ./run0$m/
       cp ./MD_data/state.dat state.dat
       ./ci_stru.exe
       cd ..
 
#       ./geoman.py -d 1 9 10 11  ./run0$m/ci_qm.xyz >>   ./run0$m/angle_ci.dat
#
#
#        echo "#   traj0$m"            >>  ./internal/angle_ci.dat
#        head -n2 ./run0$m/ci_qm.xyz >  ./internal/tmp
#        tail -n1 ./internal/tmp       >>  ./internal/angle_ci.dat
#        tail -n1 ./run0$m/angle_ci.dat >>  ./internal/angle_ci.dat
#
#        cat ./run0$m/ci_qm.xyz   >> ./internal/ci_all.xyz


       fi


     done
