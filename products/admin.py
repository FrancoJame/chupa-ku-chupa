from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'has_image')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    @admin.display(boolean=True, description='Image in storage')
    def has_image(self, obj):
        return obj.has_uploaded_image()

    @admin.display(description='Preview')
    def image_preview(self, obj):
        from django.utils.html import format_html
        if not obj:
            return '—'
        return format_html(
            '<img src="{}" style="max-height:120px;border-radius:8px;" />',
            obj.get_image_url(),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('image_preview',)
        return ()

    def get_fieldsets(self, request, obj=None):
        photo_fields = ('image', 'image_preview') if obj else ('image',)
        return (
            (None, {'fields': ('name', 'category', 'description', 'price', 'stock_quantity', 'is_active')}),
            (
                'Photo',
                {
                    'fields': photo_fields,
                    'description': 'Upload a photo. With a Railway bucket connected, it is saved to object storage.',
                },
            ),
        )
