# example/urls.py
from django.urls import path

from example.views import home, send_email

from django.conf import settings
from django.conf.urls.static import static

# urls.py
from django.conf.urls import handler404
from .views import custom_page_not_found_view

handler404 = custom_page_not_found_view


urlpatterns = [
    path('', home,name="home"),
    path('send_email', send_email,name="send_email"),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)