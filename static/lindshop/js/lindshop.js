var Lindshop = (function() {

	// The url that will be prepended for all API Calls.
	var apiUrl = "/api/";

	/**
	 * Adds a a product to the cart and creates a cart item of it.
	 */
	var addItem = function(data, callback) {
		$.post(apiUrl+"carts/1/add_item/", {id_product: parseInt(data.id_product), quantity: parseInt(data.quantity), attributes: data.attributes, csrfmiddlewaretoken: csrf}, function(response) {
			callback(response);
		});
	}

	var getCartHtml = function(id_cart, callback) {
		$.get(apiUrl+"carts/"+id_cart+"/get_cart_html/", function(response) {
			callback(response);
		});
	}

	/**
	 * Updates the quantity of the cart item to `quantity`.
	 */
	var updateItemQuantity = function (id_item, quantity) {
		console.log("changeProductQuantity");
	}

	/**
	 * Deletes an item from the cart.
	 */
	var deleteItem = function (id_item) {
		console.log("deleteItem");
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


	return {
		apiUrl: apiUrl, 
		addItem: addItem, 
		getCartHtml: getCartHtml
	}

}());