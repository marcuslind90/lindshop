$('#notification-form').on('submit', function(e){
	e.preventDefault();
	id_order 			= $('input[name="id_order"]').val();
	notification_type 	= $('select[name="notification_type"]').val();
	note 				= $('textarea[name="note"]').val();

	console.log(id_order);
	console.log(notification_type);
	console.log(note);

	$.post("/en/dashboard/add-notification/", {csrfmiddlewaretoken: csrf, id_order: id_order, notification_type: notification_type, note: note}, function(data){
		console.log("OK");
	});
});