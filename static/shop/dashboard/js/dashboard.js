jQuery(document).ready(function($) {
	$(".clickable-row").click(function() {
		window.document.location = $(this).data("href");
	});

	jQuery(function($) {
		$(document).tooltip({
			selector: '[data-toggle="tooltip"]'
		});
	});
});