from trytond.model import (
    DeactivableMixin, Exclude, Model, ModelSQL, ModelView, UnionMixin, fields,
    sequence_ordered)
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Get, If
from trytond.tools import lstrip_wildcard
from trytond.tools.multivalue import migrate_property
from trytond.transaction import Transaction
from trytond.config import config

if config.getboolean('attachment', 'filestore', default=True):
    file_id = 'file_id'
    thumbnail_id = 'thumbnail_id'
    store_prefix = config.get('attachment', 'ImageGalery', default=None)
else:
    file_id = None
    thumbnail_id = None
    store_prefix = None


class ProductImageGalery(sequence_ordered(), ModelSQL, ModelView):
    'Product Image Galery'
    __name__ = 'product.image.galery'

    name = fields.Char('Name', required=True)
    template = fields.Many2One(
        'product.template', "Product Template",
        required=True, ondelete='CASCADE', select=True,
        search_context={'default_products': False},
        domain=[
            If(Eval('active'), ('active', '=', True), ()),
            ],
        help="The product images "
        "inherited by the variant.")
    data = fields.Binary('Data', filename='name',
        file_id=file_id, store_prefix=store_prefix)
    thumbnail = fields.Binary('Data Thumbnail', filename='name',
        file_id=thumbnail_id, store_prefix=store_prefix)
    file_id = fields.Char('File ID', readonly=True)
    thumbnail_id = fields.Char('Thumbnail ID', readonly=True)
    path_data = fields.Function(fields.Char('Path Data'), 'get_path')
    path_thumbnail = fields.Function(fields.Char('Path thumbnail'), 'get_path')

    def get_path(self, name):
        path = ''
        if name == 'path_data':
            path = '/' + self.file_id[:2] + '/' + self.file_id[2:4] + '/' + self.file_id
        if name == 'path_thumbnail':
            path = '/' + self.thumbnail_id[:2] + '/' + self.thumbnail_id[2:4] + '/' + self.thumbnail_id
        return path
    

class Template(metaclass=PoolMeta):
    __name__ = "product.template"

    image_galery = fields.One2Many('product.image.galery', 'template', 'Product Image Galery')
