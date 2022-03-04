from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError

from setuptools import setup, find_packages

files = ["*"]

class linux_deps(sdist_orig):

    def run(self):
        try:
            self.spawn(['bash', 'install-dependencies.sh'])
        except DistutilsExecError:
            self.warn('Installing system dependencies failed.')
        super().run()


setup(name='deepdub',
    version='3.0.0',

    packages=find_packages(),
    package_data = {'deepdub' : files },

    entry_points={
        'console_scripts': [
            'deepdub=deepdub.main:main',
        ]
    },

    cmdclass={
        'linux_deps': linux_deps
    }
    
)
