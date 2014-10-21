demoApp.controller('instanceController', function($scope, $http, $timeout, $routeParams, $location, $sce, $rootScope, favicoService) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    if(! $routeParams.image_name) {
        $location.path('/');
    }

    //Var Ready
    $scope.image_ready = false;
    $scope.instance_ready = false;

    $scope.ask_instance = {
        image_name : '',
        time : ''
    }


    //Check if instance already exist
    $http.get('/api/myinstance').
        success(function(data) {
            var instances = data;
            angular.forEach(instances, function(instance) {
                if (instance.status != 'DELETED' && instance.type == $routeParams.image_name){
                    $location.path('/instance/'+instance.type+'/'+instance.id);
                }
            })
            $scope.instance_ready = true;
        }).
        error(errorCallback);

    $http.get('/api/image/'+$routeParams.image_name).
        success(function(data) {
            $scope.image = data;
            $scope.image.info = $sce.trustAsHtml(data.info);

            $scope.ask_instance = {
                image_name : $routeParams.image_name,
                time : $scope.image.default_time
            }
            $scope.image_ready = true;
        }).
        error(errorCallback)


    if( $routeParams.id) {
        $scope.instance_id = $routeParams.id;

        $scope.state = {
            system_up: false
        };
        
        var refreshDelay = 5000,
            refreshCallback = function() {
                $http.get('/api/instance/' + $scope.instance_id).
                    success(function(data) {
                        angular.extend($scope.state, data);

                        if ($scope.state.system_up) {
                            refreshDelay = 60000;                                                
                        }
                        if ($scope.state.life_time === 0 ) {
                            refreshDelay = 10000;
                        }

                        var title = $scope.image.name;

                        if($scope.state.life_time !== false){
                            var color = '#5CB85C';
                            if ( $scope.state.life_time < 5 ) {
                                color = '#d00';
                                title = 'TIMEOUT !!';
                            }
                            favicoService.badge($scope.state.life_time,{'bgColor' : color});
                        }
                        $rootScope.app_title = title;
                        refreshTimeout = $timeout(refreshCallback, refreshDelay)
                    }).
                    error(function(error) {
                        errorCallback(error);
                        refreshTimeout = false;
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
                    }, 2000);
            }
        )
        
        $scope.$on('$routeChangeStart', function() {
            $timeout.cancel(refreshTimeout);
        });

        refreshCallback();
    }

    $scope.createInstance = function(time) {
        $scope.creation_in_progress = true
        $http.put('/api/instance/'+ $routeParams.image_name, $scope.ask_instance).
            success(function(data) {
                $location.path('/instance/'+$routeParams.image_name+'/'+data.id);

            }).
            error(errorCallback);
    };

    $scope.post_load = false;
    $scope.edit_instance = {
        id: $scope.instance_id,
        add_time: 0
    }

    $scope.postInstance = function() {
        $scope.post_load = true;
        $http.post('/api/instance/'+ $routeParams.image_name, $scope.edit_instance).
            success(function(data) {
                refreshCallback();
                $scope.post_load = false;
                $scope.edit_instance.add_time = 0;
            }).
            error(function(error){
                $scope.post_load = false;
                errorCallback(error);
            });
    }
});
