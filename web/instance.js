demoApp.controller('instanceController', function($scope, $http, $interval,$routeParams,$location) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    if(! $routeParams.image_name) {
        $location.path('/');
    }

    $http.get('/image/'+$routeParams.image_name).
        success(function(data) {
            $scope.image = data;
        }).
        error(errorCallback)

    $scope.createInstance = function() {
        $scope.cloud_instance = {};

        $http.put('/instance/'+ $routeParams.image_name).
            success(function(data) {
                $scope.cloud_instance = data;

                var refreshInterval = $interval(
                    function() {
                        $http.get('/instance/' + $scope.cloud_instance.id).
                            success(function(data) {
                                $scope.state = data;

                                if ($scope.state.system_up) {
                                    $interval.cancel(refreshInterval);
                                }
                            }).
                            error(errorCallback);
                    },
                    15000
                );
            }).
            error(errorCallback);
    };
});
