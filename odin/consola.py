
# By: LawlietJH
# Odyssey in Dystopia

from .helps import *
import random, os
import operator
from datetime import datetime

TITULO  = 'Odyssey in Dystopia'
__version__ = 'v1.2.0'

class Arbol:
	
	def __init__(self, element, permiso='rwx', content=''):
		self.hijos   = []
		self.element = element
		self.permiso = permiso
		self.content = content
	
	def __str__(self):
		return self.element
	
	def agregarElemento(self, elementoPadre, element, permiso='rwx', content='folder'):
		if content=='folder': permiso = 'd'+permiso
		else: permiso = '-'+permiso
		subarbol = self.buscarSubarbol(elementoPadre)
		subarbol.hijos.append(Arbol(element, permiso, content))
		subarbol.hijos = self.sortChilds(subarbol)
	
	def sortChilds(self, arbol):
		hijos = []
		hijos = [ (i, str(h), 'f' if h.content == 'folder' else '')
					for i, h in enumerate(arbol.hijos) ]
		hijos.sort(key=lambda x: x[1])
		
		# Almacena solo los que son carpetas
		hijos2 = [ (i, h if f == 'f' else '') for i, h, f in hijos ]
		hijos2.sort(key=lambda x: x[1])
		try:
			while hijos2[0][1] == '': hijos2.pop(0)
		except: pass
		
		# Almacena solo los que son archivos.
		hijos3 = [ (i, h if f != 'f' else '') for i, h, f in hijos ]
		hijos3.sort(key=lambda x: x[1])
		try:
			while hijos3[0][1] == '': hijos3.pop(0)
		except: pass
		
		hijos = hijos2 + hijos3
		hijos = [ arbol.hijos[i] for i, _ in hijos ]
		
		return hijos
	
	def buscarSubarbol(self, element, arbol=None):
		if arbol == None: arbol = self
		if arbol.element == element:
			return arbol
		for subarbol in arbol.hijos:
			arbolBuscado = self.buscarSubarbol(element, subarbol)
			if (arbolBuscado != None):
				return arbolBuscado
		return None
	
	def profundidad(self, arbol):
		if len(arbol.hijos) == 0: 
			return 1
		return 1 + max(map(self.profundidad, arbol.hijos))
	
	def ejecutarProfundidadPrimero(self, arbol, funcion, nvl=0):
		funcion(arbol.element+('/' if arbol.content == 'folder' or arbol.element=='root' else ''), nvl)
		for hijo in arbol.hijos:
			self.ejecutarProfundidadPrimero(hijo, funcion, nvl+1)
	
	def printElement(self, element, nvl):
		# ~ print(' |  '*(nvl-1)+' |--'*(nvl), element)
		print('  |   '*(nvl-1)+'  |--'*((nvl-(nvl-1)) if nvl > 0 else 0), element)



