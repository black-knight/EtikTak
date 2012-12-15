from EtikTakApp.models.supermarket import SuperMarket, SuperMarketLocation
from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class SuperMarketLocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
            map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(SuperMarket)
admin.site.register(SuperMarketLocation, SuperMarketLocationAdmin)

