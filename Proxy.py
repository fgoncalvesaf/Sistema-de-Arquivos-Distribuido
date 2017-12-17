'''
'	Projeto Final.
'	
'	Grupo: Francisco Goncalves de Almeida Filho - 403429
'		   Gabriel Araujo Saboya - 372960
'
'	Proxy:
'
'''

import Pyro4
from random import randint

@Pyro4.expose
class Proxy(object):
	def __init__(self):
		#metodo para inicializacao do servico
		super(Proxy, self).__init__()

	def register_data_server(self, uri):
		name_server.register_data_server(uri)
		datanode_id = name_server.get_datanode_by_uri(uri)
		self.write_in_log('Novo DataNode registrado.' + '[' + datanode_id + ']')

	def get_file(self, name):

		try:
			uri = name_server.get_datanode_uri(name)
			datanode_id = name_server.get_datanode_by_uri(uri)
			datanode_server = Pyro4.Proxy(uri)
			response = datanode_server.read_file(name)
			self.write_in_log('Cliente leu o arquivo ' + name + ' do DataNode: ' + datanode_id)
			return response
		except:
			try:
				uri = name_server.get_datanode_uri_backup(name)
				datanode_id = name_server.get_datanode_by_uri(uri)
				datanode_server = Pyro4.Proxy(uri)
				response = datanode_server.read_file(name)
				self.write_in_log('Cliente leu o arquivo ' + name + ' do DataNode: ' + datanode_id)
				return response
			except:
				self.write_in_log('Cliente nao conseguiu ler o arquivo ' + name + ' do DataNode: ' + datanode_id)

	def remove_file(self, name):
		try:
			uri = name_server.get_datanode_uri(name)
			datanode_server = Pyro4.Proxy(uri)
			datanode_id = name_server.get_datanode_by_uri(uri)
			response = datanode_server.remove_file(name)
			if response:
				self.write_in_log('Cliente removeu o arquivo: ' + name + ' do DataNode: ' + datanode_id)
			uri2 = name_server.get_datanode_uri_backup(name)
			datanode_server2 = Pyro4.Proxy(uri2)
			datanode_id2 = name_server.get_datanode_by_uri(uri2)
			response2 = datanode_server2.remove_file(name)
			if response2:
				self.write_in_log('Arquivo ' + name + ' removido do backup no DataNode: ' + datanode_id2)
			name_server.remove_file(name)
		except:
			self.write_in_log('Arquivo ' + name + ' nao pode ser removido')



	def write_file_append(self, name, msg):

		try:
			uri = name_server.get_datanode_uri(name)
			datanode_server = Pyro4.Proxy(uri)
			datanode_server.write_file_append(name, msg)
			uri2 = name_server.get_datanode_uri_backup(name)
			datanode_server2 = Pyro4.Proxy(uri2)
			datanode_server2.write_file_append(name, msg)
			self.write_in_log('Cliente escreveu [' + msg + '] no arquivo: ' + name)
		except:
			self.write_in_log('Cliente nao pode escrever [' + msg + '] no arquivo: ' + name)


	def create_file(self, name):
		try:
			uris = name_server.get_all_datanodes_uri()
			num = len(uris)
			randnum = randint(1, num)
			uri = uris[randnum-1]
			datanode_server = Pyro4.Proxy(uri)
			datanode_server.create_or_clean_file(name)
			name_server.add_file_to_datanode(name, uri)
			datanode_id = name_server.get_datanode_by_uri(uri)
			randnum2 = randint(1, num)
			while randnum2 == randnum:
				randnum2 = randint(0, num)
			uri2 = uris[randnum2-1]
			datanode_server2 = Pyro4.Proxy(uri2)
			datanode_server2.create_or_clean_file(name)
			datanode_id2 = name_server.get_datanode_by_uri(uri2)
			name_server.add_file_to_datanode_backup(name, uri2)
			self.write_in_log('Cliente criou o arquivo ' + name + ' no DataNode ' + datanode_id + ' e um backup no DataNode ' + datanode_id2)
		except:
			self.write_in_log('Nao foi possivel criar o arquivo o arquivo ' + name)


	def clean_file(self, name):
		try:
			uri = name_server.get_datanode_uri(name)
			datanode_server = Pyro4.Proxy(uri)
			datanode_server.create_or_clean_file(name)
			uri2 = name_server.get_datanode_uri_backup(name)
			datanode_server2 = Pyro4.Proxy(uri2)
			datanode_server2.create_or_clean_file(name)
			self.write_in_log('Cliente apagou o conteudo do arquivo ' + name + ' no DataNode ' + datanode_id + ' e no backup no DataNode ' + datanode_id2)
		except:
			self.write_in_log('Não foi possivel apagar o arquivo arquivo: ' + name)
	

	def write_in_log(self, msg):
		with open(system_log, 'a') as f:
			msg = msg + "\n"
			f.write(msg)
			f.close()

#Exec
system_log = 'system_log.txt'
name_server = Pyro4.Proxy('PYRO:obj_848809160b73443db637f2a075bd7ccd@localhost:54101')
daemon = Pyro4.Daemon()                
uri = daemon.register(Proxy)
print("Uri: ", uri)
with open('system_log.txt', 'w') as f:
			f.write("Proxy inicializado. \n")
			f.close()
daemon.requestLoop()