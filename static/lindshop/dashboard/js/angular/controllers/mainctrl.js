'use strict';
angular.module('dashboard')
.controller('mainCtrl', function($scope, $http, $location){
	// Initiate Controller by setting values
	console.log("Main Ctrl Loaded!");

	$scope.navigateTo = function(url) {
		$location.path(url);
	}

	$scope.successHandler = function(response, stay, parentPath, childPath) {
		$(".error").text("").hide();
		$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

		if(!stay){
			$scope.navigateTo(parentPath);
		}
		else if(childPath) {
			$scope.navigateTo(childPath);
		}
	}

	$scope.errorHandler = function(response) {
		$.each(response['data'], function(key, value){
			$("#"+key+" .error").text(value).show();
		});
	}

}).directive('autoActive', ['$location', function ($location) {
	/*
		Directive to handle active-links in menu.
	*/
	return {
		restrict: 'A',
		scope: false,
		link: function (scope, element) {
			function setActive() {
				var path = $location.path();
				if (path) {
					angular.forEach(element.find('li'), function (li) {
						var anchor = li.querySelector('a');
						if (anchor.href.match('#' + path + '(?=\\?|$)')) {
							angular.element(li).addClass('active');
						} else {
							angular.element(li).removeClass('active');
						}
					});
				}
			}

			setActive();

			scope.$on('$locationChangeSuccess', setActive);
		}
	}
}]);