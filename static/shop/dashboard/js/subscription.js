// Create the charts. Use data from the HTML document.
var ctx = document.getElementById("productType").getContext("2d");
var productCart = new Chart(ctx).Doughnut(productChartData, {
	legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
});

// Create ajax functions
$('a#check-payments').click(function(e){
	e.preventDefault();
	var location = $(this)
	$(this).addClass('disabled');
	$(this).attr('disabled', true);
	$('i.fa', this).addClass('fa-spin');

	$.post("/en/dashboard/check-payments/", {csrfmiddlewaretoken: csrf}, function(data){
		location.removeClass('disabled');
		location.attr('disabled', false);
		$('i.fa', location).removeClass('fa-spin');

		window.location.reload(true);
	});
});