'use strict';
angular.module('dashboard')
.controller('stockCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
		cache: true, 
	}



	getWarehouses(config, function(response) {
		$scope.warehouses = response.data;
	});


	function getWarehouses(config, callback) {
		$http.get('/api/warehouses/', config).then(function(response) {
			callback(response);
		});
	}

	console.log("appearanceCtrl Loaded!");
})
.controller('warehouseCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
		cache: true, 
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
		console.log($scope.warehouse);
		// If it should UPDATE a category with a PUT Call
		if($scope.warehouse.id){
			$http.put('/api/warehouses/'+$scope.warehouse.id+'/?callback=JSON_CALLBACK', $scope.warehouse).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/stock/');
				}

				console.log(response);
			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/warehouses/?callback=JSON_CALLBACK', $scope.warehouse).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/stock/');
				}
				else {
					$scope.navigateTo('/stock/warehouse/'+response.data.id);
				}
				console.log(response);
			});
		}
	};

	$scope.deleteWarehouse = function() {
		$http.delete('/api/warehouses/'+$scope.warehouse.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/stock/');
		});
	};

});