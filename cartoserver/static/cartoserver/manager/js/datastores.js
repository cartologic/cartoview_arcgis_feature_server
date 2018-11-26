/* Below are the states that are used */
app.config(['$stateProvider',
  function ($stateProvider) {
  $stateProvider
    .state('datastores', {
    url:'/settings',
    params:{
      resource: "Datastore"
    },
    views:{
      'list@':{
        templateUrl: ANGULAR_TEMPLATES_ROOT + 'datastores/list.html',
        controller:'ListController'
      }
    }
      
  })
  .state('datastores.details', {
    url: "/{itemId:int}",
    views: {
        "item@" : {
          controller: 'DetailsController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'datastores/details.html' 
        }
    }
  })
  .state('datastores.add', {
    url: "/add-datastore",
    params:{
      resource: "Datastore",
      nextState: "datastores.details",
      resourceName:"Datastore"
    },
    views: {
        "item@" : {
          controller: 'AddController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'datastores/add.html' 
        }
    }
  })
  .state('datastores.edit', {
    url: "/edit-datastore/{itemId:int}",
    params:{
      resource: "Datastore",
      nextState: "datastores.details",
      resourceName:"Datastore"
    },
    views: {
        "item@" : {
          controller: 'datastores.EditController',
          templateUrl: ANGULAR_TEMPLATES_ROOT + 'datastores/edit.html' 
        }
    }
  });


}]);