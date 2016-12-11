'use strict';
angular.module('dashboard')
.controller('paymentCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getCurrencies(config, function(response) {
		$scope.currencies = response.data;
	});

	getTaxrules(config, function(response) {
		$scope.taxrules = response.data;
	});

	function getCurrencies(config, callback) {
		$http.get('/api/currencies/', config).then(function(response) {
			callback(response);
		});
	}

	function getTaxrules(config, callback) {
		$http.get('/api/taxrules/', config).then(function(response) {
			callback(response);
		});
	}
})
.controller('currencyCtrl', function($scope, $http, $location, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getCurrency(config, function(response){
		$scope.currency = response.data;
	});

	function getCurrency(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/currencies/'+$routeParams['id'], config).then(function(response) {
				callback(response);
			});
		}
		else {
			callback({'data':{
				'iso_code': '', 
				'format': '', 
				'default': true, 
				'language': ''
			}});
		}
	}

	$scope.saveCurrency = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.currency.id){
			$http.put('/api/currencies/'+$scope.currency.id+'/?callback=JSON_CALLBACK', $scope.currency).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/payment/');
				}

			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/currencies/?callback=JSON_CALLBACK', $scope.currency).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/payment/');
				}
				else {
					$scope.navigateTo('/payment/currency/'+response.data.id);
				}
			});
		}
	};

	$scope.deleteCurrency = function() {
		$http.delete('/api/currencies/'+$scope.currency.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/payment/');
		});
	};
})
.controller('taxruleCtrl', function($scope, $http, $location, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getTaxrule(config, function(response){
		$scope.taxrule = response.data;
	});

	function getTaxrule(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/taxrules/'+$routeParams['id'], config).then(function(response) {
				callback(response);
			});
		}
		else {
			callback({'data':{
				'iso_code': '', 
				'format': '', 
				'default': true, 
				'language': ''
			}});
		}
	}

	$scope.saveTaxrule = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.taxrule.id){
			$http.put('/api/taxrules/'+$scope.taxrule.id+'/?callback=JSON_CALLBACK', $scope.taxrule).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/payment/');
				}

			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/taxrules/?callback=JSON_CALLBACK', $scope.taxrule).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/payment/');
				}
				else {
					$scope.navigateTo('/payment/taxrule/'+response.data.id);
				}
			});
		}
	};

	$scope.deleteTaxrule = function() {
		$http.delete('/api/taxrules/'+$scope.taxrule.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/payment/');
		});
	};
});