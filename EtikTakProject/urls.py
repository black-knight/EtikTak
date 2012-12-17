from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EtikTakProject.views.home', name='home'),
    # url(r'^EtikTakProject/', include('EtikTakProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # API (webservice)
    (r'^api/', include('api.urls')),

    # Main page
    (r'^$', TemplateView.as_view(template_name="index.html")),
)
