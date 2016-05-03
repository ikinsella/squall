# Project Dependent Parameters
RDIST=R-3.2.5
WRAPPER=FibWrapper
DIR=RFib
DTAR=$(DIR).tar.gz

# Reusable Input Parameters -- Shouldn't Change If Following Project Structure Guidelines
# SRC - List of Custom Modules ie. SRC=A B C
# DEP - Directory containing project Dependencies ie. submit files, python tarball, setup script, ect.
# SRC - Name of setup script
# REQ - Name of requirements file
# SUBMIT - Name of interactive build submit file
# PTAR - Name of python distribution tarball ie. Python-2.7.tgz
# SRCTAR - Name of package which will be shipped to interactive build
# PIP - Link to get-pip.py
# PROJ - Full path to project directory where make is being run
# DIR - Name of project (top level directory)
SRC=Src
DEP=Dependencies
SETUP=$(DEP)/setup.sh
REQ=$(DEP)/requirements.R
SUBMIT=$(DEP)/interactive_build.sub
RTAR=$(DEP)/$(RDIST).tar.gz
RWRAPPER=$(DEP)/RWrapper
SRCTAR=source_code.tar.gz
PROJ=`pwd`

# Targets & Recipes
.PHONY: $(RTAR) RSCRIPT $(DTAR) $(SETUP) $(WRAPPER) $(RWRAPPER) $(REQ) clean postbuild extract sdist enode snode condor submit distribution all

all: condor postbuild

condor:
	-scp -r $(PROJ) $(CHTC_USER)@$(SUBMIT_NODE):~/
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "cd $(DIR); make snode;"

snode: sdist submit

sdist:
	-tar czvf $(SRCTAR) $(WRAPPER) $(SETUP) $(RTAR) $(REQ) $(SRC) $(RWRAPPER)

submit: $(SUBMIT)
	-mkdir log
	-cp $< .
	-condor_submit -i interactive_build.sub SRCTAR=$(SRCTAR) <<< "make enode"

enode: extract $(RTAR) $(REQ) RSCRIPT $(DIR) $(DTAR)

extract:
	-tar xzf $(SRCTAR)

$(RTAR):
	-mkdir R
	-tar xvzf $@
	-cd $(RDIST); ./configure --prefix="`pwd`"; make; make install

$(REQ):
	-$(RDIST)/lib64/R/bin/Rscript $@
	-mv $(RDIST)/lib64/R ./

RSCRIPT: $(RWRAPPER)
	-sed -i.bak 's:R_HOME_DIR=/.*:R_HOME_DIR=$$(pwd)/R:' R/bin/R
	-mv $< R/bin/

$(DIR): $(WRAPPER) $(SETUP) $(SRC)
	-mkdir $@
	-mv $^ $@/

$(DTAR): R/ $(DIR)/
	-tar czvf $@ $^

clean: $(DTAR)
	-rm $(SRCTAR)
	-rm _condor_std???
	-rm Makefile
	-exit

postbuild:
	-echo "Sleeping so condor file transfer can complete..."
	-sleep 60
	-scp $(CHTC_USER)@$(SUBMIT_NODE):~/$(DIR)/$(DTAR) $(PROJ)/$(DTAR)
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "yes|rm -rf $(DIR)"
	-echo "SUCCESS! Packaged distribution placed in: $(PROJ)/$(DTAR)"
