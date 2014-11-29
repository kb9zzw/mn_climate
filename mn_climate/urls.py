from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView, TiledGeoJSONLayerView
from ga_ows.views.wfs import WFS
import settings

# Import data models
from mn_climate.models import *

# Enable administrator interface
from django.contrib.gis import admin
admin.autodiscover()

# Storm Events View (geojson)
class StormEventsView(GeoJSONLayerView):
    model=StormEvents
    properties = StormEvents._meta.get_all_field_names()

# Storm Events view (tiled geojson)
class TiledStormEventsView(TiledGeoJSONLayerView):
    model=StormEvents
    properties = StormEvents._meta.get_all_field_names()
    #properties = ('event_type', 'begin_date', 'end_date_t', 'injuries_d', 'deaths_dir', 'event_narr',)

# Normals view (geojson)
class NormalsView(GeoJSONLayerView):
    model=Normals
    properties = Normals._meta.get_all_field_names()

# Normals view (tiled geojson)
class TiledNormalsView(TiledGeoJSONLayerView):
    model=Normals
    properties = Normals._meta.get_all_field_names()

urlpatterns = patterns('',
    # admin interface
    url(r'^admin/', include(admin.site.urls)),

    # Main page
    url(r'^$', 'mn_climate.views.index', name='index'),

    # OGC WFS
    url(r'^wfs', WFS.as_view(models=[Impact, CountyCount, ZipCount, StormEvents, Normals]), name='wfs'),

    # kml export
    url(r'^impacts.kml$', "mn_climate.views.kml", name="kml"),

    # GeoJSON services
    url(r'^impacts', "mn_climate.views.impacts", name='impacts'),
    url(r'^counts', "mn_climate.views.counts", name='counts'),
    url(r'^add_impact/$', 'mn_climate.views.add_impact', name="add_impact"),
    url(r'^storm_events/$', StormEventsView.as_view(), name="storm_events"),
    url(r'^normals/$', NormalsView.as_view(), name='normals'),

    # Tiled GeoJSON services
    url(r'^impacts/(\d+)/(\d+)/(\d+).geojson$',
        TiledGeoJSONLayerView.as_view(), name="tiled_impacts"),
    url(r'^storm_events/(\d+)/(\d+)/(\d+).geojson$',
        TiledStormEventsView.as_view(), name="tiled_storm_events"),
    url(r'^normals/(\d+)/(\d+)/(\d+).geojson$',
        TiledNormalsView.as_view(), name="tiled_normals"),

    # Shapefile exports
    url(r'^shapefile', "mn_climate.views.shapefile", name="shapefile"),

)
