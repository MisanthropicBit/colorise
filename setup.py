"""colorise module setup script for distribution."""

from __future__ import with_statement
from distutils.core import setup


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


setup(
    name='colorise',
    version=get_version('colorise/__init__.py'),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms="Platform independent",
    description=('Easily print colored text to the console'),
    license='MIT License',
    keywords='text, color, colorise, colorize',
    packages=['colorise', 'colorise.win', 'colorise.nix'],
    package_data={'colorise': ['tests', 'examples']},
    url='https://github.com/MisanthropicBit/colorise',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3'
    ]
)
