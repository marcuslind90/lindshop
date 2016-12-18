'use strict';
angular.module('dashboard')
.controller('userCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getUsers(config, function(response) {
		$scope.users = response.data;
	});


	function getUsers(config, callback) {
		$http.get('/api/users/', config).then(function(response) {
			callback(response);
		});
	}
}).controller('userSingleCtrl', function($scope, $http, $location, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getUser(config, function(response) {
		$scope.user = response.data;

		getAddress(config, function(response) {
			$scope.address = response.data;
		});
	});


	function getUser(config, callback) {
		$http.get('/api/users/'+$routeParams['id'], config).then(function(response) {
			callback(response);
		});
	}

	function getAddress(config, callback) {
		$http.get('/api/addresses/'+$scope.user.user_address[0], config).then(function(response) {
			callback(response);
		});
	}

	function getCountry(config, callback) {
		$http.get('/api/countries/'+$scope.address.country, config).then(function(response) {
			callback(response);
		});
	}

});