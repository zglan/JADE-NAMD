#!/bin/bash
# This script is used to generate input files to calculate CI optimization.
# Zhuang Jun.2012

    current=$PWD
    for ((m=1;m<=187;m++))
    do
    if [ $m -lt 10 ]

    then
       echo "RUN000$m"
       cd RUN000$m
       rm ci_opt.inp
   
       echo "iop=-6 jop=0 igeom=1 iform=1 nsav13=2 nsav7=4 +"                  > ci_opt.inp
       echo "icuts=-1 icutg=-1 iscf=11 iplscf=11 dstep=0.00001 +"             >> ci_opt.inp
       echo "iprint=1 mprint=1 iprec=100 kitscf=5000 +"                       >> ci_opt.inp
       echo " imult=1 icross=5 ncigrd=2 ief=1 lrscal=1 dmax=0.1 +"            >> ci_opt.inp
       echo "kci=5 ioutci=2 maxrtl=5000 +"                                    >> ci_opt.inp
       echo "imomap=1 +"                                                      >> ci_opt.inp
       echo "movo=1 ici1=6 ici2=3 nciref=3 mciref=0 levexc=2 iroot=3 iuvcd=2" >> ci_opt.inp
       echo "CI optimization calculation by OM2."                             >> ci_opt.inp
       echo ""                                                                >> ci_opt.inp
       tail -n12 geometry.log                                                 >> ci_opt.inp
       echo "0   0.0 0    0.0 0    0.0 0"                                     >> ci_opt.inp
       echo "14 15 16 17 18 19 20 21 22"                                      >> ci_opt.inp
       echo "1  2 "                                                           >> ci_opt.inp
       echo "0.00010   1.00000 "                                              >> ci_opt.inp
       echo "0 "                                                              >> ci_opt.inp

       
#       mndo99 <ci_opt_$m.inp> ci_opt_$m.log
     bsub -q simul -n 1 -o ci_opt.log -e ci_opt.err -i ci_opt.inp /home/simul/zhuang/program/myfirstmndo/mndo99
     cd $current
       
     fi
       if [ $m -ge 10 ]
       then
         if [ $m -lt 100 ]
         then
         echo "RUN00$m"
	  cd RUN00$m
          rm ci_opt.inp
	  
	  echo "iop=-6 jop=0 igeom=1 iform=1 nsav13=2 nsav7=4 +"                  > ci_opt.inp
          echo "icuts=-1 icutg=-1 iscf=11 iplscf=11 dstep=0.00001 +"             >> ci_opt.inp
	  echo "iprint=1 mprint=1 iprec=100 kitscf=5000 +"                       >> ci_opt.inp
	  echo " imult=1 icross=5 ncigrd=2 ief=1 lrscal=1 dmax=0.1 +"            >> ci_opt.inp
          echo "kci=5 ioutci=2 maxrtl=5000 +"                                    >> ci_opt.inp
	  echo "imomap=1 +"                                                      >> ci_opt.inp
	  echo "movo=1 ici1=6 ici2=3 nciref=3 mciref=0 levexc=2 iroot=3 iuvcd=2" >> ci_opt.inp
	  echo "CI optimization calculation by OM2."                             >> ci_opt.inp
	  echo ""                                                                >> ci_opt.inp
	  tail -n12 geometry.log                                                 >> ci_opt.inp
	  echo "0   0.0 0    0.0 0    0.0 0"                                     >> ci_opt.inp
          echo "14 15 16 17 18 19 20 21 22"                                      >> ci_opt.inp
	  echo "1  2 "                                                           >> ci_opt.inp
	  echo "0.00010   1.00000 "                                              >> ci_opt.inp
	  echo "0 "                                                              >> ci_opt.inp
            
#	  mndo99 <ci_opt_$m.inp> ci_opt_$m.log
       bsub -q simul -n 1 -o ci_opt.log -e ci_opt.err -i ci_opt.inp /home/simul/zhuang/program/myfirstmndo/mndo99
       cd $current
	  
            fi
            fi
      
     if [ $m -ge 100 ]
      
             then
             echo "RUN0$m"
          cd RUN0$m
          rm ci_opt.inp
          
          echo "iop=-6 jop=0 igeom=1 iform=1 nsav13=2 nsav7=4 +"                  > ci_opt.inp
          echo "icuts=-1 icutg=-1 iscf=11 iplscf=11 dstep=0.00001 +"             >> ci_opt.inp
          echo "iprint=1 mprint=1 iprec=100 kitscf=5000 +"                       >> ci_opt.inp
          echo " imult=1 icross=5 ncigrd=2 ief=1 lrscal=1 dmax=0.1 +"            >> ci_opt.inp
          echo "kci=5 ioutci=2 maxrtl=5000 +"                                    >> ci_opt.inp
          echo "imomap=1 +"                                                      >> ci_opt.inp
          echo "movo=1 ici1=6 ici2=3 nciref=3 mciref=0 levexc=2 iroot=3 iuvcd=2" >> ci_opt.inp
          echo "S0 optimization calculation by OM2."                             >> ci_opt.inp
          echo ""                                                                >> ci_opt.inp
          tail -n12 geometry.log                                                 >> ci_opt.inp
          echo "0   0.0 0    0.0 0    0.0 0"                                     >> ci_opt.inp
          echo "14 15 16 17 18 19 20 21 22"                                      >> ci_opt.inp
          echo "1  2 "                                                           >> ci_opt.inp
          echo "0.00010   1.00000 "                                              >> ci_opt.inp
          echo "0 "                                                              >> ci_opt.inp
            
#            mndo99 <ci_opt_$m.inp> ci_opt_$m.log
       bsub -q simul -n 1 -o ci_opt.log -e ci_opt.err -i ci_opt.inp /home/simul/zhuang/program/myfirstmndo/mndo99
       cd $current
         
           fi

          done

