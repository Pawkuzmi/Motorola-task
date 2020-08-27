import http

import mysql.connector
from werkzeug.exceptions import abort

from Device import Device


def insert_device(device):
	insert_device_query = prepare_insert_device_query(device)
	insert_allowed_locations_query = prepare_allowed_locations_query(device)

	connection = get_connection()
	cursor = connection.cursor()
	try:
		cursor.execute(insert_device_query)
		if len(device.allowed_locations) > 0:
			cursor.execute(insert_allowed_locations_query)
		connection.commit()
		connection.close()
	except mysql.connector.Error as err:
		abort(http.HTTPStatus.BAD_REQUEST, description=err.msg)


def get_radio_by_id(id):
	query = prepare_get_device_by_id(id)
	connection = get_connection()
	cursor = connection.cursor()
	try:
		cursor.execute(query)
	except mysql.connector.Error as err:
		abort(http.HTTPStatus.BAD_REQUEST, description=err.msg)

	devices = []
	for (id, alias, location) in cursor:
		devices.append(Device(id, alias, location))
	connection.close()

	for device in devices:
		assign_allowed_locations_to_device(device)

	return devices

def assign_allowed_locations_to_device(device):
	query = prepare_get_locations_by_device_query(device)
	connection = get_connection()
	cursor = connection.cursor()
	try:
		cursor.execute(query)
	except mysql.connector.Error as err:
		abort(http.HTTPStatus.BAD_REQUEST, description=err.msg)

	for (id, location, device_id) in cursor:
		device.allowed_locations.append(location)

	connection.close()

def prepare_insert_device_query(device):
	query = 'INSERT INTO device (id, alias) VALUES ({0}, "{1}")'.format(device.id, device.alias)
	return query

def prepare_allowed_locations_query(device):
	values_list = []
	for location in device.allowed_locations:
		values_list.append('("{0}", {1})'.format(location, device.id))

	separator = ', '
	values = separator.join(values_list)

	query = 'INSERT INTO allowed_location (location, device_id) VALUES {0}'.format(values)
	return query

def prepare_get_device_by_id(id):
	query = 'SELECT * FROM device WHERE id = {0}'.format(id)
	return query

def prepare_get_locations_by_device_query(device):
	query = 'SELECT * FROM allowed_location WHERE device_id = {0}'.format(device.id)
	return query

def get_connection():
	# config = {
	# 	'user': 'root',
	# 	'password': 'root',
	# 	'host': 'db',
	# 	'port': '3306',
	# 	'database': 'devices'
	# }
	config = {
		'user': 'root',
		'password': 'root',
		'host': '127.0.0.1',
		'port': '33066',
		'database': 'devices'
	}
	return mysql.connector.connect(**config,
								   auth_plugin='mysql_native_password')
