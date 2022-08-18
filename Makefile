
.PHONY: test doc all mypy black pylint pydocstyle pylint
package_name:=edwardsserial

doc:
	@export PYTHONPATH=`pwd`:$(PYTHONPATH); cd doc; make html

upload-doc:
	@cd doc; make upload


test:
	poetry run pytest  --log-level=INFO --no-cov-on-fail --cov $(package_name) --cov-report=term-missing --cov-report=html tests

mypy:
	poetry run mypy .

pylint:
	poetry run pylint $(package_name)

black:
	poetry run black .

pydocstyle:
	poetry run pydocstyle --convention=numpy $(package_name)

codestyle: black pylint pydocstyle 

all-tests: mypy test

clean:
	@rm -r dist/ build/
	cd doc; make clean
