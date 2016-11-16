(function(){
    angular
        .module('swiftlearn.dashboard', [
            'ui.bootstrap',
        ])
        .factory('EventServices', EventServices)
        .controller('DashboardController', DashboardController)
        .directive('slUserFullname', slUserFullname)
        .directive('slEventFeedItem', slEventFeedItem)

    ;

    function DashboardController($scope, EventServices) {

        $scope.events = [];
        $scope.user = {
            lastname: 'Bar',
            firstname: 'Foo',
            position: ''
        };

        EventServices.list().then(function (response) {
            $scope.events = response.data;
        });


    }


   /**
    * Directives
    * @description All directives are prefixed with `sl` (SwiftLearn)
    *               following the best practices from ng-docs
    *             https://docs.angularjs.org/guide/directive
    */

    function slUserFullname() {
        return {
            restrict: 'E',
            scope: {
                userInfo: '=info'
            },
            templateUrl: '/static/frontend/templates/includes/user_fullname.html'
        }
    }

    function slEventFeedItem() {
        return {
            restrict: 'E',
            scope: {
                event: '=event'
            },
            templateUrl: '/static/frontend/templates/includes/event_feed_item.html'
        }
    }


    /**
     * Services (Factory)
     * @description Factories used to retrieve data for templates
     */

    function EventServices($http) {
        var services = {
            list: eventList,
        };

        return services;

        function eventList() {
            return $http.get('/api/events/');
        }
    }

})();