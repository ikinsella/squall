# Project Dependent Parameters
PDIST=Python-2.7
PBIN=python2
WRAPPER=FibWrapper.py
DTAR=PyFib.tar.gz

# Reusable Input Parameters -- Shouldn't Change If Following Project Structure Guidelines
# SRC - List of Custom Modules ie. SRC=A B C
# DEP - Directory containing project Dependencies ie. submit files, python tarball, setup script, ect.
# SRC - Name of setup script
# REQ - Name of requirements file
# SUBMIT - Name of interactive build submit file
# PTAR - Name of python distribution tarball ie. Python-2.7.tgz
# SRCTAR - Name of package which will be shipped to interactive build
# PROJ - Full path to project directory where make is being run
# DIR - Name of project (top level directory)
SRC=Src
DEP=Dependencies
SETUP=setup.sh
REQ=requirements.txt
SUBMIT=interactive_build.sub
PTAR=$(PDIST).tgz
SRCTAR=source_code.tar.gz
PROJ=`pwd`
DIR=`pwd|sed 'sA.*/AA'`

# Targets & Recipes
.PHONY: $(PBIN) $(DTAR) $(SETUP) $(WRAPPER) clean postbuild extract sdist enode snode condor submit distribution all

all: condor postbuild

condor:
	-scp -r $(PROJ) $(CHTC_USER)@$(SUBMIT_NODE):~/
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "cd $(DIR); make snode DIR=$(DIR);"

snode: sdist submit

sdist:
	-tar czvf $(SRCTAR) $(WRAPPER) $(DEP)/$(SETUP) $(DEP)/$(PTAR) $(DEP)/$(REQ) $(SRC)

submit: $(DEP)/$(SUBMIT)
	-mkdir log
	-cp $< .
	-condor submit -i interactive_build.sub <<< "make enode DIR=$(DIR)"

enode: extract $(PTAR) $(PBIN) $(REQ) $(DIR) $(DTAR) clean

extract:
	-tar xzf $(SRCTAR)

$(PTAR): $(PTAR)
	-mkdir python
	-tar xvzf $<
	-cd $(PDIST)
	-./configure --prefix=$(pwd)/../python
	-make
	-make install

$(PBIN): python/bin/$(PBIN)
	-cp $< python/bin/python

$(REQ): $(REQ) pip
	-pip install -r $@

pip:
	-export PATH=$(pwd)/python/bin:$PATH
	-wget http://link.to.get-pip.py

$(DIR): $(WRAPPER) $(SETUP) $(SRC)
	-mkdir $@
	-mv $^ $@/

$(DTAR): python/ $(DIR)/
	-tar czvf $@ $^

clean: $(DTAR)
	-rm $(SRCTAR)
	-rm $(PTAR)
	-rm _condor_std???
	-rm Makefile
	-exit

postbuild:
	-scp $(CHTC_USER)@$(SUBMIT_NODE):~/$(DIR)/$(DTAR) $(PROJ)/$(DTAR)
	-ssh $(CHTC_USER)@$(SUBMIT_NODE) "yes|rm -rf $(DIR)"
	-echo "SUCCESS! Packaged distribution placed in: $(PROJ)/$(DTAR)"
