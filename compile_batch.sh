#!/bin/bash
scp -r $1/ ikinsella@submit-5.chtc.wisc.edu:~/
ssh ikinsella@submit-5.chtc.wisc.edu "cd $1; make sdist; condor_submit -i interactive_build.sub < ./condor_compile.sh"
scp ikinsella@submit-5.chtc.wisc.edu:~/$1/binaries.tar.gz $1/ 
