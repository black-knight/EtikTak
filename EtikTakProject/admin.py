from EtikTakProject.models import UserCredentials, PhoneNumber, SuperMarket, SpecificSuperMarket
from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class SpecificSuperMarketAdmin:
    formfield_overrides = {
            map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(SuperMarket)
admin.site.register(SpecificSuperMarket)

