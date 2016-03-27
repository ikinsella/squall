MREV=R2014b
MCC=/usr/local/MATLAB/$(MREV)/bin/mcc
MEX=/usr/local/MATLAB/$(MREV)/bin/mex
MFLAGS=-mv -R -singleCompThread -R -nodisplay -R -nojvm
SRCDIR=.
IDIRS=
.PHONY: clean all

all: proxSortedL1Mex.mexa64

proxSortedL1Mex.mexa64:
$(MEX) proxSortedL1Mex.c proxSortedL1.c

clean:
-rm *.dmr
-rm _condor_std???
-rm readme.txt
-rm mccExcludedFiles.log
