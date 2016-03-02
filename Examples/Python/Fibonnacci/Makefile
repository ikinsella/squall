# Reusable Input Parameters
PDIST=Python-2.7
PBIN=python2
WRAPPER=fibwrapper.py
COMPILE=condor_compile.sh
SUBMIT=interactive_build.sub
# Architecture Dependent Parameters
SRC=src
DEP=dependencies
REQ=requirements.txt
SETUP=$(DEP)/setup.sh
PYTAR=$(DEP)/$(PDIST)

# Targets & Recipes
.PHONY: clean postbuild binaries.tar.gz setup.sh executable extract sdist all

all: extract distribution binary pip requirements binaries.tar.gz postbuild clean

sdist: $(DEP)/$(COMPILE) $(DEP)/$(SUBMIT)
	-tar czf source_code.tar.gz Makefile $(WRAPPER) $(SETUP) $(PYTAR) $(DEP)/$(REQ)
	-cp $^ .

extract:
	-mkdir source_code/
	-tar xzf source_code.tar.gz -C ./source_code/

distribution: $(PDIST).tgz 
	-tar xzf $<
	-cd $(PDIST)
	-./configure --prefix=$(pwd)/../python
	-make
	-make install

binary: python/bin/$(PBIN)
	-cp $< python/bin/python

pip:
	-export PATH=$(pwd)/python/bin:$PATH
	-wget http://link.to.get-pip.py

requirements: $(REQ) pip
	-pip install -r $<
	-tar -czvf python.tar.gz python/

binaries.tar.gz: $(WRAPPER) $(SETUP) python.tar.gz
	-mkdir bin/
	-mv $^ bin/
	-tar czvf $@ bin/

postbuild: binaries.tar.gz
	-cp binaries.tar.gz ../

clean:
	-rm source_code.tar.gz
	-rm _condor_std???
	-rm Makefile
