'use strict';
angular.module('dashboard')
.controller('shippingCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
		cache: true, 
	}

	getCarriers(config, function(response) {
		$scope.carriers = response.data;
	});


	function getCarriers(config, callback) {
		$http.get('/api/carriers/', config).then(function(response) {
			callback(response);
		});
	}
})
.controller('carrierCtrl', function($scope, $http, $location, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
		cache: true, 
	}

	getCarrier(config, function(response){
		$scope.carrier = response.data;
	});

	getCountries(config, function(response){
		$scope.countries = response.data;
	});

	function getCarrier(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/carriers/'+$routeParams['id'], config).then(function(response) {
				callback(response);
			});
		}
		else {
			callback({'data':{
				'name': '', 
				'delivery_text': '', 
				'logo': true, 
				'default': '', 
				'countries': [], 
				'carrierpricing_set': []
			}});
		}
	}

	function getCountries(config, callback) {
		$http.get('/api/countries/', config).then(function(response){
			callback(response);
		});
	}

	$scope.uploadFile = function() {
		var upload_image = $scope.logo;
		var file = document.getElementById('upload_file').files[0], 
			reader = new FileReader();

		reader.onloadend = function(e){
			var data = e.target.result;
			// We are outside our AngularJS Scope, we need to import our scope.
			var scope = angular.element($("#upload_file")).scope();

			// Set the File Upload Data to the image parameter.
			scope.$apply(function(){
				scope.carrier.logo = data;
				scope.carrier.filename = file.name;
			});
		}

		if(file){
			reader.readAsDataURL(file);
		}
	};

	$scope.saveCarrier = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.carrier.id){
			$http.put('/api/carriers/'+$scope.carrier.id+'/?callback=JSON_CALLBACK', $scope.carrier).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/shipping/');
				}

			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/carriers/?callback=JSON_CALLBACK', $scope.carrier).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/shipping/');
				}
				else {
					$scope.navigateTo('/shipping/carrier/'+response.data.id);
				}
			});
		}
	};

	$scope.deleteCarrier = function() {
		$http.delete('/api/carriers/'+$scope.carrier.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/shipping/');
		});
	};
});