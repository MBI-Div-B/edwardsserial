# Contributing to edwardsserial
Thanks you for considering a contribution to `edwardsserial`. You can help to improve this software regardless of you programming experience! All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome. 

[[_TOC_]]

## Bug reports

If you find a bug, please create a new issue with the [bug report template](https://gitlab.com/codingcoffeebean/edwardsserial/-/issues/new?issuable_template=Bug).
Describe the bug and attach relevant logs or screenshots if possible.

## Getting started
We use the label ~"Good first issue" for smaller issues that are well suited for beginners.
If you want to improve the documentation look for issues labeled with ~"Documentation".

When you want to work on an issue, please open a new merge request and mention one of the core developers to review you changes.

## Development
If you want to work on the code, please read through the following guidelines for a clean code base.

### Dependency Management
We use [poetry](https://python-poetry.org) for dependency management. To install poetry, please refer to their [documentation](https://python-poetry.org/docs/#installation).

 To install your development environment with all neccessary dependencies run
```sh
poetry install
```

### Testing
Please write unittests if you add new features.
All tests located in the `tests` directory are automatically tested when pushing to Gitlab.

To run them manually use:
```sh
poetry run pytest -x tests
```
or simply
```bash
make test
```

### Typing
We strongly encourage the use of [type hints](https://docs.python.org/3/library/typing.html) and use 
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat"></a> as static type checker.

```sh
poetry run mypy edwardsserial
```
or simply
```sh
make mypy
```

### Code Style
We use <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>. Please have a look at their [documentation](https://black.readthedocs.io/en/stable/#) for details. 
You can format the code by running
```sh
poetry run black .
```
or simply
```sh
make black
```

### pre-commit
To make it simple to adhere to our development guidelines we recommend to use [pre-commit](https://pre-commit.com) to run the above checks before each commit to ensure you only commit clean code.
To use it, you only have to run 
```sh
poetry run pre-commit install
```
once for the project.




