'use strict';
var app = angular.module('cartoserverManagerApp', 
    ['ui.bootstrap', 'ui.router','angularFileUpload', "tastyResource", 'ui-notification', 'ui.codemirror',
    "leaflet-directive",'colorpicker.module', 'cgBusy']);

app.directive('onFinishRender', function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            if (scope.$last === true) {
                scope.$evalAsync(attr.onFinishRender);
            }
        }
    }
});
app.directive('ngConfirmClick', [
function(){
    return {
        link: function (scope, element, attr) {
            var msg = attr.ngConfirmClick || "Are you sure?";
            var clickAction = attr.confirmedClick;
            element.bind('click',function (event) {
                if ( window.confirm(msg) ) {
                    scope.$eval(clickAction)
                }
            });
        }
    };
}])
app.run(function ($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
    $rootScope.maxSize = MAX_PAGING_SIZE;
    $rootScope.itemsPerPage = ITEMS_PER_PAGE;
    var module = window.location.hash.split("/")[1];
    $rootScope.currentLocation = module ? module : "" ; 
    console.debug($state)
});
// app.config(function($httpProvider) {
//     $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
// });
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});


app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/geo-tables");
});
