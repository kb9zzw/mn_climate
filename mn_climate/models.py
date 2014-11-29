from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.conf.urls import patterns

IMPACT_TYPE_CHOICES = (
    (0, 'Negative'),
    (1, 'Positive'),
)

class Impact(models.Model):
    '''Minnesota Climate Impacts'''

    impact_type = models.IntegerField("Impact Type", choices=IMPACT_TYPE_CHOICES)
    location_name = models.CharField("Location Name", max_length=50)
    date = models.DateTimeField("Date", auto_now=True)
    comment = models.TextField("Comment")
    geom = models.PointField("Geometry", srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        '''Text representation of Impact'''
        return '%s (%s,%s)' % (IMPACT_TYPE_CHOICES[self.impact_type][1], self.geom.y, self.geom.x)

    class Meta:
        db_table = 'impact'

class ImpactAdmin(admin.OSMGeoAdmin):
    list_display = ('impact_type_str', 'location_name', 'date', "latlng")
    list_filter = ('impact_type', 'date', 'location_name')

    def impact_type_str(self, obj):
      return IMPACT_TYPE_CHOICES[obj.impact_type][1]
    impact_type_str.short_description = "Impact Type"
    impact_type_str.admin_order_field = "impact_type"

    def latlng(self, obj):
      return "(%s, %s)" % (obj.geom.y, obj.geom.x)
    latlng.short_description = "Longitude/Latitude"

class CountyCount(models.Model):
    '''Impact counts per county'''
    gid = models.IntegerField(primary_key=True)
    countyname = models.CharField(max_length=17, blank=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'county_count'

class ZipCount(models.Model):
    '''Impact counts per zip code'''
    gid = models.IntegerField(primary_key=True)
    zip_code = models.CharField(max_length=17, blank=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'zip_count'

class State(models.Model):
    '''Minnesota State Boundary'''
    gid = models.IntegerField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    state_field = models.FloatField(db_column='state_', blank=True, null=True)  # Field renamed because it ended with '_'.
    state_id = models.FloatField(blank=True, null=True)
    fips = models.CharField(max_length=5, blank=True)
    state_fips = models.CharField(max_length=2, blank=True)
    name = models.CharField(max_length=10, blank=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
#        managed = False
        db_table = 'state'

class County(models.Model):
    '''Minnesota county boundaries'''
    gid = models.IntegerField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    county_field = models.FloatField(db_column='county_', blank=True, null=True)  # Field renamed because it ended with '_'.
    county_id = models.FloatField(blank=True, null=True)
    county_num = models.SmallIntegerField(blank=True, null=True)
    countyname = models.CharField(max_length=17, blank=True)
    countyfips = models.CharField(max_length=3, blank=True)
    fips = models.CharField(max_length=5, blank=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
#        managed = False
        db_table = 'county'

class Zip(models.Model):
    '''Minnesota zip code boundaries'''
    gid = models.IntegerField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    mnzip_field = models.FloatField(db_column='mnzip_', blank=True, null=True)  # Field renamed because it ended with '_'.
    mnzip_id = models.FloatField(blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
#        managed = False
        db_table = 'zip'

class StormEvents(models.Model):
    '''Storm events'''
    gid = models.IntegerField(primary_key=True)
    yearmonth = models.IntegerField(blank=True, null=True)
    episode_id = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    location_i = models.IntegerField(blank=True, null=True)
    range = models.DecimalField(max_digits=254,decimal_places=10,blank=True, null=True)
    azimuth = models.CharField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=254, blank=True, null=True)
    latitude = models.DecimalField(max_digits=254,decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=254,decimal_places=10, blank=True, null=True)
    lat2 = models.IntegerField(blank=True, null=True)
    lon2 = models.IntegerField(blank=True, null=True)
    oid_field = models.IntegerField(db_column='oid_', blank=True, null=True)  # Field renamed because it ended with '_'.
    begin_year = models.FloatField(blank=True, null=True)
    begin_day = models.FloatField(blank=True, null=True)
    begin_time = models.FloatField(blank=True, null=True)
    end_yearmo = models.FloatField(blank=True, null=True)
    end_day = models.FloatField(blank=True, null=True)
    end_time = models.FloatField(blank=True, null=True)
    episode_1 = models.FloatField(db_column='episode__1', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    event_id_1 = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=254, blank=True, null=True)
    state_fips = models.FloatField(blank=True, null=True)
    year = models.FloatField(blank=True, null=True)
    month_name = models.CharField(max_length=254, blank=True)
    event_type = models.CharField(max_length=254, blank=True)
    cz_type = models.CharField(max_length=254, blank=True)
    cz_fips = models.FloatField(blank=True, null=True)
    cz_name = models.CharField(max_length=254, blank=True, null=True)
    wfo = models.CharField(max_length=254, blank=True, null=True)
    begin_date = models.CharField(max_length=254, blank=True, null=True)
    cz_timezon = models.CharField(max_length=254, blank=True, null=True)
    end_date_t = models.CharField(max_length=254, blank=True, null=True)
    injuries_d = models.FloatField(blank=True, null=True)
    injuries_i = models.FloatField(blank=True, null=True)
    deaths_dir = models.FloatField(blank=True, null=True)
    deaths_ind = models.FloatField(blank=True, null=True)
    damage_pro = models.CharField(max_length=254, blank=True, null=True)
    damage_cro = models.CharField(max_length=254, blank=True, null=True)
    source = models.CharField(max_length=254, blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    magnitude_field = models.CharField(db_column='magnitude_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    flood_caus = models.CharField(max_length=254, blank=True, null=True)
    category = models.CharField(max_length=254, blank=True, null=True)
    tor_f_scal = models.CharField(max_length=254, blank=True, null=True)
    tor_length = models.FloatField(blank=True, null=True)
    tor_width = models.FloatField(blank=True, null=True)
    tor_other_field = models.CharField(db_column='tor_other_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    tor_other1 = models.CharField(max_length=254, blank=True, null=True)
    tor_othe_1 = models.CharField(max_length=254, blank=True, null=True)
    tor_othe_2 = models.CharField(max_length=254, blank=True, null=True)
    begin_rang = models.FloatField(blank=True, null=True)
    begin_azim = models.CharField(max_length=254, blank=True, null=True)
    begin_loca = models.CharField(max_length=254, blank=True, null=True)
    end_range = models.FloatField(blank=True, null=True)
    end_azimut = models.CharField(max_length=254, blank=True, null=True)
    end_locati = models.CharField(max_length=254, blank=True, null=True)
    begin_lat = models.FloatField(blank=True, null=True)
    begin_lon = models.FloatField(blank=True, null=True)
    end_lat = models.FloatField(blank=True, null=True)
    end_lon = models.FloatField(blank=True, null=True)
    episode_na = models.CharField(max_length=254, blank=True, null=True)
    event_narr = models.CharField(max_length=254, blank=True, null=True)
    data_sourc = models.CharField(max_length=254, blank=True, null=True)
    geom = models.PointField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
    #    managed = False
        db_table = 'storm_events'

class Normals(models.Model):
    '''Minnesota Annual Climate Normals'''
    gid = models.IntegerField(primary_key=True)
    station = models.CharField(max_length=254, blank=True)
    station_na = models.CharField(max_length=254, blank=True)
    elevation = models.DecimalField(max_digits=254, decimal_places=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=254, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=254, decimal_places=10, blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)
    ann_prcp_n = models.IntegerField(blank=True, null=True)
    ann_snow_n = models.IntegerField(blank=True, null=True)
    ann_tavg_n = models.IntegerField(blank=True, null=True)
    ann_dutr_n = models.IntegerField(blank=True, null=True)
    ann_tmax_n = models.IntegerField(blank=True, null=True)
    ann_tmin_n = models.IntegerField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
#        managed = False
        db_table = 'normals'
