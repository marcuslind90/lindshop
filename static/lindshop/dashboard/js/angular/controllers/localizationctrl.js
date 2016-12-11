'use strict';
angular.module('dashboard')
.controller('localizationCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}
	$scope.sort = 'id';
	getCountries(config, function(response) {
		$scope.countries = response.data;
	});


	function getCountries(config, callback) {
		$http.get('/api/countries/', config).then(function(response) {
			callback(response);
		});
	}

	$scope.setSort = function(string) {
		if($scope.sort == string) {
			$scope.sort = '-'+string;
		}
		else {
			$scope.sort = string;
		}

		console.log($scope.sort);
	}
})
.controller('countryCtrl', function($scope, $http, $location, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getCountry(config, function(response){
		$scope.country = response.data;
	});

	function getCountry(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/countries/'+$routeParams['id'], config).then(function(response) {
				callback(response);
			});
		}
		else {
			callback({'data':{
				'name': '', 
				'slug': '', 
				'default': true
			}});
		}
	}

	$scope.saveCountry = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.country.id){
			$http.put('/api/countries/'+$scope.country.id+'/?callback=JSON_CALLBACK', $scope.country).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/localization/');
				}

			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/countries/?callback=JSON_CALLBACK', $scope.country).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/localization/');
				}
				else {
					$scope.navigateTo('/localization/country/'+response.data.id);
				}
			});
		}
	};

	$scope.deleteCountry = function() {
		$http.delete('/api/countries/'+$scope.country.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/localization/');
		});
	};
});