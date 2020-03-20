all: requirements test doc bdist

package_name:=edwardsserial

doc:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); cd doc; make html

upload-doc:
	@cd doc; make upload


test:
	py.test  --log-level=INFO --no-cov-on-fail --cov $(package_name) --cov-report term-missing --cov-report=html tests

mypy:
	python -m mypy .

pylint:
	pylint $(package_name)


black:
	python -m black .

pydocstyle:
	python -m pydocstyle --convention=numpy $(package_name)

all-tests: mypy test pylint

clean:
	@rm -r dist/ build/
	cd doc; make clean

.PHONY: test doc all
