(function() {
    angular
        .module('swiftlearn.profile', [
            'ui.bootstrap',
        ])
        .factory('ProfileServices', ProfileServices)
        .controller('ProfileController', ProfileController);

    function ProfileController($scope, ProfileServices, $log, CURRENT_USER) {
        // body...
        var self = this;

        self.ProfileServices = ProfileServices;

        $scope.$watch(function() {
            return !ProfileServices.loading;
        }, function() {
            $scope.profile = ProfileServices.members[CURRENT_USER.id];
        });
    }

    function ProfileServices($http, API_URL) {
        var service = {
            loading: false,

            list: MemberList,
            members: [],

        };
        service.list();
        return service;

        function MemberList() {
            /* @desc return list of members from endpoint
             */
            service.loading = true;
            return $http.get(API_URL + 'accounts/' + 'profiles/').then(function(response) {
                console.log(response.data, 'data');
                service.members = response.data.reduce(function(bucket, member) {
                    bucket[member.id] = member;

                    return bucket;
                }, {});

                service.loading = false;
                return response.data;
            });
        }
    }

})();
