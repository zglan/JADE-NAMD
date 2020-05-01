#!/bin/bash
# This script is used to test whether the ci optimization has been successfully finished.
# Zhuang Sep. 2012 

   for ((m=1;m<=187;m++))
    do
    if [ $m -lt 10 ]

       then
     echo "RUN000$m"                                                                    >>ci_opt_S2.log
#       tail -n20 RUN000$m/ci_opt.log                                 >>ci_opt_finish.log
     grep "State  2" RUN000$m/ci_opt.log|tail -n1                                       >>ci_opt_S2.log
       fi


       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
      echo "RUN00$m"                                                                    >>ci_opt_S2.log
#       tail -n20 RUN00$m/ci_opt.log                                 >>ci_opt_finish.log
    grep "State  2" RUN00$m/ci_opt.log|tail -n1                                       >>ci_opt_S2.log 
     fi
      fi

     if [ $m -ge 100 ]

       then
    echo "RUN0$m"                                                                    >>ci_opt_S2.log
#     tail -n20 RUN0$m/ci_opt.log                                 >>ci_opt_finish.log
    grep "State  2" RUN0$m/ci_opt.log|tail -n1                                       >>ci_opt_S2.log
     fi
    done

