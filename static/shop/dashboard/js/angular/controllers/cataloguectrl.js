'use strict';
angular.module('dashboard')
.controller('catalogueCtrl', function($scope, $http, $location){
	// Initiate Controller by setting values
	console.log("Catalogue Ctrl Loaded!");
})
.controller('categoryCtrl', function($scope, $http, $location, $routeParams){
	$scope.categories = [];
	//$scope.main_category = {name: 'Catalogue'};

	getCategory(function(response){
		$scope.main_category = response.data;
	});
	getSubCategories(function(response){
		$scope.categories = response.data;
	});
	getProducts(function(response){
		$scope.products = response.data;
	});

	function getCategory(callback) {
		if($routeParams['id']) {
			$http.get('/api/categories/'+$routeParams['id']+'?callback=JSON_CALLBACK').then(function(response){
				callback(response);
			});
		}
		else {
			callback({data: {name: 'Catalogue'}});
		}
	}

	function getSubCategories(callback) {
		if($routeParams['id']) {
			$http.get('/api/categories?parent='+$routeParams['id']+'&callback=JSON_CALLBACK', {cache: true}).then(function(response){
				callback(response);
			});
		}
		else {
			$http.get('/api/categories?callback=JSON_CALLBACK', {cache: true}).then(function(response){
				callback(response);
			});
		}
	}

	function getProducts(callback) {
		// If we're on a subcategory, get products with this category as parent.
		if($routeParams['id']) {
			var config = {
				params: {
					callback: 'JSON_CALLBACK', 
					parent: $routeParams['id'], 
				}, 
				cache: true
			}

			$http.get('/api/products', config).then(function(response){
				callback(response);
			});
		}
		// If not get all products.
		else {
			$http.get('/api/products?callback=JSON_CALLBACK', {cache: true}).then(function(response){
				callback(response);
			});
		}
	}
})
.controller('productCtrl', function($scope, $http, $routeParams){
	$scope.products = [];
	
	// If we're on a subcategory, get products with this category as parent.
	if(parent) {
		var config = {
			params: {
				callback: parent, 
				parent: $routeParams['id'], 
			}, 
			cache: true
		}

		$http.get('/api/products', config).then(function(response){
			$scope.products = response.data;
		});
	}
	// If not get all products.
	else {
		$http.get('/api/products?callback=JSON_CALLBACK', {cache: true}).then(function(response){
			$scope.products = response.data;
		});
	}
})
.controller('productSingleCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
		cache: true, 
	}
	// Get and set data.
	getProduct(config, function(response){
		$scope.product = response.data;
	});
	getCategories(config, function(response){
		$scope.categories = response.data;  // Get all Categories
	});
	getPricings(config, $routeParams['id'], function(response){  // Get pricings for this specific product
		$scope.pricings = response.data;
	});
	getTaxrules(config, null, function(response){
		$scope.taxrules = response.data;
	});
	getCurrencies(config, null, function(response){
		$scope.currencies = response.data;
	});
	getProductImages(config, $routeParams['id'], function(response){
		$scope.images = response.data;
	});
	getDefaultImage($routeParams['id'], function(response){
		$scope.upload_image = response;
	});
	/*getAttributes(config, $routeParams['id'], function(response){
		$scope.product.attribute_set = response.data;
	});*/

	function getProduct(config, callback) {
		// Load Product Data 
		if($routeParams['id']) {
			$http.get('/api/products/'+$routeParams['id'], config).then(function(response){
				callback(response);
			});
		}
		// Set default product data (For a new product)
		else {
			if($routeParams['category']){
				var category = parseInt($routeParams['category']);
			}
			else {
				var category = null;
			}
			$scope.product = {
				id: null, 
				name: '', 
				productimage_set: [], 
				short_description: '', 
				description: '', 
				active: true, 
				seo_title: '', 
				seo_description: '',
				category: category, 
				categories: [], 
				attributes: [], 
				pricing_set: []
			};	
		}
	}

	function getCategories(config, callback) {
		// Get all Categories for the Category Fields.
		$http.get('/api/categories/', config).then(function(response){
			callback(response);
		});

	};

	function getPricings(config, id_product, callback) {
		if(id_product) {
			$http.get('/api/pricings/?product='+id_product, config).then(function(response){
				callback(response);
			});
		}
		else {
			callback({data: []});
		}
	}

	function getTaxrules(config, id_taxrule, callback) {
		if(id_taxrule){
			var url = '/api/taxrules/'+id_taxrule;
		}
		else {
			var url = '/api/taxrules/';
		}
		$http.get(url, config).then(function(response){
			callback(response);
		});
	}

	function getCurrencies(config, id_currency, callback) {
		if(id_currency){
			var url = '/api/currencies/'+id_currency;
		}
		else {
			var url = '/api/currencies/';
		}

		$http.get(url, config).then(function(response){
			callback(response);
		});
	}

	function getAttributes(config, id_product, callback) {
		$http.get('/api/attributes/?product='+id_product, config).then(function(response){
			callback(response);
		});
	}

	function getProductImages(config, id_product, callback) {
		if(id_product){
			$http.get('/api/images/?product='+id_product, config).then(function(response){
				callback(response);
			});
		}
		else {
			callback({data: []});
		}
	}

	function getDefaultImage(id_product, callback) {
		callback({
			'image': null, 
			'filename': null, 
			'alt': '', 
			'featured': false, 
			'product': id_product, 
			'uploading': false
		});
	}

	$scope.addImage = function() {
		var upload_image = $scope.upload_image;
		var file = document.getElementById('upload_file').files[0], 
			reader = new FileReader();

		reader.onloadend = function(e){
			var data = e.target.result;
			// We are outside our AngularJS Scope, we need to import our scope.
			var scope = angular.element($("#upload_file")).scope();

			// Set the File Upload Data to the image parameter.
			scope.$apply(function(){
				scope.upload_image.image = data;
				scope.upload_image.filename = file.name;
			});

			// If this is the first uploaded image, then set it to featured.
			if($scope.images.length == 0) {
				scope.$apply(function(){
					scope.upload_image.featured = true;
				});
			}

			// Send the data to the Backend REST API
			$http.post('/api/images/', scope.upload_image).then(function(response){
				// Add the saved image to the Image Scope to include it on the page.
				$scope.images.push(response.data.image_data);
			});

			// Reset the #upload_file data after file has been uploaded.
			scope.$apply(function(){
				getDefaultImage($scope.product.id, function(response){
					scope.upload_image = response;
					$('#upload_file').val(null);
				});
			});
		}

		if(file){
			$scope.upload_image.uploading = true;
			reader.readAsDataURL(file);
		}
	}

	$scope.addPricing = function() {
		var data = {
			id: null, 
			price: 0, 
			product: $scope.product.id, 
			plan: null, 
		}

		getTaxrules(config, 1, function(response){
			data.taxrule = response.data.id;
			getCurrencies(config, 1, function(response){
				data.currency = response.data.id;
				$scope.pricings.push(data);
			});
		});
	}

	$scope.addAttributeChoice = function(attribute) {
		var choice = {
			'value': '', 
			'slug': ''
		};
		// If attribute already has an ID. Set it here.
		if(attribute.id){
			choice['attribute'] = attribute.id;
		}
		attribute.attributechoice_set.push(choice);
	};

	$scope.addAttribute = function() {
		var attribute = {
			'name': 'New Attribute', 
			'text_input': false, 
			'slug': 'new-attribute', 
			'attributechoice_set': [], 
			'product': $scope.product.id
		}
		$scope.product.attribute_set.push(attribute);
	};

	$scope.saveProduct = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.product.id){
			$http.put('/api/products/'+$scope.product.id+'/?callback=JSON_CALLBACK', $scope.product).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/category/'+$scope.product.category);
				}

				console.log(response);
			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/products/?callback=JSON_CALLBACK', $scope.product).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/category/'+$scope.product.category);
				}
				else {
					$scope.navigateTo('/product/'+response.data.id);
				}

				console.log(response);
			});
		}
	};

	$scope.savePricing = function(pricing) {
		if(pricing.id) {
			var url = '/api/pricings/'+pricing.id+'/?callback=JSON_CALLBACK';
			$http.put(url, pricing).then(function(response){
				$('#savebox-pricings').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.
				console.log(response);
			});
		}
		else {
			var url = '/api/pricings/?callback=JSON_CALLBACK';
			$http.post(url, pricing).then(function(response){
				$('#savebox-pricings').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.
				console.log(response);
			});
		}
	};

	$scope.saveAttribute = function(attribute) {
		console.log(attribute);
		if(attribute.id) {
			$http.put('/api/attributes/'+attribute.id+'/?callback=JSON_CALLBACK', attribute).then(function(response){
				console.log(response);
			});
		}
		else {
			$http.post('/api/attributes/?callback=JSON_CALLBACK', attribute).then(function(response){
				console.log(response);
			});
		}
	};

	$scope.deleteProduct = function() {
		$http.delete('/api/products/'+$scope.product.id+'/?callback=JSON_CALLBACK').then(function(response){
			if($scope.product.category){
				$scope.navigateTo('/category/'+$scope.product.category);
			}
			else {
				$scope.navigateTo('/catalogue/');
			}
		});
	};

	$scope.deleteImage = function(id) {
		var image_delete = $scope.images[id];
		// If attempting to delete the featured image
		if(image_delete.featured){
			// If there's "earlier" images, set the previous image to featured instead.
			if($scope.images[id-1]){
				$scope.setFeaturedImage(id-1);
			}
			// If there's "later" images, set the next image to featured instead.
			else if($scope.images[id+1]){
				$scope.setFeaturedImage(id+1);
			}
			// If this is only image, don't set anything to featured.
		}
		$http.delete('/api/images/'+image_delete.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.images.splice(id, 1);
		});
	};

	$scope.deletePricing = function(id) {
		var pricing_delete = $scope.pricings[id];
		$http.delete('/api/pricings/'+pricing_delete.id+'/?callback=JSON_CALLBACK').then(function(response){
			$scope.pricings.splice(id, 1);
		});
	};

	$scope.deleteAttribute = function(index) {
		$scope.product.attribute_set.splice(index, 1);
	};

	$scope.deleteAttributeChoice = function(attribute, index) {
		//var choice_delete = $scope.product.attribute_set.attributechoice_set[id];
		attribute.attributechoice_set.splice(index, 1);
	};

	$scope.setFeaturedImage = function(id) {
		// Loop through all images and set featured to false.
		$scope.images.forEach(function(entry){
			entry.featured = false;
		});
		// Set featured to true for the image clicked.
		$scope.images[id].featured = true;

		// Send Update API call that saves the change.
		$scope.images.forEach(function(entry){
			delete entry.image;
			$http.patch('/api/images/'+entry.id+'/', entry).then(function(response){
				console.log(response);
			});
		});
		
	};
})
.directive('featuredTooltip', function(){
	// Directive that enables Tooltip for Featured Image if the image is `featured=true`.
	return {
		restrict: 'A', 
		scope: {
			'condition': '='
		}, 
		link: function(scope, element, attributes) {
			scope.$watch('condition', function(condition){
				if(condition) {
					element.attr('data-toggle', 'tooltip');
					element.attr('data-placement', 'top');
					element.attr('title', "Featured Image");
				}
				else {
					element.attr('data-toggle', null);
					element.attr('data-placement', null);
					element.attr('title', null);
					element.tooltip('destroy');
				}
			});
		}
	}
})
.directive('featuredImage', ['$http', function($http){
	return {
		restrict: 'A', 
		link: function(scope, element, attributes) {
			scope.$watch('data-product', function(){
				$http.get('/api/images/?product='+element.data('product')+'&featured=true&callback=JSON_CALLBACK').then(function(response){
					console.log(response.data[0].image);
					element.attr('src', response.data[0].image);
				});
			});
		}
	}
}])
.directive('showtab', function(){
	return {
		link: function(scope, element, attributes) {
			element.click(function(e){
				e.preventDefault();
				$(element).tab('show');
			});
		}
	}
});