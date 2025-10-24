"""
URL configuration for proekSERV project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path('serv/', include('SAMserv.urls')),  # ← подключаем маршруты
]

