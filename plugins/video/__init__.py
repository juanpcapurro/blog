"""
    ReST directive for embedding selfhosted videos
"""
from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives

class Video(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {'defaultaudio': bool}
    final_argument_whitespace = False

    def run(self):
        src = directives.uri(self.arguments[0])
        extension = self.arguments[0].split('.')[-1]
        muted = '' if 'defaultaudio' in self.options else 'muted'
        html = f'<video controls {muted}>  <source src="{src}" type="video/{extension}">  </video>'
        return [nodes.raw('', html , format='html')]

def register():
    directives.register_directive('video', Video)
