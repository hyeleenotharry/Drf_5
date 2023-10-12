from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import Home


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", Home.as_view()),
        path("user/", include("user.urls")),
        path("book/", include("book.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
