class modem:
	name = None
	dbm = None
	status = None
	fill_color = "#3CB371"
	text_color = "#FFFFFF"
# 	def __init__(self, name):
# 		self.name = name
# 		self.dbm = None
# 		self.status = None
# 		self.fill_color = None
# 		self.text_color = None
	
	def set_colors(self):
		if self.status == "(Workable)\n":
			self.fill_color = "#FFD700"
			self.text_color = "#000000"
		elif self.status == "(Marginal)\n":
			self.fill_color = "#DC143C"
		elif self.status == "Baaaad":
			self.fill_color = "#DC143C"
		
