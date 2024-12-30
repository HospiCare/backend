# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django
sys.path.insert(0, os.path.abspath('../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HospiCare'
copyright = '2024, HospiCare Team'
author = 'HospiCare Team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinxcontrib_django",
        ]

django_settings = "app.settings"
django_show_db_tables = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']