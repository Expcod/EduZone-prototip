from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Root URL pattern
    path('api/core/', include('core.urls')),
    path('api/simlab/', include('simlab.urls')),
    path('api/', include('core.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('learning_styles/', include('learning_styles.urls', namespace='learning_styles')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
