#!/bin/bash

# This script is used to copy structures in conical intersection from MD directories to all_ci_xyz directory.
#Zhuang Jun. 2012

    for ((m=1;m<=129;m++))
    do
    if [ $m -lt 10 ]

       then
       echo "RUN000$m"
       cp ../run000$m/ci_qm.xyz all_ci_xyz/$m.xyz
       fi


       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
       cp ../run00$m/ci_qm.xyz all_ci_xyz/$m.xyz
      fi
      fi

     if [ $m -ge 100 ]

       then
       echo "RUN0$m"
       cp ../run0$m/ci_qm.xyz all_ci_xyz/$m.xyz
     fi

    done

