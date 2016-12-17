'use strict';
angular.module('dashboard')
.controller('stockCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getWarehouses(config, function(response) {
		$scope.warehouses = response.data;
	});


	function getWarehouses(config, callback) {
		$http.get('/api/warehouses/', config).then(function(response) {
			callback(response);
		});
	}
})
.controller('warehouseCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getCountries(config, function(response){
		$scope.countries = response.data;

		getWarehouse(config, function(response){
			$scope.warehouse = response.data;
		});
	});

	function getCountries(config, callback) {
		$http.get('/api/countries/', config).then(function(response){
			callback(response);
		});
	}

	function getWarehouse(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/warehouses/'+$routeParams['id'], config).then(function(response){
				callback(response);
			});
		}
		else {
			var data = {};
			console.log("Setting default data!");
			data['data'] =  {
				"id": null,
				"name": "",
				"address": "",
				"default": true
			};

			$scope.countries.forEach(function(country){
				if(country.default){
					data['data']['country'] = country.id;
				}
			});

			if($routeParams['parent']){
				data['data']['parent'] = parseInt($routeParams['parent']);
			}

			callback(data);
		}
	}

	$scope.saveWarehouse = function(stay) {
		// If it should UPDATE a category with a PUT Call
		if($scope.warehouse.id){
			$http.put('/api/warehouses/'+$scope.warehouse.id+'/?callback=JSON_CALLBACK', $scope.warehouse).then(
				function(response) { $scope.successHandler(response, stay, '/stock/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/warehouses/?callback=JSON_CALLBACK', $scope.warehouse).then(
				function(response) { $scope.successHandler(response, stay, '/stock/', '/stock/warehouse/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
	};

	$scope.deleteWarehouse = function() {
		$http.delete('/api/warehouses/'+$scope.warehouse.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/stock/');
		});
	};

});