$('select[name="language"]').on('change', function(){
	$(this).parent('form').submit();
});