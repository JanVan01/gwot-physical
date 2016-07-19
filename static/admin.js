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

function remove_sensor(id) {
	remove_x('sensor', id);
}

function remove_notifier(id) {
	remove_x('notification', id);
}

function remove_location(id, markerIndex) {
	remove_x('location', id, function() {
		var marker = markerGroup[markerIndex];
		map.removeLayer(marker);
	});
}

function remove_subscription(id) {
	remove_x('subscription', id);
}

function remove_x(endpoint, id, callback) {
	if (!confirm('Are you sure you want to delete the selected entry?')) {
		return;
	}
	request(
		'DELETE', '/api/1.0/config/' + endpoint + '/' + id,
		function () {
			success_msg('The data has been deleted successfully.');
			$('#entry_' + id).remove();
			if (callback) {
				callback();
			}
		}
	);
}

function split_module(classpath) {
	var module = classpath.substring(0, classpath.lastIndexOf("."));
	var class_name = classpath.substring(classpath.lastIndexOf(".") + 1, classpath.length);
	return {
		module: module,
		class: class_name
	}
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

function update_config() {
	var name = $('#name').val();
	var interval = $('#interval').val();
	var location = $('#location').val();
	request(
		'PUT', '/api/1.0/config',
		'Settings updated successfully.',
		{
			name: name,
			interval: interval,
			location: location
		}
	);
}

function change_location(id) {
	update_Location_fields();
	var data = {
		id: $('#id').val(),
		name: $('#name').val(),
		lat: $('#lat').val(),
		lon: $('#lon').val(),
		height: $('#height').val()
	};
	var method = 'POST'; // Create
	if (id) {
		data.id = id;
		method = 'PUT'; // Update
	}
	request(
		method, '/api/1.0/config/location',
		function () {
			success_msg('Sensor has been saved successfully.');
			window.location = '/config/locations';
		},
		data
	);

}

function change_sensor(id) {
	var classpath = split_module($('#module').val());
	var data = {
		module: classpath.module,
		class_name: classpath.class,
		active: $('#active').is(':checked'),
		description: $('#description').val(),
		settings: {}
	};
	$('.custom-settings').each(function () {
		var elem = $(this);
		data.settings[elem.attr('id')] = elem.val();
	});
	var method = 'POST'; // Create
	if (id) {
		data.id = id;
		method = 'PUT'; // Update
	}
	request(
		method, '/api/1.0/config/sensor',
		function () {
			success_msg('Sensor has been saved successfully.');
			window.location = '/config/sensors'
		},
		data
	);
}

function change_notification(id) {
	var classpath = split_module($('#module').val());
	var data = {
		module: classpath.module,
		class_name: classpath.class,
		active: $('#active').is(':checked'),
		description: $('#description').val(),
		settings: {}
	};
	$('.custom-settings').each(function () {
		var elem = $(this);
		data.settings[elem.attr('id')] = elem.val();
	});
	var method = 'POST'; // Create
	if (id) {
		data.id = id;
		method = 'PUT'; // Update
	}
	request(
		method, '/api/1.0/config/notification',
		function () {
			success_msg('Notification has been saved successfully.');
			window.location = '/config/notifications';
		},
		data
	);
}

function change_subscription(nid, sid) {
	var data = {
		notifier: nid,
		sensor: $('#sensor').val(),
		settings: {}
	};
	$('.custom-settings').each(function () {
		var elem = $(this);
		data.settings[elem.attr('id')] = elem.val();
	});
	var method = 'POST'; // Create
	if (sid) {
		data.id = sid;
		method = 'PUT'; // Update
	}
	request(
		method, '/api/1.0/config/subscription',
		function () {
			success_msg('Subscription has been saved successfully.');
			window.location = '/config/notifications/' + nid + '/subscriptions/' + sid;
		},
		data
	);
}


var markerGroup = [];
var map = null;
var marker = null;
function create_location_map(data) {
	map = L.map('map').setView([0, 0], 1);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(map);
	for (i = 0; i < data.length; i++) {
		var loc = data[i];
		var marker = L.marker(L.latLng(loc.lon, loc.lat)).addTo(map).bindPopup(loc.name);
		markerGroup.push(marker);
	}
	var featureGroup = new L.featureGroup(markerGroup);
	map.fitBounds(featureGroup.getBounds());
}

function create_location_chooser_map() {
	map = L.map('map');
	var lon = $('#lon').val();
	var lat = $('#lat').val();
	var edit = true;
	if (!lon || !lat) {
		edit = false;
		map.setView([0, 0], 1);
		map.locate({setView: true, maxZoom: 17});
		map.on('locationfound', function (e) {
			marker = L.marker(e.latlng).addTo(map).bindPopup('Estimated location').openPopup();
		});
	} else {
		map.setView([lon, lat], 17);
		L.marker(L.latLng(lon, lat)).addTo(map).bindPopup('Original location').openPopup();
	}
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(map);
	map.on('click', function (e) {
		if (marker !== null) {
			map.removeLayer(marker);
			marker = null;
		}
		marker = L.marker(e.latlng).addTo(map);
		if (edit) {
			marker.bindPopup('<a href="javascript:reset_marker()">Reset to original location.</a>').openPopup();
		}
	});
}

function reset_marker() {
	map.removeLayer(marker);
	marker = null;
	var lon = $('#lon').val();
	var lat = $('#lat').val();
	map.setView([lon, lat], 17);
}

function update_Location_fields() {
	if (marker === null) {
		return;
	}
	var ll = marker.getLatLng();
	$('#lon').val(ll.lng);
	$('#lat').val(ll.lat);
}

function show_marker_on_location_map(index) {
	var marker = markerGroup[index];
	var featureGroup = new L.featureGroup([marker]);
	map.fitBounds(featureGroup.getBounds());
	marker.openPopup();
}
