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


    if( $routeParams.id) {
        $scope.instance_id = $routeParams.id;
        var refreshDelay = 5000,
            refreshCallback = function() {
                $http.get('/instance/' + $scope.instance_id).
                    success(function(data) {
                        $scope.state = data;

                        if ($scope.state.system_up) {
                            refreshDelay = 60000;
                        }

                        refreshTimeout = $timeout(refreshCallback, refreshDelay)
                    }).
                    error(function(error) {
                        errorCallback(error);

                        refreshTimeout = $timeout(refreshCallback, refreshDelay)
                    });
            },
            refreshTimeout = $timeout(refreshCallback, refreshDelay);

        $scope.$on('$routeChangeStart', function() {
            $timeout.cancel(refreshTimeout);
        });
    }

    $scope.createInstance = function() {
        $scope.creation_in_progress = true
        $http.put('/instance/'+ $routeParams.image_name).
            success(function(data) {
                $location.path('/instance/'+$routeParams.image_name+'/'+data.id)

            }).
            error(errorCallback);
    };
});
