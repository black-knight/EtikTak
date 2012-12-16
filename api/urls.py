from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

supermarket_handler = Resource(SupermarketHandler)
supermarket_location_handler = Resource(SupermarketLocationHandler)

urlpatterns = patterns('',
    url(r'^supermarket/(?P<supermarket_id>[^/]+)/', supermarket_handler, { 'emitter_format': 'json' }),
    url(r'^supermarkets$', supermarket_handler, { 'emitter_format': 'json' }),
    url(r'^supermarket_location/(?P<supermarket_location_id>[^/]+)/', supermarket_location_handler, { 'emitter_format': 'json' }), 
    url(r'^supermarket_locations$', supermarket_location_handler, { 'emitter_format': 'json' }),
)
