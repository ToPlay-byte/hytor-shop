from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('pages', include('django.contrib.flatpages.urls')),
    path('', include('apps.company.urls')),
    path('account/', include('apps.users.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('orders/', include('apps.payment.urls', namespace='payment')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
