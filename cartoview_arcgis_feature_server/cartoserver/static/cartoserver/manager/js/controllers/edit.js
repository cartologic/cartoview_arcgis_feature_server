'use strict';

/* Here the controllers are defines */

//generic controller
app.controller('EditController',
  ['$rootScope','$scope','$state','$stateParams', 'DataServices', 'Notification',
  function ($rootScope, $scope, $state, $stateParams, DataServices, Notification) {
    $scope.item = DataServices[$stateParams.resource].get($stateParams.itemId);

    $scope.save = function(){
      var promise = $scope.item.patch()
      promise.success(function(data){ //success
        Notification.success(( $stateParams.resourceName || 'Item')+ " updated successfully!");
        angular.forEach($rootScope.items,function(item,index){
            if(item.id == data.id){
              $rootScope.items[index] = data;
            }
        });
        $state.go($stateParams.nextState,{itemId:data.id})
        $rootScope.refresh()
      });
      promise.error(function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
}]);

//featurelayer edit controller
app.controller('featurelayers.EditController',
  ['$rootScope','$scope','$state','$stateParams', 'DataServices', 'Notification',
  function ($rootScope,$scope, $state, $stateParams, DataServices, Notification) {
    $scope.item = DataServices.FeatureLayer.get($stateParams.itemId,function(){
      var item = $scope.item;
      item.drawing_info = JSON.stringify(JSON.parse(item.drawing_info),null,2)
    });
    
    $scope.save = function(){
      var promise = $scope.item.patch()
      promise.success(function(data){ //success
        Notification.success(( $stateParams.resourceName || 'Item')+ " updated successfully!");
        angular.forEach($rootScope.items,function(item,index){
            if(item.id == data.id){
              $rootScope.items[index] = data;
            }
        });
        $state.go($stateParams.nextState,{itemId:data.id})
      });
      promise.error(function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
}]);


//webmaps edit controller
app.controller('webmaps.EditController',
  ['$rootScope','$scope','$state','$stateParams', 'DataServices', 'Notification',
  function ($rootScope, $scope, $state, $stateParams, DataServices, Notification) {
    initExtentMap();
    $scope.item = DataServices.Webmap.get($stateParams.itemId,function(){
      var item = {};
      angular.copy($scope.item.item, item)
      item.text = JSON.parse($scope.item.text);
      $scope.item.id = item.id;
      //properties must not be exposed to client.
      delete item.id;
      delete item.created;
      delete item.modified;
      delete item.resource_uri;
      $scope.item.text = JSON.stringify(item, null, 4)
    });
    
    $scope.save = function(){
      var config = JSON.parse($scope.item.text);
      $scope.item.item.name =  config.name,
      $scope.item.item.title = config.title,
      $scope.item.item.url = config.url,
      $scope.item.item.type = config.type,
      $scope.item.item.typeKeywords = config.typeKeywords,
      $scope.item.item.description = config.description,
      $scope.item.item.tags = config.tags,
      $scope.item.item.snippet = config.snippet,
      $scope.item.item.thumbnail = config.thumbnail,
      $scope.item.item.extent = config.extent

      var promise = $scope.item.patch()
      promise.success(function(data){ //success
        Notification.success(($stateParams.resourceName || 'Item')+ " updated successfully!");
        angular.forEach($rootScope.items,function(item,index){
            if(item.id == data.id){
              $rootScope.items[index] = data;
            }
        });
        $state.go($stateParams.nextState,{itemId:data.id})
      });
      promise.error(function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
}]);


app.controller('tiles.EditController',
  ['$rootScope', '$scope','$state','$stateParams', 'DataServices', 'Notification','utils',
  function ($rootScope, $scope, $state, $stateParams, DataServices, Notification, utils) {
    
    $scope.geotables = DataServices.Geotable.query({
      limit:1000000, // TODO: support paging = false in rest api
      offset: 0
    },function(){
      if($stateParams.itemId){
        $scope.item = DataServices.TileLayer.get($stateParams.itemId, function(){
          angular.forEach($scope.item.layers, function(layer,index){
            layer.$temp = {
              geotable: utils.find($scope.geotables,layer.content_type_id, 'content_type_id')
            }
          })
        });

      }
      else{
        $scope.item = DataServices.TileLayer;
        $scope.item.layers = [];
        $scope.item.add_to_catalog = false;
      }
    });

    $scope.save = function(){
      angular.forEach($scope.item.layers,function(layer,index){
          layer.content_type_id = layer.$temp.geotable.content_type_id
          layer.order = index;
      })
      var promise ;
      if($stateParams.itemId){
        promise = $scope.item.patch()
      }
      else{
        promise = $scope.item.post()
      }
      promise.success(function(data){ //success
        Notification.success("Service "+ ($stateParams.itemId ? "updated" : "added" ) + " successfully!");
        angular.forEach($rootScope.items,function(item,index){
            if(item.id == data.id){
              $rootScope.items[index] = data;
            }
        });
        $state.go("tiles.details",{itemId:data.id})
        $rootScope.refresh();
      });
      promise.error(function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
    $scope.addLayer = function(){
      var layer = {
        name: "layer_" + $scope.item.layers.length,
        $temp: {isOpen:true}
      }
      $scope.item.layers.push(layer)
      if($stateParams.itemId){
        layer.service = $scope.item.resource_uri;
      }
    }
    $scope.moveSelectedLayersUp = function(){
      
      angular.forEach($scope.item.layers,function(layer,index){
          if(layer.$temp.selected){
            var array = $scope.item.layers;
            // If there is a previous element in sections
            if(index > 0 && !array[index-1].$temp.selected){
              // Swap elements
              array.splice(index-1,2,array[index],array[index-1]);
            }
          }
      })
    }

    $scope.moveSelectedLayersDown = function(){
      var array = $scope.item.layers;
      for (var index=array.length - 2; index >= 0; index--){
        var layer = array[index]
        if(layer.$temp.selected && !array[index+1].$temp.selected){
          // Swap elements
          array.splice(index,2,array[index+1],array[index]);
        }
      }
    }

    $scope.invertColor = function(hexTripletColor) {
      if(hexTripletColor){
        var color = hexTripletColor;
        color = color.substring(1);           // remove #
        color = parseInt(color, 16);          // convert to integer
        if(color > 0x888888) return "#000000"
      }
      return "#FFFFFF"  
    }


}]);


app.controller('datastores.EditController',
  ['$rootScope','$scope','$state','$stateParams', 'DataServices', 'Notification',
  function ($rootScope, $scope, $state, $stateParams, DataServices, Notification) {
    $scope.item = DataServices[$stateParams.resource].get($stateParams.itemId);

    $scope.save = function(){
      var promise = $scope.item.patch()
      promise.success(function(data){ //success
        Notification.success(( $stateParams.resourceName || 'Item')+ " updated successfully!");
        angular.forEach($rootScope.items,function(item,index){
            if(item.id == data.id){
              $rootScope.items[index] = data;
            }
        });
        $state.go($stateParams.nextState,{itemId:data.id})
        $rootScope.refresh()
      });
      promise.error(function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }

    $scope.delete = function(){
      $rootScope.selectedItem.delete().success(function(){
        $state.go($state.$current.parent);
        $rootScope.refresh();
      });
    }

}]);

var extentMap = null;
function initExtentMap() {
 var jsonEditor = CodeMirror.fromTextArea(document.getElementById('jsonEditor'), {
        mode: "javascript"
    });
  jsonEditor.setValue('"bookmarks": [\n\t{\n\t\t"name": "<bookmark name>",\n\t\t"extent": <copy extent genrerated here>\n\t}\n]');
  $('#jsonModal').on('shown.bs.modal', function (e) {
    jsonEditor.refresh();
  });
  $('#myModal').on('shown.bs.modal', function (e) {
    //if (!extentMap) {
      extentMap = L.map('map', {
        center: [30, 30],
        zoom: 3
      });
      L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 18
      }).addTo(extentMap);
      updateExtent();
      extentMap.on('moveend', updateExtent);
    //}
  });

  function updateExtent() {
    var extentStr = "[[" + extentMap.getBounds().getWest() + "," + extentMap.getBounds().getSouth() + "],[" + extentMap.getBounds().getEast() + "," + extentMap.getBounds().getNorth() + "]]";
    $('#mapExtent').text(extentStr);
    var bookmarkExtent =
        '"extent": {"xmin": ' + extentMap.getBounds().getWest() + ',"ymin": ' + extentMap.getBounds().getSouth()
        + ',"ymax": ' + extentMap.getBounds().getNorth() + ',"xmax": ' + extentMap.getBounds().getEast() + ',"spatialReference": {"wkid": 4326,"latestWkid": 4326}}';
    $('#bookmarkExtent').text(bookmarkExtent);
  }
}


