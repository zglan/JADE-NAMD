#!/bin/bash
# This script is used to extract geometries from ci_mndo_stru file to every directories. 

    for ((m=1;m<=187;m++))
    do
    if [ $m -lt 10 ]

       then
       echo "RUN000$m"
       mkdir RUN000$m
       grep -A 13 "Point           $m" ci_mndo_stru >  RUN000$m/geometry.log
       fi


       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
        mkdir RUN00$m
       grep -A 13 "Point          $m" ci_mndo_stru >  RUN00$m/geometry.log
      fi
      fi

     if [ $m -ge 100 ]

       then
       echo "RUN0$m"
        mkdir RUN0$m
      grep -A 13 "Point         $m" ci_mndo_stru >  RUN0$m/geometry.log 
     fi
  
    done

