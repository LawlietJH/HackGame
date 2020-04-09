
# By: LawlietJH
# Odyssey in Dystopia

import threading
import datetime
import psutil
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
		temp          = datetime.datetime.fromtimestamp(init_time_raw)
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
			
			if WG.IsWindowVisible(HWND) and WG.GetWindowText(HWND) != '': info.append((HWND, WG.GetWindowText(HWND)))
		
		info = []
		WG.EnumWindows(aux, info)

		for inf in info:
			
			print(inf)
			if nameprocess in inf[1]:
				
				PyCWnd1 = WU.FindWindow( None, inf[1] )
				PyCWnd1.SetForegroundWindow()
				PyCWnd1.SetFocus()
				return True
	
	def Hide(xD=True):
		
		import win32console,win32gui
		window = win32console.GetConsoleWindow()
		
		if xD == True:
			win32gui.ShowWindow(window,0)
			return True
		elif xD == False:
			win32gui.ShowWindow(window,1)
			return False


