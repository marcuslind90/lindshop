'use strict';
angular.module('dashboard')
.controller('mainCtrl', function($scope, $http, $location){
	// Initiate Controller by setting values
	console.log("Main Ctrl Loaded!");

	$scope.navigateTo = function(url) {
		$location.path(url);
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