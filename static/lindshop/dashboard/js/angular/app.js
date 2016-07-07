'use strict';
var app = angular.module('dashboard', ['ngRoute', 'ngAnimate', 'checklist-model']);
app.config(["$routeProvider", function($routeProvider){
	$routeProvider
	.when('/orders/', {controller: "orderCtrl", templateUrl: "/static/lindshop/dashboard/js/angular/templates/order-list.html"})
	.when('/orders/:id', {controller: 'orderSingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/order-single.html"})
	.when('/catalogue/', {controller: 'categoryCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/catalogue.html"})
	.when('/catalogue/add-product/:category?', {controller: 'productSingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/product-single.html"})
	.when('/catalogue/add-category/', {controller: 'categorySingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/category-single.html"})
	.when('/catalogue/add-category/:parent/', {controller: 'categorySingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/category-single.html"})
	.when('/category/:id/', {controller: 'categoryCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/catalogue.html"})
	.when('/category/:id/edit/', {controller: 'categorySingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/category-single.html"})
	.when('/product/:id/', {controller: 'productSingleCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/product-single.html"})
	.when('/appearance/', {controller: 'appearanceCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/appearance.html"})
	.when('/appearance/menu/', {controller: 'menuCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/menu.html"})
	.when('/appearance/menu/:id/', {controller: 'menuCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/menu.html"})
	.when('/appearance/slideshow/', {controller: 'slideshowCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/slideshow.html"})
	.when('/appearance/slideshow/:id/', {controller: 'slideshowCtrl', templateUrl: "/static/lindshop/dashboard/js/angular/templates/slideshow.html"})
	.otherwise({redirectTo: "/orders"})
}]);