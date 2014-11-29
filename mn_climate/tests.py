from django.test import TestCase, Client
from django.contrib.gis.geos import Point
from models import *
from django.core.management import call_command

class ModelTests(TestCase):

    fixtures = ['initial', 'test_impacts']

    def setUp(self) :
        pass
    
    def testSaveImpact(self):
        impact = Impact()
        impact.impact_type = 1 
        impact.location_name = 'Fish Lake'
        impact.comment = 'This is a Fish Lake'
        impact.geom = Point(-92.282409668, 46.9446372242)
        impact.save()

        qs = Impact.objects.filter(location_name='Fish Lake')
        self.assertEquals(1, qs[0].impact_type)

    def testZipCount(self) :
        qs = ZipCount.objects.filter(zip_code='55614')
        self.assertEquals(5, qs[0].count)

    def testCountyCount(self) :
        qs = CountyCount.objects.filter(countyname='Lake')
        self.assertEquals(7, qs[0].count)

    def testNormals(self) :
        qs = Normals.objects.filter(station='GHCND:USC00218692')
        self.assertEquals(350, qs[0].ann_tmin_n)

    def testStormEvents(self) :
        qs = StormEvents.objects.filter(event_id=510208)
        self.assertEquals('Flash Flood', qs[0].event_type)

class ViewTests(TestCase):

    def testIndex(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(200, response.status_code)

    def testAddImpact(self):
        c = Client()
        response = c.post('/add_impact/', { 'impact_type': 1, 'location_name': 'Boga Lake', 'comment': 'Testing Boga Lake', 'coordinates': '-91.2867736816,47.8113100163' })
        self.assertEquals(response.content, 'success')

        qs = Impact.objects.filter(location_name='Boga Lake')
        self.assertEquals('Testing Boga Lake', qs[0].comment)

    def testAddImpactMissingRequired(self):
        c = Client()
        response = c.post('/add_impact/', { 'impact_type': 1, 'location_name': 'Missing', 'comment': 'My Comment'})
        self.assertEquals(response.content, 'error')

    def testImpactGeojson(self):
        c = Client()
        response = c.get('/impacts/')
        self.assertEquals(200, response.status_code)

    def testShapefile(self):
        c = Client()
        response = c.get('/shapefile?layer=impacts')
        self.assertEquals(200, response.status_code)

    def testKml(self):
        c = Client()
        response = c.get('/impacts.kml/')
        self.assertEquals(200, response.status_code)

    def testCountyCount(self):
        c = Client()
        response = c.get('/counts?area=county&impact_type=0')
        self.assertEquals(200, response.status_code)

    def testZipCount(self):
        c = Client()
        response = c.get('/counts?area=zip&impact_type=1')
        self.assertEquals(200, response.status_code)

    def testTiledImpacts(self):
        c = Client()
        response = c.get('/impacts/10/252/362.geojson')
        self.assertEquals(200, response.status_code)

    def testWfsGetCapabilities(self):
        c = Client()
        response = c.get('/wfs?service=wfs&request=GetCapabilities')
        self.assertEquals(200, response.status_code)

    def testNormals(self):
        c = Client()
        response = c.get('/normals/')
        self.assertEquals(200, response.status_code)

    def testTiledNormals(self):
        c = Client()
        response = c.get('/normals/10/246/360.geojson')
        self.assertEquals(200, response.status_code)

    def testStormEvents(self):
        c = Client()
        response = c.get('/storm_events/')
        self.assertEquals(200, response.status_code)

    def testTiledStormEvents(self):
        c = Client()
        response = c.get('/storm_events/10/252/361.geojson')
        self.assertEquals(200, response.status_code)

