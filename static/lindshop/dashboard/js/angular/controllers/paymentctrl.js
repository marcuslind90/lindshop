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

	getVouchers(config, function(response) {
		$scope.vouchers = response.data;
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

	function getVouchers(config, callback) {
		$http.get('/api/vouchers/', config).then(function(response) {
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
			$http.put('/api/currencies/'+$scope.currency.id+'/?callback=JSON_CALLBACK', $scope.currency).then(
				function(response) { $scope.successHandler(response, stay, '/payment/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/currencies/?callback=JSON_CALLBACK', $scope.currency).then(
				function(response) { $scope.successHandler(response, stay, '/payment/', '/payment/currency/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
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
			$http.put('/api/taxrules/'+$scope.taxrule.id+'/?callback=JSON_CALLBACK', $scope.taxrule).then(
				function(response) { $scope.successHandler(response, stay, '/payment/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/taxrules/?callback=JSON_CALLBACK', $scope.taxrule).then(
				function(response) { $scope.successHandler(response, stay, '/payment/', '/payment/taxrule/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
	};

	$scope.deleteTaxrule = function() {
		$http.delete('/api/taxrules/'+$scope.taxrule.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/payment/');
		});
	};
})
.controller('voucherCtrl', function($scope, $http, $location, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getVoucher(config, function(response){
		$scope.voucher = response.data;
	});

	function getVoucher(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/vouchers/'+$routeParams['id'], config).then(function(response) {
				callback(response);
			});
		}
		else {
			callback({'data':{
				'code': '', 
				'value': '', 
				'value_type': "percentage"
			}});
		}
	}

	$scope.saveVoucher = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.voucher.id){
			$http.put('/api/vouchers/'+$scope.voucher.id+'/?callback=JSON_CALLBACK', $scope.voucher).then(
				function(response) { $scope.successHandler(response, stay, '/payment/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/vouchers/?callback=JSON_CALLBACK', $scope.voucher).then(
				function(response) { $scope.successHandler(response, stay, '/payment/', '/payment/voucher/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
	};

	$scope.deleteVoucher = function() {
		$http.delete('/api/vouchers/'+$scope.voucher.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/payment/');
		});
	};
});