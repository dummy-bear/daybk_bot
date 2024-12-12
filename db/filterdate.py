from dateutil.parser import parse
from datetime import datetime, timedelta

class Filterdates():
	def __init__(self, s):
		self.frm = parse(s.split()[1],dayfirst=True)
		self.to = self.frm + timedelta(days=1)
		
	def __str__(self):
		s=self.frm+" - "+self.to
		return s

