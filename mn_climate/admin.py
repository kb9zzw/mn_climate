from django.contrib.gis import admin
from models import *

#admin.site.register(Impact, admin.OSMGeoAdmin)
admin.site.register(Impact, ImpactAdmin)
