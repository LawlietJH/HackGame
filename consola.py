
import operator
from datetime import datetime

#https://sites.google.com/site/programacioniiuno/temario/unidad-5---grafos/rboles?tmpl=%2Fsystem%2Fapp%2Ftemplates%2Fprint%2F&showPrintDialog=1

TITULO  = 'Hack Game'
__version__ = 'v1.0.9'

class Arbol:
	
	def __init__(self, elemento):
		self.hijos = []
		self.elemento = elemento
	
	def __str__(self):
		return self.elemento
	
	def agregarElemento(self, arbol, elementoPadre, elemento):
		subarbol = self.buscarSubarbol(arbol, elementoPadre);
		subarbol.hijos.append(Arbol(elemento))
		subarbol.hijos = self.sortChilds(subarbol)
	
	def sortChilds(self, arbol):
		hijos1, hijos2 = [], []
		hijos1 = [ (i, str(h)) for i, h in enumerate(arbol.hijos) ]
		hijos1.sort(key=lambda x: x[1])
		hijos2 = [ arbol.hijos[i] for i, _ in hijos1 ]
		return hijos2
	
	def buscarSubarbol(self, arbol, elemento):
		if arbol.elemento == elemento:
			return arbol
		for subarbol in arbol.hijos:
			arbolBuscado = self.buscarSubarbol(subarbol, elemento)
			if (arbolBuscado != None):
				return arbolBuscado
		return None
	
	def profundidad(self, arbol):
		if len(arbol.hijos) == 0: 
			return 1
		return 1 + max(map(self.profundidad, arbol.hijos))
	
	def ejecutarProfundidadPrimero(self, arbol, funcion, nvl=0):
		funcion(arbol.elemento, nvl)
		for hijo in arbol.hijos:
			self.ejecutarProfundidadPrimero(hijo, funcion, nvl+1)
	
	def printElement(self, element, nvl):
		# ~ print(' |  '*(nvl-1)+' |--'*(nvl), element)
		print('  |   '*(nvl-1)+'  |--'*((nvl-(nvl-1)) if nvl > 0 else 0), element)



