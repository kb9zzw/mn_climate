from django.test import TestCase, Client
from django.contrib.gis.geos import Point
from models import *

class ImpactModelTests(TestCase):

    def setUp(self) :
        pass
    
    def testSaveImpact(self):
        impact = Impact()
        impact.impact_type = 1 
        impact.location_name = 'Jon'
        impact.comment = 'This is a comment'
        impact.geom = Point(0,0)
        impact.save()

class VulnerableByZipModelTests(TestCase):

    def setUp(self):
        impact = Impact()
        impact.impact_type = 0
        impact.location_name = 'Test'
        impact.comment = 'Test Comment'
        impact.geom = Point(-91.700134, 47.049680)
        impact.save()

    def testZipCount(self) :
        rz = VulnerableByZip.objects.filter(zip_code=55616)
        self.assertEquals(1,rz[0].count)

class ViewTests(TestCase):

    def testAddImpact(self):
        c = Client()
        response = c.post('/add_impact/', { 'impact_type': 1, 'location_name': 'Jon', 'comment': 'My Comment', 'coordinates': '0.0,0.0' })
        self.assertEquals(response.content, 'success')

    def testAddImpactMissingRequired(self):
        c = Client()
        response = c.post('/add_impact/', { 'impact_type': 1, 'location_name': 'Jon', 'comment': 'My Comment'})
        self.assertEquals(response.content, 'error')

