V=./venv

all: de_DE en_US it_IT

venv: $(V)/touchfile

$(V)/touchfile: requirements.txt
	test -d $(V) || python3 -m venv $(V)
	. $(V)/bin/activate ; python3 -m pip install --upgrade pip
	. $(V)/bin/activate ; pip install -Ur requirements.txt
	touch $@

activate:
	. $(V)/bin/activate && exec bash

deactivate:
	$(V)/bin/deactivate

NEXT_YEAR=$$(( `date +%Y` + 1 ))
YEAR=$(NEXT_YEAR)

de_DE:
	. $(V)/bin/activate ; python ./mennorode.py --first=0 --locale=$@ $(YEAR)

en_US:
	. $(V)/bin/activate ; python ./mennorode.py --first=6 --locale=$@ $(YEAR)

it_IT:
	. $(V)/bin/activate ; python ./mennorode.py --first=0 --locale=$@ $(YEAR)


