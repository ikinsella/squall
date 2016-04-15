.PHONY: docs test env

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"
	@echo "  mongo       run mongodb instance and install if not done already"
env:
	sudo easy_install pip; \
	pip install virtualenv; \
	virtual env; \
	source env/bin/activate; \
	make deps;	
deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	flake8 --exclude=env .
RESULT = $$(brew -v)
mongo:
	if [[ $$OSTYPE == darwin* ]]; then \
		echo $(RESULT); \
		if [[ $(RESULT) == "" ]]; then \
			ruby -e “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)”;\
		fi \
		brew update; \
		brew install mongodb; \
		sudo mkdir /data/db; \
		sudo chown `id -u` /data/db; \
	else \
		echo You are not on mac. Please install mongodb; \
	fi
test:
	py.test tests
