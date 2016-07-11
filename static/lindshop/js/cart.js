console.log("Cart API Loaded");

var cart_dropdown = $('.cart-dropdown ul');
var cart_summary = $('ul.checkout-cart-list');

$(document).ready(function(){
	// Normal "Add To Cart" button. This adds the product of the button
	// to the users cart.
	$('button[name="add-product"]').click(function(e){
		e.preventDefault();
		addProductToCart($(this).data('id'))
	});

	// When "Add to cart" form on Product Page is submitted. Add product to cart.
	$('form#add-product').on('submit', function(e){
		e.preventDefault();
		addProductToCartForm();
	});

	// VoucherFields "Add" button. This is the button that submits the call
	// and add the voucher to the cart.
	$('.voucher-box .voucher-field button[name="add"]').click(function(e){
		e.preventDefault();
		addVoucher($('input[name="voucher"]').val());
	});

	// The Voucher Field Close button. Push it to hide field and display the "Add Voucher"
	// button again.
	$('.voucher-box .voucher-field button[name="close"]').click(function(e){
		e.preventDefault();
		$('.voucher-box .voucher-field').hide();
		$('.voucher-box .btn-voucher').fadeIn();
	});

	// On KeyUp, check if the input field has any value (Any character typed)
	// If so, display the Add Voucher button. If no value, display the "Close" button.
	$('.voucher-field input[name="voucher"]').keyup(function(){
		if(this.value !== ""){
			$('.voucher-box .voucher-field button[name="add"]').show();
			$('.voucher-box .voucher-field button[name="close"]').hide();
		}
		else {
			$('.voucher-box .voucher-field button[name="close"]').show();
			$('.voucher-box .voucher-field button[name="add"]').hide();
		}
	});

	// When push the "Add Voucher" button, it should display
	// the voucher field.
	$('.voucher-box .btn-voucher').click(function(e){
		e.preventDefault();
		$(this).hide();
		$('.voucher-field').fadeIn();
	});

	$('#checkout').delegate('input[name="carrier"]', 'change', function(e){
		updateCarrier($(this).val());
	});

	$('select[name="country"]').on('change', function(e){
		updateCustomerCountry($(this).val());
	});

	// When a user fill in their email in the checkout, save the email to the cart.
	// This means, even if the user does not submit the checkout, we still have the email
	// and can send reminder to the cart and checkout.
	$('input[name="email"]').on('change', function(e){
		updateCustomerEmail($(this).val());
	});

	$('input[name="payment-option"]').on('change', function(e){
		$('.payment-form').slideUp().html("");
		var location = $(this);
		var id_payment = $(this).val();
		$.post("/payment-get-form/", {'id_payment': id_payment, csrfmiddlewaretoken: csrf}, function(data){
			location.parents('.form-group').children('.payment-form').html(data).slideDown();
		});
		
		console.log($(this).val())
	});

	// Delegates. This is items that are bound to events, but created
	// in the Javascript. Cart options/actions etc.
	cart_summary.delegate('a[name="remove"]', 'click', function(e){
		e.preventDefault();
		var container = $(this).parents('.dropdown-product');
		removeProductFromCart(container.data('id'));
	});

	cart_summary.delegate('input[name="amount"]', 'change', function(e){
		e.preventDefault();
		var container = $(this).parents('.dropdown-product');
		updateAmount(container.data('id'), $(this).val());
		console.log(container.data('id')+" changed to "+$(this).val());
	});

	cart_dropdown.delegate('a[name="remove"]', 'click', function(e){
		e.preventDefault();
		var container = $(this).parents('.dropdown-product');
		removeProductFromCart(container.data('id'));
	});

	cart_dropdown.delegate('input[name="amount"]', 'change', function(e){
		e.preventDefault();
		var container = $(this).parents('.dropdown-product');
		updateAmount(container.data('id'), $(this).val());
		console.log(container.data('id')+" changed to "+$(this).val());
	});
});


function addVoucher(voucher){
	$('.voucher-box .alert-danger').hide();
	$('.voucher-box .alert-success').hide();
	console.log("addVoucher called.");
	$.post('/ajax-cart/', {action: 'add-voucher', voucher: voucher, csrfmiddlewaretoken: csrf}, function(result){
		if(result['error']){
			$('.voucher-box .alert-danger').text(result['error']).show().delay(3000).fadeOut(1000);
		}
		else {
			$('.voucher-box .alert-success').text(result['success']).show().delay(3000).fadeOut(1000);
			$('.cart-price-summary ul li.voucher').show();
			$('.voucher-box .btn-voucher').show();
			$('.voucher-box .voucher-field').hide();
		}
		updateCart();
	}, "json");
}

