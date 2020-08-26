import mysql.connector
from flask import Flask, request, abort

import DB_Helper
from Device import Device

app = Flask(__name__)
POST = 'POST'
GET = 'GET'


def favorite_colors():
	connection = get_connection()
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM favorite_colors')
	results = [{name: color} for (name, color) in cursor]
	cursor.close()
	connection.close()

	return results


@app.route('/')
def index():
	return 'App index'


@app.route('/siema')
def siema():
	return 'siema from my flask app;'


@app.route('/radios/<id>/', methods=[GET, POST])
def radios(id):
	id_int = 0
	try:
		id_int = int(id)
	except ValueError:
		abort(400, description="Incorrect id format. Must be an int.")

	if request.method == POST:
		alias = request.form['alias']
		location = request.form['location']
		device = Device(id, alias, location)
		query = DB_Helper.prepare_insert_query(device)

		connection = get_connection()
		cursor = connection.cursor()
		try:
			cursor.execute(query)
			connection.commit()
			connection.close()
			result = cursor.fetchone()
		except Exception:
			abort(400, description="Query unseccessfull")

		return 'alias: ' + alias + '; location: ' + location + '; id: ' + id

	elif request.method == GET:
		return 'siema in GET ' + id


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


if __name__ == '__main__':
	app.run(host='0.0.0.0')
