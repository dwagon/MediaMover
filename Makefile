PROJECT := media_mover
VENV    := ${WORKON_HOME}/${PROJECT}

all: ci

ci:
	docker build -t ${PROJECT} .
	docker run -v `pwd`/dist:/dist -it ${PROJECT} make test

test:
	${VENV}/bin/python ./setup.py test

pex:
	${VENV}/bin/pip install pex
	${VENV}/bin/python ./setup.py bdist_pex --pex-args '-v'

artifact_pex:
	docker build -t ${PROJECT} .
	docker run -v `pwd`/dist:/dist -it ${PROJECT} make pex

venv:
	python3 -m venv ${VENV}
	${VENV}/bin/pip install wheel
	${VENV}/bin/pip install -r requirements.txt
