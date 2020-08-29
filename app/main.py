import http

import flask
import mysql.connector
from flask import Flask, request, abort, jsonify

import DB_Helper
from Device import Device

app = Flask(__name__)
POST = 'POST'
GET = 'GET'


@app.route('/')
def index():
	return 'Hello World!'

@app.route('/radios/<id>/', methods=[GET ,POST])
def radios(id):
	id = validate_id(id)

	if request.method == POST:
		return post_new_radio(id, request)

	elif request.method == GET:
		return get_radio(id)


@app.route('/radios/<id>/location/', methods=[GET, POST])
def radio_location(id):
	validate_id(id)

	if request.method == POST:
		return post_new_location(id, request)

	elif request.method == GET:
		return get_devices_location(id)


def post_new_radio(id, req):
	alias = req.json['alias'] # TODO validate that the request contains alias
	allowed_locations = req.json['allowed_locations']
	device = Device(id, alias, None)
	device.allowed_locations = allowed_locations
	DB_Helper.insert_device(device)
	return jsonify(device.to_dict()), http.HTTPStatus.CREATED.value

def get_radio(id):
	device = DB_Helper.get_radio_by_id(id)
	if device is not None:
		return jsonify(device.to_dict()), http.HTTPStatus.OK
	return flask.Response(status=http.HTTPStatus.NOT_FOUND)


def post_new_location(id, req):
	#add a location to a device only if the location is allowed in the allowed locations list
	location_key = 'location'
	location = req.json[location_key]  # TODO validate that the request contains alias
	device = DB_Helper.get_radio_by_id(id)
	if device is not None:
		if location in device.allowed_locations:
			DB_Helper.update_device_location(device, location)
			resp = jsonify({location_key: location})
			return resp, http.HTTPStatus.OK.value
		else:
			# do nothing, leave current device's location
			return flask.Response(status=http.HTTPStatus.FORBIDDEN.value)

def get_devices_location(id):
	device = DB_Helper.get_radio_by_id(id)
	if device is not None:
		if device.location is not None:
			resp = jsonify({'location': device.location})
			return resp, http.HTTPStatus.OK.value
		else:
			return flask.Response(status=http.HTTPStatus.NOT_FOUND.value)
	else:
		return flask.Response(status=http.HTTPStatus.NOT_FOUND.value)

def validate_id(id):
	try:
		return int(id)
	except ValueError:
		abort(http.HTTPStatus.BAD_REQUEST, description="Incorrect id format. Must be an int.")


if __name__ == '__main__':
	# make service available for everyone in the local network
	app.run(host='0.0.0.0')
