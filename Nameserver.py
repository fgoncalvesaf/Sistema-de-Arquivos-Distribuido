'''
'	Projeto Final.
'	
'	Grupo: Francisco Goncalves de Almeida Filho - 403429
'		   Gabriel Araujo Saboya - 372960
'
'	Nameserver:
'
'''
import Pyro4
import itertools

@Pyro4.expose
class Nameserver(object):
	serial_num = 0
	data_servers = {}
	file_data = {}
	file_data_backup = {}
	#data_server_live = {}

	def register_data_server(self, uri):
		datanode_id = "datanode" + str(self.serial_num)
		self.data_servers.update({datanode_id:uri})
		self.serial_num = self.serial_num + 1

	def get_datanode_uri(self, name):
		return self.data_servers[self.file_data[name]]

	def get_datanode_uri_backup(self, name):
		return self.data_servers[self.file_data_backup[name]]

	def get_first_datanode(self):
		for k in self.data_servers.keys():
			return self.data_servers[k]

	def add_file_to_datanode(self, name, uri):
		datanode = None
		for key, value in self.data_servers.items():
			if value == uri:
				datanode = key
		self.file_data.update({name:datanode})

	def add_file_to_datanode_backup(self, name, uri):
		datanode = None
		for key, value in self.data_servers.items():
			if value == uri:
				datanode = key
		self.file_data_backup.update({name:datanode})

	def get_all_datanodes_uri(self):
		uris = []
		for key, value in self.data_servers.items():
			uris.append(value)
		return uris

	def remove_file(self, name):
		self.file_data.pop(name, None)
		self.file_data_backup.pop(name, None)

	def get_datanode_by_uri(self, uri):
		for key, value in self.data_servers.items():
			if value == uri:
				return key

#Exec
daemon = Pyro4.Daemon()                
uri = daemon.register(Nameserver)
print("Uri: ", uri)
daemon.requestLoop()