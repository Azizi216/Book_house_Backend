from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import Http404
from django.urls import include, path, re_path
from django.views.static import serve


def frontend_app(request, path=''):
    """Serve the built Angular app from Django for a one-server demo."""
    frontend_dist = Path(settings.FRONTEND_DIST)

    if not frontend_dist.exists():
        raise Http404('Frontend build not found. Run npm run build and copy dist to frontend_dist.')

    requested_file = frontend_dist / path

    if path and requested_file.exists() and requested_file.is_file():
        return serve(request, path, document_root=frontend_dist)

    return serve(request, 'index.html', document_root=frontend_dist)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
]

# Demo media serving. For a real production app, use Cloudinary/S3/Supabase Storage.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^(?P<path>.*)$', frontend_app),
]