class Console:
	
	def __init__(self, username, sysname):
		
		self.arbol = Arbol('root')
		self.username = username
		self.sysname  = sysname
		self.consize  = 0
		self.response = ''
		self.valid_ext = ('.txt', '.log', '.exe')
		self.rand   = lambda li, le: ''.join([str(random.choice(li)) for _ in range(le)])
		self.binary = lambda ini=512, fin=1024: self.rand([0,1], random.randrange(ini, fin, 8))
		self.system = [
			['root',    'system',   'r-x'],
			['root',    'user',     'r-x'],
			['root',    'boot.ini', '---', self.binary()+self.binary()],
			['system',  'logs',     'rwx'],
			['system',  'config',   'r-x'],
			['user',     username,  'r-x'],
			[ username, 'bin',      'rwx']
		]
		self.fileSystemUpdate(self.system)
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
			'chmod',		# Cambiar los permisos.
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
		path += raiz.element + '/'
		try: path = self.getPath(raiz.hijos[self.pathPos[x]], path, x+1)
		except: pass
		return path[:-1]+'>'
	
	def getPath2(self, path=None, extra='', raiz=None,):
		if raiz == None: raiz = self.arbol
		if path == None: path = self.pathPos
		h = None
		s = ''
		# ~ print(raiz)
		for i, x in enumerate(path):
			# ~ if x < 0: x += len(raiz.hijos)	# Si hay negativo se obtiene la posicion de la lista invertida.
			try:
				h = raiz.hijos[x]
			except:
				return 'No existe esa ruta.'
			raiz = h
			s += raiz.element + ('/' if raiz.content == 'folder' and not i == len(path)-1 else '')
		return 'root/' + s + extra
	
	def actualPath(self):
		
		self.path = self.getPath(self.arbol)
		
		return self.path
	
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
		if raiz.element == _dir: return l
		l.append(0)
		for i, h in enumerate(raiz.hijos):
			l[x] = i
			t = self.searchDir(h, _dir, x+1, l[:])
			if t: break
		return t
	
	def createLogFile(self, typeFile):
		now = str(datetime.now())
		now = now.replace(':','-')
		now = now.replace(' ','_')
		log = '{} {}.log'.format(typeFile, now)
		return log
	
	def fileSystemUpdate(self, data=[]):
		
		if data:
			
			os.system('cls')
			print('\n\n\t Console: '+self.sysname+'\n\t User: '+self.username+'\n')
			
			if data != self.system:
				for d in data:
					if not d in self.system:
						self.system.append(d)
			
			self.arbol = Arbol('root')
			
			for x in self.system: self.arbol.agregarElemento(*x)
			
			self.arbol.ejecutarProfundidadPrimero(self.arbol, self.arbol.printElement)
	
	def validate(self, command):
		command = command.split(' ')[0]
		
		if command in self.list_commands: return True
		return False
	
	def execute(self, command):
		
		def validateCommand(command, c_path, tipo=0):	# Tipos: 0=Ambos, 1=Carpeta, 2=Archivo
			origin = command
			endS = False
			fold = False
			if command[0] == '/':
				c_path = []
				command = command[1:]
			try:
				if command[-1] == '/':
					endS = True
					command = command[:-1]
			except: return command, c_path
			if len(command.split('/')) >= 1:
				command = command.split('/')
				for c in command:
					if '"' in c[0] and '"' in c[-1]: c = c[1:-1]
					elif '"' in c[0] or '"' in c[-1]:
						self.response = ['','No es un archivo valido: '+c,'', 0]
						return None, None
					if c == '..':
						try: c_path.pop()
						except: pass
						continue
					try:
						ch_raw = self.getChilds(c_path)
						ch = [ str(c) for c in ch_raw ]
						index = ch.index(c)
						c_path = c_path + [index]
					except:
						path = not '.' in c[-5:]
						ruta = self.getPath2(c_path) + ('/' if c_path else '')
						ruta += c + ('/' if path else '')
						if path: self.response = ['','No es una ruta valida: '+ruta,'', 0]
						else: self.response = ['','No existe el archivo: '+ruta,'', 0]
						return None, None
				if ch_raw[index].permiso[0] == 'd': fold = True
				command = c
				if tipo == 1:
					if not fold:
						self.response = ['','No es una carpeta: '+command,'', 0]
						return None, None
				elif tipo == 2:
					if fold:
						self.response = ['','No es un archivo: '+command+'/','', 0]
						return None, None
					elif endS:
						self.response = ['','No es una ruta valida: '+command+'/','', 0]
						return None, None
			return command, c_path
		
		def commandMatch(command, c_path):
			childs = self.getChilds(c_path)
			for ch in childs:
				if str(ch) == command:
					if ch.content == 'folder':
						self.response = ['', 'No puedes leer una Carpeta.', '', 0]
						break
					if ch.permiso[1] != '-':
						self.response = ['', ch.content, '']
					else:
						self.response = ['', 'No tienes permisos de Lectura.', '', 0]
					break
				else:
					self.response = ['', 'No existe el archivo: '+command, '', 0]
		
		self.response = []
		
		command = command.split()
		cnd = command[0]
		
		if cnd == 'help':
			
			if len(command) == 1:
				
				self.response = [
					'',
					'Los Posibles Comandos a Utilizar Son:',
					'',
					'  help  com?        Muestra un Mensaje de Ayuda.',
					'                    Puedes escribir el nombre de',
					'                    un comando para mas detalles.',
					'  cd    dir         Cambia de Directorio.',
					'  ls                Lista los archivos y carpetas. ALT: dir',
					'  exit              Cierra la Consola de Comandos',
					'  cls               Limpia la Consola de Comandos',
					'  cat   file        Leer Archivo como texto plano. ALT: type',
					'  chmod Modo nombre Permite cambiar los atributos',
					'                    de un archivo o carpeta.',
					'                    help chmod para mas detalles.',
					# ~ '  mkdir name Crea un Carpeta',
					# ~ '  rm    file Elimina un Archivo o Carpeta',
					# ~ '  con   IP   Conectar a una IP',
					# ~ '  dc    IP   Desconectarse de una IP.',
					''
				]
			
			elif len(command) == 2:
				
				command = command[1]
				
				if command == 'chmod':
					
					self.response = [Helps.chmod_content+Helps.permisos_content]
		
		elif cnd == 'cls': pass
		
		elif cnd == 'exit': self.response = ['','Cerrando...','']
		
		elif cnd == 'mkdir': pass
		
		elif cnd == 'cd':
			
			init  = False
			valid = False
			vacia = True
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
			
			for c in command:
				if c != '':
					vacia = False
			if vacia:
				self.response = ['','No es una ruta valida: '+'/'.join(command),'',0]
				return self.response
			
			while '' in command: command.remove('')				# Elimina los elementos de cadena vacia '' existente.
			
			if init:											# Si init es True entra, si es así significa que la ruta se inicio con el caracter '/'.
				childs = self.getChilds([])						# Obtenemos los Archivos y Carpetas de la Carpeta Raiz.
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
			
			command = ' '.join(command[1:])
			c_path = self.pathPos[:]
			
			if command:
				command, c_path = validateCommand(command, c_path, 1)		# Tipos: 0=Ambos, 1=Carpeta, 2=Archivo
				if command == None: return self.response
			
			temp = self.getChilds(c_path[:-1])
			temp = temp[c_path[-1]]
			if not temp.permiso[1] == 'r':				# 0 = 'd', 1 = 'r', 2 = 'w' y 3 = 'x'		<------------------------------------------------------------------- Limitar acceso a rutas inferiores si carpetas superiores no tienen permiso de Lectura.
				self.response = ['','No tienes permiso de acceso a esta ruta.','',0]
				return self.response
			
			childs = self.getChilds(c_path)
			
			if len(childs) > 0:
				
				for child in childs:
					
					ch = str(child)
					
					if child.permiso[0] == '-':
						fbytes = str(len(child.content))
						fbytes = (fbytes[:-3]+',' if len(fbytes) > 3 else '')+fbytes[-3:]
						res  = child.permiso.rjust(8)
						res += fbytes.rjust(8)
						res += ' Archivo'
						res += ' '*5
						res += ' '+ch
					else:
						res  = child.permiso.rjust(8)
						res += ' '*8
						res += ' Carpeta'
						res += str(len(child.hijos)).rjust(5)
						res += ' '+ch+'/'
					
					self.response.append(res)
				
				data  = 'Permisos'
				data += ' Bytes'.rjust(8)
				data += ' Tipo'.ljust(8)
				data += ' Arch'
				data += ' Nombre'
				
				self.response = [''] + [data] + [''] + self.response + ['']
				
			else:
				childs = self.getChilds(c_path[:-1])
				ch = childs[c_path[-1]]
				if ch.permiso[0] == '-':
					self.response = ['', 'No es una carpeta: '+ch.element, '', 0]
				else:	
					self.response = ['', 'La Carpeta Esta Vacia', '']
		
		elif cnd == 'cat' or cnd == 'type':
			
			c_path = self.pathPos[:]
			
			if   len(command) == 1: self.response = ['','Faltan Argumentos','', 0]
			elif len(command) == 2:
				
				command = command[1]
				
				command, c_path = validateCommand(command, c_path, 2)		# Tipos: 0=Ambos, 1=Carpeta, 2=Archivo
				if command == None: return self.response
				c_path.pop()
				
				if command == '':
					self.response = ['', 'No es un comando valido.', '', 0]
					return self.response
				
				if   command[0] == '"' and command[-1] == '"': command = command[1:-1]
				elif command[0] == '"' or  command[-1] == '"':
					self.response = None
					return self.response
				
				commandMatch(command, c_path)
				
			elif len(command) > 2:
				# ~ temp = ''
				command = command[1:]
				command = ' '.join(command)
				
				command, c_path = validateCommand(command, c_path, 2)		# Tipos: 0=Ambos, 1=Carpeta, 2=Archivo
				if command == None: return self.response
				c_path.pop()
				
				if command[0] == '"' and command[-1] == '"':
					
					command = command[1:-1]
					
					if '"' in command:
						self.response = None
						return self.response
					
					commandMatch(command, c_path)
					
				else:
					self.response = None
					return self.response
				
			else:
				self.response = None
				return self.response
			
			if '/' in command:				# Pendiente <---- Leer archivo en carpetas de otra ubicacion.
				self.response = None
				return self.response
		
		elif cnd == 'chmod':
			
			temp = command[1:]
			atr1 = ''
			atr2 = ''
			resp = ''
			
			if len(command) == 1:
				self.response = ['','Faltan Argumentos','', 0]
				return self.response
			
			if len(command) == 2:
				atr = temp[0]
				if atr == '--help' or atr == '-h':
					self.response = [Helps.chmod_content+Helps.permisos_content]
					return self.response
			
			if len(temp) >= 2:
				atr = temp[0]
				
				if atr == '=-' or atr == '=+':
					atr1 = atr[0]
					atr2 = atr[1]
					command = ' '.join(temp[1:])
				elif len(atr) >= 2 and len(atr) <= 4:
					atr1 = atr[0]
					atr2 = atr[1:]
					atrt = ''
					if atr1 in '+-=':
						# ~ print(atr2)
						for a in atr2:
							if a in 'rwx' and not a in atrt:
								atrt += a
							else:
								self.response = ['','No es un atributo valido: '+atr,'',0]
								return self.response
					else:
						self.response = ['','No es un atributo valido: '+atr,'',0]
						return self.response
					command = ' '.join(temp[1:])				# Agrega el Atributo al comando principal. Y deja solo en 2 partes del comando.
				else:
					self.response = ['','No es un atributo valido: '+atr,'',0]
					return self.response
			else:
				self.response = ['','No es un comando valido.','',0]
				return self.response
			
			c_path = self.pathPos[:]
			
			command, c_path = validateCommand(command, c_path, 0)			# Tipos: 0=Ambos, 1=Carpeta, 2=Archivo
			if command == None: return self.response
			
			if not c_path:
				self.response = ['','No es un comando valido.','',0]
				return self.response
			
			c_path.pop()
			childs = self.getChilds(c_path)
			
			for i, ch in enumerate(childs):
				if str(ch) == command:
					fbytes = str(len(ch.content))
					fbytes = (fbytes[:-3]+',' if len(fbytes) > 3 else '')+fbytes[-3:]
					resp  = '\nPermisos Cambiados: '+atr1+atr2+'\n'
					resp += '\nPermisos   Bytes Nombre          ===> Permisos\n\n'
					resp += ch.permiso.rjust(8)
					resp += fbytes.rjust(8)+' '
					resp += (ch.element + ('/' if ch.permiso[0] == 'd' else '')).ljust(16)
					if atr1 == '=': ch.permiso = ch.permiso[0] + '---'
					if atr2 == '+': ch.permiso = ch.permiso[0] + 'rwx'
					for a in atr2:
						if atr1 == '-':
							if   a == 'r': ch.permiso = ch.permiso[0]  + '-' + ch.permiso[2:]
							elif a == 'w': ch.permiso = ch.permiso[:2] + '-' + ch.permiso[3]
							elif a == 'x': ch.permiso = ch.permiso[:3] + '-'
						else:
							if   a == 'r': ch.permiso = ch.permiso[0]  + 'r' + ch.permiso[2:]
							elif a == 'w': ch.permiso = ch.permiso[:2] + 'w' + ch.permiso[3]
							elif a == 'x': ch.permiso = ch.permiso[:3] + 'x'	
					break
			if resp == '':
				command = command + ('/' if not '.' in command[-5:] else '')
				if command[-1] == '/':
					self.response = ['','No existe la carpeta: '+command,'',0]
				else:
					self.response = ['','No existe el archivo: '+command,'',0]
				return self.response
					
			resp += ' '*5
			resp += ch.permiso.rjust(8)
			resp += '\n'
			
			self.response = ['', resp, '']
		
		else: pass
		
		return self.response



if __name__ == "__main__":
	
	# ~ import os
	# ~ for x in os.environ:
		# ~ print(x, os.environ[x])
	
	console = Console('Eny', 'Odin.Dis_'+__version__)
	
	logs = [
		['logs', console.createLogFile('connection'), 'rwx', console.createLogFile('connection')[:-4]],
		['logs', 'connection 2020-01-25_01-48-26.241195.log', 'rwx', 'Connection 2020-01-25_01-48-26.241195'],
		['bin', 'scan.exe', 'r-x', console.binary()]
	]
	
	# ~ console.system.extend(logs)
	console.fileSystemUpdate(logs)
	
	print('\n', console.actualPath(), end=' ')
	
	com = 'cat /system/logs/"connection 2020-01-25_01-48-26.241195.log"'
	res = console.execute(com)
	res = '\n'.join(res[:-1] if res[-1] == 0 else res)
	print(com, '\n', res, console.actualPath())
	
	com = 'ls ../Eny'
	res = console.execute(com)
	res = '\n'.join(res[:-1] if res[-1] == 0 else res)
	print(com, '\n', res, console.actualPath())
	
	# ~ print('Buscado:', console.getPath2([1,0,0,-1], '> '))
	
	
