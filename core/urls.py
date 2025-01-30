from django.urls import path
from .views import home, about, services, blog, contact

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
]
