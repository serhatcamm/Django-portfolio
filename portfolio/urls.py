from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.shortcuts import redirect
from contact.api_views import latest_messages_api

urlpatterns = [
    path('favicon.ico', lambda r: redirect('static/assets/favicon.svg')),
    path('admin/api/messages/', latest_messages_api, name='latest_messages_api'),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('projects/', include('projects.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Static files are served by WhiteNoise. Django's `static()` helper is a
    # no-op when DEBUG=False, so media is served explicitly here to keep
    # uploaded images working in the production-like container.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve,
                {'document_root': settings.MEDIA_ROOT}),
    ]
