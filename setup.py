from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.bdist_egg import bdist_egg
from wheel.bdist_wheel import bdist_wheel
import subprocess
import os

def custom_command():
    libs = ['hts', 'deflate', 'bz2', 'z']
    for lib in libs:
        try:
            ldconfig = subprocess.Popen(['ldconfig', '-p'], stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', lib], stdin=ldconfig.stdout, stdout=subprocess.PIPE)
            output = grep.communicate()[0]

            if not output:
                conda_prefix = os.getenv('CONDA_PREFIX')
                if conda_prefix is not None and os.path.isfile(f'{conda_prefix}/lib/lib{lib}.so'):
                    print(f'Found {lib} in {conda_prefix}/lib')
                else:
                    raise EnvironmentError(f"{lib} library not found. Please install it and try again.")
        except Exception as e:
            print(f"Error checking library {lib}: {str(e)}")
    #for lib in libs:
    #    if subprocess.call(['ldconfig', '-p', '|', 'grep', lib]) != 0:
    #        raise EnvironmentError(f"{lib} library not found. Please install it and try again.")
    subprocess.call(['make'])

class CustomInstallCommand(install):
    """Customized setuptools install command."""
    def run(self):
        custom_command()
        install.run(self)

class CustomBDistEggCommand(bdist_egg):
    """Customized setuptools bdist_egg command."""
    def run(self):
        custom_command()
        bdist_egg.run(self)

class CustomBDistWheelCommand(bdist_wheel):
    """Customized setuptools bdist_wheel command."""
    def run(self):
        custom_command()
        bdist_wheel.run(self)

setup(
    name='pyballc',
    version='0.0.1',
    description='Python module for reading BAllC files',
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
        'bdist_egg': CustomBDistEggCommand,
        'bdist_wheel': CustomBDistWheelCommand,
    },
    package_data={
        'pyballc': ['_pyballcools.so'],
    },
    install_requires=[  
        'pysam',
    ],
)

