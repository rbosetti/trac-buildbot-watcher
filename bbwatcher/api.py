import xmlrpclib

from model import Builder, Build

class BuildBotSystem(object):
	def __init__(self, url):
		self.server = xmlrpclib.ServerProxy(url)
	def getAllBuildsInInterval(self, start, stop):
		return self.server.getAllBuildsInInterval(start, stop)
	def getBuilder(self, name):
		s = self.server
		builds = [Build(name, s.getBuild(-i)) for i in range(5, 1, -1)]
		return Builder(name, builds, [])
	def getAllBuilders(self):
		return self.server.getAllBuilders()
