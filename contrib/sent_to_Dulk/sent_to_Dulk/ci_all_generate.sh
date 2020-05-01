#!/bin/bash

    for ((m=1;m<=200;m++))
    do
	     if [ $m -lt 10 ]

	     then
	  echo "run000$m"
	  cat run000$m/ci_qm.xyz >> ci_opt/ci_all.xyz
    fi
    if [ $m -ge 10 ]
    then
       if [ $m -lt 100 ]
       then
          echo "run00$m"
          cat run00$m/ci_qm.xyz >> ci_opt/ci_all.xyz
       fi
     fi

     if [ $m -ge 100 ]
     then
           echo "run0$m"
           cat run0$m/ci_qm.xyz >> ci_opt/ci_all.xyz
     fi
     done

