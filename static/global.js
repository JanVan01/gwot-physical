function error_msg(message) {
	alert_msg(message, 'danger');
}

function warning_msg(message) {
	alert_msg(message, 'warning');
}

function info_msg(message) {
	alert_msg(message, 'info');
}

function success_msg(message) {
	alert_msg(message, 'success');
}

function dismiss_alert() {
	$('#alert').hide();
}

function success_redirect(message, url) {
	success_msg(message);
	setTimeout(function(){ window.location = url; }, 1000);
}

function alert_msg(message, classy) {
	$('#alert').removeClass('alert-danger');
	$('#alert').removeClass('alert-warning');
	$('#alert').removeClass('alert-info');
	$('#alert').removeClass('alert-success');
	$('#alert').addClass("alert-" + classy);
	$('#alert_message').html(message);
	$('#alert').show();
}

function request(method, url, success, data) {
	var options = {
		url: url,
		method: method,
		error: function (ajax, status, error) {
			error_msg('<strong>Error!</strong> Sorry, the requested action could not be executed.');
		},
		contentType: 'application/json',
		dataType: "json",
		headers: {
			accept: 'application/json'
		}
	};
	if (typeof success === 'function') {
		options.success = function (data, status, ajax) {
			success(data);
		};
	} else if (typeof success === 'string') {
		options.success = function (data, status, ajax) {
			success_msg(success);
		};
	}
	if (data) {
		options.processData = false;
		options.data = JSON.stringify(data);
	}
	$.ajax(options);
}

function add_subscription(id) {
	var data = {
		notifier: id,
		sensor: $('#sensor').val(),
		settings: {}
	};
	$('.custom-settings').each(function () {
		var elem = $(this);
		data.settings[elem.attr('id')] = elem.val();
	});
	request(
		'POST', '/api/1.0/notification/subscription',
		function () {
			success_redirect('Subscription has been saved successfully.', '/subscriptions');
		},
		data
	);
}
