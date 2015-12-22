# Cartoview ArcGIS Feature Server

[ESRI GeoServices REST API implemtnation](https://www.esri.com/library/whitepapers/pdfs/geoservices-rest-spec.pdf) using Django and PostGIS. You can manage and publish your GIS data as ESRI feature service layers with ArcGIS GeoServices REST API. Allowing these layers to be fully intrgtate with esri API's and templates.

This django app can be used as a [Cartoview](https://github.com/cartologic/cartoview) app or you can use it in any django project.

to use with cartoview 

1. Download the app package form [here](http://cartologic.com/cartoview2/apps/)
2. in your [cartoview](github.com/cartologic/cartoview) installation, login as admin
3. go to "Apps" then "Manage Apps" then "Install new app"
4. upload the downloaded package and click install
5. wait untill the installation finish

to use in normal django project

## Requirements
- Python 2.7
- Postgresql 9.4 + PostGIS 2.1
- Django 1.6
- [GeoDjango](https://docs.djangoproject.com/en/1.6/ref/contrib/gis/install/)
- psycopg2 2.6.1
- django-tastypie 0.12.2
- Pillow 2.5.3

## Installation
- Download the application from GitHub
- Install requirements uisng '''pip install -r requirements.txt'''
- create new django project or use your existing one
- in settings.py
```python
INSTALLED_APPS = (
  ...
  "cartoview_arcgis_featureserver.cartoserver",
  ...
)
GEOS_LIBRARY_PATH = 'C:/OSGeo4W/bin/geos_c.dll' 
GDAL_LIBRARY_PATH = 'C:/OSGeo4W/bin/gdal111.dll'
POSTGIS_VERSION = (2, 1, 8) # NOTE: write your installed postgis version

```
- in urls.py
```python
urlpatterns = patterns('',
    ...
    url(r'^cartoserver/', include('cartoview_arcgis_featureserver.cartoserver.urls')),
    ...
)

```

## Usage
Add the default datastore
-----------
- datastore is a postgis database to store the geodata
- you need to define the connection parameters for this database first
- you can add multiple datastores
- when you add a new datastore, cartoserver will detect all geo tables in this datastore so that you can publish feature layers using these tables
- default datastore is the datastore which will be used to store the user uploaded shapefiles
- go to http://localhost:8000/cartoserver
- choose settings then click + button
- then enter your connection parameters
- when you add the first datastore it will be set as the default datastore automatically
- ![Add Datastore](screenshots/1.jpg)

Upload you shapefiles
-----------
- from the geotables sections you can upload your shapefiles

Publish Your feature layers
-----------
- from Feature Layers section you can publish your feature layers

Publish Tiles Layers
-----------
- from Tiles section you can publish tiles layers

Support
-------
Query API


# License
BSD2

Copyright (c) 2015, Cartologic.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software must display the following acknowledgement: This product includes software developed by the Cartologic.
4. Neither the name of the Cartologic nor the names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY CARTOLOGIC ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL CARTOLOGIC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

