# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from typing import List


project = "Synthora"
copyright = "2024-2025, Syntropix.AI"
author = "Syntropix.AI"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "nbsphinx",
]

nbsphinx_execute = "never"
nbsphinx_allow_errors = True
nbsphinx_prolog = r"""
.. raw:: html

    <style>
    div.nbinput div.prompt,
    div.nboutput div.prompt {
        display: none;
    }
    </style>
"""

templates_path = ["_templates"]
exclude_patterns: List[str] = []

myst_enable_extensions = ["colon_fence", "dollarmath", "amsmath"]

nb_execution_mode = "off"
nb_execution_timeout = 300

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

source_suffix = [".rst", ".md"]

html_theme_options = {
    "logo": {
        "text": "Synthora",
        "image_dark": "http://syntropix.ai/wp-content/uploads/2024/11/White-logo-no-background.png",
        "image_light": "http://syntropix.ai/wp-content/uploads/2024/11/Color-logo-no-background.png",
    },
    "repository_url": "https://github.com/syntropix-ai/synthora",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
}

html_favicon = "http://syntropix.ai/wp-content/uploads/2025/01/symbol.svg"
