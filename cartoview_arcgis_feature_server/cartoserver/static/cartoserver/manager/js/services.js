

app.factory("FeatureLayer", ["TastyResource", function (TastyResource) {
    var resource = TastyResource({
        url: REST_URL + "featurelayer/",
        cache: false
    });
    return resource;
}]);


app.factory("Geotable", ["TastyResource", 'FeatureLayer', function (TastyResource, FeatureLayer) {
    
    var resource = TastyResource({
        url: REST_URL + "geotable/",
        cache: false
    });
    // var getGeotable = resource.get;
    
    // resource.get = function(id, success, error){
    	
    // 	return getGeotable(id, function(){
    // 		//console.debug(arguments)
    // 		if(typeof success == 'function'){
    // 			success.call(arguments)
    // 		}

    // 	},error)
    // }
    return resource;
}]);

app.factory("Webmap", ["TastyResource", function (TastyResource) {
    var resource = TastyResource({
        url: REST_URL + "itemdata/",
        cache: false
    });
    return resource;
}]);

app.factory("Datastore", ["TastyResource", function (TastyResource) {
    var resource = TastyResource({
        url: REST_URL + "datastore/",
        cache: false
    });
    return resource;
}]);

app.factory("TileLayer", ["TastyResource", function (TastyResource) {
    var resource = TastyResource({
        url: REST_URL + "tilesservice/",
        cache: false
    });
    return resource;
}]);


app.factory("DataServices", ['Geotable', 'FeatureLayer','Webmap','Datastore',"TileLayer",
    function(Geotable,FeatureLayer, Webmap, Datastore,TileLayer){
	return  {
		Geotable:Geotable,
		FeatureLayer:FeatureLayer,
        Webmap:Webmap,
        Datastore:Datastore,
        TileLayer:TileLayer
	}
}]);