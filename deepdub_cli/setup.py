from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError

from setuptools import setup  


class linux_deps(sdist_orig):

    def run(self):
        try:
            self.spawn(['bash', 'install-dependencies.sh'])
        except DistutilsExecError:
            self.warn('Installing system dependencies failed.')
        super().run()


setup(name='deepdub',
    version='1.1.0',
    packages=[],
    cmdclass={
        'linux_deps': linux_deps
    }
)
