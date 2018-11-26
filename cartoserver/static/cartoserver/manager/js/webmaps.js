/* Below are the states that are used */
app.config(['$stateProvider',
  function ($stateProvider) {
  $stateProvider
    .state('webmaps', {
    url:'/web-maps',
    params:{
      resource: "Webmap"
    },
    views:{
      'list@':{
        templateUrl: ANGULAR_TEMPLATES_ROOT + 'webmaps/list.html',
        controller:'ListController'
      }
    }
      
  })
  .state('webmaps.add', {
    url: "/add",
    views: {
        "item@" : {
          controller: 'webmaps.AddController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'webmaps/add.html' 
        }
    }
  })
  .state('webmaps.details', {
    url: "/{itemId}",
    views: {
        "item@" : {
          controller: 'webmaps.DetailsController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'webmaps/details.html' 
        }
    }
  })
  
  .state('webmaps.edit', {
    url: "/edit/{itemId}",
    params:{
      resource: "Webmap",
      nextState: "webmaps.details",
      resourceName:"map"
    },
    views: {
        "item@" : {
          controller: 'webmaps.EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'webmaps/edit.html' 
        }
    }
  });


}]);