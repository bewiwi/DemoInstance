demoApp.controller('imageController', function($scope, $http, $location) {
    var errorCallback = function(error) {
        $scope.error = error;
    };

    $http.get('/image').
        success(function(data) {
            $scope.images = data;
        }).
        error(errorCallback);

    $scope.redirect_instance = function(image_name){
        $location.path('/instance/'+image_name);
    }
});
