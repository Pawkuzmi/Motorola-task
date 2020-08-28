import http

import mysql.connector
from flask import Flask, request, abort

import DB_Helper
from Device import Device

app = Flask(__name__)
POST = 'POST'
GET = 'GET'


@app.route('/')
def index():
	return 'Hello World!'

@app.route('/radios/<id>/', methods=[GET, POST])
def radios(id):
	validate_id(id)

	if request.method == POST:
		return post_new_radio(id, request)

	elif request.method == GET:
		return get_radio(id)


@app.route('/radios/<id>/location/', methods=[POST])
def assign_location(id):
	validate_id(id)

	location = request.form['location']  # TODO validate that the request contains alias
	device = DB_Helper.get_radio_by_id(id)
	if device is not None:
		if location in device.allowed_locations:
			DB_Helper.update_device_location(device, location)
			return 'location ' + location + ' allowed', http.HTTPStatus.OK
		else:
			#do nothing, leave current device's location
			return 'location ' + location + ' NOT allowed.', http.HTTPStatus.FORBIDDEN


def post_new_radio(id, req):
	alias = req.form['alias'] # TODO validate that the request contains alias
	allowed_locations = req.form.getlist('allowed-locations')
	device = Device(id, alias, None)
	device.allowed_locations = allowed_locations
	DB_Helper.insert_device(device)
	return 'Device saved', http.HTTPStatus.CREATED

def get_radio(id):
	device = DB_Helper.get_radio_by_id(id)
	if device is not None:
		return str(device), http.HTTPStatus.OK
	return 'Missing device with id: {0}'.format(id),http.HTTPStatus.NOT_FOUND

def validate_id(id):
	try:
		int(id)
	except ValueError:
		abort(http.HTTPStatus.BAD_REQUEST, description="Incorrect id format. Must be an int.")


if __name__ == '__main__':
	app.run(host='0.0.0.0')
