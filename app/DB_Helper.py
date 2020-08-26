def prepare_insert_query(device):
	query = 'INSERT INTO device (id, alias, location) VALUES ({0}, "{1}", "{2}")'.format(device.id, device.alias,
																					 device.location)
	return query
