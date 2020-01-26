all: requirements test doc bdist

package_name:=edwardsserial

doc:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); cd doc; make html

upload-doc:
	@cd doc; make upload

bdist:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); python3 setup.py bdist_wheel

test:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); py.test  --log-level=INFO --no-cov-on-fail --cov $(package_name) --cov-report term-missing --cov-report=html src/tests

mypy:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); mypy src

pylint:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); pylint src/$(package_name)


black:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); black src

pydocstyle:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); pydocstyle --convention=numpy src/$(package_name)

all-tests: mypy test pylint

clean:
	@rm -r dist/ build/
	cd doc; make clean

.PHONY: test doc all
