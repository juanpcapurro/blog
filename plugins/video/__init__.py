"""
    ReST directive for embedding selfhosted videos
"""
from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives

class Video(Directive):
    has_content = False
    html = '<video controls muted>  <source src="%(src)s" type="video/webm">  </video>'
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        self.options['src'] = directives.uri(self.arguments[0])
        return [nodes.raw('', self.html % self.options, format='html')]

def register():
    directives.register_directive('video', Video)
