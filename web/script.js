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
            NEW_INSTANCE: 'Instances',
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
            ADD_TIME:'Extend lifetime (min.)',
            SUBMIT: 'Submit',

            LOGIN:'Please log in',
            LIST_INSTANCE:'History',
            EMAIL_SEND:'SEND',
            EMAIL_INFO:'An email will be send with your link',
            RETURN_HOME : 'Return Home',

            INSTANCE_LAUNCHED_AT: 'Startup time',
            INSTANCE_LIFE_TIME: 'Life time  (min.)',
            INSTANCE_ACTIONS: 'Actions',

            INSTANCE_STATUS : 'Status',
            INSTANCE_DELETED: 'Deleted',
            INSTANCE_CREATED: 'Instance démarrée',
            INSTANCE_DONE: 'Application démarrée',
            INSTANCE_UP : 'Instance running'
        });
        $translateProvider.translations('fr', {
            NEW_INSTANCE: 'Instances',
            CREATING_INSTANCE: 'Cr&eacute;ation de votre environnement de d&eacute;monstration',
            STARTING_INSTANCE: 'D&eacute;marrage de votre environnement de d&eacute;monstration',
            STARTING_SYSTEM: 'Configuration de votre environnement de d&eacute;monstration',
            CREATE_INSTANCE_OF: 'Cr&eacute;ation de l\'instance ',
            ABOUT: 'A propos',
            YOU_CAN_CONNECT: 'Vous pouvez vous connecter à ',
            YOUR_INSTANCE_FINISH:'Votre instance se terminera dans ',
            FOR:'pour',
            ERROR:'ERREUR',

            TIME:'Temps',
            ADD_TIME: 'Prolonger (min.)',
            SUBMIT: 'Valider',

            LOGIN:'Connectez vous',
            LIST_INSTANCE:'Historique',
            EMAIL_SEND:'Envoyer',
            EMAIL_INFO:'Un email va vous être envoyé avec votre lien pour vous connecter',
            RETURN_HOME : 'Retourner à l\' accueil',

            INSTANCE_LAUNCHED_AT: 'Jour / heure de démarrage',
            INSTANCE_LIFE_TIME: 'Durée de vie (min.)',
            INSTANCE_ACTIONS: 'Actions',

            INSTANCE_STATUS : 'Etat',
            INSTANCE_DELETED: 'Supprimée',
            INSTANCE_CREATED: 'Instance démarrée',
            INSTANCE_DONE: 'Application démarrée',
            INSTANCE_UP : 'Instance en cours'
        });
        $translateProvider.preferredLanguage('fr');
    });
