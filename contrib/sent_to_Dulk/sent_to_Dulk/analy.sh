#/bin/sh



       current=$PWD
       dire=$current

       traj=200

       for  ((  m = 1 ;  m <= $traj ;  m++  ))
       do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"


#       mkdir run000$m

       cp MDextr.py   run000$m/MDextr.py
       cp mndotools.py run000$m/mndotools.py      
          
       cd run000$m 
    
          rm  -r ./MD_data

           chmod +x MDextr.py
          ./MDextr.py 
          

       cd ..




       fi

       if [ $m -ge 10 ]        
       then
         if  [ $m -lt 100 ]
         then
         
          echo "RUN00$m"

#           mkdir run00$m       
          cp MDextr.py   run00$m/MDextr.py
          cp mndotools.py run00$m/mndotools.py
          cd run00$m

          rm  -r ./MD_data
          chmod +x MDextr.py
         ./MDextr.py
         cd ..
         fi
      fi


        if [ $m -ge 100 ]
        then

          echo "RUN0$m"

#          mkdir run0$m
          cp MDextr.py   run0$m/MDextr.py
          cp mndotools.py run0$m/mndotools.py
          cd run0$m

          rm  -r ./MD_data

          chmod +x  MDextr.py
         ./MDextr.py
         cd ..
       fi


     done


