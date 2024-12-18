from dateutil.parser import parse
from datetime import datetime, timedelta

class Filterdates():
	def __init__(self, s):
		self.frm = parse(s,dayfirst=True, fuzzy=True)
		self.to = self.frm + timedelta(days=1)
		
	def __str__(self):
		s=str(self.frm)+" - "+str(self.to)
		return s
