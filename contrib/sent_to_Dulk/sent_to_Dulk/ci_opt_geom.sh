#!/bin/bash
# This script is used to extract CI optimizing geometries.
# Zhuang Sep.2012  

    for ((m=1;m<=187;m++))
    do
    if [ $m -lt 10 ]
    
       then
#     echo "RUN000$m"                                              >>ci_opt_geom.log
#       cat RUN000$m/run000$m.xyz                                 >>ci_opt_geom.log
    tail -n14 RUN000$m/molden.dat                                 >>ci_opt_geom.log
       fi


       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
#       echo "RUN00$m"                                              >>ci_opt_geom.log
#       cat RUN00$m/run00$m.xyz                                  >>ci_opt_geom.log
   tail -n14 RUN00$m/molden.dat                                 >>ci_opt_geom.log 
     fi
      fi

     if [ $m -ge 100 ]

       then
#     echo "RUN0$m"                                              >>ci_opt_geom.log
#      cat RUN0$m/run0$m.xyz                                    >>ci_opt_geom.log
   tail -n14 RUN0$m/molden.dat                                 >>ci_opt_geom.log 
    fi
    done


