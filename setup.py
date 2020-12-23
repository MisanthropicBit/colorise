"""colorise module setup script for distribution."""

from setuptools import setup
import os


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


setup(
    name='colorise',
    version=get_version(os.path.join('colorise', '__init__.py')),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms='Platform independent',
    python_requires='>=3.6',
    description=('Easily print colored text to the console'),
    license='BSD 3-Clause License',
    keywords='text, color, colorise, colorize, console, terminal',
    packages=['colorise', 'colorise.win', 'colorise.nix'],
    package_data={'colorise': ['tests', 'examples']},
    url='https://github.com/MisanthropicBit/colorise',
    project_urls={
        'Issue Tracker': 'https://github.com/MisanthropicBit/colorise/issues',
        'Documentation': 'https://colorise.readthedocs.io/en/latest/'
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
