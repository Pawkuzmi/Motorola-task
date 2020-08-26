class Device:
	def __init__(self, id, alias, location):
		self.id = id
		self.alias = alias
		self.allowed_locations = []
		self.location = location
		# self.location = None

