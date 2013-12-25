$(document).ready(function() {
	$urlbox = $('#url');
	$fg = $('.form-group');
	$count = $('#count');
	$btn = $('#submit');
	baseUrl = $('#baseurl').html();

	$btn.click(function() {
		url = $urlbox.val();
		$(this).addClass('disabled').attr('disabled', 'disabled');

		$.ajax({
			url: '/',
			type: 'POST',
			data: {url: url},
		})
		.done(function(data) {
			$fg.addClass('has-success');
			$urlbox.val(baseUrl + data);

			$urlbox[0].select();
			$count.html(parseInt($count.html(), 10) + 1);
		})
		.fail(function(jqXHR) {
			$fg.addClass('has-error');
			$urlbox.val(jqXHR.responseText || 'Something went wrong!');
		})
		.always(function() {
			$btn.removeClass('disabled');
			$btn.removeAttr('disabled');
		});
	});

	$fg.click(function() {
		$(this).removeClass('has-success has-error');
	})
});