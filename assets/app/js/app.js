var app = angular.module('swiftlearn', []);

app
    .controller('TestController', TestController)


function TestController($scope) {
    $scope.hello = 'world'
}