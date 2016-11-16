(function() {
    angular
        .module('swiftlearn.components', [
            'ui.bootstrap'

        ])
        .controller('NavController', NavController)

    ;

    function NavController($scope, ProfileServices, CURRENT_USER){
        var self = this;

        self.ProfileServices = ProfileServices;

        $scope.$watch(function() {
            return !ProfileServices.loading;
        }, function() {
            $scope.profile = ProfileServices.members[CURRENT_USER.id];
        });
    }

})();