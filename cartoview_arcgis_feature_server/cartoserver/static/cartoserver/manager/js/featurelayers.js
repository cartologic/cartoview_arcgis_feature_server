/* Below are the states that are used */
app.config(['$stateProvider',
  function ($stateProvider) {
  $stateProvider
    .state('featurelayers', {
    url:'/feature-layers',
    params:{
      resource: "FeatureLayer"
    },
    views:{
      'list@':{
        templateUrl: ANGULAR_TEMPLATES_ROOT + 'featurelayers/list.html',
        controller:'ListController'
      }
    }
      
  })
  .state('featurelayers.details', {
    url: "/{itemId:int}",
    params:{
      resource: "FeatureLayer"
    },
    views: {
        "item@" : {
          controller: 'DetailsController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'featurelayers/details.html' 
        }
    }
  })
  .state('featurelayers.add', {
    url: "/add",
    views: {
        "item@" : {
          controller: 'featurelayers.AddController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'featurelayers/add.html' 
        }
    }
  })
  .state('featurelayers.publish', {
    url: "/publish/{geotable:int}",
    views: {
        "item@" : {
          controller: 'featurelayers.AddController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'featurelayers/add.html' 
        }
    }
  })
  .state('featurelayers.edit', {
    url: "/edit/{itemId:int}",
    params:{
      resource: "FeatureLayer",
      nextState: "featurelayers.details",
      resourceName:"Feature Layer"
    },
    views: {
        "item@" : {
          controller: 'featurelayers.EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'featurelayers/edit.html' 
        }
    }
  });


}]);