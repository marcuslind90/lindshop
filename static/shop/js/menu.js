$('ul.nav-stacked ul.nav-stacked').hide();

if($('li.active').length > 0){
	$('li.active').parents('ul.nav-stacked').show().prev().find('i').removeClass('fa-angle-down').addClass('fa-angle-up');
}

if($('li.active i').length > 0) {
	$('li.active > a > span > i').removeClass('fa-angle-down').addClass('fa-angle-up');
	$('li.active').next('ul.nav-stacked').show();
}

$('ul.nav-stacked li a span').click(function(e){
	e.preventDefault();

	if($('i', this).hasClass('fa-angle-down')){
		$('i', this).removeClass('fa-angle-down');
		$('i', this).addClass('fa-angle-up');

		$(this).closest('li').next('ul.nav-stacked').slideDown(100);
	}
	else {
		$('i', this).removeClass('fa-angle-up');
		$('i', this).addClass('fa-angle-down');

		$(this).closest('li').next('ul.nav-stacked').slideUp(100);
	}
});



