'''
'	Projeto Final.
'	
'	Grupo: Francisco Goncalves de Almeida Filho - 403429
'		   Gabriel Araujo Saboya - 372960
'
'	DataNode:
'
'''
import os
import Pyro4

@Pyro4.expose
class DataNode(object):
	def read_file(self, name):
		if os.path.isfile(name):
			with open(name, 'r') as f:
				content = f.read()
				return content

	def write_file_concat(self, name, msg):
		with open(name, 'a') as f:
			f.write(msg)
			f.close()

	def write_file_append(self, name, msg):
		with open(name, 'a') as f:
			msg = msg + "\n"
			f.write(msg)
			f.close()

	def write_file_above_all(self, name, msg):
		name_buffer = 'file_buffer.txt'
		create_or_clean_file(name_buffer)
		with open(name_buffer, 'a') as b:
			b.write(msg + "\n")
			with open(name, 'r') as f:
				for line in f:
					b.write(line)
				f.close()
			b.close()
		copy_file(self, name_buffer, name)
		remove_file(name_buffer)

	def create_or_clean_file(self, name):
		with open(name, 'w') as f:
			f.close()

	def remove_file(self, name):
		if os.path.isfile(name):
			os.remove(name)
			return True
		else:
			return False

	def copy_file(self, target, new_file):
		create_or_clean_file(new_file)
		with open(new_file, 'a') as n:
			with open(target, 'r') as f:
				for line in f:
					n.write(line)
				f.close()
			n.close()
		with open(new_file, 'r') as f:
			return f.read()

#Exec -------------------------------------------------------------
#Criar URI DataNode
daemon = Pyro4.Daemon()                
uri = daemon.register(DataNode)

#registrar URI do Proxy

server_proxy = Pyro4.Proxy('PYRO:obj_a50072389c2549b996863acf689c3315@localhost:54111')
server_proxy.register_data_server(uri)
 
#espera uma chamada
daemon.requestLoop()

#Testes-------------------------------------------------------------
#read_file('arquivoInexistente.txt')
#create_or_clean_file('teste.txt')
#print(read_file('teste.txt'))
#for i in range(0,1000):
#	write_file_append('teste.txt', 'linha ' + str(i) + ': teste de linha blablablabla')
#print(read_file('teste.txt'))
#write_file_concat('teste.txt', 'CONCATENAR')
#write_file_concat('teste.txt', 'CONCATENAR')
#print(read_file('teste.txt'))
#write_file_above_all('teste.txt', 'POR CIMA DE TUDO')
#print(read_file('teste.txt'))
#copy_file('teste.txt', 'teste2.txt')
#create_or_clean_file('teste.txt')
#---------------------------------------------------------------------