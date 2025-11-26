
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('pro.dash_urls')),  
    path('main/', include('pro.urls')),   
  
  


    path('api/', include('pro.urls')),
    path("chaining/", include("smart_selects.urls")),  
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
