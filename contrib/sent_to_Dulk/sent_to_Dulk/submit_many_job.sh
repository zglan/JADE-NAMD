#/bin/sh


       traj=200

      for  ((  m = 1 ;  m <= $traj ;  m++  ))
     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"

       cd ./run000$m 
    
       rm *.e
       rm *.o
       rm *.log
       rm *.out
       rm fort*
       rm *.dat
       bsub -q simul -n 1 -o mndo.log -e mndo.err -i mndo.inp /home/simul/zhuang/program/myfirstmndo/mndo99
#      ~/MNDO/mndo99.x < mndo.inp > mndo.out &
#       $FSHOME/bin/mndo/qmndo99_dyna_fullnac mndo.inp 
#       $FSHOME/bin/mndo/qmndo99_dyna_newversion mndo.inp -l h_rt=900:00:00

       sleep 2
       cd ..

       fi

       if [ $m -ge 10 ]       
       then
       if [ $m -lt 100 ] 
       then
       echo "RUN00$m"

       cd ./run00$m

       rm *.e
       rm *.o
       rm *.log
       rm *.dat

       rm *.out
       rm fort*
       bsub -q simul -n 1 -o mndo.log -e mndo.err -i mndo.inp /home/simul/zhuang/program/myfirstmndo/mndo99
#      ~/MNDO/mndo99.x < mndo.inp > mndo.out &
#       $FSHOME/bin/mndo/qmndo99_dyna_newversion mndo.inp -l h_rt=900:00:00
#       $FSHOME/bin/mndo/qmndo99_dyna_fullnac mndo.inp 
       sleep 2

       cd ..
       
       fi
       fi




        if [ $m -ge 100 ]

       then
       echo "RUN0$m"

       cd ./run0$m

       rm *.e
       rm *.o
       rm *.log

       rm *.out
       rm fort*
       bsub -q simul -n 1 -o mndo.log -e mndo.err -i mndo.inp /home/simul/zhuang/program/myfirstmndo/mndo99
#      ~/MNDO/mndo99.x < mndo.inp > mndo.out &
#       $FSHOME/bin/mndo/qmndo99_dyna_newversion mndo.inp -l h_rt=900:00:00
#        $FSHOME/bin/mndo/qmndo99_dyna_fullnac mndo.inp
       sleep 2
       cd ..

       fi


     done
