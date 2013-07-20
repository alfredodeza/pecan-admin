from pecan import request
from webhelpers.html.tags import *
from webhelpers.text import *

def css(url):
    """
    Called from a template to add a CSS resource to the page.
    """
    if 'css_sources' not in request.context:
        request.context['css_sources'] = []
    request.context['css_sources'].append(url)
    return ''


def js(url):
    """
    Called from a template to add a JS resource to the page.
    """
    if 'js_sources' not in request.context:
        request.context['js_sources'] = []
    request.context['js_sources'].append(url)
    return ''
