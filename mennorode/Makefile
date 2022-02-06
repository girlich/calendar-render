V=./venv

all:

venv: $(V)/touchfile

$(V)/touchfile: requirements.txt
	test -d $(V) || python3 -m venv $(V)
	. $(V)/bin/activate; pip install -Ur requirements.txt
	touch $@

activate:
	bash -c source $(V)/bin/activate

deactivate:
	$(V)/bin/deactivate

test:
	. $(V)/bin/activate ; python ./mennorode.py 2022

