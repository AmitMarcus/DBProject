var mouse = angular.module('mouse', ['mouse.controllers', 'ngRoute', 'ngMap']);

mouse.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/mosaic.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "mosaic.complex";
                }
            }
        })
        .when('/hottest_city/', {
            templateUrl: 'views/hottest_city.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "hottest_city.complex";
                }
            }
        })
        .when('/hottest_season/', {
            templateUrl: 'views/hottest_season.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "hottest_season.complex";
                }
            }
        })
        .when('/most_popular_owners/', {
            templateUrl: 'views/most_popular_owners.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "most_popular_owners.complex";
                }
            }
        })
        .when('/categories_of_most_commented_events/', {
            templateUrl: 'views/categories_of_most_commented_events.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "categories_of_most_commented_events.complex";
                }
            }
        })
        .when('/most_sentimental_owners/', {
            templateUrl: 'views/most_sentimental_owners.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "most_sentimental_owners.complex";
                }
            }
        })
        .when('/count_events_by_city/', {
            templateUrl: 'views/count_events_by_city.html',
            controller: 'countEventsByCity',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "count_events_by_city.complex";
                }
            }
        })
        .when('/top_places_of_top_category/', {
            templateUrl: 'views/top_places_of_top_category.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "top_places_of_top_category.complex";
                }
            }
        })
        .when('/best_streets_USA_UK/', {
            templateUrl: 'views/best_streets_USA_UK.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "best_streets_USA_UK.complex";
                }
            }
        })
        .when('/event/', {
            templateUrl: 'views/event.html',
            controller: 'event'
        })
        .when('/search/', {
            templateUrl: 'views/search.html',
        })
        .otherwise({
            redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
});

mouse.factory('ServerService', ['$location', function ($location) {
    return {
        address: 'http://' + $location.host() + ':' + $location.port()
    };
}]);

angular.module('mouse.controllers', [])
    .controller('main', function ($scope, $http, $location, ServerService) {
        $http.get(ServerService.address + '/api/query/cities.simple/')
            .then(function (response) {
                console.log(response);
                $scope.cities = response.data;
            });
    
        $http.get(ServerService.address + '/api/query/message.simple/')
            .then(function (response) {
                console.log(response);
                $scope.message = response.data[0];
            });
    
        $scope.searchString = "";

        $scope.search = function () {
            console.log("Search...");
            var data = {};
            data.searchString = $scope.searchString;

            $http.post(ServerService.address + '/api/search/', data)
                .then(function (response) {
                    console.log(response);
                    $scope.searchResults = response.data;
                    $location.path("/search");
                });
        }
        
        $scope.sendMsg = function (data) {
            $http.post(ServerService.address + '/api/message/add/', data)
                .then(function (response) {
                    console.log(response);
                    $scope.message = data;
                });
        }

        $scope.getMapStyles = function () {
            return [{"featureType":"all","elementType":"labels","stylers":[{"visibility":"on"}]},{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"administrative.country","elementType":"labels.text.fill","stylers":[{"color":"#e5c163"}]},{"featureType":"administrative.locality","elementType":"labels.text.fill","stylers":[{"color":"#c4c4c4"}]},{"featureType":"administrative.neighborhood","elementType":"labels.text.fill","stylers":[{"color":"#e5c163"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21},{"visibility":"on"}]},{"featureType":"poi.business","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#e5c163"},{"lightness":"0"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"labels.text.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"labels.text.stroke","stylers":[{"color":"#e5c163"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"color":"#575757"}]},{"featureType":"road.arterial","elementType":"labels.text.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.arterial","elementType":"labels.text.stroke","stylers":[{"color":"#2c2c2c"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"road.local","elementType":"labels.text.fill","stylers":[{"color":"#999999"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}];
        }
    })
    .controller('event', function ($scope, $http, $routeParams, ServerService) {
        $scope.ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        var eventId = $routeParams.id;
        $http.get(ServerService.address + '/api/event/' + eventId + '/')
            .then(function (response) {
                console.log(response);
                $scope.event = response.data;
            
                if ($scope.event.latitude != null) {
                    var data = {};
                    data.latitude = $scope.event.latitude
                    data.longitude = $scope.event.longitude

                    $http.post(ServerService.address + '/api/nearby_events_by_coordinates/', data)
                        .then(function (response) {
                            console.log(response);
                            $scope.nearby = response.data;
                        });                    
                }

            });

        $http.get(ServerService.address + '/api/event/' + eventId + '/comments/')
            .then(function (response) {
                console.log(response);
                $scope.comments = response.data;
            });

        $scope.inUpdateProcess = false;
        $scope.updateButtonCaption = "Update Counters";
        $scope.updateCounters = function () {
            if ($scope.inUpdateProcess) {
                return;
            }
            
            $scope.inUpdateProcess = true;
            $scope.updateButtonCaption = "Please wait...";
            
            $http.get(ServerService.address + '/api/event/' + eventId + '/update/')
                .then(function (response) {
                    $http.get(ServerService.address + '/api/event/' + eventId + '/')
                        .then(function (response) {
                            console.log(response);
                            $scope.event = response.data;
                            $scope.inUpdateProcess = false;
                            $scope.updateButtonCaption = "Update Counters";

                            $('#updateNotify').modal();
                        });
                });
        }
        
        $scope.isInUpdateProcess = function () {
            return $scope.inUpdateProcess;
        }

        $scope.sendComment = function () {
            var data = {};
            data.newComment = $scope.newComment;

            $http.post(ServerService.address + '/api/event/' + eventId + '/comments/add/', data)
                .then(function (response) {
                    console.log(response);
                    $http.get(ServerService.address + '/api/event/' + eventId + '/comments/')
                        .then(function (response) {
                            console.log(response);
                            $scope.comments = response.data;
                        
                            $scope.newComment = "";

                            $('#addCommentNotify').modal();
                        });
                });
        }

        $scope.buyTickets = function (path) {
            if (path != null) {
                window.open(path, '_blank');
            }
        };
    })
    .controller('query', function ($scope, $http, ServerService, $routeParams) {
        $http.get(ServerService.address + '/api/query/' + $routeParams.queryName + '/')
            .then(function (response) {
                console.log(response);
                $scope.data = response.data;
            });
    })
    .controller('countEventsByCity', function ($scope, $http, ServerService, $routeParams) {
        $http.get(ServerService.address + '/api/query/cities.simple/')
            .then(function (response) {
                console.log(response);
                $scope.cities = response.data;
            });
    
        $scope.chooseCity = function() {
           $http.get(ServerService.address + '/api/count_events_by_city/' + $scope.chosenCityId + '/')
            .then(function (response) {
                console.log(response);
                $scope.chosenCity = response.data;
            });         
        }
    });;
