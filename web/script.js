	// create the module and name it demoApp
	var demoApp = angular.module('demoApp', ['ngRoute']);

	// configure our routes
	demoApp.config(function($routeProvider) {
		$routeProvider

			// route for the home page
			.when('/', {
				templateUrl : 'pages/image.html',
				controller  : 'mainController'
			})

			// route for the about page
			.when('/about', {
				templateUrl : 'pages/about.html',
				controller  : 'aboutController'
			})

			// route for the contact page
			.when('/instance', {
				templateUrl : 'pages/instance.html',
				controller  : 'contactController'
			});
	});

	// create the controller and inject Angular's $scope
	demoApp.controller('mainController', function($scope) {
		// create a message to display in our view
		$scope.message = 'Everyone come and see how good I look!';
	});

	demoApp.controller('aboutController', function($scope) {
		$scope.message = 'Look! I am an about page.';
	});

	demoApp.controller('contactController', function($scope) {
		$scope.message = 'Contact us! JK. This is just a demo.';
	});
