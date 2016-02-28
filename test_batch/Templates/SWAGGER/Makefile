MREV=R2014b
MCC=/usr/local/MATLAB/$(MREV)/bin/mcc
MEX=/usr/local/MATLAB/$(MREV)/bin/mex
MFLAGS=-mv -R -singleCompThread -R -nodisplay -R -nojvm
SRC=src
SUB=$(SRC)/subroutines
DEP=dependencies
JSON=$(DEP)/jsonlab
INCL= -I $(SRC) -I $(JSON) -I $(SUB) -I 


all: Fib binaries.tar.gz

sdist:
	tar czhf source_code.tar.gz src dependencies ProxSortedL1

extract:
	-mkdir source_code/
	tar xzf source_code.tar.gz -C ./source_code/

Fib: $(SRC)/WholeBrain_MVPA.m
	$(MCC) $(MFLAGS) $(INCL) -o $@ $^


binaries.tar.gz: WholeBrain_RSA run_WholeBrain_RSA.sh
	mkdir bin/
	mv WholeBrain_RSA WholeBrain_RSA.sh bin/
	tar czvf $@ bin/


clean:
	-rm *.dmr
	-rm _condor_std???
	-rm readme.txt
	-rm mccExcludedFiles.log

clean-all: binaries.tar.gz
	rm -rf src/ bin/
