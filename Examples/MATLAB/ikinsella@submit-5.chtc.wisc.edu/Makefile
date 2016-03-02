# Reusable Input Parameters
MREV=R2014b
WRAPPER=fibwrapper.m
# Architecture Dependent Parameters
SRC=src
SUB=$(SRC)/subroutines
DEP=dependencies
JSON=$(DEP)/jsonlab
SETUP=$(DEP)/setupMCR
INCL= -I $(SRC) -I $(JSON) -I $(SUB)
# Constants
MCC=/usr/local/MATLAB/$(MREV)/bin/mcc
MEX=/usr/local/MATLAB/$(MREV)/bin/mex
MFLAGS=-mv -R -singleCompThread -R -nodisplay -R -nojvm
# Targets & Recipes
.PHONY: clean postbuild binaries.tar.gz setup.sh executable extract sdist all

all: binaries.tar.gz postbuild

sdist:
	-tar czf source_code.tar.gz Makefile $(WRAPPER) $(SRC) $(DEP)

extract:
	-mkdir source_code/
	-tar xzf source_code.tar.gz -C ./source_code/
	-cd source_code/

executable: $(WRAPPER)
	$(MCC) $(MFLAGS) $(INCL) -o $@ $<

setup.sh: $(SETUP)/setup$(MREV).sh
	-cp $< $@

binaries.tar.gz: executable setup.sh
	-mkdir bin/
	-mv $^ bin/
	-tar czvf $@ bin/

postbuild: binaries.tar.gz
	-cp binaries.tar.gz ../

clean:
	-rm source_code.tar.gz
	-rm _condor_std???
	-rm Makefile
