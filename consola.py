
import random
import operator
from datetime import datetime

#https://sites.google.com/site/programacioniiuno/temario/unidad-5---grafos/rboles?tmpl=%2Fsystem%2Fapp%2Ftemplates%2Fprint%2F&showPrintDialog=1

TITULO  = 'Hack Game'
__version__ = 'v1.1.3'

class Arbol:
	
	def __init__(self, elemento, content=''):
		self.hijos    = []
		self.elemento = elemento
		self.content  = content
	
	def __str__(self):
		return self.elemento
	
	def agregarElemento(self, arbol, elementoPadre, elemento, content='folder'):
		subarbol = self.buscarSubarbol(arbol, elementoPadre);
		subarbol.hijos.append(Arbol(elemento, content))
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
		self.consize  = 0
		self.response = ''
		self.valid_ext = ('.txt', '.log', '.exe')
		self.rand = lambda li, le: ''.join([str(random.choice(li)) for _ in range(le)])
		self.fileSystem()
		self.pathPos = self.searchDir(self.arbol, self.username)
		self.path = self.getPath(self.arbol)
		self.list_commands = [
			'help',			# Pedir la ayuda de comandos.
			'cls',			# Limpiar Pantalla.
			'exit',			# Salir de Consola, cerrar el Juego.
			'cd',			# Permite cambiar de directorio.
			'dir',			# Lista los Archivos y Carpetas.
			'ls',			# Lista los Archivos y Carpetas.
			'cat',			# Leer Archivo como texto plano.
			'type',			# Leer Archivo como texto plano.
			# ~ 'mkdir',		# Crear Carpeta.
			# ~ 'rm',			# Eliminar Archivo o Carpeta.
			# ~ 'connect',		# Conectar a una IP.
			# ~ 'disconnect'	# Desconectarse de una IP.
		]
	
	def setConSize(self, consize):
		self.consize = consize
	
	def getResponse(self):
		return self.response
	
	def getCommands(self):
		return self.list_commands
	
	def getPath(self, raiz, path='', x=0):
		path += raiz.elemento + '/'
		try: path = self.getPath(raiz.hijos[self.pathPos[x]], path, x+1)
		except: pass
		return path[:-1]+'>'
	
	def getChilds(self, path=None, raiz=None):
		if raiz == None: raiz = self.arbol
		if path == None: path = self.pathPos
		h = None
		for x in path:
			h = raiz.hijos[x]
			raiz = h
		return raiz.hijos
	
	def splitText(self, t_c):
		l_c = len(t_c)
		t_r = l_c//self.consize
		if l_c%self.consize > 0: t_r += 1
		t_c  = [ t_c[x*self.consize:(x+1)*self.consize] for x in range(t_r) ]
		return t_c
	
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
	
	def createLogFile(self, typeFile):
		now = str(datetime.now())
		now = now.replace(':','-')
		now = now.replace(' ','_')
		log = '{} {}.log'.format(typeFile, now)
		return log
	
	def fileSystem(self):
		
		self.arbol.agregarElemento(self.arbol, 'Root', 'System')
		self.arbol.agregarElemento(self.arbol, 'Root', 'User')
		self.arbol.agregarElemento(self.arbol, 'System', 'Logs')
		self.arbol.agregarElemento(self.arbol, 'User', self.username)
		self.arbol.agregarElemento(self.arbol, 'Logs', self.createLogFile('Connection'), self.createLogFile('Connection')[:-4])
		# ~ self.arbol.agregarElemento(self.arbol, 'Logs', 'Connection 29-01-2020 03-54-12.log')
		
		self.arbol.agregarElemento(self.arbol, self.username, 'Documents')
		self.arbol.agregarElemento(self.arbol, self.username, 'Desktop')
		
		self.arbol.agregarElemento(self.arbol, 'Documents', 'New')
		
		binary = self.rand([0,1], random.randrange(128,256,8))
		# ~ binary  = 'HolaSoyUnTextoDemasiadoLargoComoParaPoderProcesarloEnUna'
		# ~ binary += 'SolaLineaDeComandosParaQueSsiSeMePuedaAsignarMasDeUna'
		# ~ binary += 'LineaParaPoderMostrarmeCorrectamente.'
		self.arbol.agregarElemento(self.arbol, 'Documents', 'Scan.exe', binary )
		
		# ~ binary  = 'hola soy un texto demasiado largo como para poder procesarlo en una '
		# ~ binary += 'sola linea de comandos para que asi se me pueda asignar mas de una '
		# ~ binary += 'linea para poder mostrarme correctamente.'
		# ~ self.arbol.agregarElemento(self.arbol, 'Documents', 'EnyScan.txt', binary )
		
		self.arbol.ejecutarProfundidadPrimero(self.arbol, self.arbol.printElement)
	
	def validate(self, command):
		command = command.split(' ')[0]
		
		# ~ print(command, command in self.list_commands)
		
		if command in self.list_commands: return True
		return False
	
	def execute(self, command):
		
		self.response = []
		
		command = command.split()
		cnd = command[0]
		
		if cnd == 'help':
			self.response = [
				'',
				'Los Posibles Comandos a Utilizar Son:',
				'',
				'  help  com?  Muestra un Mensaje de Ayuda.',
				'              Puedes escribir el nombre de',
				'              un comando para mas detalles.',
				'  cd    dir   Cambia de Directorio.',
				'  ls          Lista los archivos y carpetas. ALT: dir',
				'  exit        Cierra la Consola de Comandos',
				'  cls         Limpia la Consola de Comandos',
				'  cat   file  Leer Archivo como texto plano. ALT: type',
				# ~ '  mkdir name Crea un Carpeta',
				# ~ '  rm    file Elimina un Archivo o Carpeta',
				# ~ '  con   IP   Conectar a una IP',
				# ~ '  dc    IP   Desconectarse de una IP.',
				''
			]
		
		elif cnd == 'cls': pass
		
		elif cnd == 'exit': self.response = ['','Cerrando...','']
		
		elif cnd == 'mkdir': pass
		
		elif cnd == 'cd':
			
			init  = False
			valid = False
			temp_path = self.pathPos[:]							# Generamos una copia exacta de la lista de la Ruta Actual.
			
			if   len(command) == 1: command = command[0]
			elif len(command) == 2: command = command[1]
			else:
				self.response = None
				return self.response
			
			if command[0] == '/': init = True
			
			command = command.split('/')						# separa la cadena en fragmentos, dividiendola en cada '/', ejemplo: /Hola/Mundo/ ---> ['','Hola','Mundo','']
			
			if command == ['',''] or command == ['cd']:			# Si la lista solo contiene dos cadenas vacias, significa que el comando solo indicaba '/'
				self.pathPos = []
				return self.response
			
			while '' in command: command.remove('')				# Elimina los elementos de cadena vacia '' existente.
			
			if init:											# Si init es True entra, si es así significa que la ruta se inicio con el caracter '/'.
				childs = self.getChilds([])				# Obtenemos los Archivos y Carpetas de la Carpeta Raiz.
				for i, ch in enumerate(childs):					# Recorremos la lista
					if command[0] == str(ch):					# Si la primera ruta es igual a una Carpeta en la Carpeta Raiz.
						valid = True							# Se toma como valido
						temp_path = [i]							# Y se viaja a esa Carpeta de la Carpeta Raiz
						command.pop(0)							# Para finalizar se elimina esa carpeta del Command para procesar si existen más.
						break
			
			for elem in command:								# Extrae cada elemento de la lista.
				
				valid = False
				folders = []
				ch = self.getChilds(temp_path)		# Obtiene la lista de Hijos en la Ruta (Path) actual.
				
				if elem == '..':
					if temp_path: temp_path.pop()				# Si el temp_path no es una lista vacia, elimina el ultimo elemento de la lista.
					valid = True
					continue
				elif '.' in elem:
					# ~ if elem.endswith(self.valid_ext):			# Si tiene extension, entonces no es una Carpeta.
					self.response = ['','No es una carpeta: "'+elem+'"','', 0]
					return self.response
					# ~ else:
						# ~ self.response = ['','No es una carpeta: "'+elem+'"','']
						# ~ return self.response
				
				for i, x in enumerate(ch):
					y = str(x)									# Convierte el elemento hijo a String.
					if not y.endswith(self.valid_ext):			# Si no tiene extension, entonces es una Carpeta.
						folders.append((i, x))					# La agregamos a la lista de Carpetas.
				
				if folders:										# Si la lista no es vacia...
					for i, f in folders:						# Recorre la lista y enumera cada elemento a partir del 0.
						if elem == str(f):						# Si el elemento es igual a uno de los hijos...
							valid = True
							temp_path.append(i)					# Se agrega la posicion del hijo para indicar en que carpeta se adentrara.
							break
					if not valid:
						self.response = ['','No existe la carpeta: "'+elem+'"','', 0]
						break
				else:
					self.response = ['','No existe la carpeta: "'+elem+'"','', 0]
					break
			
			if valid: self.pathPos = temp_path
		
		elif cnd == 'ls' or cnd == 'dir':
			
			childs = self.getChilds()
			
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
		
		elif cnd == 'cat' or cnd == 'type':
			
			if   len(command) == 1: self.response = ['','Faltan Argumentos','', 0]
			elif len(command) == 2:
				command = command[1]
				
				if   command[0] == '"' and command[-1] == '"': command = command[1:-1]
				elif command[0] == '"' or  command[-1] == '"':
					self.response = None
					return self.response
				
				childs = self.getChilds()
				for ch in childs:
					if str(ch) == command:
						if ch.content == 'folder':
							self.response = ['', 'No puedes leer una Carpeta.', '', 0]
							break
						self.response = ['', ch.content, '']
						break
					else:
						self.response = ['', 'No existe el archivo: "'+command+'"', '', 0]
			elif len(command) > 2:
				# ~ temp = ''
				command = command[1:]
				if command[0][0] == '"' and command[-1][-1] == '"':
					
					command = ' '.join(command)
					command = command[1:-1]
					
					if '"' in command:
						self.response = None
						return self.response
					
					childs = self.getChilds()
					
					for ch in childs:
						if str(ch) == command:
							if ch.content == 'folder':
								self.response = ['', 'No puedes leer una Carpeta.', '', 0]
								break
							self.response = ['', ch.content, '']
							break
						else:
							self.response = ['', 'No existe el archivo: '+command, '', 0]
				else:
					self.response = None
					return self.response
				
			else:
				self.response = None
				return self.response
			
			if '/' in command:				# Pendiente <---- Leer archivo en carpetas de otra ubicacion.
				self.response = None
				return self.response
			
		else: pass
		
		return self.response



if __name__ == "__main__":
	
	# ~ import os
	# ~ for x in os.environ:
		# ~ print(x, os.environ[x])
	
	console = Console('Eny', 'HGSys')
	
	print('\n', console.actualPath(), end=' ')
	
	com = 'cd Documents/'
	res = console.execute(com)
	res = '\n'.join(res)
	print(com, '\n', res, console.actualPath(), end=' ')
	
	com = 'cat EnyScan.exe'
	res = console.execute(com)
	res = '\n'.join(res)
	print(com, '\n', res, console.actualPath(), end=' ')
	
