(function() {
    angular
        .module('swiftlearn.components', [
            'ui.bootstrap'

        ])
        .controller('NavController', NavController)

    ;

    function NavController($scope){
        var self = this;
        self.logout = function(){
            

        }
    }

})();