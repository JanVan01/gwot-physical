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

function toc() {
	var toc = "<nav role='navigation' class='table-of-contents'><strong>Table of Contents</strong>";

	var i = 0;
	var h2 = 0;
	var h3 = 0;
	$(":header").each(function () {
		var prefix = "";
		var el = $(this);
		var level = parseInt(el.prop("tagName").replace('H', ''));
		if (level == 2) {
			h2++;
			h3 = 0;
			prefix = h2 + "&nbsp;&nbsp;"
		}
		else if (level == 3) {
			h3++;
			prefix = "&nbsp;&nbsp;" + h2 + "." + h3 + "&nbsp;&nbsp;"
		}
		else {
			return;
		}
		i++;
		var name = "toc_header_" + i
		el.prepend("<a name='" + name + "'></a>");
		toc += "<br /><a href='#" + name + "'>" + prefix + el.text() + "</a>";
	});

	toc += "</nav>";

	$("h1").after(toc);
}