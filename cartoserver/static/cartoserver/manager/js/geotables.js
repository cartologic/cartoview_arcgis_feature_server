/* Below are the states that are used */
app.config(['$stateProvider',
  function ($stateProvider) {
  $stateProvider
    .state('geotables', {
    url:'/geo-tables',
    params:{
      resource: "Geotable"
    },
    views:{
      'list@':{
        templateUrl: ANGULAR_TEMPLATES_ROOT + 'geotables/list.html',
        controller:'geotables.ListController'
      }
    }
      
  })
  .state('geotables.details', {
    url: "/{itemId:int}",
    views: {
        "item@" : {
          controller: 'geotables.DetailsController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'geotables/details.html' 
        }
    }
  })
  .state('geotables.add', {
    url: "/add",
    views: {
        "item@" : {
          controller: 'geotables.AddController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'geotables/add.html' 
        }
    }
  })
  .state('geotables.edit', {
    url: "/edit/{itemId:int}",
    params:{
      resource: "Geotable",
      nextState: "geotables.details",
      resourceName:"Geotable"
    },
    views: {
        "item@" : {
          controller: 'EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'geotables/edit.html' 
        }
    }
  });


}]);