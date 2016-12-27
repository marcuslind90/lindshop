'use strict';
var app = angular.module('dashboard', ['ngRoute', 'ngAnimate', 'checklist-model']);
app.config(["$routeProvider", "$sceDelegateProvider", function($routeProvider, $sceDelegateProvider){
	$routeProvider
	.when('/orders/', {controller: "orderCtrl", templateUrl: templates['order-list']})
	.when('/orders/:id', {controller: 'orderSingleCtrl', templateUrl: templates['order-single']})
	.when('/catalogue/', {controller: 'categoryCtrl', templateUrl: templates['catalogue']})
	.when('/catalogue/add-product/:category?', {controller: 'productSingleCtrl', templateUrl: templates['product-single']})
	.when('/catalogue/add-category/', {controller: 'categorySingleCtrl', templateUrl: templates['category-single']})
	.when('/catalogue/add-category/:parent/', {controller: 'categorySingleCtrl', templateUrl: templates['category-single']})
	.when('/category/:id/', {controller: 'categoryCtrl', templateUrl: templates['catalogue']})
	.when('/category/:id/edit/', {controller: 'categorySingleCtrl', templateUrl: templates['category-single']})
	.when('/product/:id/', {controller: 'productSingleCtrl', templateUrl: templates['product-single']})
	.when('/appearance/', {controller: 'appearanceCtrl', templateUrl: templates['appearance']})
	.when('/appearance/menu/', {controller: 'menuCtrl', templateUrl: templates['menu']})
	.when('/appearance/menu/:id/', {controller: 'menuCtrl', templateUrl: templates['menu']})
	.when('/appearance/slideshow/', {controller: 'slideshowCtrl', templateUrl: templates['slideshow']})
	.when('/appearance/slideshow/:id/', {controller: 'slideshowCtrl', templateUrl: templates['slideshow']})
	.when('/payment/', {controller: 'paymentCtrl', templateUrl: templates['payment']})
	.when('/payment/currency/', {controller: 'currencyCtrl', templateUrl: templates['currency']})
	.when('/payment/currency/:id/', {controller: 'currencyCtrl', templateUrl: templates['currency']})
	.when('/payment/taxrule/', {controller: 'taxruleCtrl', templateUrl: templates['taxrule']})
	.when('/payment/taxrule/:id/', {controller: 'taxruleCtrl', templateUrl: templates['taxrule']})
	.when('/payment/voucher/', {controller: 'voucherCtrl', templateUrl: templates['voucher']})
	.when('/payment/voucher/:id/', {controller: 'voucherCtrl', templateUrl: templates['voucher']})
	.when('/localization/', {controller: 'localizationCtrl', templateUrl: templates['localization']})
	.when('/localization/country/', {controller: 'countryCtrl', templateUrl: templates['country']})
	.when('/localization/country/:id/', {controller: 'countryCtrl', templateUrl: templates['country']})
	.when('/shipping/', {controller: 'shippingCtrl', templateUrl: templates['shipping']})
	.when('/shipping/carrier/', {controller: 'carrierCtrl', templateUrl: templates['carrier']})
	.when('/shipping/carrier/:id/', {controller: 'carrierCtrl', templateUrl: templates['carrier']})
	.when('/stock/', {controller: 'stockCtrl', templateUrl: templates['stock']})
	.when('/stock/warehouse/', {controller: 'warehouseCtrl', templateUrl: templates['warehouse']})
	.when('/stock/warehouse/:id/', {controller: 'warehouseCtrl', templateUrl: templates['warehouse']})
	.when('/users/', {controller: 'userCtrl', templateUrl: templates['user-list']})
	.when('/users/:id/', {controller: 'userSingleCtrl', templateUrl: templates['user-detail']})
	.otherwise({redirectTo: "/orders"});

	$sceDelegateProvider.resourceUrlWhitelist([
		'self', 
		static_root+'**'
	]);

}]);