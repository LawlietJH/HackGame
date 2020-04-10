
# By: LawlietJH
# Odyssey in Dystopia

from datetime      import datetime
import threading
import psutil
import pygame						# python -m pip install pygame
import ctypes
import time
import math
import os

# Manipulacion de DLLs de Windows ======================================
from ctypes import windll
#=======================================================================

# pip install pywin32 ==================================================
from win32com.shell import shell
import win32api			as WA
import win32con			as WC
import win32gui			as WG
import win32ui			as WU
import win32net			as WN
import win32com			as WCM
import win32process		as WP
import win32security	as WS
import win32clipboard	as WCB
import win32console		as WCS
#=======================================================================

TITULO  = 'Odyssey in Dystopia'		# Nombre
__version__ = 'v1.2.4'				# Version
__author__ = 'LawlietJH'			# Desarrollador

#=======================================================================
#=======================================================================
#=======================================================================

run_command = lambda Comando: os.popen(Comando).read()

#=======================================================================

class Helps:
	
	class Data:
		# Funcion que retorna el valor en bytes como Cadena simplificado a KB, MB, GB, etc.
		def pretty_memory_size(nbytes):
			
			if nbytes == 0: return '0 B'
			
			metric = ('B', 'kB', 'MB', 'GB', 'TB')
			nunit = int(math.floor(math.log(nbytes, 1024)))
			nsize = round(nbytes/(math.pow(1024, nunit)), 2)
			
			return '{} {}'.format(format(nsize, '.2f'), metric[nunit])
		
		def updateMemory():
			wagms = WA.GlobalMemoryStatus()
			Helps.Data.fm_total      = Helps.Data.pretty_memory_size(wagms['TotalPhys'])
			Helps.Data.fm_free       = Helps.Data.pretty_memory_size(wagms['AvailPhys'])
			Helps.Data.fm_used       = Helps.Data.pretty_memory_size(wagms['TotalPhys']-wagms['AvailPhys'])
			Helps.Data.fm_percent    = round(100-(wagms['AvailPhys']/wagms['TotalPhys']*100), 2)
			
		pid           = os.getpid()
		proc          = psutil.Process(pid)
		proc_dict     = proc.as_dict()
		init_time_raw = proc.create_time()
		temp          = datetime.fromtimestamp(init_time_raw)
		init_time     = temp.strftime("%Y-%m-%d %H:%M:%S")
		
		wagms = WA.GlobalMemoryStatus()
		fm_total      = pretty_memory_size(wagms['TotalPhys'])
		fm_free       = pretty_memory_size(wagms['AvailPhys'])
		fm_used       = pretty_memory_size(wagms['TotalPhys']-wagms['AvailPhys'])
		fm_percent    = round(100-(wagms['AvailPhys']/wagms['TotalPhys']*100), 2)
		
		# ~ virtual_mem   = dict(psutil.virtual_memory()._asdict())
		# ~ vm_percent    = virtual_mem['percent']
		# ~ vm_total      = pretty_memory_size(virtual_mem['total'])
		# ~ vm_used       = pretty_memory_size(virtual_mem['used'])
		# ~ vm_free       = pretty_memory_size(virtual_mem['free'])
		
		cpu_per       = psutil.cpu_percent()
		proc_mem_info = proc.memory_info()
		memory_use    = pretty_memory_size(proc_mem_info.rss)
		
		temp          = None
	
	class Content:
		
		'''
	Las computadoras tienen el poder y el poder lo tienes tú.
	La conexión entre el bien y el mal existe más allá de unos y ceros.
	Unos y ceros, prediciendo el futuro.
	'''
		
		intro_text = '''
__Hola,_ y bienvenido a dystopia,
'''.replace('_','____')
# ~ __ el sistema con más inteligencias artificiales del mundo.__
# ~ En estos momentos,_ tu mente está dentro del sistema.__
# ~ No tendrás acceso al mundo real,_ hasta que los administradores te liberen.__
# ~ La única manera de desplazarte en éste sistema,_ es utilizando tu pensamiento.__
# ~ Hemos adaptado este entorno virtual para ti.__
# ~ Podrás manipularlo con tu mente_ como si de una computadora se tratara.__
# ~ Es un entorno similar a lo que estabas acostumbrado.__
# ~ Hemos inhabilitado algunos de tus recuerdos por orden de los administradores,_ así que deberás aprender a volver a utilizarlo.__
# ~ Sabemos que irás recordando todo poco a poco,__ así que te sugerimos que no te alarmes,_ todo está bien.__
# ~ '''.replace('_','____')
# ~ Sabemos que irás recordando todo poco a poco,__ así que te sugerimos que no te alarmes,___ todo está bien.____
		
		help_ = '''

 Los Posibles Comandos a Utilizar Son:

   help  command     Muestra un Mensaje de Ayuda. Puedes escribir el nombre
                     de un comando para mas detalles.
   cd    dir         Cambia de Directorio.
   ls                Lista los archivos y carpetas. ALT: dir
   exit              Cierra la Consola de Comandos. Cierra sesión.
   cls               Limpia la Consola de Comandos. Vacia el buffer.
   cat   file        Leer Archivo como texto plano. ALT: type
   chmod Modo nombre Permite cambiar los atributos de un archivo o carpeta.
                     help chmod para más detalles.
	'''
	# Pendientes:
	# mkdir name Crea un Carpeta
	# rm    file Elimina un Archivo o Carpeta
	# con   IP   Conectar a una IP
	# dc    IP   Desconectarse de una IP.
		
		permisos = '''
 Tipos de Permisos.

 [R] Lectura:
  * Archivos:    Permite, fundamentalmente, visualizar el contenido del archivo.
  * Directorios: Permite saber qué archivos y directorios contiene el directorio
                 que tiene este permiso.

 [W] Escritura:
  * Archivos:    Permite modificar el contenido del archivo.
  * Directorios: Permite crear archivos en el directorio, bien sean archivos
                 ordinarios o nuevos directorios. Se pueden borrar directorios,
                 copiar archivos en el directorio, mover, cambiar el nombre, etc.

 [X] Ejecución:
  * Archivos:    Permite ejecutar el archivo como si de un programa ejecutable
                 se tratase.
  * Directorios: Permite situarse sobre el directorio para poder examinar su
                 contenido, copiar archivos de o hacia él.
	'''
		
		chmod = '''
 (+-=) Los parentesis '()' indican que solo se puede utilizar uno a la vez.
       Puede ser: +, -, =.
 [rwx] Los corchetes '[]' indican que se pueden usar uno o más a la vez.
       Puede ser: r, w, x, rw, rx, wx, rwx. El orden de los caracteres no importa.

 El comando 'chmod' permite cambiar los permisos de:
 Lectura (r), Escritura (w) y/o Ejecución (x).

 Los argumentos validos son: chmod (+-=)[rwx] nombre
 
 Los permisos tambien pueden ser un número.
 Los números de permisos son:
 
                              0 = ---    4 = r--
                              1 = --x    5 = r-x
                              2 = -w-    6 = rw-
                              3 = -wx    7 = rwx
 
 Ejemplos:
 
   chmod +xr nombre    # Esto le dará el atributo de ejecución y
                         lectura al archivo o carpeta 'nombre'.
   chmod =r nombre     # Esto le quitará todos los atributos y le
                         dará unicamente el atributo de lectura al
                         archivo o carpeta 'nombre'.
   chmod -r nombre     # Esto le quitará el atributo de lectura al
                         archivo o carpeta 'nombre'.
   chmod 4 nombre      # Esto le quitará todos los atributos y solo
                         le dará el atributo de lectura archivo o
                         carpeta 'nombre'.
 Extra:
 
   chmod =- nombre     # Esto le quitará todos los atributos al
                         archivo o carpeta 'nombre'.
   chmod =+ nombre     # Esto le dará todos los atributos al
                         archivo o carpeta 'nombre'.
	'''
		
		save = '''
 Este comando permite Guardar la partida actual.
	'''
		
		cls = '''
 Este comando permite vaciar el Buffer de consola,
 eliminando los datos cargados y restaurando la
 pantalla a su estado original.
	'''
		
		exit_ = '''
 Este comando permite cerrar la sesión actual.
	'''
	
	class Boton(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Botones.
		
		def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
			
			pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
			self.image = Helps.Fun.load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
			self.x = self.image.get_width()
			self.y = self.image.get_height()
			self.name = Nombre.split('/')[-1].split('.')[0]
			
		def getSize(self):
			return self.x, self.y
		
		def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
			self.x = TX
			self.y = TY
			self.image = pygame.transform.scale(self.image, (TX, TY))
		
		def getName(self):
			return self.name
	
	class Atajos:
		
		atajos = [
			'Esc: Cerrar Sesión Actual.',
			'F10 o Ctrl + P: Captura de Pantalla.',
			'F11 o Ctrl + F: Poner/Quitar Pantalla Completa.',
			'Ctrl + J: Poner Canción Anterior.',
			'Ctrl + K: Pausar/Continuar Canción.',
			'Ctrl + L: Poner Canción Siguiente.',
			'Ctrl + M: Poner/Quitar Mute para la Música.',
			'Ctrl + Felcha Derecha: Adelantar la Canción en 10 Segundos.',
			'Ctrl + Felcha Izquierda: Retroceder la Canción en 10 Segundos.',
			'Ctrl + \'+\': Subir Volumen de la Música en 1%. Mantener pulsado para subir el volumen rapidamente.',
			'Ctrl + \'-\': Bajar Volumen de la Música en 1%. Mantener pulsado para bajar el volumen rapidamente.',
			'Ctrl + Shift + L: Limpiar Terminal.',
			'Ctrl + Shift + \'+\': Subir Volumen de la Música en 10%.',
			'Ctrl + Shift + \'-\': Bajar Volumen de la Música en 10%.',
		]
	
	class Musica:
		
		def __init__(self, ljust):
			self.canciones = [
				'Creador - Nombre de Canción'.ljust(ljust-2)+'Duración',
				'Mega Drive - Converter'.ljust(ljust)+'6:30',
				'Mega Drive - Source Code'.ljust(ljust)+'4:53',
				'Mega Drive - Seas Of Infinity'.ljust(ljust)+'2:08',
				'Dynatron - Pulse Power'.ljust(ljust)+'6:00',
				'Dynatron - Vox Magnetismi'.ljust(ljust)+'3:46',
				'Varien - Born of Blood, Risen From Ash'.ljust(ljust)+'4:06',
				'Varien - Blood Hunter'.ljust(ljust)+'3:47',
				'Varien - Of Foxes and Hounds'.ljust(ljust)+'5:04',
				'Kroww - Hysteria'.ljust(ljust)+'5:14',
				'Scandroid - Thriller (Fury Weekend Remix)'.ljust(ljust)+'4:52',
				'Neovaii - Easily'.ljust(ljust)+'4:18',
				'Stephen - Crossfire'.ljust(ljust)+'4:31',
			]
	
	class Threads:
		
		def __init__(self, r=10):
			self.t = [None for x in range(r)]	# Aqui se toma si esta activo o no el hilo.
			self.c = [None for x in range(r)]	# Aqui almacena los nombres de los hilos.
			self.l = [None for x in range(r)]	# Aqui se indica el tiempo de vida de los hilos.
			self.lives = 50						# Cantidad de chequeos por hacer para comprobar si se esta autilizando aun, si llega a 0, se libera el recurso.
		
		def waiting(self, pos, t):
			self.t[pos] = 1
			time.sleep(t)
			self.t[pos] = 0
		
		def freeThread(self, thr_pos):
			temp = self.l
			for i, l in enumerate(temp):
				if l == None: continue
				if i is not thr_pos and type(l) is int and l > 0:
					self.l[i] -= 1
					if self.l[i] == 0:
						self.t[i] = None
						self.c[i] = None
						self.l[i] = None
		
		def isActive(self, name, time):	# Esta funcion sirve para hacer una pausa de tiempo determinado, Devuelve True Mientras el Hilo siga activo, cuando termina su ejecución devuelve False.
			
			thr_pos = None
			
			if name not in self.c:	#Inicializa el Hilo.
				thr_pos = self.t.index(None)
				self.c[thr_pos] = name
				self.l[thr_pos] = self.lives
				self.t[thr_pos] = threading.Thread(target=self.waiting, args=[thr_pos, time])
				self.t[thr_pos].start()
			else:	# Si ya existe, indica el número de Hilo.
				thr_pos = self.c.index(name)
				self.c.index(name)
				self.l[thr_pos] = self.lives
				self.freeThread(thr_pos)
				
			if not self.t[thr_pos]:	# Si ya no esta activo el Hilo devuelve False y libera el espacio para nuevos hilos.
				self.t[thr_pos] = None
				self.c[thr_pos] = None
				self.l[thr_pos] = None
				return False
			
			return True
	
	class Utilidades:
		
		# Función Que Comprueba si el SO es Linux, Devuelve TRUE/FALSE
		def isWindows():
			
			osver = os.popen("ver").read()
			
			if osver.find("Windows") > 0: return True
			else: return False
		
		# Función Que Comprueba si el SO es Linux, Devuelve TRUE/FALSE
		def isLinux():
			
			osver = os.popen("ver").read()
			
			if osver.find("Linux") > 0: return True
			else: return False
		
		def isUserAnAdmin(): return shell.IsUserAnAdmin()
		
		def get_screen_size():
			user32 = ctypes.windll.user32
			screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
			return screenSize
		
		def minimizeWindowCMD(): WG.ShowWindow(WG.GetForegroundWindow(), WC.SW_MINIMIZE)
		
		def isSlowMachine():
			# Es 1 si la computadora tiene un procesador de gama baja (lento)
			val = WA.GetSystemMetrics(WC.SM_SLOWMACHINE)		# SM_SLOWMACHINE = 73
			return val == 1
		
		def getTimeActiveSystem(raw=False):
			
			mili = WA.GetTickCount()
			if raw: return mili
			
			secs = (mili // 1000)
			mins = (secs // 60)
			hrs  = (mins // 60)

			time  = str(hrs %24).zfill(2)+':'
			time += str(mins%60).zfill(2)+':'
			time += str(secs%60).zfill(2)
			
			return time
		
		def minimizeAll():
			
			name = 'odin/min.vbs'
			codigo = """
				' VBS Script para Minimizar todas las ventanas.
				
				Set var = CreateObject("Shell.Application")
				var.MinimizeAll
			"""
			
			with open(name,'w') as File:
				File.write(codigo)
				File.close()
			
			key = run_command('cscript '+name).split('\n')
			
			# ~ time.sleep(3)
			os.remove(name)
		
		def closeCMD(): WCS.FreeConsole()
		
		def setTopWindow(nameprocess):
			
			def aux(HWND,info):
				
				if WG.IsWindowVisible(HWND) and WG.GetWindowText(HWND) != '':
					info.append((HWND, WG.GetWindowText(HWND)))
			
			info = []
			WG.EnumWindows(aux, info)

			for inf in info:
				
				print(inf)
				if nameprocess in inf[1]:
					
					PyCWnd1 = WU.FindWindow( None, inf[1] )
					PyCWnd1.SetForegroundWindow()
					PyCWnd1.SetFocus()
					return True
		
		def HideConsole(xD=True):
			import win32console,win32gui
			window = win32console.GetConsoleWindow()
			if xD == True:    win32gui.ShowWindow(window,0)
			elif xD == False: win32gui.ShowWindow(window,1)
			return xD
	
	class Fun:
		
		def normalizeTime(mili, desface=0):
			secs  = (mili // 1000) + desface
			mins  = (secs // 60)
			hrs   = (mins // 60)
			time  = str(hrs%24).zfill(2)
			time += ':'+str(mins%60).zfill(2)
			time += ':'+str(secs%60).zfill(2)
			return time
		
		def anormalizeTime(time, mili=False):
			m = 0
			if type(time) == datetime:
				m = int(str(time)[-6:-3])
				time = str(time)[11:-7]
			time = time.split(':')
			time[1] = int(time[0])*60 + int(time[1])	# Convertimos las horas en minutos y se lo sumamos a los minutos.
			time = time[1]*60 + int(time[2])			# Convertimos los minutos en segundos y se lo sumamos a los segundos.
			if mili:
				time = time * 1000						# Convertimos los segundos en milisegundos.
				time += m
			return time
		
		def i_let(t, c, p):		# Insertar letra. T = Texto, C = Caracter, P = Posicion
			t = t[:p-1] + c + t[p-1:]		# Se agrega el texto desde el inicio hasta la posicion p -1, agrega el nuevo caracter en dicha posicion y se agrega el resto desde p -1.
			return t
		
		def add_comand(l_comandos, textos):	# Inserta Comandos a la Lista
			plus = ' '
			if textos and textos[-1] == 0:
				textos.pop()
				plus = ''
			cont = l_comandos[-1][1]
			for text in textos: l_comandos.append([plus+text, cont])
			return l_comandos
		
		def match_x_y(x, y, box):
			if  x > box[0] and x < box[0]+box[2] \
			and y > box[1] and y < box[1]+box[3]:
				return True
			return False
		
		def load_image(filename, transparent=False):
			
			try: image = pygame.image.load(filename)
			except pygame.error as message: raise SystemError
			
			# ~ image = image.convert()
			
			if transparent:
				
				color = image.get_at((0,0))
				image.set_colorkey(color, pygame.RLEACCEL)
				
			return image
	

# ~ x = Helps.Fun.normalizeTime(10000)
# ~ y = Helps.Fun.anormalizeTime(x)
# ~ print(x, y)

# ~ threads = Helps.Threads(5)
# ~ threads.isActive('Temp', 1)

# ~ while True:
	# ~ if not threads.isActive('Hola', .5):
		# ~ print(True, 1, threads.l)
	# ~ else:
		# ~ print(False, 1, threads.l)
		
	
	
	
	
	
