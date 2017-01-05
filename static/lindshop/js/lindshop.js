var Lindshop = (function() {
	// The url that will be prepended for all API Calls.
	var apiUrl = "/api/";

	/**
	 * We setup configuration and prepare CSRF tokens for any Ajax requests that
	 * will be done in the module.
	 */
	function init() {
		var csrftoken = getCookie('csrftoken');
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
	}

	/**
	 * Adds a a product to the cart and creates a cart item of it.
	 */
	var addItem = function(data, callback) {
		$.post(apiUrl+"carts/1/add_item/", {id_product: parseInt(data.id_product), quantity: parseInt(data.quantity), attributes: data.attributes}, function(response) {
			callback(response);
		});
	}

	/**
	 * Returns the HTML of the cart content. This is used to update the frontend 
	 * cart after changes to the backend. For example after product have been added or deleted.
	 */
	var getCartHtml = function(id_cart, callback) {
		$.get(apiUrl+"carts/"+id_cart+"/get_cart_html/", function(response) {
			callback(response);
		});
	}

	/**
	 * Updates the quantity of the cart item to `quantity`.
	 */
	var updateItemQuantity = function (data, callback) {
		
		$.ajax({
			url: apiUrl+"cartitems/"+data.id_item+"/update_amount/", 
			data: {
				amount: parseInt(data.amount)
			}, 
			success: function(response) {
				callback(response);
			}, 
			type: "PUT"
		});
	}

	/**
	 * Deletes an item from the cart.
	 */
	var deleteItem = function (id_item, callback) {
		$.ajax({
			url: apiUrl+"cartitems/"+data.id_item+"/", 
			success: function(response) {
				callback(response);
			}, 
			type: "DELETE"
		});
	}

	/**
	 * This can be used for Infinity Scrolls and more. It will get all the products
	 * of a category by pagination.
	 */
	var getCategoryProducts = function(id_category, filter, order_by, page) {
		console.log("getCategoryProducts");
	}

	/**
	 * Add voucher to cart in Checkout.
	 */
	var addVoucher = function(voucher) {
		console.log("addVoucher");
	}

	/**
	 * Check if the method require CSRF or not.
	 */
	var csrfSafeMethod = function (method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	/**
	 * Get cookie of the user, can be used to get csrf-token.
	 */
	var getCookie = function(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	// Initiate our Module and call our constructor
	// that set default settings such as prepare CSRF token.
	init();

	return {
		apiUrl: apiUrl, 
		addItem: addItem, 
		getCartHtml: getCartHtml, 
		updateItemQuantity: updateItemQuantity
	}

}());