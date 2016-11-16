(function() {
    'use strict';

    angular
        .module('swiftlearn', [
            'ui.bootstrap',
            'ui.router',
            'swiftlearn.profile',
            'swiftlearn.components',
            'swiftlearn.dashboard'
        ])
        .constant('TEMPLATE_URL', '/static/frontend/templates/')
        .constant('API_URL', '/api/')
        .config(csrf)
        .config(routes)

    ;

    function csrf($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

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

    function routes($stateProvider, $urlRouterProvider, TEMPLATE_URL) {
        $urlRouterProvider.otherwise('/dashboard');

        $stateProvider

        .state('profile', {
            url: '/profile',
            templateUrl: TEMPLATE_URL +'/profile/'+'profile.html', 
            controller: 'ProfileController'

        })
    }

})();
