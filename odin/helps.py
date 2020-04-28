
# By: LawlietJH
# Odyssey in Dystopia

from datetime      import datetime
import threading
import binascii						# hexlify y unhexlify
import psutil
import pygame						# python -m pip install pygame
import ctypes
import base64
import time
import math
import bz2
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

TITULO      = 'Odyssey in Dystopia'	# Nombre
__version__ = 'v1.2.5'				# Version
__author__  = 'LawlietJH'			# Desarrollador

#=======================================================================
#=======================================================================
#=======================================================================

run_command = lambda Comando: os.popen(Comando).read()

#=======================================================================

class Helps:
	
	encode_bz2 = lambda data: binascii.hexlify(bz2.compress(data.encode())).decode()
	decode_bz2 = lambda data: bz2.decompress(binascii.unhexlify(data)).decode()
	encode_b64 = lambda data: base64.urlsafe_b64encode(data.encode()).decode()
	decode_b64 = lambda data: base64.urlsafe_b64decode(data).decode()
	
	class Data:
		# Funcion que retorna el valor en bytes como Cadena simplificado a KB, MB, GB, etc.
		def pretty_memory_size(nbytes):
			
			if nbytes == 0: return '0 B'
			
			metric = ('B', 'kB', 'MB', 'GB', 'TB')
			nunit = int(math.floor(math.log(nbytes, 1024)))
			nsize = round(nbytes/(math.pow(1024, nunit)), 2)
			
			return '{} {}'.format(format(nsize, '.2f'), metric[nunit])
		
		def updateVariables():
			wagms = WA.GlobalMemoryStatus()
			Helps.Data.fm_total   = Helps.Data.pretty_memory_size(wagms['TotalPhys'])
			Helps.Data.fm_free    = Helps.Data.pretty_memory_size(wagms['AvailPhys'])
			Helps.Data.fm_used    = Helps.Data.pretty_memory_size(wagms['TotalPhys']-wagms['AvailPhys'])
			Helps.Data.fm_percent = round(100-(wagms['AvailPhys']/wagms['TotalPhys']*100), 2)
			
			# Obtener Memoria RAM utilizada por este proceso:
			# Metodo #1 Memory Info
			proc = psutil.Process(Helps.Data.pid)
			Helps.Data.proc_mem_info = proc.memory_info()
			Helps.Data.memory_use    = Helps.Data.pretty_memory_size(Helps.Data.proc_mem_info.rss)
			Helps.Data.cpu_per       = psutil.cpu_percent()
			# ~ print(WP.GetProcessMemoryInfo(WP.GetCurrentProcess()))
			
			# ~ wp_cp = WP.GetCurrentProcess()
			# ~ WG.SetActiveWindow(wp_cp)
			# ~ WG.SetForegroundWindow(wp_cp)
			
			# Metodo #2 WMIC
			# ~ com = 'wmic process where processid={} get WorkingSetSize'.format(pid)
			# ~ res = run_command(com)
			# ~ res = res.split('\n')[2].strip()
			# ~ res = int(res) / (1024**2)
			
		# ~ print(WA.GlobalMemoryStatus())
		
		pid           = os.getpid()
		# ~ print(pid)
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
__Hola,_ y bienvenido a dystopia,__ el sistema con más inteligencias artificiales del mundo.__
En estos momentos,_ tu mente está dentro del sistema.__
No tendrás acceso al mundo real,_ hasta que los administradores te liberen.__
La única manera de desplazarte en éste sistema,_ es utilizando tu pensamiento.__
Hemos adaptado este entorno virtual para ti.__
Podrás manipularlo con tu mente_ como si de una computadora se tratara.__
Es un entorno similar a lo que estabas acostumbrado.___
Hemos inhabilitado algunos de tus recuerdos por orden de los administradores,_ así que deberás aprender a volver a utilizarlo.__
Sabemos que irás recordando todo poco a poco,__ así que te sugerimos que no te alarmes,_ todo está bien.__
'''.replace('_','____')
		
		help_ = '''
 Los Posibles Comandos a Utilizar Son:

   help  command   Muestra un Mensaje de Ayuda para un comando especifico.
                   Ejemplo: 'help chmod', 'help cd', 'help ls', etc.
                   Usa esto para saber muchos más detalles y reglas.
   
   cd    path      Cambia de Directorio.
   ls    path      Lista los archivos y carpetas. ALT: dir
   cat   file      Leer Archivo como texto plano. ALT: type
   chmod mode name Permite cambiar los atributos de un archivo o carpeta.
   cls             Limpia la Terminal. Vacia el buffer. ALT: clear
   exit            Cierra la Sesión actual. ALT: logout
	'''
		# Pendientes:
		# mkdir name Crea un Carpeta
		# rm    file Elimina un Archivo o Carpeta
		# con   IP   Conectar a una IP
		# dc    IP   Desconectarse de una IP.
		
		cd = '''
   Change Directory.
 
 El comando 'cd' permite desplazarse en los distintos niveles de carpetas.
 
 Es posible utilizar '/' para indicar que se adentrará en una carpeta.
 Es posible utilizar '../' para indicar que se retrocederá un nivel.
 
 Se puede utilizar la tecla de tabulacion 'TAB' para autocompletar un
 nombre de archivo o carpeta siempre y cuando coincidan.
 
 Incluir '/' al final del nombre de una carpeta es opcional, es decir
 'cd bin/nueva' o 'cd bin/nueva/' son completamente validos. 
 
 Ejemplos:
 
   cd /          # Esto indicará que se desea ir a la carpeta raiz.
   cd /System/   # Esto indicará que se desea ir a la carpeta raiz
                   y luego a System.
   cd ../        # Esto indicará que se desea retrodceder un nivel.
   cd bin/nueva  # Esto permitirá entrar en la carpeta 'bin' y luego
                   en 'nueva'.
