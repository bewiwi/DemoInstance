	// create the module and name it demoApp
	var demoApp = angular.module('demoApp', ['ngRoute','pascalprecht.translate']);

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
			})

            .when('/instance/:image_name', {
                templateUrl : 'pages/instance.html'
            })

			// route for the contact page
			.when('/instance', {
				templateUrl : 'pages/instance.html'
			});
	});



    demoApp.config(function ($translateProvider) {
        $translateProvider.translations('en', {
            SELECT_IMAGE: 'Select image',
            CREATING_INSTANCE: 'Creating instance',
            STARTING_INSTANCE: 'Starting instance',
            STARTING_SYSTEM: 'Starting system',
            CREATE_INSTANCE_OF: 'Create instance of ',
            ABOUT: 'About',
            YOU_CAN_CONNECT: 'You can connect to',
            YOUR_INSTANCE_FINISH:'Your instance will be destroy in '

        });
        $translateProvider.translations('fr', {
            SELECT_IMAGE: 'Selectionez une image',
            CREATING_INSTANCE: 'Cr&eacute;ation de l\'instance',
            STARTING_INSTANCE: 'D&eacute;marrage instance',
            STARTING_SYSTEM: 'D&eacute;marrage du systeme',
            CREATE_INSTANCE_OF: 'Cr&eacute;ation de l\'instance ',
            ABOUT: 'A propos',
            YOU_CAN_CONNECT: 'Vous pouvez vous connecter &acute;',
            YOUR_INSTANCE_FINISH:'Votre instance se terminera dans '
        });
        $translateProvider.preferredLanguage('fr');
    });