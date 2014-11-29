"""
Django settings for maps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Import local settings
from local_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug
TEMPLATE_DEBUG = template_debug

ALLOWED_HOSTS = allowed_hosts

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'djgeojson',
    'mn_climate',
    'ga_ows',
    'shapes',
    'pipeline',
    'flatblocks',
    #'django_pdb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mn_climate.urls'

WSGI_APPLICATION = 'mn_climate.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }
}

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, "mn_climate/fixtures/"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "mn_climate/templates/"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_ROOT = '/var/www/html/static'


STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  #'pipeline.finders.FileSystemFinder',
  #'pipeline.finders.AppDirectoriesFinder',
  'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# npm install -g cssmin
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = '/usr/bin/env cssmin'
PIPELINE_CSSMIN_ARGUMENTS = ''

PIPELINE_CSS = {
    'libraries': {
        'source_filenames': (
            'bower_components/bootstrap/dist/css/bootstrap.css',
            'bower_components/leaflet/dist/leaflet.css',
            'bower_components/Leaflet.awesome-markers/dist/leaflet.awesome-markers.css',
            'bower_components/leaflet.markercluster/dist/MarkerCluster.Default.css',
            'bower_components/leaflet.markercluster/dist/MarkerCluster.css',
            'bower_components/Leaflet.StyledLayerControl/css/styledLayerControl.css',
            'bower_components/L.GeoSearch/src/css/l.geosearch.css',
            'app.css',
        ),
        'output_filename': 'css/libs.min.css',
    }
}

# npm install -g uglify-js
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_UGLIFYJS_BINARY = '/usr/bin/env uglifyjs'
PIPELINE_UGLIFYJS_ARGUMENTS = ''

PIPELINE_JS = {
    'libraries': {
        'source_filenames': (
            'bower_components/jquery/dist/jquery.js',
            'bower_components/jquery-cookie/jquery.cookie.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
            'bower_components/leaflet/dist/leaflet.js',
            'bower_components/Leaflet.awesome-markers/dist/leaflet.awesome-markers.js',
            'bower_components/leaflet-ajax/dist/leaflet.ajax.js',
            'bower_components/leaflet-tilelayer-geojson/TileLayer.GeoJSON.js',
            'bower_components/leaflet.markercluster/dist/leaflet.markercluster.js',
            'bower_components/webgl-heatmap-leaflet/js/webgl-heatmap.js',
            'bower_components/webgl-heatmap-leaflet/js/webgl-heatmap-leaflet.js',
            'bower_components/Leaflet.StyledLayerControl/src/styledLayerControl.js',
            'bower_components/L.GeoSearch/src/js/l.control.geosearch.js',
            'bower_components/L.GeoSearch/src/js/l.geosearch.provider.google.js',
        ),
        'output_filename': 'js/libs.min.js',
    }
}

STATICFILES_DIR = (
    os.path.join(BASE_DIR, "mn_climate/static"),
)
