# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'colorise'
copyright = '2019, Alexander Asp Bock'
author = 'Alexander Asp Bock'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
release = '1.0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    'description':     'A Python module for printing colored text in terminals.',
    'logo':            '../_images/colorise-logo.png',
    'github_user':     'MisanthropicBit',
    'github_repo':     'colorise',
    'github_banner':   'true',
    'github_button':   'false',
    'extra_nav_links': {
        'Issues':        'https://github.com/MisanthropicBit/colorise/issues',
        'Pull Requests': 'https://github.com/MisanthropicBit/colorise/pulls',
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

base_url = 'https://github.com/{github_user}/{github_repo}/blob/{branch}'\
    .format(branch='master', **html_theme_options)


def linkcode_resolve(domain, info):
    """Resolve links to github source code."""
    if domain != 'py' or '.' in info['fullname']:
        return None

    module_path = info['module'].replace('.', os.sep)

    if module_path == project:
        module_path = os.path.join(module_path, '__init__')

    return os.path.join(base_url, module_path + '.py')


autodoc_mock_imports = ['colorise.win']