'''
		
		ls = '''
   List Directory.
 
 Alternativa a 'ls': Puedes utilizar el comando 'dir'.
 
 El comando 'ls' te permite listar el contenido de una carpeta.
 
 Es posible utilizar todas las opciones que permite el comando 'cd' para
 listar carpetas en distintas rutas sin necesidad de desplazarse.
 
 Se puede utilizar la tecla de tabulacion 'TAB' para autocompletar un
 nombre de archivo o carpeta siempre y cuando coincidan.
 
 Ejemplos:
 
   ls            # Mostrará todo el contenido de la ruta actual.
   ls ../        # Mostrará el contenido de la carpeta un nivel atras.
   ls /          # Mostrará el contenido de la carpeta raiz.
   ls bin/nueva  # Mostrará el contenido de la carpeta 'nueva'.
'''
		
		cat = '''
   Concatenate.
 
 Alternativa a 'cat': Puedes utilizar el comando 'type'.
 
 El comando 'ls' te permite listar el contenido de una carpeta.
 
 Es posible utilizar todas las opciones que permite el comando 'cd' para
 listar carpetas en distintas rutas sin necesidad de desplazarse.
 
 Se puede utilizar la tecla de tabulacion 'TAB' para autocompletar un
 nombre de archivo o carpeta siempre y cuando coincidan.
 
 Ejemplos:
 
   cat file.txt          # Mostrará el contenido del archivo 'file.txt'.
   cat ../'file.txt'     # Mostrará el contenido del archivo 'file.txt'
                           un nivel atras.
   cat /file.txt         # Mostrará el contenido del archivo 'file.txt'
                           en la carpeta raiz.
   cat bin/file.txt      # Mostrará el contenido del archivo 'file.txt'
                           en la carpeta 'nueva'.
   cat "file 2.txt"      # Se debe poner comillas dobles si el nombre
                           contiene espacios.
   cat bin/"file 2.txt"  # Se debe agregar comillas dobles de esta forma
                           si el archivo esta en otra ruta y si contiene
                           espacios en el nombre.
 
 (Funcionalidades Pendientes de Agregar)
 
 Es posible enumerar las lineas impresas en pantalla, escribiendo el
 parametro '-n' antes del nombre de archivo: 'cat -n archivo.txt'
 
 Es posible utilizar este comando para crear un archivo de texto plano y
 escribir en él utilizando por ejemplo el comando: 'cat > archivo.txt'
 
 Es posible saber cuantos caracteres son posibles de imprimir por cada
 linea en pantalla utilizando el comando: 'cat -s' o 'cat --show'
 
 Es posible limitar los caracteres  que son posibles de imprimir por
 cada linea en pantalla utilizando el comando: 'cat -l 50 archivo.txt'
 Si la cantidad de caracteres sobrepasa los del limite de la consola
 se tomará por defecto el limite original.
 
