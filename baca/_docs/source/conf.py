import abjad
import os
import sys
from docutils import nodes
from pygments.formatters.latex import LatexFormatter
from sphinx.highlighting import PygmentsBridge


sys.path.insert(0, os.path.abspath(os.path.join('..', '..', '..')))


class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r'''formatcom=\footnotesize'''


PygmentsBridge.latex_formatter = CustomLatexFormatter

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    #'sphinx.ext.coverage',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_autodoc_typehints',
    'abjad.docs.ext.abjadbook',
    ]


doctest_path = [
    os.path.abspath(abjad.__path__[0]),
    ]

doctest_global_setup = r'''
from __future__ import print_function
import abjad
import baca
'''

doctest_global_cleanup = r'''
for server in servertools.Server._servers.values():
    server.quit()
'''

nodes.doctest_block = nodes.literal_block

intersphinx_mapping = {
    'abjad': ('http://abjad.mbrsi.org', None),
    'python': ('http://docs.python.org/3.2', None),
    }

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'Bača API'

copyright = u'1997-2018, Trevor Bača'

#version = '0.1'

#release = '0.1'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'default'

# only import and set the theme if we're building docs locally
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

htmlhelp_basename = 'ScoreLibrarydoc'

latex_elements = {
    'inputenc': r'\usepackage[utf8x]{inputenc}',
    'utf8extra': '',

    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
\usepackage{upquote}
\pdfminorversion=5
\setcounter{tocdepth}{2}
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
\hypersetup{unicode=true}
    ''',
    }

latex_documents = [
    (
        'index',
        'ScoreLibrary.tex',
        u'Score Library API',
        u'Trevor Bača',
        'manual',
        ),
    ]

#latex_use_parts = True

latex_domain_indices = False

man_pages = [
    (
        'index',
        'Scores',
        u'Bača API',
        [u'Trevor Bača'],
        1,
        )
    ]

texinfo_documents = [
    (
        'index',
        'Scores',
        u'Bača API',
        u'Trevor Bača',
        'ScoreLibrary',
        'One line description of project.',
        'Miscellaneous',
        ),
    ]

### EXTESNIONS ###

abjadbook_console_module_names = ('baca',)
graphviz_dot_args = ['-s32']
graphviz_output_format = 'svg'
