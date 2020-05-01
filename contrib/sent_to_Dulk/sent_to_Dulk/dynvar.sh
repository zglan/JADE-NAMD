#/bin/sh

   

     for  ((  m = 1 ;  m <= 123 ;  m++  ))

     do 
       if [ $m -lt 10 ]
       
       then
       echo "RUN000$m"

       cp dynvar.in ./run000$m/



       fi

       if [ $m -ge 10 ]

       then
       if [ $m -lt 100 ]
       then
       echo "RUN00$m"
      
       cp dynvar.in ./run00$m/
 

       fi
      fi



       if [ $m -ge 100 ]

       then
       echo "RUN0$m"

       cp dynvar.in ./run0$m/

      fi




     done


