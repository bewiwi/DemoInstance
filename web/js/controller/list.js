demoApp.controller('listController', function($scope, $http,$location) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    $http.get('/api/myinstance').
        success(function(data) {
            $scope.instances = data;

        }).
        error(errorCallback);

    $scope.go_to_instance = function (instance) {
        $location.path('/instance/'+instance.type+'/'+instance.id);
    }
});
