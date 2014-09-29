	// create the module and name it demoApp
	var demoApp = angular.module('demoApp', ['ngRoute']);

	// configure our routes
	demoApp.config(function($routeProvider) {
		$routeProvider

			// route for the home page
			.when('/', {
				templateUrl : 'pages/image.html'
			})

			// route for the about page
			.when('/about', {
				templateUrl : 'pages/about.html',
				controller  : 'aboutController'
			})

            .when('/instance/:image_name', {
                templateUrl : 'pages/instance.html'
            })

			// route for the contact page
			.when('/instance', {
				templateUrl : 'pages/instance.html'
			});
	});

	demoApp.controller('aboutController', function($scope) {
		$scope.message = 'Look! I am an about page.';
	});
