#/bin/sh



       traj=120

       present_dir=$PWD

       rm ./hopping_info

       for  ((  m = 1 ;  m <= $traj ;  m++  ))
       do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"
         cp ./adiapes.exe   ./run000$m/MD_data/
         cp ./adiapes_input ./run000$m/MD_data/
          cd ./run000$m/MD_data/
          rm ./hopping_info.dat
          rm ./adia_state.dat
          ./adiapes.exe < adiapes_input
          cd $present_dir
                    
          echo "# RUN000$m" >> ./hopping_info
          cat ./run000$m/MD_data/hopping_info.dat >> ./hopping_info

       fi

       if [ $m -ge 10 ]        
       then
         if  [ $m -lt 100 ]
         then
         
          echo "RUN00$m"

          cp ./adiapes.exe   ./run00$m/MD_data/
          cp ./adiapes_input ./run00$m/MD_data/

          cd ./run00$m/MD_data/
          rm ./hopping_info.dat
          rm ./adia_state.dat         
          ./adiapes.exe  < adiapes_input
          cd $present_dir

          echo "# RUN00$m" >> ./hopping_info
          cat ./run00$m/MD_data/hopping_info.dat >> ./hopping_info


         fi
      fi


        if [ $m -ge 100 ]
        then

          echo "# RUN0$m"


          cp ./adiapes.exe   ./run0$m/MD_data/
          cp ./adiapes_input ./run0$m/MD_data/

          cd ./run0$m/MD_data/
          rm ./hopping_info.dat
          rm ./adia_state.dat
          ./adiapes.exe < adiapes_input 
          cd $present_dir

          echo "RUN0$m" >> ./hopping_info
          cat ./run0$m/MD_data/hopping_info.dat >> ./hopping_info


       fi


     done


