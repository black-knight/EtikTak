from EtikTakApp.models import *

from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class SupermarketLocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
            map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(Supermarket)
admin.site.register(SupermarketLocation, SupermarketLocationAdmin)
admin.site.register(User)

