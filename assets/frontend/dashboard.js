(function(){
    angular
        .module('swiftlearn.dashboard', [
            'ui.bootstrap',
        ])
        .controller('DashboardController', DashboardController)

    ;

     function DashboardController($scope) {
        // body...
        $scope.hello = 'fasfasf';
        console.log('asfafs')
    }

})();