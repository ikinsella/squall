#!/bin/bash
# Usage: 1st arg name of batch directory followin standard format
# copy batch directory to submit node
scp -r $1/ ikinsella@submit-5.chtc.wisc.edu:~/
# On the Submit Node: Use make file to tarzip sourcecode and send it to a build node in an interactive job
# On the Build Node: Use script and make file to automate compilation, cleanup. tarzipped binaries will be sent back to submit node
ssh ikinsella@submit-5.chtc.wisc.edu "cd $1; make sdist; condor_submit -i interactive_build.sub < ./condor_compile.sh"
# Copy tarzipped binaries from submit node to working directory
scp ikinsella@submit-5.chtc.wisc.edu:~/$1/binaries.tar.gz $1/
# Remove everything which was added to the submit node
ssh ikinsella@submit-5.chtc.wisc.edu "rm -rf $1"
