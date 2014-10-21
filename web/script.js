	// create the module and name it demoApp
	var demoApp = angular.module('demoApp', ['ngRoute', 'ngCookies','pascalprecht.translate', 'ui.slider'])
        .run(function($rootScope,favicoService){
            $rootScope.$on('$routeChangeStart',function(){
                $rootScope.app_title = 'DemoInstance';
                favicoService.reset();
            });
        });

	// configure our routes
	demoApp.config(function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl : 'pages/image.html'
			})

            .when('/login', {
                templateUrl : 'pages/login.html'
            })

            .when('/login/:token', {
                controller : function($routeParams, $cookies, $location){
                    $cookies.token = $routeParams.token;
                    $location.path('/');
                },
                template : ''
            })

            .when('/list', {
                templateUrl : 'pages/list.html'
            })

			.when('/about', {
				templateUrl : 'pages/about.html'
			})

            .when('/instance/:image_name', {
                templateUrl : 'pages/instance.html'
            })

            .when('/instance/:image_name/:id', {
                templateUrl : 'pages/instance.html'
            })

			.when('/instance', {
				templateUrl : 'pages/instance.html'
			});
	});



    demoApp.config(function ($translateProvider, $httpProvider) {

        $httpProvider.interceptors.push(['$location','$q',function($location, $q) {
            return {
                'responseError': function(rejection) {
                    if ( rejection.status == 401 ){
                        $location.path('/login');
                    }
                    return $q.reject(rejection);
                }
            };
        }]);

        $translateProvider.translations('en', {
            SELECT_IMAGE: 'Select image',
            CREATING_INSTANCE: 'Creating instance',
            STARTING_INSTANCE: 'Starting instance',
            STARTING_SYSTEM: 'Starting system',
            CREATE_INSTANCE_OF: 'Create instance of ',
            ABOUT: 'About',
            YOU_CAN_CONNECT: 'You can connect to',
            YOUR_INSTANCE_FINISH:'Your instance will be destroy in ',
            FOR:'for',
            ERROR:'ERROR',
            TIME:'Time',
            LOGIN:'Please log in',
            LIST_INSTANCE:'My instances',
            RETURN_HOME : 'Return Home'

        });
        $translateProvider.translations('fr', {
            SELECT_IMAGE: 'Sélectionnez une image',
            CREATING_INSTANCE: 'Cr&eacute;ation de l\'instance',
            STARTING_INSTANCE: 'D&eacute;marrage instance',
            STARTING_SYSTEM: 'D&eacute;marrage du systeme',
            CREATE_INSTANCE_OF: 'Cr&eacute;ation de l\'instance ',
            ABOUT: 'A propos',
            YOU_CAN_CONNECT: 'Vous pouvez vous connecter à ',
            YOUR_INSTANCE_FINISH:'Votre instance se terminera dans ',
            FOR:'pour',
            ERROR:'ERREUR',
            TIME:'Temps',
            LOGIN:'Connectez vous',
            LIST_INSTANCE:'Mes instances',
            RETURN_HOME : 'Retourner à l\' accueil'
        });
        $translateProvider.preferredLanguage('fr');
    });
