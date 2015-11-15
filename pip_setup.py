"""
Install Pip by typing "python pip_setup.py install"
"""

from setuptools import setup, find_packages

setup(
    name = 'pip',
    version = '7.1.2',
    author = 'Pip',
    author_email = '@pip',
    maintainer = 'Pip',
    description = 'Install Pip by typing "python pip_setup.py install".',
    license = 'Pip',
    install_requires = ['pip==7.1.2'],
    )
