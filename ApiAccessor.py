import requests

class ApiAc:

	def __init__(self, web):
		self.web = web
		
	def getApi (self):
		response = requests.get(self.web)
		return response.json()