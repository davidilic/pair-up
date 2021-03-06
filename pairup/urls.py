from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('base.urls')),
    path('rooms/', include('rooms.urls')),
    path('topics/', include('topics.urls')),
    path('activity/', include('activity.urls')),
    path('delete/', include('deletion.urls')),

    path('api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
