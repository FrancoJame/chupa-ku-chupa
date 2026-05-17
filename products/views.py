from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id, is_active=True)
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user, 'role', None) == 'MANAGER'

class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'category', 'description', 'price', 'stock_quantity', 'image', 'is_active']
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        image_file = form.cleaned_data.get('image')
        if image_file:
            form.instance.image = None

        try:
            self.object = form.save()
        except Exception as exc:
            messages.error(self.request, f'Could not save the product: {exc}')
            return self.form_invalid(form)

        if image_file:
            try:
                self.object.image = image_file
                self.object.save(update_fields=['image'])
            except Exception as exc:
                messages.warning(
                    self.request,
                    'Product saved, but the image could not be uploaded. '
                    'Connect your Railway bucket to this service (Credentials tab) '
                    f'and redeploy. ({exc})',
                )

        return HttpResponseRedirect(self.get_success_url())
