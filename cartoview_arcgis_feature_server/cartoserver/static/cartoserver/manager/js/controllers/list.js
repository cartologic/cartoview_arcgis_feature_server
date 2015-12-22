'use strict';


/* Here the controllers are defines */
angular.module('cartoserverManagerApp').controller('ListController',
  ['$rootScope', '$scope', '$http', '$stateParams', 'DataServices', 
  function ($rootScope,$scope, $http, $stateParams, DataServices) {  
  $rootScope.selectedItem = null
  $scope.currentPage = 1;
  $scope.messages = []


  $scope.loadData = function(currentPage){
    $scope.currentPage = currentPage;
    $rootScope.items = DataServices[$stateParams.resource].query({
      limit:ITEMS_PER_PAGE,
      offset: ($scope.currentPage - 1 ) * ITEMS_PER_PAGE
    },function(){
      $scope.totalItems = $rootScope.items.meta.total_count;
    });
  }
  $scope.loadData(1);
  
  // //ui control
  $scope.selectItem = function(item, clearMesssages){
    if (clearMesssages) $scope.messages = [];
    $rootScope.selectedItem = item;
  };
  $rootScope.refresh = function(){
    $scope.loadData($scope.currentPage);
  }
}]);

angular.module('cartoserverManagerApp').controller('geotables.ListController',
  ['$rootScope', '$scope', '$http', '$stateParams', 'DataServices', 
  function ($rootScope,$scope, $http, $stateParams, DataServices) {  
  $rootScope.selectedItem = null
  $scope.myTablesOnly = false
  $scope.currentPage = 1;
  $scope.messages = []

  $scope.loadData = function(currentPage){
    $scope.currentPage = currentPage;
    $rootScope.items = DataServices[$stateParams.resource].query({
      limit:ITEMS_PER_PAGE,
      offset: ($scope.currentPage - 1 ) * ITEMS_PER_PAGE,
      is_mine: $scope.myTablesOnly
    },function(){
      $scope.totalItems = $rootScope.items.meta.total_count;
    });
  }
  $scope.loadData(1);
  
  // //ui control
  $scope.selectItem = function(item, clearMesssages){
    if (clearMesssages) $scope.messages = [];
    $rootScope.selectedItem = item;
  };
  $rootScope.refresh = function(){
    $scope.loadData($scope.currentPage);
  }
}]);