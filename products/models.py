from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.core.files.storage import default_storage

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_default_image_url(self):
        return static('products/images/default-product.svg')

    def get_image_url(self):
        if not self.image:
            return self.get_default_image_url()
        try:
            if default_storage.exists(self.image.name):
                return reverse('serve_media', kwargs={'path': self.image.name})
        except Exception:
            pass
        try:
            url = self.image.url
            if url.startswith('http'):
                return url
        except Exception:
            pass
        return self.get_default_image_url()

    def has_uploaded_image(self):
        if not self.image:
            return False
        try:
            return default_storage.exists(self.image.name)
        except Exception:
            return False
