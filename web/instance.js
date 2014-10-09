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

            $scope.ask_instance = {
                image_name : $routeParams.image_name,
                time : $scope.image.default_time
            }
        }).
        error(errorCallback)



    if( $routeParams.id) {
        $scope.instance_id = $routeParams.id;
        $scope.state = {
            system_up: false
        };
        
        var refreshDelay = 5000,
            refreshCallback = function() {
                $http.get('/instance/' + $scope.instance_id).
                    success(function(data) {
                        angular.extend($scope.state, data);

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
            refreshTimeout;

        $scope.$watch(
            'state.system_up',
            function(v) {
                if (!v) return;
                
                $('html, body')
                    .animate({
                        scrollTop: $(document).height()
                    }, 5000);
            }
        )
        
        $scope.$on('$routeChangeStart', function() {
            $timeout.cancel(refreshTimeout);
        });

        refreshCallback();
    }

    $scope.createInstance = function(time) {
        $scope.creation_in_progress = true
        $http.put('/instance/'+ $routeParams.image_name, $scope.ask_instance).
            success(function(data) {
                $location.path('/instance/'+$routeParams.image_name+'/'+data.id)

            }).
            error(errorCallback);
    };
});
