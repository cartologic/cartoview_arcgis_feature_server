'use strict';


/* Here the controllers are defines */

angular.module('cartoserverManagerApp').controller('AddController',
  ['$scope', '$rootScope', '$state','$http', '$stateParams', 'DataServices', 'Notification', 'utils',
  function ($scope, $rootScope, $state, $http, $stateParams, DataServices, Notification, utils) {  
    $scope.item = DataServices[$stateParams.resource];
    $scope.save = function(){
      $scope.item.post().then(function(response){ //success
        Notification.success("You have added the new item successfully!");
        $state.go($stateParams.nextState,{itemId:response.data.id})
        $rootScope.refresh();
      }, function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
}]); 

angular.module('cartoserverManagerApp').controller('featurelayers.AddController',
  ['$scope', '$rootScope', '$state','$http', '$stateParams', 'DataServices', 'Notification', 'utils',
  function ($scope, $rootScope, $state, $http, $stateParams, DataServices, Notification, utils) {  
    $scope.item = DataServices.FeatureLayer;
    $scope.item.add_to_catalog = false;

    $scope.geotables = DataServices.Geotable.query({
      limit:1000000, // TODO: support paging = false in rest api
      offset: 0
    },function(){
      if($stateParams.geotable){
        $scope.geotable = utils.findById($scope.geotables, $stateParams.geotable);
        $scope.item.name = $scope.geotable.title
        $scope.item.description = $scope.geotable.description
      }
    });

    $scope.save = function(){
      $scope.item.geotable = $scope.geotable.id;
      $scope.item.post().then(function(response){ //success
        Notification.success("You have published the new feature layer successfully!")
        $state.go('featurelayers.details',{itemId:response.data.id})
        $rootScope.refresh();
      }, function(response){//error
        Notification.error("Error: " + response.data.error_message);
      });
    }
}]); 

angular.module('cartoserverManagerApp').controller('geotables.AddController',
  ['$scope', '$rootScope', '$state','$http', '$stateParams', 'FileUploader', 'Geotable', 'Notification',
  function ($scope, $rootScope, $state, $http, $stateParams, FileUploader, Geotable, Notification) {  
    
  $scope.addOperation = {step:1}
  $scope.promise = null;
  $scope.waitMsg = "Please wait while processing your data."
  $scope.error = false;
  $scope.saveNew = function () {

    $scope.promise = $http({
      method: 'POST',
      url: SAVE_NEW_URL,
      data: $.param($scope.tableProperties),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    }).success(function(data, status, headers, config) {
      if(data.success === false){
        Notification.error(data.error_msg);
      }
      else{
        Notification.success("Shapefile data is loaded to the database successfully!");
        Notification.success("Geotable is created successfully!");
        $state.go('geotables.details',{itemId:data.id})
        $rootScope.refresh();
      }
    }).error(function(data, status, headers, config) {
      $scope.errorMsg ="There is a problem in loading data from your shapefile.";
      $scope.error = true;
      Notification.error($scope.errorMsg);

    });
  };

  var uploader = $scope.uploader = new FileUploader({
    url: UPLOAD_URL,
    alias:'shapefile',
    queueLimit: 1
  });
  uploader.onCompleteItem = function(fileItem, response, status, headers) {
      if(response.success){
        //go to next step
        $scope.addOperation.step = 2;
        $scope.tableProperties = response.shapefileInfo
        $scope.tableProperties.title = $scope.tableProperties.name;
        $scope.hasSRID = response.shapefileInfo.srid != null;
        $scope.hasGeometryType = response.shapefileInfo.type != null;
        Notification.success("Your file is uploaded successfully!");
        if(!$scope.hasSRID)
          Notification.warning("Cannot specify the spatial reference of your shapefile please enter it manually");
      }
      else{
        Notification.error(response.error_msg);
      }
  };
}]);


angular.module('cartoserverManagerApp').controller('webmaps.AddController',
  ['$scope', '$rootScope', '$state','$http', '$stateParams', 'DataServices', 'Notification', 'utils',
  function ($scope, $rootScope, $state, $http, $stateParams, DataServices, Notification, utils) {  
    $scope.item = DataServices.Webmap;
    initExtentMap();

    $scope.geotables = DataServices.Geotable.query({
      limit:1000000, // TODO: support paging = false in rest api
      offset: 0
    },function(){
      if($stateParams.geotable){
        $scope.geotable = utils.findById($scope.geotables, $stateParams.geotable);
        $scope.item.name = $scope.geotable.title
        $scope.item.description = $scope.geotable.description
      }
    });

    $scope.save = function(){
      var config = JSON.parse($scope.item.text);
      $scope.item.item = {
        name: config.name,
        title: config.title,
        url: config.url,
        type: config.type,
        typeKeywords: config.typeKeywords,
        description: config.description,
        tags: config.tags,
        snippet: config.snippet,
        thumbnail: config.thumbnail,
        extent:config.extent
      }

      $scope.item.post().then(function(response){ //success
        Notification.success("You have created the new webmap successfully!")
        $state.go('webmaps.details',{itemId:response.data.item.id})
        $rootScope.refresh();
      }, function(response){//error
        Notification.error("Error: " + response.data.error_message);
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
