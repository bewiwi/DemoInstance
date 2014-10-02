demoApp.controller('instanceController', function($scope, $http, $timeout, $routeParams, $location, $sce) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    if(! $routeParams.image_name) {
        $location.path('/');
    }

    $http.get('/image/'+$routeParams.image_name).
        success(function(data) {
            $scope.image = data;
            $scope.image.info = $sce.trustAsHtml(data.info)
        }).
        error(errorCallback)

    $scope.createInstance = function() {
        $scope.cloud_instance = {};

        $http.put('/instance/'+ $routeParams.image_name).
            success(function(data) {
                $scope.cloud_instance = data;

                var refreshDelay = 15000,
                    refreshCallback = function() {
                        $http.get('/instance/' + $scope.cloud_instance.id).
                            success(function(data) {
                                $scope.state = data;

                                if ($scope.state.system_up) {
                                    refreshDelay = 60000;
                                }

                                refreshTimeout = $timeout(refreshCallback, refreshDelay)
                            }).
                            error(function() {
                                errorCallback();

                                refreshTimeout = $timeout(refreshCallback, refreshDelay)
                            });
                    },
                    refreshTimeout = $timeout(refreshCallback, refreshDelay);

                $scope.$on('$routeChangeStart', function() {
                    $timeout.cancel(refreshTimeout);
                });
            }).
            error(errorCallback);
    };
});
