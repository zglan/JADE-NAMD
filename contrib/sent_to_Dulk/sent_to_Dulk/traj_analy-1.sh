#/bin/sh
# This script is used to extract geometry parameters as function of simulation time of each trajectory.
# [1] geoman.py is used to ectract the changing of bond-bond distances or angles or dihedral angles with time
# [2] The first three rows of data files we have extracted are factors, so we use sed command to delete them and use paste command 
#       to subsequent lines of files with same styles. awk command is also used to select lines you need.
# [3] Using traj_plot.sh to plot data.



  traj=200
  current=$PWD
      rm -r traj_results-1
      mkdir traj_results-1
      cp plot_dihdral-1 traj_results-1/
      cp plot_distance traj_results-1/
  
    for  ((  m = 1 ;  m <= $traj ;  m++  ))
     do 

       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"
       cd run000$m

#    Extracting parameters    
       ./geoman.py -d 4 2 3 1       traj.out >   dih_4_2_3_1_$m.dat

#    Deleting first 3 rows and selecting lines 
       sed '1,3d' dih_4_2_3_1_$m.dat         >dih_4_2_3_1.dat
       cd $current

#   Ploting 
       cp ./run000$m/dis_1_2.dat           traj_results-1/
       cp ./run000$m/dih_4_2_3_1.dat       traj_results-1/

       cd traj_results-1/

       gnuplot < plot_dihdral-1
       cp dihedral.eps  en_000$m.eps

       gnuplot < plot_distance
       cp distance.eps en_total_000$m.eps
       cd $current

       fi



       if [ $m -ge 10  ]
       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
       cd run00$m

#    Extracting parameters    
       ./geoman.py -d 4 2 3 1       traj.out >   dih_4_2_3_1_$m.dat

#    Deleting first 3 rows and selecting lines 
       sed '1,3d' dih_4_2_3_1_$m.dat         >dih_4_2_3_1.dat
       cd $current

#   Ploting 
       cp ./run00$m/dis_1_2.dat           traj_results-1/
       cp ./run00$m/dih_4_2_3_1.dat       traj_results-1/

       cd traj_results-1/

       gnuplot < plot_dihdral-1
       cp dihedral.eps  en_00$m.eps

       gnuplot < plot_distance
       cp distance.eps en_total_00$m.eps
 
      cd $current

       fi
       fi



       if [ $m -ge 100  ]
       then
       echo "RUN0$m"
       cd run0$m

#    Extracting parameters    
       ./geoman.py -d 4 2 3 1       traj.out >   dih_4_2_3_1_$m.dat

#    Deleting first 3 rows and selecting lines 
       sed '1,3d' dih_4_2_3_1_$m.dat         >dih_4_2_3_1.dat
       cd $current

#   Ploting 
       cp ./run0$m/dis_1_2.dat           traj_results-1/
       cp ./run0$m/dih_4_2_3_1.dat       traj_results-1/

       cd traj_results-1/

       gnuplot < plot_dihdral-1
       cp dihedral.eps  en_0$m.eps

       gnuplot < plot_distance
       cp distance.eps en_total_0$m.eps

       cd $current
       fi


     done
