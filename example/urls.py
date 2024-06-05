# example/urls.py
from django.urls import path

from example.views import index, home, send_email

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', index),
    path('', home,name="home"),
    path('send_email', send_email,name="send_email"),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)