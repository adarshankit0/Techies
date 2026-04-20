from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main App
    path('', include('base.urls')),

    # API
    path('api/', include('base.api.urls')),

    # CodeTechies (NEW FEATURE)
    path('code/', include('codetechies.urls')),
]

# Media files (images, avatars etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)