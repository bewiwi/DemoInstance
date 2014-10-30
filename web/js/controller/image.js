demoApp.controller('imageController', function($scope, $http, $location) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    $http.get('/api/image').
        success(function(data) {
            $scope.images = data;
            var keys = Object.keys($scope.images);
            if (keys.length == 1) {
                $scope.redirect_instance(keys[0]);
            }
        }).
        error(errorCallback);

    $scope.redirect_instance = function(image_name){
        $location.path('/instance/'+image_name);
    }
});
