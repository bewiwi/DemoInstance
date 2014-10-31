module.exports = function(grunt) {
    grunt.initConfig({
        //pkg: grunt.file.readJSON('package.json'),

        concat: {
            js_application: {
                src: [
                    'script.js',
                    'js/service/*.js',
                    'js/controller/*.js'
                ],
                dest: 'public/js/app.js',
                options: {
                    banner: ";(function(window, undefined){\n",
                    footer: "\n}(window));"
                }
            },
            js_vendors: {
                src: [
                    'bower_components/jquery/dist/jquery.min.js',
                    'bower_components/angular/angular.min.js',
                    'bower_components/angular-route/angular-route.min.js',
                    'bower_components/angular-cookies/angular-cookies.min.js',
                    'bower_components/angular-translate/angular-translate.min.js',
                    'bower_components/favico.js/favico-0.3.5.min.js',
                    'bower_components/bootstrap/js/alert.js',
                    'bower_components/bootstrap/js/tooltip.js',
                    'bower_components/bootstrap/js/alert.js',
                    'bower_components/angular-slider/slider.js'
                ],
                dest: 'public/js/vendor.js'
            },
            css_app: {
                src: [
                    'css/style_theme_1.css',
                    'css/slider.css',
                    'css/table.css',
                    'css/alert.css'
                ],
                dest: 'public/css/app.css'
            },
            css_vendors: {
                src: [
                    'bower_components/bootstrap/dist/css/bootstrap.css',
                    'bower_components/components-font-awesome/css/font-awesome.css',
                    'bower_components/angular-slider/slider.css'
                ],
                dest: 'public/css/vendor.css'
            }
        },
        copy: {
            stylesheets: {
                files: [{
                        expand: true,
                        src: [
                            'bower_components/bootstrap/fonts/*',
                            'bower_components/components-font-awesome/fonts/*'
                        ],
                        dest: 'public/fonts/',
                        flatten: true
                }]
            },
            sourceMaps:  {
                files: [
                    {src: ['bower_components/jquery/dist/jquery.min.map'], dest: 'public/js/jquery.min.map'},
                    {src: ['bower_components/angular/angular.min.js.map'], dest: 'public/js/angular.min.js.map'},
                    {src: ['bower_components/angular-cookies/angular-cookies.min.js.map'], dest: 'public/js/angular-cookies.min.js.map'},
                    {src: ['bower_components/bootstrap/dist/css/bootstrap.css'], dest: 'public/css/bootstrap.css.map'}
                ]
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.registerTask('default', ['concat','copy']);
};