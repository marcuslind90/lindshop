'use strict';
angular.module('dashboard')
.controller('orderCtrl', function($scope, $http, $location){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getOrders(config, function(response) {
		$scope.orders = response.data;
	});

	function getOrders(config, callback) {
		$http.get('/api/orders', config).then(function(response){
			callback(response);
		});
	}
})
.controller('orderListCtrl', function($scope, $http){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getUser(config, function(response) {
		$scope.user = response.data;
	});

	function getUser(config, callback) {
		$http.get('/api/users/'+$scope.order.user, config).then(function(response){
			callback(response);
		});
	}
})
.controller('orderSingleCtrl', function($scope, $http, $location, $routeParams){
	// Initiate Controller by setting values
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	var currentDate = new Date();
	$scope.notification = {'notification_type': 'shipping', 'date_created': currentDate}; // Set default value

	getOrder(config, function(response) {
		$scope.order = response.data;

		getUser(config, function(response) {
			$scope.user = response.data;

			getAddress(config, function(response) {
				$scope.address = response.data;
			});
		});
	});

	function getOrder(config, callback) {
		$http.get('/api/orders/'+$routeParams['id'], config).then(function(response){
			callback(response);
		});
	}

	function getUser(config, callback) {
		$http.get('/api/users/'+$scope.order.user, config).then(function(response){
			callback(response);
		});
	}

	function getAddress(config, callback) {
		$http.get('/api/addresses/'+$scope.user.user_address[0], config).then(function(response) {
			callback(response);
		});
	}

	$scope.addNotification = function() {
		$http.post('/api/orders/'+$routeParams['id']+'/add_notification/?callback=JSON_CALLBACK', $scope.notification).then(function(response){
			$scope.order.order_notification.push($scope.notification);
			$scope.notification = {'notification_type': 'shipping', 'date_created': currentDate}; // Set default value
			console.log("Saved Notification!");
		});
	};
})
.controller('notificationCtrl', function($scope, $http, $routeParams){
	console.log("notificationCtrl Loaded");
});