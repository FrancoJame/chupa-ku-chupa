from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = 'List each product and whether its image file exists in storage.'

    def handle(self, *args, **options):
        for product in Product.objects.select_related('category').order_by('name'):
            if not product.image:
                status = 'no image field'
            elif product.has_uploaded_image():
                status = f'OK -> {product.image.name}'
            else:
                status = f'MISSING in storage -> {product.image.name}'
            self.stdout.write(f'{product.name}: {status}')
