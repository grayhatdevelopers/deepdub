from .django_urls import *
from django.conf.urls import include, url

urlpatterns += [
    #url(r'^admin/', admin.site.urls),
    url(r'^', include('wooey.urls')),
    url(r'^', include('django.contrib.auth.urls')),
]
