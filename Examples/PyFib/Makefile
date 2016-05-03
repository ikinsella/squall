# Project Dependent Parameters
PDIST=Python-2.7
PBIN=python2.7
WRAPPER=FibWrapper
DIR=PyFib
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
REQ=$(DEP)/requirements.txt
SUBMIT=$(DEP)/interactive_build.sub
PTAR=$(DEP)/$(PDIST).tgz
SRCTAR=source_code.tar.gz
PIP=https://bootstrap.pypa.io/get-pip.py
PROJ=`pwd`

# Targets & Recipes
.PHONY: $(PBIN) $(PTAR) $(DTAR) $(SETUP) $(WRAPPER) $(REQ) clean postbuild extract sdist enode snode condor submit distribution all

all: condor postbuild

condor:
	-scp -r $(PROJ) $(CHTC_USER)@$(SUBMIT_NODE):~/
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "cd $(DIR); make snode;"

snode: sdist submit

sdist:
	-tar czvf $(SRCTAR) $(WRAPPER) $(SETUP) $(PTAR) $(REQ) $(SRC)

submit: $(SUBMIT)
	-mkdir log
	-cp $< .
	-condor_submit -i interactive_build.sub SRCTAR=$(SRCTAR) <<< "make enode"

enode: extract $(PTAR) $(PBIN) $(REQ) $(DIR) $(DTAR)

extract:
	-tar xzf $(SRCTAR)

$(PTAR):
	-mkdir python
	-tar xvzf $@
	-cd $(PDIST); ./configure --prefix="`pwd`/../python"; make; make install

$(PBIN): python/bin/$(PBIN)
	-cp $< python/bin/python

$(REQ):
	-wget $(PIP)
	-python/bin/python get-pip.py
	-python/bin/pip install -r $@

$(DIR): $(WRAPPER) $(SETUP) $(SRC)
	-mkdir $@
	-mv $^ $@/

$(DTAR): python/ $(DIR)/
	-tar czvf $@ $^

clean: $(DTAR)
	-rm $(SRCTAR)
	-rm get-pip.py
	-rm _condor_std???
	-rm Makefile
	-exit

postbuild:
	-echo "Sleeping so condor file transfer can complete..."
	-sleep 60
	-scp $(CHTC_USER)@$(SUBMIT_NODE):~/$(DIR)/$(DTAR) $(PROJ)/$(DTAR)
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "yes|rm -rf $(DIR)"
	-echo "SUCCESS! Packaged distribution placed in: $(PROJ)/$(DTAR)"
