#!/bin/bash

    for ((m=1;m<=108;m++))
    do
    if [ $m -lt 10 ]

       then
       echo "RUN000$m"                                                        >>ci_opt_complete.log
       tail -n20 RUN000$m/ci_opt/ci_opt_$m.log                                >>ci_opt_complete.log
       fi


       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"                                                        >>ci_opt_complete.log
       tail -n20 RUN00$m/ci_opt/ci_opt_$m.log                                >>ci_opt_complete.log
      fi
      fi

     if [ $m -ge 100 ]

       then
      echo "RUN0$m"                                                         >>ci_opt_complete.log
      tail -n20 RUN0$m/ci_opt/ci_opt_$m.log                                 >>ci_opt_complete.log
     fi
    done

