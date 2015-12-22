'use strict';

/* Here the controllers are defines */

//generic controller
app.controller('DetailsController',
  ['$rootScope','$scope', '$state', '$stateParams', 'DataServices',
  function ($rootScope, $scope, $state, $stateParams, DataServices) {
    $rootScope.selectedItem = DataServices[$stateParams.resource].get($stateParams.itemId)
    $scope.delete = function(){
      $rootScope.selectedItem.delete().success(function(){
        console.debug($state)
        $state.go($state.$current.parent);
        $rootScope.refresh();
      });
    }
}]);

//geotables details controller
app.controller('geotables.DetailsController',
  ['$rootScope','$scope', '$state', '$stateParams', 'DataServices',
  function ($rootScope, $scope, $state, $stateParams, DataServices) {
    $scope.downloadLink = REST_URL  + "geotable/" + $stateParams.itemId + "/download/"
    $rootScope.selectedItem = DataServices.Geotable.get($stateParams.itemId,function(){
      var item = $rootScope.selectedItem

      //TODO: enable paging here
      item.featureLayers = DataServices.FeatureLayer.query({geo_table:item.id})
    });
    $scope.delete = function(){
      $rootScope.selectedItem.delete().success(function(){
        $state.go('geotables');
        $rootScope.refresh();
      });
    }
}]);

//webapps details controller
app.controller('webmaps.DetailsController',
  ['$rootScope','$scope', '$state', '$stateParams', 'DataServices',
  function ($rootScope, $scope, $state, $stateParams, DataServices) {
    $rootScope.selectedItem = DataServices.Webmap.get($stateParams.itemId,function(){
      var item = {};
      angular.copy($rootScope.selectedItem.item, item)
      item.text = JSON.parse($rootScope.selectedItem.text);
      //properties must not be exposed to client.
      delete item.id;
      delete item.created;
      delete item.modified;
      delete item.resource_uri;
      $rootScope.selectedItem.text = JSON.stringify(item, null, 4)
    });
    $scope.delete = function(){
      $rootScope.selectedItem.delete($rootScope.selectedItem.item.id).success(function(){
        $state.go('webmaps');
        $rootScope.refresh();
      });
    }
}]);

//webapps details controller
app.controller('tiles.DetailsController',
  ['$rootScope','$scope', '$state', '$stateParams', 'DataServices', 'leafletData',
  function ($rootScope, $scope, $state, $stateParams, DataServices, leafletData) {
    $scope.mapCenter= {
        lat: 0,
        lng: 0,
        zoom: 15
    };
    $scope.layers = {
      baselayers: {
          xyz: {
              name: 'OpenStreetMap (XYZ)',
              url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              type: 'xyz'
          }
      },
      overlays:{}
    };
    $rootScope.selectedItem = DataServices.TileLayer.get($stateParams.itemId,function(){
      var item = $rootScope.selectedItem;
      $scope.layers.overlays.layer = {url:item.service_url,type: 'xyz',visible: true,name: item.name};
      leafletData.getMap().then(function(map) {
        
        var extent = item.extent
        var p1 = L.latLng(extent[1],extent[0]),
            p2 = L.latLng(extent[3],extent[2]);
        $scope.bounds = L.latLngBounds(p1, p2);
        map.fitBounds($scope.bounds,{padding:[10,10]});

      })

    });
    $scope.delete = function(){
      $rootScope.selectedItem.delete().success(function(){
        $state.go('tiles');
        $rootScope.refresh();
      });
    }
}]);