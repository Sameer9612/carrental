"""
URL configuration for carrental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from car.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home , name="home"),
    path("contact/" , contact , name="contact"),
    path("about/" , about , name="about"),
    path('category/<slug:val>', CategoryView.as_view(), name="category"),
    path('category-tittle/<val>', CategoryTittle.as_view(), name="category-title"),
    path("register/",Registerview.as_view(), name='Register'),
    path("login/", auth_view.LoginView.as_view(template_name='login.html'), name='login'),
     path('profile/', ProfileView.as_view(), name='profile'),
    path('address/',views.get,name='address'),
    path('update-address/<int:pk>/', UpdateAddress.as_view(), name='update_address'),
    path('logout/', custom_logout, name='logout'),
    path('rent-now/<int:product_id>/', views.rent_car, name='rent_car'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/', views.some_view, name='some_view'),
     path('paymentdone/', views.payment_done, name='payment_done'),
     path('payment-failed/', views.payment_failed, name='payment_failed'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
