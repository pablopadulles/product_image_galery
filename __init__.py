
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.ProductImageGalery,
        product.Template,
        module='product_image_galery', type_='model')
    Pool.register(
        module='product_image_galery', type_='wizard')
    Pool.register(
        module='product_image_galery', type_='report')
    
