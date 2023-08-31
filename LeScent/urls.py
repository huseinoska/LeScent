"""
URL configuration for LeScent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from PerfumeShopApp import views
from PerfumeShopApp.views import AddProductView

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("category/<str:category_name>/", views.category_products, name="category_products"),
    path("products/<int:product_id>/", views.product_details, name="product_details"),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('update_quantity/<int:product_id>/', views.update_quantity_view, name='update_quantity'),
    path("admin/", admin.site.urls, name="admin"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),
    path("order_success/", views.order_success_view, name="order_success_view"),
    path('add_product/', AddProductView.as_view(), name='add_product'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

