from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from bookings.models import Booking

class CustomLoginView(LoginView):
    """Custom login view that properly handles and displays form errors"""
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        """Ensure form is always in context"""
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            from django.contrib.auth.forms import AuthenticationForm
            context['form'] = AuthenticationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle POST request with proper error handling"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(self.get_success_url())
        else:
            # Authentication failed - show error
            from django.contrib.auth.forms import AuthenticationForm
            form = AuthenticationForm()
            form.add_error(None, 'Invalid username or password.')
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return '/'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return f"{reverse_lazy('login')}?next={next_url}"
        return reverse_lazy('login')

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    """Customer account dashboard showing profile and booking status"""
    template_name = 'accounts/customer_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all bookings for this customer
        bookings = Booking.objects.filter(user=user).order_by('-created_at')
        
        # Count bookings by status
        pending_count = bookings.filter(status='PENDING').count()
        confirmed_count = bookings.filter(status__in=['AVAILABLE', 'FREE_SOON']).count()
        cancelled_count = bookings.filter(status='CANCELLED').count()
        
        context['user_profile'] = user
        context['bookings'] = bookings
        context['pending_count'] = pending_count
        context['confirmed_count'] = confirmed_count
        context['cancelled_count'] = cancelled_count
        context['total_bookings'] = bookings.count()
        
        return context
