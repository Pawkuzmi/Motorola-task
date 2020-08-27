class Device:
	def __init__(self, id, alias, location):
		self.id = id
		self.alias = alias
		self.allowed_locations = []
		self.location = location

	def __str__(self):
		return 'id: {0}, alias: {1}, location: {2}, allowed locations: {3}'.format(self.id, self.alias, self.location, self.allowed_locations)
