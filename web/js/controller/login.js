demoApp.controller('loginController', function($scope, $http) {
    var errorCallback = function(error) {
        $scope.error = error;
        console.log(error)
    };

    $scope.user = { 'email': '' };

    $scope.addUser = function (email) {
        $http.put('/api/user',$scope.user).
            success(function(data) {
                $scope.error = undefined;
                $scope.user = data;
            }).
            error(errorCallback);
    }
});
