demoApp.controller('instanceController', function($scope, $http, $interval) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    $scope.createInstance = function() {
        $scope.cloud_instance = {};

        $http.get('/instance/start').
            success(function(data) {
                $scope.cloud_instance = data;

                var refreshInterval = $interval(
                    function() {
                        $http.get('/instance/' + $scope.cloud_instance.id).
                            success(function(data) {
                                $scope.state = data;

                                if ($scope.state.demo_address) {
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
