'use strict';
angular.module('dashboard')
.controller('orderCtrl', function($scope, $http, $location){
	// Initiate Controller by setting values
	//$scope.orderlist = $scope.orderlist || [];
	$http.get('/api/orders?callback=JSON_CALLBACK').then(function(response){
		console.log(response);
		$scope.orderlist = response.data;
	});
})
.controller('orderSingleCtrl', function($scope, $http, $location, $routeParams){
	// Initiate Controller by setting values
	var currentDate = new Date();
	$scope.order;
	$scope.notification = {'notification_type': 'shipping', 'date_created': currentDate}; // Set default value

	$http.get('/api/orders/'+$routeParams['id']+'?callback=JSON_CALLBACK').then(function(response){
		$scope.order = response.data;
	});

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