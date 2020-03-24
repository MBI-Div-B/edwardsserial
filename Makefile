all: requirements test doc bdist

package_name:=edwardsserial

doc:
	@export PYTHONPATH=`pwd`/src:$(PYTHONPATH); cd doc; make html

upload-doc:
	@cd doc; make upload


test:
	poetry run py.test  --log-level=INFO --no-cov-on-fail --cov $(package_name) --cov-report=term-missing --cov-report=html tests

mypy:
	poetry run mypy .

pylint:
	poetry run pylint $(package_name)


black:
	poetry run black .

pydocstyle:
	poetry run pydocstyle --convention=numpy $(package_name)

all-tests: mypy test pylint

clean:
	@rm -r dist/ build/
	cd doc; make clean

.PHONY: test doc all
