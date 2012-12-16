from piston.handler import BaseHandler
from piston.emitters import *
from EtikTakApp.models.supermarket import *

class SupermarketHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Supermarket
    Emitter.register('json', JSONEmitter, 'application/json; charset=utf-8')

    def read(self, request, supermarket_id=None):
        base = Supermarket.objects

        if supermarket_id:
            return base.get(pk=supermarket_id)
        else:
            return base.all()

class SupermarketLocationHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = SupermarketLocation
    Emitter.register('json', JSONEmitter, 'application/json; charset=utf-8')

    def read(self, request, supermarket_location_id=None):
        base = SupermarketLocation.objects

        if supermarket_location_id:
            return base.get(pk=supermarket_location_id)
        else:
            return base.all()

