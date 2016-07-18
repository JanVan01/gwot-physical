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

function alert_msg(message, classy) {
	$('#alert').removeClass('alert-danger');
	$('#alert').removeClass('alert-warning');
	$('#alert').removeClass('alert-info');
	$('#alert').removeClass('alert-success');
	$('#alert').addClass("alert-"+classy);
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
			$('#ajax_form').reset();
		};
	}
	else if (typeof success === 'string') {
		options.success = function (data, status, ajax) {
			success_msg(success);
			$('#ajax_form').reset();
		};
	}
	if (data) {
		options.processData = false;
		options.data = JSON.stringify(data);
		console.log(options.data);
	}
	$.ajax(options);
}

function remove_sensor(id) {
	remove_x('/api/1.0/config/sensor/' + id)
}

function remove_notifier(id) {
	remove_x('/api/1.0/config/notification/' + id)
}

function remove_location(id) {
	remove_x('/api/1.0/config/location/' + id)
}

function remove_subscription(id) {
	remove_x('/api/1.0/config/subscription/' + id)
}

function remove_x(url) {
	if (!confirm('Are you sure you want to delete the selected entry?')) {
		return;
	}
	request('DELETE', url, 'The data has been deleted successfully.');
}

function change_password() {
	pw1 = $('#password').val();
	pw2 = $('#password2').val();
	if (pw1.length < 4) {
		error_msg('<strong>Error!</strong> Please specify a password with at least 4 chars..');
		return;
	}
	if (pw1 != pw2) {
		error_msg("<strong>Error!</strong> The passwords don't match.");
		return;
	}
	request(
		'PUT', '/api/1.0/config/password',
		'The password has been changed successfully and will be needed for the next login.',
		{password: pw1}
	);
}

var markerGroup = [];
var mymap = null;
function create_location_map(data) {
	mymap = L.map('map').setView([0, 0], 1);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);
	for (i = 0; i < data.length; i++) {
		var loc = data[i];
		var marker = L.marker(L.latLng(loc.lon, loc.lat)).addTo(mymap).bindPopup(loc.name);
		markerGroup.push(marker);
	}
	var featureGroup = new L.featureGroup(markerGroup);
	mymap.fitBounds(featureGroup.getBounds());
}

function show_marker_on_location_map(index) {
	var marker = markerGroup[index];
	var featureGroup = new L.featureGroup([marker]);
	mymap.fitBounds(featureGroup.getBounds());
	marker.openPopup();
}