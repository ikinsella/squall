# Reusable Input Parameters
MREV=R2014b
MCC=/usr/local/MATLAB/$(MREV)/bin/mcc
MEX=/usr/local/MATLAB/$(MREV)/bin/mex
MFLAGS=-mv -R -singleCompThread -R -nodisplay -R -nojvm
SUBMIT=interactive_build.sub
SRCTAR=source_code.tar.gz
BINTAR=MatFib.tar.gz
SETUP_SCRIPT=setup.sh
EXE=executable
PROJ=`pwd`
DIR=`pwd|sed 'sA.*/AA'`

# Architecture Dependent Parameters
WRAPPER=FibWrapper.m
SRC=Src
DEP=Dependencies
JSON=$(DEP)/jsonlab
SETUP=$(DEP)/setupMCR
INCL=-I $(SRC) -I $(JSON)

# Targets & Recipes
.PHONY: clean postbuild $(BINTAR) $(SETUP_SCRIPT) $(EXE) extract sdist snode enode condor all

all: condor postbuild

condor:
	-scp -r $(PROJ) $(CHTC_USER)@$(SUBMIT_NODE):~/
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "cd $(DIR); make snode;"

snode: sdist submit

sdist:
	-tar czf $(SRCTAR) $(WRAPPER) $(SRC) $(DEP)

submit: $(DEP)/$(SUBMIT)
	-mkdir log
	-cp $< .
	-condor_submit -i interactive_build.sub SRCTAR=$(SRCTAR) <<< "make enode"

enode: extract $(BINTAR) clean

extract:
	-tar xvzf $(SRCTAR)

$(EXE): $(WRAPPER)
	$(MCC) $(MFLAGS) $(INCL) -o $@ $<

$(SETUP_SCRIPT): $(SETUP)/setup$(MREV).sh
	-cp $< $@

$(BINTAR): $(EXE) $(SETUP_SCRIPT)
	-mkdir bin/
	-mv $^ bin/
	-tar cvzf $@ bin/

clean: $(BINTAR)
	-rm $(SRCTAR)
	-rm $(WRAPPER)
	-rm _condor_std???
	-rm Makefile
	-rm run_executable.sh
	-rm readme.txt
	-rm *.log
	-exit

postbuild:
	-scp $(CHTC_USER)@$(SUBMIT_NODE):~/$(DIR)/$(BINTAR) $(PROJ)/$(BINTAR)
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "yes|rm -rf $(DIR)"
	-echo "SUCCESS! Compiled Binaries placed in: $(PROJ)/$(BINTAR)"
