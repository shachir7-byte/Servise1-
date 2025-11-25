"""
URL configuration for proekSERV project.
"""
# urls/proekSERV

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # ← добавлено

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/orders/'), name='home'),  # ← главная страница
    path('', include('SAMserv.urls')),  # ← подключаете все маршруты из SAMserv
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)