function Instance($scope,$http) {
    $http.get('/instance/start').
        success(function(data) {
            $scope.cloud_instance = data;
        });
}