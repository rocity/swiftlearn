(function() {
    'use strict';

    angular
        .module('swiftlearn', [
            'ui.bootstrap',
            'ui.router',
            'swiftlearn.dashboard'
        ])
        .constant('TEMPLATE_URL', '/static/frontend/templates/')
        .config(routes)

    ;

    /////////////////////////////
    function routes($stateProvider, $urlRouterProvider, TEMPLATE_URL) {
        $urlRouterProvider.otherwise('/dashboard');

        $stateProvider

        .state('dashboard', {
            url: '/dashboard',
            templateUrl: TEMPLATE_URL + 'dashboard.html', 
            controller: 'DashboardController'

        })
    }

})();