class Console:
	
	def __init__(self, username, sysname):
		
		self.arbol = Arbol('Root')
		self.username = username
		self.sysname  = sysname
		self.response = ''
		self.valid_ext = ('.txt', '.log', '.exe')
		self.fileSystem()
		self.pathPos = self.searchDir(self.arbol, self.username)
		self.path = self.getPath(self.arbol)
		self.list_commands = [
			'help',			# Pedir la ayuda de comandos.
			'cls',			# Limpiar Pantalla.
			'exit',			# Salir de Consola, cerrar el Juego.
			'cd',			# Permite cambiar de directorio.
			'dir',			# Lista los Archivos y Carpetas.
			'mkdir',		# Crear Carpeta
			'rm',			# Eliminar Archivo o Carpeta
			'cat',			# Leer Archivo como texto plano.
			'connect',		# Conectar a una IP
			'disconnect'	# Desconectarse de una IP.
		]
		
	def getResponse(self):
		return self.response
	
	def getCommands(self):
		return self.list_commands
	
	def getPath(self, raiz, path='', x=0):
		path += raiz.elemento + '/'
		try: path = self.getPath(raiz.hijos[self.pathPos[x]], path, x+1)
		except: pass
		return path[:-1]+'>'
	
	def getChilds(self, raiz):
		h = None
		for x in self.pathPos:
			h = raiz.hijos[x]
			raiz = h
		return raiz.hijos
	
	def searchDir(self, raiz, _dir, x=0, l=[]):
		t = None
		if raiz.elemento == _dir: return l
		l.append(0)
		for i, h in enumerate(raiz.hijos):
			l[x] = i
			t = self.searchDir(h, _dir, x+1, l[:])
			if t: break
		return t
	
	def actualPath(self):
		
		self.path = self.getPath(self.arbol)
		
		return self.path
	
	def fileSystem(self):						                          # <--------------------------------------- pendiente el sistema de carpetas.
		
		self.arbol.agregarElemento(self.arbol, 'Root', 'System')
		self.arbol.agregarElemento(self.arbol, 'Root', 'User')
		self.arbol.agregarElemento(self.arbol, 'System', 'Logs')
		self.arbol.agregarElemento(self.arbol, 'User', self.username)
		self.arbol.agregarElemento(self.arbol, 'Logs', self.createLogFile('Connection'))
		# ~ self.arbol.agregarElemento(self.arbol, 'Logs', 'Connection 29-01-2020 03-54-12.log')
		
		self.arbol.agregarElemento(self.arbol, self.username, 'Documents')
		self.arbol.agregarElemento(self.arbol, self.username, 'Escritorio')
		self.arbol.agregarElemento(self.arbol, self.username, 'Papelera')
		
		self.arbol.agregarElemento(self.arbol, 'Documents', 'Nueva')
		self.arbol.agregarElemento(self.arbol, 'Documents', 'EnyScan.exe')
		
		self.arbol.ejecutarProfundidadPrimero(self.arbol, self.arbol.printElement)
		
		
	def createLogFile(self, typeFile):
		now = str(datetime.now())
		now = now.replace(':','-')
		now = now.replace(' ','_')
		log = '{} {}.log'.format(typeFile, now)
		return log
	
	def validate(self, command):
		command = command.split(' ')[0]
		
		# ~ print(command, command in self.list_commands)
		
		if command in self.list_commands: return True
		return False
	
	def execute(self, command):
		
		self.response = []
		
		if command == 'help':
			self.response = [
				'',
				'Los Posibles Comandos a Utilizar Son:',
				'',
				'  help  com? Muestra un Mensaje de Ayuda.',
				'             Puedes escribir el nombre de',
				'             un comando para mas detalles.',
				'  cd    dir  Cambia de Directorio.',
				'  exit       Cierra la Consola de Comandos',
				'  cls        Limpia la Consola de Comandos',
				'  mkdir name Crea un Carpeta',
				'  rm    file Elimina un Archivo o Carpeta',
				'  cat   file Leer Archivo como texto plano',
				'  con   IP   Conectar a una IP',
				'  dc    IP   Desconectarse de una IP.',
				'  dir   name Lista los archivos y carpetas.',
				''
			]
		
		elif command == 'cls': pass
		
		elif command == 'exit': self.response = ['','Cerrando...','']
		
		elif command[:6] == 'mkdir ': pass
			
		elif command[:3] == 'cd ':
			
			command = command[3:].split('/')				# separa la cadena en fragmentos, dividiendola en cada '/', ejemplo: /Hola/Mundo/ ---> ['','Hola','Mundo','']
			
			if command == ['','']: self.pathPos = []		# Si la lista solo contiene dos cadenas vacias, significa que el comando solo indicaba '/'
			
			while '' in command: command.remove('')			# Elimina los elementos de cadena vacia '' existente.
			
			for elem in command:							# Estrae cada elemento de la lista.
				
				if elem == '..':
					if self.pathPos: self.pathPos.pop()		# Si el pathPos no es una lista vacia, elimina el ultimo elemento de la lista. 
				else:
					valid = False
					folders = []
					ch = self.getChilds(self.arbol)			# Obtiene la lista de Hijos en la Ruta (Path) actual.
					
					for i, x in enumerate(ch):
						y = str(x)							# Extraemos cada elemento.
						if not y.endswith(self.valid_ext):	# Si no tiene extension, entonces es una Carpeta.
							folders.append((i, x))			# La agregamos a la lista de Carpetas.
					
					if folders:								# Si la lista no es vacia...
						for i, f in folders:				# Recorre la liste y enumera cada elemento a partir del 0.
							if elem == str(f):				# Si el elemento es igual a uno de los hijos...
								valid = True
								self.pathPos.append(i)		# Se agrega la posicion del hijo para indicar en que carpeta se adentrara.
								break
						if not valid:
							if elem.endswith(self.valid_ext):
								self.response = ['',elem+' No es una Carpeta.','']
							else:
								self.response = ['','No existe la carpeta: '+elem,'']
					else: self.response = ['','No existe la carpeta: '+elem,'']
		
		elif command == 'dir':
			
			childs = self.getChilds(self.arbol)
			
			if len(childs) > 0:
				
				for child in childs:
					
					ch = str(child)
					
					if '.' in ch[-5:]:
						res = 'Archivo'
						res  = res.ljust(11)
						res += ' '+ch
					else:
						res = 'Carpeta'
						res  = res.ljust(8)
						res += str(len(child.hijos)).rjust(3)
						res += ' '+ch
					
					self.response.append(res)
				
				data  = 'Tipo'.ljust(8)
				data += ''.center(3)
				data += ' Nombre'
				
				self.response = [''] + [data] + [''] + self.response + ['']
				
			else:
				self.response = ['', 'La Carpeta Esta Vacia', '']
				
		else: pass
		
		return self.response



if __name__ == "__main__":
	
	# ~ import os
	# ~ for x in os.environ:
		# ~ print(x, os.environ[x])
	
	console = Console('Eny', 'HGSys')
	
	print('\n', console.actualPath(), end=' ')
	
	com = 'cd Documents'
	# ~ if console.validate(com):
	res = console.execute(com)
	res = '\n'.join(res)
	print(com, res, '\n', console.actualPath(), end=' ')
	
	com = 'cd Nueva'
	res = console.execute(com)
	res = '\n'.join(res)
	print(com, res, '\n', console.actualPath(), end=' ')
	
	com = 'cd ../../Documents/Nuevo'
	res = console.execute(com)
	res = '\n'.join(res)
	print(com, res, console.actualPath(), end='\n')
	
	# ~ for x in range(2):
		
		# ~ com = 'cd ..'
		# ~ print(com)
		
		# ~ res = console.execute(com)
		# ~ res = '\n'.join(res)
		# ~ print(res)
		
		# ~ print('\n', console.actualPath(), end=' ')
		
	# ~ for x in range(2):
		
		# ~ com = 'cd /'
		# ~ print(com)
		
		# ~ res = console.execute(com)
		# ~ res = '\n'.join(res)
		# ~ print(res)
		
		# ~ print('\n', console.actualPath(), end=' ')
	
	
	# ~ for x in range(2):
		
		# ~ com = 'cd ..'
		# ~ print(com)
		
		# ~ res = console.execute(com)
		# ~ res = '\n'.join(res)
		# ~ print(res)
		
		# ~ print('\n', console.actualPath(), end=' ')
		
		# ~ com = 'cd /'
		# ~ print(com)
		
		# ~ res = console.execute(com)
		# ~ res = '\n'.join(res)
		# ~ print(res)
		
		# ~ print('\n', console.actualPath(), end=' ')
	
