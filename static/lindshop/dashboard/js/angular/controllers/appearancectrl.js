'use strict';
angular.module('dashboard')
.controller('appearanceCtrl', function($scope, $http, $location){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getMenus(config, function(response) {
		$scope.menus = response.data;
	});

	getSlideshows(config, function(response) {
		$scope.slideshows = response.data;
	});

	function getSlideshows(config, callback) {
		$http.get('/api/slideshows/', config).then(function(response) {
			callback(response);
		});
	}

	function getMenus(config, callback) {
		$http.get('/api/menus/', config).then(function(response) {
			callback(response);
		});
	}

	console.log("appearanceCtrl Loaded!");
})
.controller('menuCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}
	// Get default menu data
	$scope.selectedCategories = [];
	getMenu(config, function(response){
		$scope.menu = response.data;
	});

	// Get all Categories
	getCategories(config, function(response){
		$scope.categories = response.data;
	});

	function getMenu(config, callback) {
		// Load Product Data 
		if($routeParams['id']) {
			$http.get('/api/menus/'+$routeParams['id'], config).then(function(response){
				callback(response);
			});
		}
		// Set default product data (For a new product)
		else {

			$scope.menu = {
				id: null, 
				name: '', 
				menuitem_set: []
			};	
		}
	}

	function getCategories(config, callback) {
		// Get all Categories for the Category Fields.
		$http.get('/api/categories/', config).then(function(response){
			callback(response);
		});
	}

	function getCategory(id_category, config, callback) {
		console.log("Getting Category!");
		$http.get('/api/categories/'+id_category, config).then(function(response){
			callback(response);
		});
	}

	$scope.formatItem = function($index) {
		var item = $scope.menu.menuitem_set[$index];

		if(item['label'] == '') {
			if(item['item_type'] == "category") {
				getCategory(item['object_id'], config, function(response){
					$scope.menu.menuitem_set[$index]['formatted_label'] = response.data.name;
				});
			}
		}
		else {
			$scope.menu.menuitem_set[$index]['formatted_label'] = item['label'];
		}
	}

	$scope.addCategories = function() {

		angular.forEach($scope.selectedCategories, function(value, key){
			// If it's true/checked...
			if(value) {
				// ... then add it to the menu
				console.log(value + " " + key);
				var menu_item = {
					item_type: 'category', 
					object_id: key, 
					label: '', 
					url: ''
				}

				$scope.menu.menuitem_set.push(menu_item);
			}
		});

		// Reset to false / uncheck in end.
		$scope.selectedCategories = [];
	}

	$scope.removeItem = function(index) {
		$scope.menu.menuitem_set.splice(index, 1);
	}

	$scope.saveMenu = function(stay) {
		console.log($scope.menu);
		// If it should UPDATE a category with a PUT Call
		if($scope.menu.id){
			$http.put('/api/menus/'+$scope.menu.id+'/?callback=JSON_CALLBACK', $scope.menu).then(
				function(response) { $scope.successHandler(response, stay, '/appearance/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/menus/?callback=JSON_CALLBACK', $scope.menu).then(
				function(response) { $scope.successHandler(response, stay, '/appearance/', '/appearance/menu/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
	};

	$scope.deleteMenu = function() {
		$http.delete('/api/menus/'+$scope.menu.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/appearance/');
		});
	};

})
.controller('slideshowCtrl', function($scope, $http, $routeParams){
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		},  
	}

	getSlideshow(config, function(response){
		$scope.slideshow = response.data;
	});

	getDefaultSlide(function(response){
		$scope.slide = response;
	});

	function getDefaultSlide(callback) {
		callback({
			image: '', 
			filename: '', 
			url: '', 
			alt: '', 
			uploading: false
		});
	}

	function getSlideshow(config, callback) {
		// Load Product Data 
		if($routeParams['id']) {
			$http.get('/api/slideshows/'+$routeParams['id'], config).then(function(response){
				callback(response);
			});
		}
		// Set default product data (For a new product)
		else {
			$scope.slideshow = {
				id: null, 
				name: '', 
				slide_set: []
			};	
		}
	}

	$scope.addSlide = function() {
		var upload_image = $scope.slide;
		var file = document.getElementById('upload_file').files[0], 
			reader = new FileReader();

		reader.onloadend = function(e){
			var data = e.target.result;
			// We are outside our AngularJS Scope, we need to import our scope.
			var scope = angular.element($("#upload_file")).scope();

			// Set the File Upload Data to the image parameter.
			scope.$apply(function(){
				scope.slide.image = data;
				scope.slide.filename = file.name;
			});

			scope.slideshow.slide_set.push(scope.slide);

			scope.$apply(function(){
				getDefaultSlide(function(response){
					scope.slide = response;
					$('#upload_file').val(null);
				});
			});
		}

		if(file){
			$scope.slide.uploading = true;
			reader.readAsDataURL(file);
		}
	}

	$scope.deleteSlide = function(index) {
		$scope.slideshow.slide_set.splice(index, 1);
	}

	$scope.saveSlideshow = function(stay) {
		console.log($scope.slideshow);
		// If it should UPDATE a category with a PUT Call
		if($scope.slideshow.id){
			$http.put('/api/slideshows/'+$scope.slideshow.id+'/?callback=JSON_CALLBACK', $scope.slideshow).then(
				function(response) { $scope.successHandler(response, stay, '/appearance/'); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/slideshows/?callback=JSON_CALLBACK', $scope.slideshow).then(
				function(response) { $scope.successHandler(response, stay, '/appearance/', '/appearance/slideshow/'+response.data.id); }, 
				function(response) { $scope.errorHandler(response); }
			);
		}
	};

	$scope.deleteSlideshow = function() {
		$http.delete('/api/slideshows/'+$scope.slideshow.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.navigateTo('/appearance/');
		});
	};
});