#/bin/sh

   
       rm -r results
       mkdir results
      cp plot_gnuplot results/
      cp plot_total_energy results/
     for  ((  m = 1 ;  m <= 200;  m++  ))

     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"

#       rm ./result/E*.dat
       cp ./run000$m/MD_data/E*.dat ./results
       cp ./run000$m/stat.out ./results 
     
       cd ./results
       gnuplot < plot_gnuplot
       cp energy.eps  en_000$m.eps

       gnuplot < plot_total_energy
       cp total_energy.eps en_total_000$m.eps
       cd ..



       fi

       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
       
#       rm ./result/E*.dat
       cp ./run00$m/MD_data/E*.dat ./results
       cp ./run00$m/stat.out ./results
       cd ./results
       gnuplot < plot_gnuplot
       cp energy.eps  en_00$m.eps

       gnuplot < plot_total_energy
       cp total_energy.eps en_total_00$m.eps
       cd ..

       fi
      fi



       if [ $m -ge 100 ]

       then
       echo "RUN0$m"

#       rm ./result/E*.dat
       cp ./run0$m/MD_data/E*.dat ./results
       cp ./run0$m/stat.out ./results
       cd ./results
       gnuplot < plot_gnuplot
       cp energy.eps  en_0$m.eps
 
       gnuplot < plot_total_energy
       cp total_energy.eps en_total_0$m.eps
       cd ..


      fi




     done


