# Leaflet Home Control

## What?
This leaflet plugin adds a control in the zoom control panel to send the map back to the original zoom and center position

## How?
Initialise your map object with the `home` attribute set to `true`

    var map = L.map('map', {center: new L.LatLng(..,..), zoom: 13, home: true});	
	
You also should add the image icon into your application as well as the CSS into your css styles	