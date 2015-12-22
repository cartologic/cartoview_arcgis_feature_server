/* Below are the states that are used */
app.config(['$stateProvider',
  function ($stateProvider) {
  $stateProvider
    .state('tiles', {
    url:'/tiles',
    params:{
      resource: "TileLayer"
    },
    views:{
      'list@':{
        templateUrl: ANGULAR_TEMPLATES_ROOT + 'tiles/list.html',
        controller:'ListController'
      }
    }
      
  })
  .state('tiles.details', {
    url: "/{itemId:int}",
    views: {
        "item@" : {
          controller: 'tiles.DetailsController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'tiles/details.html' 
        }
    }
  })
  .state('tiles.add', {
    url: "/add",
    views: {
        "item@" : {
          controller: 'tiles.EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'tiles/edit.html' 
        }
    }
  })
  .state('tiles.edit', {
    url: "/edit/{itemId:int}",
    views: {
        "item@" : {
          controller: 'tiles.EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'tiles/edit.html' 
        }
    }
  });


}]);