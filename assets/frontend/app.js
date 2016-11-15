(function(){
    'use strict';

    angular
        .module('swiftlearn', [
            'ui.bootstrap',
            'ui.router'
        ])
        .controller('DashboardController', DashboardController)

    ;

    function DashboardController($scope) {
        // body...
       
        console.log('asfafs')
    }

})();