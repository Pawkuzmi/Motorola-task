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
	return 'App index'


@app.route('/siema')
def siema():
	return 'siema from my flask app;'


@app.route('/radios/<id>/', methods=[GET, POST])
def radios(id):
	try:
		int(id)
	except ValueError:
		abort(http.HTTPStatus.BAD_REQUEST, description="Incorrect id format. Must be an int.")

	if request.method == POST:
		return post_new_radio(id, request)

	elif request.method == GET:
		return get_radio(id)


@app.route('/radios/<id>/location/', methods=[POST])
def assign_location(id):
	location = request.form['location']  # TODO validate that the request contains alias
	devices = DB_Helper.get_radio_by_id(id)
	# allowed_locations = req.form.getlist('allowed-locations')
	# device = Device(id, alias, allowed_locations)
	# DB_Helper.insert_device(device)
	# return 'Device saved', http.HTTPStatus.CREATED


def post_new_radio(id, req):
	alias = req.form['alias'] # TODO validate that the request contains alias
	allowed_locations = req.form.getlist('allowed-locations')
	device = Device(id, alias, None)
	device.allowed_locations = allowed_locations
	DB_Helper.insert_device(device)
	return 'Device saved', http.HTTPStatus.CREATED

def get_radio(id):
	devices = DB_Helper.get_radio_by_id(id)
	if len(devices) == 1:
		return str(devices[0]), http.HTTPStatus.OK
	return 'Missing device with id: {0}'.format(id),http.HTTPStatus.NOT_FOUND


if __name__ == '__main__':
	app.run(host='0.0.0.0')
