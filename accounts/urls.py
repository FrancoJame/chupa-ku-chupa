from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, dashboard_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('manager-dashboard/', dashboard_views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('admin/status/', dashboard_views.admin_status_dashboard, name='admin_status'),
]

