import configparser
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

	# ID of a device id a primary key, so getting a device from DB will take at most 1 device
	if len(devices) == 1:
		assign_allowed_locations_to_device(devices[0])
		return devices[0]
	return None

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


def update_device_location(device, location):
	query = prepare_update_device_location_query(device, location)
	connection = get_connection()
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
	except mysql.connector.Error as err:
		abort(http.HTTPStatus.BAD_REQUEST, description=err.msg)

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

def prepare_update_device_location_query(device, location):
	query = 'UPDATE device SET location = "{0}" WHERE id = {1}'.format(location, device.id)
	return query

def get_connection():
	config = configparser.ConfigParser()
	config.read('config.ini')

	config = {
		'user': config['mysqlDB']['user'],
		'password': config['mysqlDB']['password'],
		'host': config['mysqlDB']['host'],
		'port': config['mysqlDB']['port'],
		'database': config['mysqlDB']['database']
	}
	return mysql.connector.connect(**config,
								   auth_plugin='mysql_native_password')
