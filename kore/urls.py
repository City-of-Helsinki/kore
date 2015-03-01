from django.conf.urls import patterns, include, url
from django.contrib import admin

from schools.api import router

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'v1/', include(router.urls))
)
