'use strict';
var app = angular.module('dashboard', ['ngRoute', 'ngAnimate', 'checklist-model']);
app.config(["$routeProvider", function($routeProvider){
	$routeProvider
	.when('/orders/', {controller: "orderCtrl", templateUrl: "/static/shop/dashboard/js/angular/templates/order-list.html"})
	.when('/orders/:id', {controller: 'orderSingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/order-single.html"})
	.when('/catalogue/', {controller: 'categoryCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/catalogue.html"})
	.when('/catalogue/add-product/:category?', {controller: 'productSingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/product-single.html"})
	.when('/catalogue/add-category/', {controller: 'categorySingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/category-single.html"})
	.when('/catalogue/add-category/:parent/', {controller: 'categorySingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/category-single.html"})
	.when('/category/:id/', {controller: 'categoryCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/catalogue.html"})
	.when('/category/:id/edit/', {controller: 'categorySingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/category-single.html"})
	.when('/product/:id/', {controller: 'productSingleCtrl', templateUrl: "/static/shop/dashboard/js/angular/templates/product-single.html"})
	.otherwise({redirectTo: "/orders"})
}]);