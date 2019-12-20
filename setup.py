import codecs

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup

# Work around mbcs bug in distutils.
# Sebastian 2019-03-04: not sure whether this is still needed...
# http://bugs.python.org/issue10945
try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    func = lambda name, enc=ascii: {True: enc}.get(name == "mbcs")
    codecs.register(func)


pfile = Project(chdir=False).parsed_pipfile
install_requires = convert_deps_to_pip(pfile["packages"], r=False)
test_requirements = convert_deps_to_pip(pfile["dev-packages"], r=False)


if __name__ == "__main__":
    setup(use_scm_version=True, install_requires=install_requires)
