#! /bin/bash
# sampling shell input
rm linking.gjf
myfiles=`more myfiles.dat`

        for onefile in $myfiles;
        do cat $onefile >> linking.gjf;
        echo -e '\n--Link1--\n' >> linking.gjf;
        done
        