'''
		
		save = '''
 Este comando permite Guardar la partida actual.
 
 Por defecto el Sistema de Juego Guardará Partida
 cada 5 minutos de manera silenciosa.
	'''
		
		cls = '''
   Clear Screen.
 
 Alternativa a 'cls': Puedes utilizar el comando 'clear'.
 
 Este comando permite vaciar el Buffer de consola, eliminando los
 datos cargados y restaurando la pantalla a su estado original.
	'''
		
		exit_ = '''
   Cerrar Sesión.
 
 Alternativa a 'exit': Puedes utilizar el comando 'logout'.
 
 Este comando permite cerrar la sesión actual.
	'''
		
		chmod = '''
   Change Mode.
 
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
	
	class Boton(pygame.sprite.Sprite, pygame.font.Font):				# Clase Para Botones.
		
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
	
	class Playlist:
		
		musica = [
			('musica/Varien - Born of Blood, Risen From Ash.mp3',             0, {'By':'Varien',     'Song':'Born of Blood, Risen From Ash',        'Album':'',                 'Duration':'00:04:06', 'Released':'2019/04/05', 'Sountrack':'',   'Type':'MP3 192kbps'}),
			('musica/Varien - Blood Hunter.mp3',                              1, {'By':'Varien',     'Song':'Blood Hunter',                         'Album':'',                 'Duration':'00:03:47', 'Released':'2018/02/10', 'Sountrack':'',   'Type':'MP3 192kbps'}),
			('musica/Varien - Of Foxes and Hounds.mp3',                       2, {'By':'Varien',     'Song':'Of Foxes and Hounds',                  'Album':'',                 'Duration':'00:05:04', 'Released':'2018/04/02', 'Sountrack':'',   'Type':'MP3 192kbps'}),
			('musica/Mega Drive - Completely Circuitry (GosT remix).mp3',     3, {'By':'Mega Drive', 'Song':'Completely Circuitry (GosT remix)',    'Album':'V1.4 remixes',     'Duration':'00:05:30', 'Released':'2015/01/24', 'Sountrack':'3',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Converter.mp3',                             4, {'By':'Mega Drive', 'Song':'Converter',                            'Album':'Mega Drive',       'Duration':'00:06:30', 'Released':'2013/11/18', 'Sountrack':'2',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Crypt Diver.mp3',	                          5, {'By':'Mega Drive', 'Song':'Crypt Diver',                          'Album':'199XAD',           'Duration':'00:04:54', 'Released':'2019/10/04', 'Sountrack':'4',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Digital Ghost.mp3',                         6, {'By':'Mega Drive', 'Song':'Digital Ghost',                        'Album':'Mega Drive',       'Duration':'00:04:46', 'Released':'2013/11/18', 'Sountrack':'3',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - H.exe.mp3',                                 7, {'By':'Mega Drive', 'Song':'H.exe',                                'Album':'199XAD',           'Duration':'00:03:16', 'Released':'2019/10/04', 'Sountrack':'8',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - I Am The Program (Perturbator remix).mp3',  8, {'By':'Mega Drive', 'Song':'I Am The Program (Perturbator remix)', 'Album':'V1.4 remixes',     'Duration':'00:04:33', 'Released':'2015/01/24', 'Sountrack':'2',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Run The Code.mp3',                          9, {'By':'Mega Drive', 'Song':'Run The Code',                         'Album':'Seas Of Infinity', 'Duration':'00:06:05', 'Released':'2017/05/18', 'Sountrack':'8',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Seas Of Infinity.mp3',                     10, {'By':'Mega Drive', 'Song':'Seas Of Infinity',                     'Album':'Seas Of Infinity', 'Duration':'00:02:08', 'Released':'2017/05/18', 'Sountrack':'1',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Source Code.mp3',                          11, {'By':'Mega Drive', 'Song':'Source Code',                          'Album':'199XAD',           'Duration':'00:05:00', 'Released':'2019/10/04', 'Sountrack':'11', 'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Streets of Fire.mp3',                      12, {'By':'Mega Drive', 'Song':'Streets of Fire',                      'Album':'199XAD',           'Duration':'00:05:37', 'Released':'2019/10/04', 'Sountrack':'9',  'Type':'MP3 128kbps'}),
			('musica/Mega Drive - Terror Eyes.mp3',                          13, {'By':'Mega Drive', 'Song':'Terror Eyes',                          'Album':'199XAD',           'Duration':'00:05:11', 'Released':'2019/10/04', 'Sountrack':'10', 'Type':'MP3 128kbps'}),
			('musica/Mega Drive - The Glowing of Gunner All.mp3',            14, {'By':'Mega Drive', 'Song':'The Glowing of Gunner All',            'Album':'The Grid',         'Duration':'00:04:54', 'Released':'2017/11/17', 'Sountrack':'11', 'Type':'MP3 128kbps'}),
			('musica/Dynatron - Pulse Power.mp3',                            15, {'By':'Dynatron',   'Song':'Pulse Power',                          'Album':'Escape Velocity',  'Duration':'00:06:00', 'Released':'2012/11/22', 'Sountrack':'8',  'Type':'MP3 192kbps'}),
			('musica/Kroww - Hysteria.mp3',                                  16, {'By':'Kroww',      'Song':'Hysteria',                             'Album':'',                 'Duration':'00:05:14', 'Released':'2019/09/24', 'Sountrack':'',   'Type':'MP3 192kbps'}),
			('musica/Scandroid - Thriller (Fury Weekend Remix).mp3',         17, {'By':'Scandroid',  'Song':'Thriller',                             'Album':'',                 'Duration':'00:04:52', 'Released':'2018/10/15', 'Sountrack':'',   'Type':'MP3 128kbps'}),
			('musica/Neovaii - Easily.mp3',                                  18, {'By':'Neovaii',    'Song':'Easily',                               'Album':'',                 'Duration':'00:04:18', 'Released':'//',         'Sountrack':'',   'Type':'MP3 128kbps'}),
			('musica/Stephen - Crossfire.mp3',                               19, {'By':'Stephen',    'Song':'Crossfire',                            'Album':'',                 'Duration':'00:04:31', 'Released':'//',         'Sountrack':'',   'Type':'MP3 128kbps'}),
		]
	
	class Musica:
		
		def __init__(self, ljust):
			self.canciones = [
				'Creador - Nombre de Canción'.ljust(ljust-2)+'Duración',
				'Varien - Born of Blood, Risen From Ash'.ljust(ljust)+'4:06',
				'Varien - Blood Hunter'.ljust(ljust)+'3:47',
				'Varien - Of Foxes and Hounds'.ljust(ljust)+'5:04',
				'Mega Drive - Completely Circuitry (GosT remix)'.ljust(ljust)+'5:30',
				'Mega Drive - Converter'.ljust(ljust)+'6:30',
				'Mega Drive - Crypt Diver'.ljust(ljust)+'4:54',
				'Mega Drive - Digital Ghost'.ljust(ljust)+'4:46',
				'Mega Drive - H.exe'.ljust(ljust)+'3:16',
				'Mega Drive - I Am The Program (Perturbator remix)'.ljust(ljust)+'4:33',
				'Mega Drive - Run The Code'.ljust(ljust)+'6:05',
				'Mega Drive - Seas Of Infinity'.ljust(ljust)+'2:08',
				'Mega Drive - Source Code'.ljust(ljust)+'5:00',
				'Mega Drive - Streets of Fire'.ljust(ljust)+'5:37',
				'Mega Drive - Terror Eyes'.ljust(ljust)+'5:11',
				'Mega Drive - The Glowing of Gunner All'.ljust(ljust)+'4:54',
				'Dynatron - Pulse Power'.ljust(ljust)+'6:00',
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
		
		def getData(self, busq, raw=False):
			
			thr_pos = None
			
			if type(busq) == int:
				if busq >= 0 and busq < len(self.c): thr_pos = busq
				else: raise SystemError('\n\n El valor de busqueda debe ser entre 0 y {}.'.format(len(self.c)))
			elif type(busq) == str:
				if busq in self.c: thr_pos = self.c.index(busq)
				else: return False	# ~ raise SystemError('\n\n El hilo de nombre "{}" no esta activo.'.format(busq))
			else: raise SystemError('\n\n Tipo de Dato Erroneo, solo puedes mandar un entero o una cadena.')
			
			if raw: data = thr_pos
			else: data = [self.t[thr_pos], self.c[thr_pos], self.l[thr_pos]]
			
			return data
		
		# ~ def resetData(self, busq, data=[None, None, None]):
			
			# ~ thr_pos = self.getData(busq, True)		# Obtiene solo la posicion del hilo buscado.
			
			# ~ if not type(data) in [list, tuple]:
				# ~ raise SystemError('\n\n Tipo de Dato Erroneo, solo puedes mandar una lista o una tupla.')
			
			# ~ self.t[thr_pos] = data[0]
			# ~ self.c[thr_pos] = data[1]
			# ~ self.l[thr_pos] = data[2]
		
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

	# ~ threads.isActive('Hola', 1)
	# ~ if not threads.isActive('Hola', .5): pass
		# ~ print(True, 1, threads.l)
	# ~ else:
		# ~ print(False, 1, threads.l)
	
	# ~ time.sleep(.001)
	
	
	
	
