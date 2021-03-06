from IPython import nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from mako.lookup import TemplateLookup

from mfr.core import extension, TEMPLATE_BASE
from mfr.extensions.ipynb import exceptions


class IpynbRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            TEMPLATE_BASE
        ]).get_template('ipynb_viewer.mako')

    def render(self):
        try:
            with open(self.file_path, 'r') as file_pointer:
                notebook = nbformat.reads(file_pointer.read(), as_version=4)
        except ValueError:
            raise exceptions.InvalidFormat('Could not read ipython notebook file.')

        exporter = HTMLExporter(config=Config({
            'HTMLExporter': {
                'template_file': 'basic',
            },
            'CSSHtmlHeaderTransformer': {
                'enabled': False,
            },
        }))
        (body, _) = exporter.from_notebook_node(notebook)
        return self.TEMPLATE.render(base=self.assets_url, body=body, md5=self.extra.get('md5'))

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
