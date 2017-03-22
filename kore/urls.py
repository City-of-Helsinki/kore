from django.conf.urls import include, url
from django.contrib import admin

from schools.api import router

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'v1/', include(router.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
