'''
'	Projeto Final.
'	
'	Grupo: Francisco Goncalves de Almeida Filho - 403429
'		   Gabriel Araujo Saboya - 372960
'
'	Client:
'
'''
import Pyro4

def read_file(name):
	return proxy_server.get_file(name)

def write_file_append(name, msg):
	proxy_server.write_file_append(name, msg)

def delete_content(name):
	proxy_server.clean_file(name)

def delete_file(name):
	proxy_server.remove_file(name)

def create_file(name):
	proxy_server.create_file(name)

def run_interface(command_input):
	command_input = command_input.lower().split('#')
	if len(command_input) == 2:
		if command_input[0] == 'novo':
			create_file(command_input[1])
			return True
		if command_input[0] == 'deletar':
			delete_file(command_input[1])
			return True
		if command_input[0] == 'ler':
			print(read_file(command_input[1]))
			return True
		if command_input[0] == 'apagar':
			delete_content(command_input[1])
			return True
	elif len(command_input) == 1:
		if command_input[0] == 'flw':
			print('Flw vei!')
			return False
	elif len(command_input) == 3:
		if command_input[0] == 'escrever':
			write_file_append(command_input[1], command_input[2])
			return True
	else:
		return True

#Exec
# URI DO PROXY

proxy_server = Pyro4.Proxy('PYRO:obj_a50072389c2549b996863acf689c3315@localhost:54111')

running = True
print('-------------------------------------------------------- ')
print(' | Bem vindo ao TxTCloud!')
print(' | Instrucoes: ')
print(' |   1 - Criar arquivo: novo#exemplo.txt')
print(' |   2 - Deletar arquivo: deletar#exemplo.txt')
print(' |   3 - Escrever no arquivo: escrever#exemplo.txt#mensagem')
print(' |   4 - Ler conteudo do arquivo: ler#exemplo.txt')
print(' |   5 - Limpar conteudo do arquivo: apagar#exemplo.txt')
print(' |   6 - Sair: flw')
print('-------------------------------------------------------- ')
print(' ')
while(running):
	command_input = input()
	running = run_interface(command_input)