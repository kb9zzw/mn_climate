from django import forms
from models import *

class ImpactQueryForm(forms.Form):
    '''Form for querying impacts by impact_type'''
    impact_type = forms.ChoiceField(choices=IMPACT_TYPE_CHOICES, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        impact_type = cleaned_data.get('impact_type')
        return cleaned_data

LAYER_CHOICES = (
  ('impacts', 'impacts'),
  ('county_counts', 'county_counts'),
  ('zip_counts', 'zip_counts'),
  ('storm_events', 'storm_events'),
  ('normals', 'normals'),
)

class ShapefileForm(forms.Form):
  '''Form for exporting a layer as a shapefile'''
  layer = forms.ChoiceField(choices=LAYER_CHOICES, required=True)

  def clean(self):
    cleaned_data = self.cleaned_data
    layer = cleaned_data.get('layer')
    return cleaned_data

AREA_CHOICES=(
    ('county','county'),
    ('zip','zip'),
)
class CountQueryForm(forms.Form):
    '''Form for querying impact counts per area by impact_type'''
    area = forms.ChoiceField(choices=AREA_CHOICES, required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        area = cleaned_data.get('area')
        return cleaned_data

class AddImpactForm(forms.Form):
    '''Defines the form used to collect Climate Impacts from the user'''
    #import pdb; pdb.Pdb(skip=['django.*']).set_trace()
    coordinates = forms.CharField(max_length=200, required=True)
    impact_type = forms.ChoiceField(choices=IMPACT_TYPE_CHOICES, required=True)
    location_name = forms.CharField(max_length=50, required=True)
    comment = forms.CharField(max_length=500,
            widget=forms.Textarea(attrs={'cols': 34, 'rows': 5}), required=True)

    def clean(self):
        '''Returns cleaned/validated data from the form'''
        cleaned_data = self.cleaned_data

        coordinates = cleaned_data.get('coordinates')
        impact_type = cleaned_data.get('impact_type')
        location_name = cleaned_data.get('location_name')
        comment = cleaned_data.get('comment')

        return cleaned_data