function addProductToCartForm(){
	console.log("addProductToCartForm()");
	var id_product = $('input[name="id_product"]').val();
	var attributes = [];
	$('.product-attributes select').each(function(index, element){

		var temp_arr = {};
		temp_arr['attribute'] = $(this).attr('name');
		temp_arr['value'] = $(this).val();
		//temp_arr[$(this).attr('name')] = $(this).val();
		attributes[index] = JSON.stringify(temp_arr);
	});
	console.log(attributes);
	$.post('/ajax-cart/', {action: 'add-product-form', id_product: id_product, attributes: attributes, csrfmiddlewaretoken: csrf}, function(result){
		console.log(result);
		updateCart();
		//$('#cartModal').modal();
	});
}

function addProductToCart(id_product){
	console.log("addProductToCart()");
	disableButton(id_product);
	$.post('/ajax-cart/', {action: 'add-product', id_product: id_product, csrfmiddlewaretoken: csrf}, function(result){
		enableButton(id_product);
		updateCart();
		$('#cartModal').modal();
	});
}

function removeProductFromCart(id_product){
	$.post('/ajax-cart/', {action: 'remove-product', id_product: id_product, csrfmiddlewaretoken: csrf}, function(result){
		updateCart();
	});
}

function updateAmount(id_product, amount){
	$.post('/ajax-cart/', {action: 'update-amount', id_product: id_product, amount: amount, csrfmiddlewaretoken: csrf}, function(result){
		console.log(result);
		updateCart();
	});
}

function updateCarrier(id_carrier){
	$.post('/ajax-cart/', {action: 'update-carrier', id_carrier: id_carrier, csrfmiddlewaretoken: csrf}, function(result){
		updateCart();
	});
}

function updateCustomerEmail(email){
	$.post('/ajax-cart/', {action: 'update-email', email: email, csrfmiddlewaretoken: csrf}, function(result){
		console.log("Email updated to "+email);
	});
}

function updateCustomerCountry(id_country, cb){
	$.post('/ajax-cart/', {action: 'update-country', id_country: id_country, csrfmiddlewaretoken: csrf}, function(result){
		getCarrierList();
	});
}

function getCarrierList(){
	console.log("getCarrierList Called");
	$.post('/ajax-checkout/', {action: 'list-carriers', csrfmiddlewaretoken: csrf}, function(result){
		$('.form-group#carriers').html(result);
		updateCarrier($('input[name="carrier"]:checked').val());
	});	
}

function updateCart(){
	$.post('/ajax-cart/', {action: 'update-cart', csrfmiddlewaretoken: csrf}, function(result){
		console.log(result);
		if(result['amount'] > 0){
			$('.itemlist', cart_dropdown).html(result['html']);
			$('.empty-cart', cart_dropdown).hide();
			$('.dropdown-toggle .badge').text(result['amount']).show();
			$('.cart-summary', cart_dropdown).show();
			$('.cart-summary p.total_price').text(result['total']);
		}
		else {
			$('.itemlist', cart_dropdown).html(result['html']);
			$('.empty-cart', cart_dropdown).show();
			$('.dropdown-toggle .badge').text("0").hide();
			$('.cart-summary', cart_dropdown).hide();
		}

		// If Checkout Cart Summary exist.
		if(cart_summary.length > 0){
			cart_summary.html(result['html']);
			$('.cart-price-summary .summary span').text(result['total_decimals']);
			$('.cart-price-summary .vat span').text(result['total_vat']);
			$('.cart-price-summary .voucher span').text("-"+result['total_discount']);
			$('.cart-price-summary .total span').text(result['total_to_pay']);
			$('.cart-price-summary .shipping span').text(result['total_shipping']);
		}
	}, "json");
}

function disableButton(id_product){
	$('button[data-id="'+id_product+'"]').attr('disable', 'disabled');
	$('button[data-id="'+id_product+'"]').addClass('disabled');
	$('button[data-id="'+id_product+'"]').prop('disable', true);
}


function enableButton(id_product){
	$('button[data-id="'+id_product+'"]').attr('disable', '');
	$('button[data-id="'+id_product+'"]').removeClass('disabled');
	$('button[data-id="'+id_product+'"]').prop('disable', false);
}
