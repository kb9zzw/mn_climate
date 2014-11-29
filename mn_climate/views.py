from models import *
from forms import *
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.gis.geos import Point
from djgeojson.serializers import Serializer as GeoJSONSerializer
from shapes.views import ShpResponder
from django.contrib.gis.shortcuts import render_to_kml

# Views
def index(request):
    '''Main view'''

    # Load data into view
    args = {}
    args.update(csrf(request))
    args['form'] = AddImpactForm()
    args['impacts'] = Impact.objects.all()

    return render_to_response('index.html', args, context_instance=RequestContext(request))

def impacts(request):
    '''Querys impacts based on impact type, returns geojson query set'''
    form = ImpactQueryForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        impact_type = cd['impact_type']
        if impact_type != '':
            # serialize by impact_type
            querySet = Impact.objects.filter(impact_type=cd['impact_type'])
            geojson = GeoJSONSerializer().serialize(querySet)
        else:
            # serialize all impacts
            geojson = GeoJSONSerializer().serialize(Impact.objects.all())
        return HttpResponse(geojson)
    else :
        return HttpResponseBadRequest('form is invalid')

def counts(request):
    '''Returns impact counts per area as geojson query set'''
    form = CountQueryForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        area = cd['area']
        if area == 'county': # count by county
            geojson = GeoJSONSerializer().serialize(CountyCount.objects.all())
        else:   # it must be zip
            geojson = GeoJSONSerializer().serialize(ZipCount.objects.all())
        return HttpResponse(geojson)
    else:
        return HttpResponseBadRequest('invalid form data')

def add_impact(request):
    #import pdb; pdb.Pdb(skip=['django.*']).set_trace()
    if request.method == 'POST':
        form = AddImpactForm(request.POST)
        if form.is_valid():
            new_point = Impact()
            cd = form.cleaned_data
            coordinates = cd['coordinates'].split(',')
            new_point.geom = Point(float(coordinates[0]), float(coordinates[1]))
            new_point.impact_type = cd['impact_type']
            new_point.comment = cd['comment']
            new_point.location_name = cd['location_name']

            new_point.save()
            return HttpResponse('success')
        else :
            return HttpResponseBadRequest('error')
    else :
        form = AddImpactForm()

    args = {}
    args.update(csrf(request))
    args['form'] = AddImpactForm()
    return render_to_response('mn_climate/add_impact.html', args, context_instance=RequestContext(request))

def shapefile(request):
    form = ShapefileForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        layer = cd['layer']
    else :
        return HttpResponseBadRequest('error, unknown layer')

    if layer == 'impacts':
        # Return impacts shapefile
        data = Impact.objects.all()
        shp_response = ShpResponder(data)
        shp_response.file_name = "impacts"
    elif layer == 'county_counts':
        data = CountyCount.objects.all()
        shp_response = ShpResponder(data)
        shp_response.file_name = "county_counts"
    elif layer == 'zip_counts':
        data = ZipCount.objects.all()
        shp_response = ShpResponder(data)
        shp_response.file_name = "zip_counts"
    elif layer == 'storm_events':
        data = StormEvents.objects.all()
        shp_response = ShpResponder(data)
        shp_response.file_name = 'storm_events'
    elif layer == 'normals':
        data = Normals.objects.all()
        shp_response = ShpResponder(data)
        shp_response.file_name = 'normals'
    else :
        return HttpResponseBadRequest('error, unsupported layer')

    return shp_response()


def kml(request):
  impacts = Impact.objects.all()
  return render_to_kml('impacts.kml', { "impacts": impacts } )
