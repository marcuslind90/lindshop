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
			$http.get('/api/categories?parent='+$routeParams['id']+'&callback=JSON_CALLBACK').then(function(response){
				callback(response);
			});
		}
		else {
			$http.get('/api/categories?callback=JSON_CALLBACK').then(function(response){
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
			}

			$http.get('/api/products', config).then(function(response){
				callback(response);
			});
		}
		// If not get all products.
		else {
			$http.get('/api/products?callback=JSON_CALLBACK').then(function(response){
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
		}

		$http.get('/api/products', config).then(function(response){
			$scope.products = response.data;
		});
	}
	// If not get all products.
	else {
		$http.get('/api/products?callback=JSON_CALLBACK').then(function(response){
			$scope.products = response.data;
		});
	}
})
.controller('categorySingleCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}

	getCategory(config, function(response){
		console.log(response);
		$scope.category = response.data; // Get the category of this page.
	});
	getCategories(config, function(response){
		$scope.categories = response.data;  // Get all Categories
	});

	function getCategory(config, callback) {
		if($routeParams['id']) {
			$http.get('/api/categories/'+$routeParams['id'], config).then(function(response){
				callback(response);
			});
		}
		else {
			var data = {};
			console.log("Setting default data!");
			data['data'] =  {
				"id": null,
				"name": "",
				"description": "",
				"image": null,
				"slug": "",
				"parent": null
			};
			
			if($routeParams['parent']){
				data['data']['parent'] = parseInt($routeParams['parent']);
			}

			callback(data);
			
		}
	}

	function getCategories(config, callback) {
		// Get all Categories for the Category Fields.
		$http.get('/api/categories/', config).then(function(response){
			callback(response);
		});
	};

	$scope.saveCategory = function(stay) {
		console.log($scope.category);
		// If it should UPDATE a category with a PUT Call
		if($scope.category.id){
			$http.put('/api/categories/'+$scope.category.id+'/?callback=JSON_CALLBACK', $scope.category).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/category/'+response.data.id);
				}

				console.log(response);
			});
		}
		// If it should CREATE a product with a POST call
		else {
			$http.post('/api/categories/?callback=JSON_CALLBACK', $scope.category).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/category/'+response.data.id);
				}
				else {
					$scope.navigateTo('/category/'+response.data.id);
				}
				console.log(response);
			});
		}
	};

	$scope.deleteCategory = function() {
		$http.delete('/api/categories/'+$scope.category.id+'/?callback=JSON_CALLBACK').then(function(response){
			if($scope.category.parent){
				$scope.navigateTo('/category/'+$scope.category.parent);
			}
			else {
				$scope.navigateTo('/catalogue/');
			}
		});
	};

})
.controller('productSingleCtrl', function($scope, $http, $routeParams){
	// Set config for HTTP calls
	var config = {
		params: {
			callback: 'JSON_CALLBACK', 
		}, 
	}
	$scope.stock = [];
	$scope.dataPreset = {
		'label': '', 
		'selected': null
	};
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
	getWarehouses(config, function(response){
		$scope.warehouses = response.data;
		// For each warehouse fetched, get the stock of the product in each warehouse
		$scope.warehouses.forEach(function(warehouse){
			getStock(config, $routeParams['id'], warehouse.id, function(response){
				$scope.stock[warehouse.id] = response.data;
			});
		});
	});

	getDataPresets(config, function(response){
		$scope.dataPresets = response.data;
	});
	

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
				attribute_set: [], 
				pricing_set: [], 
				productdata_set: []
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
			'uploading': false
		});
	}

	function getWarehouses(config, callback) {
		$http.get('/api/warehouses/', config).then(function(response){
			callback(response)
		});
	}

	function getStock(config, id_product, id_warehouse, callback) {
		if(id_product){
			console.log(id_product);
			$http.get('/api/stock/?product='+id_product+'&warehouse='+id_warehouse, config).then(function(response){
				callback(response);
			});
		}
		else {
			callback({data:[]});
		}

	}

	function getDataPresets(config, callback) {
		$http.get('/api/productdatapresets/', config).then(function(response){
			callback(response);
		});
	};

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
			if($scope.product.productimage_set.length == 0) {
				scope.$apply(function(){
					scope.upload_image.featured = true;
				});
			}

			scope.product.productimage_set.push(scope.upload_image);

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

	$scope.addDiscount = function() {
		var data = {
			value: 0, 
			value_type: "percentage", 
			min_amount: 0, 
			product: $scope.product.id
		}
		$scope.product.discount_set.push(data);
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

	$scope.addStock = function(warehouse) {
		var stock = {
			'stock': 1, 
			'shelf': '', 
			'product': $scope.product.id, 
			'warehouse': warehouse.id
		};
		$scope.stock[warehouse.id].push(stock);
	};

	$scope.addData = function() {
		$scope.product.productdata_set.push({
			'label': '', 
			'value': ''
		});
	};

	$scope.saveDataPreset = function() {
		var preset = {
			'label': $scope.dataPreset.label, 
			'data': $scope.product.productdata_set
		}

		$http.post('/api/productdatapresets/?callback=JSON_CALLBACK', preset).then(function(response){
			$scope.dataPresets.push(response.data);
			console.log(response);
		});
	}

	$scope.loadDataPreset = function() {
		// If a preset is selected...
		if($scope.dataPreset.selected != null) {
			// ... then fetch the data and add it to this product...
			$http.get('/api/productdatapresets/'+$scope.dataPreset.selected+'/?callback=JSON_CALLBACK').then(function(response){
				response.data.data.forEach(function(entry){
					$scope.product.productdata_set.push({
						'label': entry.label, 
						'value': entry.value
					});
				});
				console.log(response.data.data);
			});
		}
	}

	$scope.saveProduct = function(stay) {
		// If it should UPDATE a product with a PUT Call
		if($scope.product.id){
			$http.put('/api/products/'+$scope.product.id+'/?callback=JSON_CALLBACK', $scope.product).then(function(response){
				$('#savebox').show().delay(4000).fadeOut();  // Display the "Saved!" box and fade it out after a few seconds.
				
				// Save the Stock Data
				$scope.saveStock();

				// If stay is not true, then navigate the user back to category page.
				if(!stay){
					$scope.navigateTo('/category/'+$scope.product.category);
				}

				console.log(response);
			});
		}
		// If it should CREATE a product with a POST call
		else {
			console.log($scope.product);
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

	$scope.saveStock = function(callback) {
		$scope.stock.forEach(function(stock){
			stock.forEach(function(stock_item){
				if(stock_item.id){
					$http.put('/api/stock/'+stock_item.id+'/?callback=JSON_CALLBACK', stock_item).then(function(response){
						console.log(response);
					});
				}
				else {
					$http.post('/api/stock/?callback=JSON_CALLBACK', stock_item).then(function(response){
						console.log(response);
					});
				}
			});
		});
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
		var image_delete = $scope.product.productimage_set[id];
		// If attempting to delete the featured image
		if(image_delete.featured){
			// If there's "earlier" images, set the previous image to featured instead.
			if($scope.product.productimage_set[id-1]){
				$scope.setFeaturedImage(id-1);
			}
			// If there's "later" images, set the next image to featured instead.
			else if($scope.product.productimage_set[id+1]){
				$scope.setFeaturedImage(id+1);
			}
			// If this is only image, don't set anything to featured.
		}

		$scope.product.productimage_set.splice(id, 1);
	};

	$scope.deleteDiscount = function(index) {
		$scope.product.discount_set.splice(index, 1);
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
		attribute.attributechoice_set.splice(index, 1);
	};

	$scope.deleteStock = function(warehouse, index) {
		console.log("Delete");
		$scope.stock[warehouse.id].splice(index, 1);
	};

	$scope.deleteData = function(index) {
		$scope.product.productdata_set.splice(index, 1);
	};

	$scope.setFeaturedImage = function(id) {
		// Loop through all images and set featured to false.
		$scope.product.productimage_set.forEach(function(entry){
			entry.featured = false;
		});

		// Set featured to true for the image clicked.
		$scope.product.productimage_set[id].featured = true;
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