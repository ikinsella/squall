#!/bin/bash
#
# Setup Matlab Runtime Environment on Condor
#
echo "------------------------------------------"
echo Setting up environment variables
MCRROOT="v82"
echo ---
LD_LIBRARY_PATH=.:${MCRROOT}/runtime/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/bin/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/os/glnxa64;
XAPPLRESDIR=${MCRROOT}/X11/app-defaults ;
export XAPPLRESDIR;
export LD_LIBRARY_PATH;
echo LD_LIBRARY_PATH is ${LD_LIBRARY_PATH};
echo "------------------------------------------"
