
# By: LawlietJH
# Odyssey in Dystopia
# Luvenia y Luvonne, Levanen.
# Dynatron, Mega Drive, Avandra, Ferus Melek, Varien, Peter Gundry.

# ~ from os import 

from odin.database import Database, initDB
from odin.consola  import Console
from odin.helps    import Helps
from odin          import round_rect

from datetime      import datetime
import threading
import random
import pygame						# python -m pip install pygame
import ctypes
import os							# path, mkdir, environ, system

from win32api import GetKeyState	# python -m pip install pywin32
from win32con import VK_CAPITAL		# python -m pip install pywin32

TITULO  = 'Odyssey in Dystopia'		# Nombre
__version__ = 'v1.2.3'				# Version

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

class Boton(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Botones.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
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

def get_screen_size():
    user32 = ctypes.windll.user32
    screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screenSize

def setFontSize(tam):
	global Font_tam, Font_def, T_pix, T_pix_y
	Font_tam = tam						# Constante, para hacer manipulación del tamaño de algunas letras y en la matriz para tener un margen correcto y otras cosas más.
	Font_def = 'Inc-R '+str(Font_tam)	# Fuente por defecto.
	T_pix     = tam//2					# Tamaño de Pixeles entre cada letra en linea de comandos.
	T_pix_y   = T_pix*2					# Tamaño de Pixeles entre cada salto de linea en la linea de comandos.


def load_image(filename, transparent=False):
	
	try: image = pygame.image.load(filename)
	except pygame.error as message: raise SystemError
	
	# ~ image = image.convert()
	
	if transparent:
		
		color = image.get_at((0,0))
		image.set_colorkey(color, pygame.RLEACCEL)
		
	return image

#===================================================================================================

def dibujarTexto(texto, posicion, fuente, color):		# Dibuja Texto En Pantalla.
	
	Texto = fuente.render(texto, 1, color)		# Se Pasa El Texto Con La Fuente Especificada.
	screen.blit(Texto, posicion)				# Se Dibuja En Pantalla El Texto en la Posición Indicada.

def dibujarTextoTemporal(c_ticks, msn, ticks, ret=True):
	c_ticks += 1			# Aumento en el contador de ticks.
	if c_ticks < ticks:		# Cantidad de ticks que durara el mensaje en pantalla. 60 ticks = 1 segundo.
		texto = msn
		len_t = len(texto)
		t_temp = ((RESOLUCION[s_res][0]//2)-((len_t*T_pix)//2), (RESOLUCION[s_res][1]//2)-(T_pix*2))				# Centrará el mensaje.
		rect_opaco(screen, [t_temp[0]-5, t_temp[1]-5, (len_t*T_pix)+10, (T_pix*2)+10], COLOR['Blanco'], 192)		# Recuadro Degradado.
		pygame.draw.rect(screen, COLOR['Gris'], [t_temp[0]-5, t_temp[1]-5, (len_t*T_pix)+10, (T_pix*2)+10], 1)		# Contorno.
		dibujarTexto(texto, [t_temp[0], t_temp[1]], FUENTES[Font_def], COLOR['Negro'])
	else:
		if ret: return 0		# Resetea el contador de ticks.
		else: return c_ticks	# Resetea el contador de ticks.
	return c_ticks

def rect_opaco(screen, surface, color=(0,0,0), alpha=128):		# Rectangulo Opaco, sirve para crear rectangulos transparentes.
	
	img = pygame.Surface(surface[2:])
	img.set_alpha(alpha)
	img.fill(color)
	screen.blit(img, surface[:2])

#===================================================================================================

def saveThread():
	db_temp = Database(DBName)
	db_temp.updateUserFilesAll(console)
	db_temp.orderUserFiles()				# Ordena todos los datos en la Tabla UserFiles en la Base de Datos.
	db_temp.con.commit()
	db_temp.con.close()
	if debug: print('Session Saved at: '+str(datetime.now())[:-7])

def dbConnectionThread():
	global db, console, vista_actual, Prefijo
	global l_com_lim, pos_limit, pos_limit_r
	global l_canciones_activas, l_comandos
	global l_com_ps, con_tam_buffer
	global db_con_thread_finish
	
	console = initDB(DBName, console)
	
	if console.temporal:
		l_canciones_activas, l_comandos, l_com_ps, con_tam_buffer = console.temporal
	
	if len(l_comandos) > 3:
		if l_comandos[-2][0] == ' Cerrando...':
			for x in range(4): l_comandos.pop()
	
	# ~ vista_actual = l_vistas['Consola']			# Vista Actual.
	Prefijo = console.actualPath()+' '			# Simbolo de prefijo para comandos.
	
	l_com_lim   = ( RESOLUCION_CMD[s_res][1]-45) // T_pix_y							# Limite de lineas en consola
	pos_limit   = ( RESOLUCION_CMD[s_res][0]-30 - (len(Prefijo)*(T_pix))) // T_pix	# Limite de letras en linea de comandos.
	pos_limit_r = ((RESOLUCION_CMD[s_res][0]-30)//T_pix)-1							# Limite Real de letras en linea de comandos. 
	console.setConSize(pos_limit_r)													# Se indica el limite de caracteres para consola.
	
	db_con_thread_finish = True
	
	if debug: print('Session Loaded: '+str(console.username))

def getGlobalTime(raw=0):
	# Esta funcion devuelve el tiempo transcurrido desde el inicio de sesion.
	# Raw:
	# 0  = Devuelve Cadena en formtato HH:MM:SS.
	# 1  = Devuelve Entero en formato de Segundos.
	# 2+ = Tiempo objeto Datetime.
	
	time = datetime.now()-global_time_init
	
	if   raw == 0: time = str(time)[:-7]
	elif raw == 1: time = anormalizeTime(str(time)[:-7])//1000
	else: pass
	
	return time

def u_puntero(con, l_con, cant, p_pos):	# Actualizar puntero. U = Update.
	
	p_p_pos = ((p_pos+cant)*T_pix)		# Posicion de Puntero en Pixeles.
	puntero = [
			[ l_con[0]+5 + p_p_pos, l_con[1]+5 ],				# Posicion Inicial en X
			[ l_con[0]+5 + p_p_pos, l_con[1]+con['L_y']-5 ]		# Posicion Inicial en Y
		]
	
	return puntero

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

def clic_boton(screen, pos, rec=0):	# Detecta un Clic en las coordenadas de un boton, contando la posicion de botones derecha a izquierda.
	
	x_pos = RESOLUCION[s_res][0]-btn_x-15*((rec%10)+1)-btn_x*(rec%10)
	y_pos = 5 + (52 if rec >= 10 else 0)
	x, y  = pos
	
	if x > x_pos and x < x_pos + btn_x + 10:
		if y > y_pos and y < btn_y + y_pos + 10:
			return True
	
	return False

def clic_music_checkbox(evento, x_pos, y_pos, pos):
	
	global music_checkbox_down
	
	x_pos -= 20
	tam_x, tam_y = 15, 20
	
	if pos in l_canciones_activas:
		
		rect_opaco(screen, [x_pos+3, y_pos+3, tam_x-6, tam_y-6], COLOR['Verde'], 200)
		
	if evento.type == pygame.MOUSEMOTION:
		
		x, y = evento.pos
		
		if  (x >= x_pos and x <= x_pos+tam_x) \
		and (y >= y_pos and y <= y_pos+tam_y):
			
			rect_opaco(screen, [x_pos, y_pos, tam_x, tam_y], COLOR['Verde'])
	
	elif evento.type == pygame.MOUSEBUTTONDOWN:
		
		if evento.button == 1 and music_checkbox_down == False:
			
			x, y = evento.pos
			
			if  (x >= x_pos and x <= x_pos+tam_x) \
			and (y >= y_pos and y <= y_pos+tam_y):
				
				music_checkbox_down = True
			
	elif evento.type == pygame.MOUSEBUTTONUP and music_checkbox_down:
		
		if evento.button == 1:
			
			x, y = evento.pos
			
			if  (x >= x_pos and x <= x_pos+tam_x) \
			and (y >= y_pos and y <= y_pos+tam_y):
				
				if pos in l_canciones_activas:
					l_canciones_activas.pop(l_canciones_activas.index(pos))
				else:
					l_canciones_activas.append(pos)
					
				music_checkbox_down = False
				
	pygame.draw.rect(screen, COLOR['Verde'], [x_pos, y_pos, tam_x, tam_y], 1)

def match_x_y(x, y, box):
	if  x > box[0] and x < box[0]+box[2] \
	and y > box[1] and y < box[1]+box[3]:
		return True
	return False

def splitText(text):
	
	t = []				# Lista de Fragmentos del Texto original
	s = []				# Lista de Salida.
	
	while True:
		
		if text.endswith(text[:pos_limit_r]):				# Si el final del texto restante es igual a el texto de inicio a la posicion pos_limit_r 
			t.append(text[:pos_limit_r])					# Se agrega a la lista de fragmentos, el fragmento final de texto.
			break											# Se rompe el ciclo, ya que esto anterior indica que ya no hay nada que procesar de la cadena de texto.
		
		t.append(text[:pos_limit_r])						# Se agrega el fragemto de texto desde el inicio del texto hasta la posicion pos_limit_r
		
		if len(t[-1].split(' ')) == 1:						# Si el ultimo fragmento agregado solo es 1 sola cadena sin espacios, entonces
			text = text[pos_limit_r:]						# Se corta el texto dejando desde pos_limit_r en adelante.
		else:												# Si el ultimo fragmento si tenia espacios, entonces
			if t[-1][0] != ' ':								# Si el ultimo fragmento de texto en su ultimo caracter NO era un espacio
				t[-1] = t[-1].split(' ')					# Se separa el texto dividido en cada espacio 
				text = t[-1].pop() + text[pos_limit_r:]		# la ultima palabra del ultimo fragmento de texto se saca de la lista de fragmentos y se devuelve al texto original. Esto evita que las palabras queden cortadas por mitad.
			else:											# Si, si habia un espacio al final, la ultima palabra del texto entonces NO se considera cortada
				text = text[pos_limit_r:]					# Entonces el fragmento de texto ya procesado, se elimina del texto original.
	
	for x in t:												# Por ultimo se extrae cada fragmento de texto, que se encuentra cada uno como una lista de palabras. 
		if type(x) == list:									# Si el fragmento si es una lista
			s.append(' '.join(x))							# Se agrega a la lista de Salida, todas las palabras del fragmento unidas de nuevo con un espacio.
		else:												# Si no era una lista, significa que era una sola palabra
			s.append(x)										# Se agrega tal cual a la lista de salida
		
	return s

def normalizeListComand():		# Si al cambiar resolucion algun texto en pantalla se sale de la consola, pasa el texto sobrante a una nueva linea.
	
	global l_comandos
	
	temp = l_comandos[:]
	t_des = 0
	
	for i, (com, pos) in enumerate(temp):
		sT = splitText(com[1:])
		if len(sT) > 1:
			t_chr = l_comandos[i+t_des][0][0]
			if t_chr == ' ':
				l_comandos[i+t_des] = (t_chr+sT.pop(0), pos)
				while len(sT) > 0:
					t_des += 1
					l_comandos.insert(i+t_des, (t_chr+sT.pop(0), pos))

def normalizeTime(mili, desface=0):
	
	secs = (mili // 1000) + desface
	mins = (secs // 60)
	hrs  = (mins // 60)
	
	time = str(hrs%24).zfill(2)+':'+str(mins%60).zfill(2)+':'+str(secs%60).zfill(2)
	
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

def printTFiles(Prefijo, t_files=[]):
	
	global l_comandos
	
	if len(l_comandos) > 0:
		cont = l_comandos[-1][1]+1
		l_comandos.append((Prefijo, cont))
	else:
		l_comandos.append((Prefijo, 1))
	
	for x in range(len(t_files)):
		if not '.' in t_files[x][-5:]:
			t_files[x] += '/'
	
	l_comandos = add_comand(l_comandos, [''] + ['../'] + t_files + [''])

def temporizer(secs=1):
	global temporizer_init
	
	secs = secs*1000
	actual = anormalizeTime(datetime.now(), True)
	
	if temporizer_init == 0:
		temporizer_init = actual
	
	if temporizer_init+secs <= actual:
		temporizer_init = 0
		return True
	
	return False

#===================================================================================================
#===================================================================================================
#===================================================================================================

def main():
	
	global screen, s_res, pos_limit, pos_limit_r, l_com_lim, FUENTES
	global Prefijo, l_comandos, l_canciones_activas, global_time_init
	global l_vistas, vista_actual, console, l_com_ps, con_tam_buffer
	global db_con_thread_finish
	
	# Inicializaciones =================================================
	
	ss_x, ss_y = get_screen_size()
	# ~ s_x = ss_x//2-RESOLUCION[s_res][0]//2
	# ~ s_y = ss_y//2-RESOLUCION[s_res][1]//2
	# ~ print(ss_x, ss_y, RESOLUCION[s_res], s_x, s_y)
	# ~ os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(s_x, s_y)
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	
	screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
	screen.fill(COLOR['Negro'])													# Rellena el Fondo de Negro.
	
	BGimg_General = load_image('images/background.bmp')							# Carga el Fondo de la Ventana.
	BGimg_General = pygame.transform.scale(BGimg_General, RESOLUCION[s_res])	# Cambia la resolucion de la imagen.
	BGimg_Login = load_image('images/login_background.bmp')						# Carga el Fondo de la Ventana.
	BGimg_Login = pygame.transform.scale(BGimg_Login, RESOLUCION[s_res])		# Cambia la resolucion de la imagen.
	
	Icono  = pygame.image.load('images/Icon.png')			# Carga el icono del Juego.
	
	btn_show_pass = Boton('images/iconos/show_pass.bmp')	# Boton de Ojo Mostrar u Ocultar Password.
	btn_ajustes   = Boton('images/iconos/Ajustes.bmp')		# Boton de Ajustes.
	btn_apagar    = Boton('images/iconos/Apagar.bmp')		# Boton de Apagar.
	btn_atajos    = Boton('images/iconos/Atajos.bmp')		# Boton de Atajos.
	btn_avances   = Boton('images/iconos/Avances.bmp')		# Boton de Avances.
	btn_bateria   = Boton('images/iconos/Bateria.bmp')		# Boton de Bateria.
	btn_cerebro   = Boton('images/iconos/Cerebro.bmp')		# Boton de Cerebro.
	btn_chip      = Boton('images/iconos/Chip.bmp')			# Boton de Chip.
	btn_conexion  = Boton('images/iconos/Conexion.bmp')		# Boton de Conexion.
	btn_consola   = Boton('images/iconos/Consola.bmp')		# Boton de Consola.
	btn_dystopia  = Boton('images/iconos/Dystopia.bmp')		# Boton de Dystopia.
	btn_laberinto = Boton('images/iconos/Laberinto.bmp')	# Boton de Laberinto.
	btn_mail      = Boton('images/iconos/Mail.bmp')			# Boton de Mail.
	btn_usb       = Boton('images/iconos/USB.bmp')			# Boton de USB.
	btn_virus     = Boton('images/iconos/Virus.bmp')		# Boton de Virus.
	
	l_icons = [													# Lista actual de iconos a imprimir.
			btn_ajustes,
			# ~ btn_apagar,
			# ~ btn_avances,
			btn_atajos,
			# ~ btn_bateria,
			# ~ btn_cerebro,
			# ~ btn_chip,
			# ~ btn_conexion,
			# ~ btn_consola,
			# ~ btn_dystopia,
			# ~ btn_laberinto,
			# ~ btn_mail,
			# ~ btn_usb,
			# ~ btn_virus
		]
	
	pygame.display.set_icon(Icono)								# Agrega el icono a la ventana.
	pygame.display.set_caption(TITULO+' '+__version__)			# Titulo de la Ventana del Juego.
	
	pygame.init()												# Inicia El Juego.
	pygame.mixer.init()											# Inicializa el Mesclador.
	
	playlist = [
		('musica/Mega Drive - Converter.mp3',                     0, {'By':'Mega Drive', 'Song':'Converter',                     'Album':'Mega Drive',       'Duration':'00:06:30', 'Released':'2013/11/18', 'Sountrack':'2',  'Type':'MP3 192kbps'}),
		('musica/Mega Drive - Source Code.mp3',                   1, {'By':'Mega Drive', 'Song':'Source Code',                   'Album':'199XAD',           'Duration':'00:04:53', 'Released':'2019/10/04', 'Sountrack':'11', 'Type':'MP3 192kbps'}),
		('musica/Mega Drive - Seas Of Infinity.mp3',              2, {'By':'Mega Drive', 'Song':'Seas Of Infinity',              'Album':'Seas Of Infinity', 'Duration':'00:02:08', 'Released':'2017/05/18', 'Sountrack':'1',  'Type':'MP3 192kbps'}),
		('musica/Dynatron - Pulse Power.mp3',                     3, {'By':'Dynatron',   'Song':'Pulse Power',                   'Album':'Escape Velocity',  'Duration':'00:06:00', 'Released':'2012/11/22', 'Sountrack':'8',  'Type':'MP3 192kbps'}),
		('musica/Dynatron - Vox Magnetismi.mp3',                  4, {'By':'Dynatron',   'Song':'Vox Magnetismi',                'Album':'Escape Velocity',  'Duration':'00:03:46', 'Released':'2012/11/22', 'Sountrack':'5',  'Type':'MP3 192kbps'}),
		('musica/Varien - Born of Blood, Risen From Ash.mp3',     5, {'By':'Varien',     'Song':'Born of Blood, Risen From Ash', 'Album':'',                 'Duration':'00:04:06', 'Released':'2019/04/05', 'Sountrack':'',   'Type':'MP3 192kbps'}),
		('musica/Varien - Blood Hunter.mp3',                      6, {'By':'Varien',     'Song':'Blood Hunter',                  'Album':'',                 'Duration':'00:03:47', 'Released':'2018/02/10', 'Sountrack':'',   'Type':'MP3 192kbps'}),
		('musica/Varien - Of Foxes and Hounds.mp3',               7, {'By':'Varien',     'Song':'Of Foxes and Hounds',           'Album':'',                 'Duration':'00:05:04', 'Released':'2018/04/02', 'Sountrack':'',   'Type':'MP3 192kbps'}),
		('musica/Kroww - Hysteria.mp3',                           8, {'By':'Kroww',      'Song':'Hysteria',                      'Album':'',                 'Duration':'00:05:14', 'Released':'2019/09/24', 'Sountrack':'',   'Type':'MP3 192kbps'}),
		('musica/Scandroid - Thriller (Fury Weekend Remix).mp3',  9, {'By':'Scandroid',  'Song':'Thriller',                      'Album':'',                 'Duration':'00:04:52', 'Released':'2018/10/15', 'Sountrack':'',   'Type':'MP3 128kbps'}),
		('musica/Neovaii - Easily.mp3',                          10, {'By':'Neovaii',    'Song':'Easily',                        'Album':'',                 'Duration':'00:04:18', 'Released':'//',         'Sountrack':'',   'Type':'MP3 128kbps'}),
		('musica/Stephen - Crossfire.mp3',                       11, {'By':'Stephen',    'Song':'Crossfire',                     'Album':'',                 'Duration':'00:04:31', 'Released':'//',         'Sountrack':'',   'Type':'MP3 128kbps'}),
	]
	
	if debug: l_canciones_activas = []
	else: l_canciones_activas = [i for i in range(len(playlist))]
	
	music = pygame.mixer.music									# Indicamos quien será la variable para Manipular el Soundtrack.
	song_pos = random.randint(0, len(playlist)-1)				# Genera un numero random entre 0 y la longitud de la lista de canciones menos 1.
	song_actual = playlist[song_pos][0]							# Selecciona la cancion en la posicion song_pos.
	music.load(song_actual)										# Carga el Soundtrack
	
	# ~ music.set_pos(60.0) # Segundos
	
	# ~ music.set_endevent(pygame.USEREVENT)
	# ~ music.stop()			# Detiene la cancion.
	# ~ music.rewind()			# Reinicia la cancion desde el segundo 0.
	# ~ music.set_pos(60.0)			# Inicia en el segundo 60 de la cancion.
	
	FUENTES = {
		   'Inc-R 18':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 18),
		   'Inc-R 16':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 16),
		   'Inc-R 14':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 14),
		   'Inc-R 12':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 12),
		   'Retro 16':pygame.font.Font("fuentes/Retro Gaming.ttf", 16),
		   'Wendy 18':pygame.font.Font("fuentes/Wendy.ttf", 18)
		  }
	
	VERDE   = COLOR['Verde']
	VERDE_C = COLOR['Verde Claro']
	AZUL    = COLOR['Azul']
	AZUL_C  = COLOR['Azul Claro']
	
	# Variables ========================================================
	
	game_over = False				# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()		# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	
	segundos   = 0			# Contador de Tiempo, 1 seg por cada 60 Ticks.
	ticks      = 0			# Contador de Ticks.
	Comando    = ''			# Comando en linea actual.
	p_pos      = 0			# Posicion del Puntero, para manipular en que posicion estara en la cadena 'Comando'. p_pos = 5 significaria entonces que estara el puntero en el caracter 5.
	
	# Dimensiones de Consola:
	# P = Punto inicial. T = Tamaño. M = Margen. L = linea
	con = {
		'P_x':5,    'P_y':5,
		'L_x':None, 'L_y':20,
		'T_x':RESOLUCION_CMD[s_res][0]-10,
		'T_y':RESOLUCION_CMD[s_res][1]-10,
		'T_m':5
	}
	
	con['L_x'] = con['T_x'] - ( con['T_m']*2 )						# Agrega los valores para L_x.
	
	t_con = [ con['P_x'], con['P_y'], con['T_x'], con['T_y'] ]		# Tamanios de Consola
	l_con = [														# Linea de Consola para los comandos
		con['P_x']+con['T_m'],
		con['P_y']+con['T_y']-con['L_y']-con['T_m'],
		con['L_x'],
		con['L_y']
	]
	
	p_letra = [ l_con[0]+5, l_con[1]+2 ]			# Posicion Inicial de texto.
	
	# Booleanos:
	a_shift = False if GetKeyState(VK_CAPITAL) == 0 else True	# Saber si esta activo el Bloq. Mayus o las teclas Shift de izquierda o derecha.
	
	k_down  = False			# Indica si se esta manteniendo presionada cualquier tecla.
	k_wait  = 0				# Medidor de Ticks para el k_down
	k_back  = False			# Indica si se esta presionando la tecla BackSpace.
	k_del   = False			# Indica si se esta presionando la tecla DEL o SUPR.
	k_char  = False			# Indica si se esta presionando una tecla de letra, numero o espacio.
	k_izq   = False			# Indica si se esta presionando la tecla flecha izquierda.
	k_der   = False			# Indica si se esta presionando la tecla flecha derecha.
	k_arr   = False			# Indica si se esta presionando la tecla flecha arriba.
	k_aba   = False			# Indica si se esta presionando la tecla flecha abajo.
	exe     = False			# Indica si se ejecutara un comando o no.
	c_res   = False			# Cambio de Resolucion.
	s_full  = False			# Indica si esta la Pantalla Completa activada.
	s_fullF = False			# Indica si se tomo una captura de pantalla.
	s_shot  = False			# Indica si se tomo una captura de pantalla.
	s_song_vol = False		# Indica si se intenta subir o bajar el volumen.
	
	s_full_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
	s_shot_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
	s_song_vol_ticks = 0			# Indica el tiempo en ticks que se mostrara un texto.
	
	# Cache de comandos para las teclas de Flecha Arriba y Abajo.
	cache_com = []
	cache_pos = 0
	
	#===================================================================
	
	ajust_pos_y = 1
	ajust_init_x, ajust_init_y =  25, 50	# Ajustar a la posicion
	ajust_v_tamX, ajust_v_tamY = 110, 30
	cant_scroll = 3
	
	#===================================================================
	# Variables de la Musica:
	
	song_vol           = 20					# Volumen al 20%
	song_vol_pres_min  = False
	song_vol_pres_plus = False
	song_vol_mute      = False
	song_change_down   = False
	song_change_up     = False
	song_stop          = False
	song_fade_secs     = 1
	song_fade_ticks    = 0
	song_desface       = 0
	
	music.set_volume(song_vol / 100)	# Selecciona en Nivel de Volumen entre 0.0 y 1.0.
	music.play()						# -1 Repetira infinitamente la canción.
	
	#===================================================================
	
	global_time_init = datetime.now()
	save_game = False
	
	#===================================================================
	# Login Data:
	
	console_name = 'Odin.Dis_'+__version__
	username    = ''
	password    = ''
	login_pos   = 1
	login_vista = 0
	login_rect_user_list = []
	login_list_active = False
	login_show_pass = False
	login_carga = False
	login_list = []
	login = False
	login_error = False
	login_new = False
	login_btn_pos = 2
	
	#===================================================================
	
	# Inicio Del Juego:
	while game_over is False:
		
		# Validaciones de la Musica:
		#===============================================================
		if ticks % 60 == 0:
			song_time = normalizeTime(music.get_pos(), song_desface)
			if l_canciones_activas:				# Si hay canciones activas, entonces...
				if not music.get_busy():		# Si no esta activa la cancion, entonces...
						song_pos = (song_pos+1) % len(playlist)				# Cambia la cancion
						while not song_pos in l_canciones_activas:			# Si el numero de cancion no esta en la lista de canciones activas,
							song_pos = (song_pos+1) % len(playlist)			# Sigue cambiando a la siguiente.
						music.load(playlist[song_pos][0])					# Carga la cancion
						music.play()										# Reproduce la cancion.
						song_desface = 0									# Reinicia la variable de desface que controla el avance de tiempo con CTRL+Felcha Derecha o Izquierda.
						song_break = 0										# Reinicia la variable de espera de 3 segundos
				else:
					# Esta seccion verifica si la canción actual aun sigue en la lista de canciones activas. Sino, tratará de cambiarla inmediatamente.
					temp = song_pos
					while not temp in l_canciones_activas:
						temp = (temp+1) % len(playlist)
					if not temp == song_pos:
						song_pos = temp
						music.stop()
						music.load(playlist[song_pos][0])
						music.play()
						song_desface = 0
			else:
				music.stop()
		#===============================================================
		
		ticks += 1
		
		# Chequeo Constante de Eventos del Teclado:
		events = pygame.event.get()
		
		for evento in events:
			
			# ~ print(evento)
			
			if evento.type == pygame.QUIT: game_over = True		# Si Se Presiona El Botón Cerrar, Cerrara El Juego.
			
			elif evento.type == pygame.MOUSEBUTTONDOWN:			# Manipulación del Mouse.
				
				# evento.button:
				# Clic  Izq = 1 - Clic  Cen = 2 - Clic Der = 3
				# Rueda Arr = 4 - Rueda Aba = 5
				
				# ~ print(evento.pos)
				if evento.button == 1:
					
					x, y = evento.pos
					
					if vista_actual == l_vistas['Login']:
						
						tam_f = 16
						text = 'Usuario:'
						
						tb_user = [
							RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118,
							RESOLUCION[s_res][1]//3 + 25,
							(int(len(text)*tam_f/4) + 118) * 2, 30
						]
						
						tb_pass = [
							RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118,
							RESOLUCION[s_res][1]//3 + 70 + 25,
							(int(len(text)*tam_f/4) + 118) * 2, 30
						]
						
						b_ul = [ tb_user[0]+tb_user[2] + 20, tb_user[1], 30, 30 ]		# box user list.
						
						b_sp = [ rect_pos2[0]+rect_pos2[2] + 20, rect_pos2[1], 30, 30 ]	# box show pass.
						
						b_btn_c = [RESOLUCION[s_res][0]//2 - 130, int((RESOLUCION[s_res][1]//2)+150), 100, 30]		# box boton cancelar
						b_btn_a = [RESOLUCION[s_res][0]//2 +  30, int((RESOLUCION[s_res][1]//2)+150), 100, 30]		# box boton aceptar
						
						if not login_new:
							if match_x_y(x, y, tb_user):
								if   login_pos == 1: username = Comando
								elif login_pos == 2: password = Comando
								Comando = username
								p_pos = len(Comando)
								login_pos = 1
									
							elif match_x_y(x, y, tb_pass):
								if   login_pos == 1: username = Comando
								elif login_pos == 2: password = Comando
								Comando = password
								p_pos = len(Comando)
								login_pos = 2
							
							elif match_x_y(x, y, b_ul):
								if login_list_active: login_list_active = False
								else: login_list_active = True
							
							if login_list_active:
								for u, p, box in login_rect_user_list:
									if match_x_y(x, y, box):
										username = u
										password = p
										if   login_pos == 1: Comando = username; p_pos = len(Comando)
										elif login_pos == 2: Comando = password; p_pos = len(Comando)
							
						else:
							if match_x_y(x, y, b_btn_c):
								login_new = False
							elif match_x_y(x, y, b_btn_a):
								login_new = False
								login = True
						
						if match_x_y(x, y, b_sp):
							if login_show_pass: login_show_pass = False
							else: login_show_pass = True
						
					elif vista_actual == l_vistas['Consola']:
						
						if clic_boton(screen, evento.pos, 0):
							vista_actual = l_vistas['Ajustes']	# Detecta si se presiono el primer boton.
							l_icons = [
								btn_consola,
								# ~ btn_ajustes,
								btn_atajos,
							]
						
						elif clic_boton(screen, evento.pos, 1):
							vista_actual = l_vistas['Atajos']	# Detecta si se presiono el primer boton.
							l_icons = [
								btn_consola,
								btn_ajustes,
								# ~ btn_atajos,
							]
						
					elif vista_actual == l_vistas['Ajustes']:
						
						if clic_boton(screen, evento.pos, 0):
							vista_actual = l_vistas['Consola']	# Detecta si se presiono el primer boton.
							l_icons = [
								# ~ btn_consola,
								btn_ajustes,
								btn_atajos,
							]
						
						elif clic_boton(screen, evento.pos, 1):
							vista_actual = l_vistas['Atajos']	# Detecta si se presiono el primer boton.
							l_icons = [
								btn_consola,
								btn_ajustes,
								# ~ btn_atajos,
							]
						
						if x > ajust_init_x and x < ajust_init_x+215:
							
							ajust_pos_y = 2
							
							if y > ajust_init_y*ajust_pos_y and y < ajust_init_y*ajust_pos_y+ajust_v_tamY-10: c_res = False if c_res else True
							
							if c_res:
								for i in range(1, len(RESOLUCION)):
									if x > ajust_init_x+115 and x < ajust_init_x+ajust_v_tamX+100 \
									and y > ajust_init_y*ajust_pos_y+(ajust_v_tamY*i) and y < 20+ajust_init_y*ajust_pos_y+(ajust_v_tamY*i):
										s_res = ((s_res+i)%len(RESOLUCION))
										
										if s_full: screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
										else:
											if (ss_x, ss_y) == RESOLUCION[s_res]:
												s_full = True
												screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
												s_full_ticks = 0
											else:
												os.environ['SDL_VIDEO_CENTERED'] = '1'
												screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
												
										BGimg_General = load_image('images/background.bmp')											# Carga el Fondo de la Ventana.
										BGimg_General = pygame.transform.scale(BGimg_General, RESOLUCION[s_res])							# Cambia la resolucion de la imagen.
										
										l_com_lim = ( RESOLUCION_CMD[s_res][1]-45) // T_pix_y								# Limite de lineas en consola
										pos_limit = ( RESOLUCION_CMD[s_res][0]-30 - (len(Prefijo)*(T_pix))) // T_pix		# Limite de letras en linea de comandos.
										pos_limit_r = ((RESOLUCION_CMD[s_res][0]-30)//T_pix)-1								# Limite Real de letras en linea de comandos. 
										console.setConSize(pos_limit_r)														# Se indica el limite de caracteres para consola.
										
										con = { 'P_x':5, 'P_y':5, 'L_x':None, 'L_y':20,
												'T_x':RESOLUCION_CMD[s_res][0]-10, 'T_y':RESOLUCION_CMD[s_res][1]-10, 'T_m':5 }					# Dimensiones Generales para la Consola.
										con['L_x'] = con['T_x'] - ( con['T_m']*2 )																# Agrega los valores para L_x.
										t_con = [ con['P_x'], con['P_y'], con['T_x'], con['T_y'] ]												# Tamanios de Consola.
										l_con = [ con['P_x']+con['T_m'], con['P_y']+con['T_y']-con['L_y']-con['T_m'], con['L_x'], con['L_y'] ]	# Linea de Consola para los comandos.
										p_letra = [ l_con[0]+5, l_con[1]+2 ]																	# Posicion Inicial de texto.
										c_res = False
										
										normalizeListComand()
							
						else: c_res = False
						
					elif vista_actual == l_vistas['Atajos']:
						
						if clic_boton(screen, evento.pos, 0):
							vista_actual = l_vistas['Consola']	# Detecta si se presiono el primer boton.
							l_icons = [
								# ~ btn_consola,
								btn_ajustes,
								btn_atajos,
							]
						
						elif clic_boton(screen, evento.pos, 1):
							vista_actual = l_vistas['Ajustes']	# Detecta si se presiono el primer boton.
							l_icons = [
								btn_consola,
								# ~ btn_ajustes,
								btn_atajos,
							]
						
				if evento.button == 4:
					if vista_actual == l_vistas['Consola']:
						# Si la posicion en lista de comandos es menor que la cantidad de lineas de comandos
						if l_com_ps < len(l_comandos):
							# Si la cantidad de lineas en lista de comandos es mayor al limite de lineas de comandos en pantalla
							# Y si la suma de posicion + el limite es menor a la cantidad de comandos, significa que por encima hay mas lineas de texto.
							# En resumen, Detecta si hay mas texto por encima 
							if len(l_comandos) > l_com_lim and (l_com_ps + l_com_lim) < len(l_comandos):
								# Y Permite desplazarse hacia arriba linea por linea, hasta que no haya mas encima.
								l_com_ps += cant_scroll
					
				elif evento.button == 5:
					if vista_actual == l_vistas['Consola']:
						if l_com_ps > 0:	# Mientras haya lineas debajo permite dezplazarse.
							l_com_ps -= cant_scroll
			
			#=================================================================================
			
			elif evento.type == pygame.KEYDOWN:		# Manipulación del Teclado.
				
				# Al presionar cualquier tecla.
				k_down = True
				k_wait = 1
				
				#=================================================================================
				
				if evento.key == pygame.K_ESCAPE:
					
					if vista_actual == l_vistas['Consola']:
						
						temp = [
							str(l_canciones_activas), str(l_comandos),
							str(l_com_ps), str(con_tam_buffer)
						]
						db = Database(DBName)
						db.updateUserConfig(console.username, temp)
						db.con.commit()
						db.con.close()
						
						threading.Thread(target=saveThread).start()
						
						vista_actual = l_vistas['Login']
						
						l_canciones_activas = []
						
						segundos   = 0			# Contador de Tiempo, 1 seg por cada 60 Ticks.
						ticks      = 0			# Contador de Ticks.
						Comando    = ''			# Comando en linea actual.
						l_comandos = []			# Lista de comandos ejecutados.
						l_com_ps   = 0			# Poicion actual de lista de comandos ejecutados mostrados, 0 equivale a los mas recientes.
						p_pos      = 0			# Posicion del Puntero, para manipular en que posicion estara en la cadena 'Comando'. p_pos = 5 significaria entonces que estara el puntero en el caracter 5.
						
						# Booleanos:
						c_res   = False			# Cambio de Resolucion.
						
						s_full_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
						s_shot_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
						s_song_vol_ticks = 0			# Indica el tiempo en ticks que se mostrara un texto.
						
						# Cache de comandos para las teclas de Flecha Arriba y Abajo.
						cache_com = []
						cache_pos = 0
						
						#===================================================================
						# Variables de la Musica:
						song_stop       = False
						song_fade_ticks = 0
						song_desface    = 0
						
						#===================================================================
						# Login Data:
						username    = ''
						password    = ''
						login_pos   = 1
						login_vista = 0
						login_list_active = False
						login_show_pass = False
						login_carga = False
						login_list = []
						login = False
						
					elif vista_actual == l_vistas['Login']:
						game_over = True		# Tecla ESC Cierra el Juego.
				
				#=================================================================================
				# Teclas Bloq Mayus, y las teclas Shift izquerdo y derecho.
				elif evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
				or evento.key == pygame.K_CAPSLOCK:
					if vista_actual == l_vistas['Consola']:
						a_shift = False if a_shift else True
				
				#=================================================================================
				# Felchas de direcciones
				elif evento.key == pygame.K_LEFT:
					if vista_actual == l_vistas['Login']:
						if login_new:
							if login_btn_pos == 2: login_btn_pos = 1
					elif vista_actual == l_vistas['Consola']:
						if p_pos > 0: p_pos -= 1
						k_izq = True
					
				elif evento.key == pygame.K_RIGHT:
					if vista_actual == l_vistas['Login']:
						if login_new:
							if login_btn_pos == 1: login_btn_pos = 2
					if vista_actual == l_vistas['Consola']:
						if p_pos < len(Comando): p_pos += 1
						k_der = True
					
				elif evento.key == pygame.K_UP:
					if vista_actual == l_vistas['Consola']:
						if len(cache_com) > 0:
							k_arr = True
							if cache_com[cache_pos] != Comando and cache_pos == 0:
								cache_com.insert(0, Comando)	# Inserta el Comando en la posicion 0 de la lista
							
							if cache_pos < len(cache_com)-1:
								cache_pos += 1					# Aumenta la posicion en 1, o sea, para mostrar uno anterior.
							if '' in cache_com[1:]: 
								cache_com = cache_com[::-1]
								cache_com.remove('')
								cache_com = cache_com[::-1]
							
							# Evita que se salga del rango de cache_com
							if not len(cache_com) <= cache_pos:
								Comando = cache_com[cache_pos][:pos_limit_r-len(Prefijo)+1]
								p_pos = len(Comando)
					
				elif evento.key == pygame.K_DOWN:
					if vista_actual == l_vistas['Consola']:
						if cache_pos > 0:
							k_aba = True
							cache_pos -= 1
							if cache_com[cache_pos] == '' and not cache_pos == 0:
								cache_com.pop(cache_pos)
								cache_pos -= 1
							Comando = cache_com[cache_pos]
							p_pos = len(Comando)
						
				#=================================================================================
				# Eliminar Caracteres
				elif evento.key == pygame.K_BACKSPACE:
					if vista_actual == l_vistas['Login']:
						if not login_new:
							if p_pos > 0:
								Comando = Comando[:p_pos-1]+Comando[p_pos:]
								p_pos  -= 1
								k_back  = True
					elif vista_actual == l_vistas['Consola']:
						if p_pos > 0:
							Comando = Comando[:p_pos-1]+Comando[p_pos:]
							p_pos  -= 1
							k_back  = True
				
				elif evento.key == pygame.K_DELETE:
					if vista_actual == l_vistas['Login']:
						if not login_new:
							if p_pos < len(Comando):
								Comando = Comando[:p_pos]+Comando[p_pos+1:]
								k_del   = True
					elif vista_actual == l_vistas['Consola']:
						if p_pos < len(Comando):
							Comando = Comando[:p_pos]+Comando[p_pos+1:]
							k_del   = True
				
				#=================================================================================
				# Acciones al Presionar ENTER.
				elif evento.key == pygame.K_RETURN:
					if vista_actual == l_vistas['Login']:
						
						if login_pos == 1 and Comando:
							username = Comando
							Comando = password
							p_pos = len(Comando)
							login_pos = 2
						elif login_pos == 2:
							password = Comando
						
						if username and password:
							temp = False
							us, pa = [], []
							for u, p in login_list: us.append(u); pa.append(p)
							if username in us:
								if password == pa[us.index(username)]:
									login = True
								else:
									login_error = True
							else:
								if not login_new:
									login_new = True
								else:
									if login_btn_pos == 2:
										login = True
									else:
										login = False
									login_btn_pos = 2
									login_new = False
						
					elif vista_actual == l_vistas['Consola']:
						if not Comando == '':
							
							l_com_ps = 0
							exe = True
							
							if len(l_comandos) > 0:
								cont = l_comandos[-1][1]+1
								l_comandos.append((Prefijo+Comando, cont))
							else:
								l_comandos.append((Prefijo+Comando, 1))
							
							# Si el comando ya existe en Cache, se eliminan todas sus replicas, dejando solo el nuevo en la lista.
							while Comando in cache_com:
								temp_pos = cache_com.index(Comando)
								cache_com.pop(temp_pos)
							
							cache_com.insert(0, Comando)
							cache_pos = 0
							
							p_pos = 0
							
				#=================================================================================
				# Combinacion de Teclas
				
				# Detecta cuando se presiona TAB:
				elif evento.unicode == '\t' and evento.mod == 0:			# mod = 0 = Sin modificador.
					if vista_actual == l_vistas['Login']:
						print(login_pos)
						if login_pos == 1:
							username = Comando
							Comando = password
							p_pos = len(Comando)
							login_pos = 2
							
					elif vista_actual == l_vistas['Consola']:
						t_root = ''
						t_files = Comando.split(' ')							# Divide el comando por los espacios.
						
						if t_files[0] in ['cd', 'cat', 'type', 'ls', 'dir']:
							t_files = [t_files[0], ' '.join(t_files[1:])]		# Si el nombre tiene un espacio, vuelve a unirlo con sus espacios.
						elif t_files[0] in ['chmod']:
							t_files = [' '.join(t_files[:2]), ' '.join(t_files[2:])]		# Agrega el Atributo al comando principal. Y deja solo en 2 partes del comando.
						else:
							pass
						
						if len(t_files) == 2:
							
							t_folders_l = t_files[1].split('/')
							
							if len(t_files[1]) > 0 and t_files[1][0] == '/':
								t_path = []
								t_root = '/'
								t_folders_l.pop(0)
							else:
								t_path = console.pathPos[:]
							
							if len(t_folders_l) > 1:
								for t in t_folders_l[:-1]:
									if t == '..':
										try: t_path.pop()
										except: pass
										continue
									t_childs = console.getChilds(t_path)
									t_ch = [ str(c) for c in t_childs]
									try: t_path = t_path + [t_ch.index(t)]
									except: break
							
							t_folder = t_folders_l[-1]
							t_childs = console.getChilds(t_path)
							t_childs = [ str(t) for t in t_childs]
							if t_files[0] in ['cd','ls']:
								t_childs = [ (c if not '.' in c[-5:] else '') for c in t_childs]
							# ~ elif t_files[0] == '':
								# ~ t_childs = [ (c if '.' in c[-5:] else '') for c in t_childs]
							t_childs = [ (c if c.startswith(t_folder) else '') for c in t_childs]
							while '' in t_childs: t_childs.remove('')
							
							if len(t_childs) > 1:
								temp = False
								temp2 = ''
								for x in t_childs:
									temp2 = x if len(x) > len(temp2) else temp2
								
								for x in range(len(temp2)):
									for y in t_childs:
										if not y.startswith(t_childs[0][:x]): temp = True; break
									if temp: x-=1; break
								
								t_folders = '/'.join(t_folders_l[:-1])
								t_folders += '/' if t_folders != '' else t_folders
								
								if len(t_folders) > 0:
									if not t_folders[0] == '/':
										t_folders = t_root + t_folders
								else:
									t_folders = t_root + t_folders
								
								Comando = t_files[0] + ' ' + t_folders + t_childs[0][:x]
								p_pos = len(Comando)
								
								printTFiles(console.getPath2(t_path, '> '), t_childs)
								
							elif len(t_childs) == 1:
								
								t_child = t_childs[0]
								
								t_folders = '/'.join(t_folders_l[:-1])
								t_folders += '/' if t_folders != '' else t_folders
								
								if len(t_folders) > 0:
									if not t_folders[0] == '/':
										t_folders = t_root + t_folders
								else:
									t_folders = t_root + t_folders
								
								if not '.' in t_child[-5:]:
									t_ext = '/'
								else:
									t_ext = ''
									if len(t_child.split(' ')) > 1:
										t_child = '"' + t_child + '"'
								
								Comando = t_files[0] + ' ' + t_folders + t_child + t_ext
								p_pos = len(Comando)
							
							else: printTFiles(console.getPath2(t_path, '> '))
				
				elif evento.unicode == '\t' and evento.mod == 1:			# mod = 1 = Shift
					if vista_actual == l_vistas['Login']:
						if login_pos == 2:
							password = Comando
							Comando = username
							p_pos = len(Comando)
							login_pos = 1
				
				#=================================================================================
				press_Fx = False
				
				# Ctrl + P o F10 para tomar una Captura de Pantalla.
				if   evento.key == pygame.K_p and evento.mod == 64 or evento.key == pygame.K_F10:
					
					s_n = 1
					s_folder = 'screenshots/'
					s_path = s_folder+'screenshot_001.jpg'
					
					if not os.path.isdir(s_folder): os.mkdir(s_folder)
					
					while os.path.exists(s_path):
						s_n += 1
						s_path = s_folder+'screenshot_{}.jpg'.format(str(s_n).zfill(3))
					
					pygame.image.save(screen, s_path)
					
					s_shot_ticks = 0
					s_shot = True
					press_Fx = True
				
				# Ctrl + F o F11 para poner Pantalla Completa.
				elif evento.key == pygame.K_f and evento.mod == 64 or evento.key == pygame.K_F11:
					
					if s_full:
						
						if (ss_x, ss_y) == RESOLUCION[s_res]:
							s_fullF = True
						else:
							os.environ['SDL_VIDEO_CENTERED'] = '1'
							screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
							s_full = False
					else:
						screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
						s_full = True
					
					# ~ pygame.key.set_mods(0)
					s_full_ticks = 0
					press_Fx = True
				
				# Ctrl + 'J': Cancion Anterior
				elif evento.key == pygame.K_j and evento.mod == 64:			# mod = 64 = Ctrl
					if l_canciones_activas:
						
						song_pos = (song_pos-1) % len(playlist)
						while not song_pos in l_canciones_activas:
							song_pos = (song_pos-1) % len(playlist)
						
						music.fadeout(song_fade_secs*1000)
						song_change_down = True
						song_desface = 0
					else:
						music.stop()
					
				# Ctrl + 'L': Cancion Siguiente
				elif evento.key == pygame.K_l and evento.mod == 64:			# mod = 64 = Ctrl
					if l_canciones_activas:
						song_pos = (song_pos+1) % len(playlist)
						while not song_pos in l_canciones_activas:
							song_pos = (song_pos+1) % len(playlist)
						music.fadeout(song_fade_secs*1000)
						song_change_up = True
						song_desface = 0
					else:
						music.stop()
					
				# Ctrl + 'K': Pausa
				elif evento.key == pygame.K_k and evento.mod == 64:			# mod = 64 = Ctrl
					if song_stop:
						song_stop = False
						music.unpause()
					else:
						song_stop = True
						music.pause()
					
				# Ctrl + '-': Volumen - 1%
				elif evento.key ==  47 and evento.mod == 64:				# mod = 64 = Ctrl
					if song_vol > 0: song_vol -= 1
					music.set_volume(song_vol/100)
					s_song_vol = True
					s_song_vol_ticks = 0
					song_vol_pres_min = True
					
				# Ctrl + '+': Volumen + 1%
				elif evento.key ==  93 and evento.mod == 64:				# mod = 64 = Ctrl
					if song_vol < 100: song_vol += 1
					music.set_volume(song_vol/100)
					s_song_vol = True
					s_song_vol_ticks = 0
					song_vol_pres_plus = True
						
				# Ctrl + M: Mute.
				elif evento.key == 109 and evento.mod == 64:				# mod = 64 = Ctrl
					song_vol = 0
					music.set_volume(song_vol/100)
					s_song_vol = True
					s_song_vol_ticks = 0
					song_vol_pres_plus = True
					
				# Ctrl + Flecha Derecha: Avanzar 10 segundos de la Cancion.
				elif evento.key == 275 and evento.mod == 64:
					if l_canciones_activas:
						song_desface += 10
						temp = music.get_pos()
						
						temp += (song_desface*1000)
						
						temp2 = playlist[song_pos][2]['Duration']
						print(temp2)
						temp2 = anormalizeTime(temp2, True)		# Convierte el texto de Duracion a Milisegundos.
						print(temp2)
						if temp > temp2: temp = temp2
						
						music.stop()
						music.load(playlist[song_pos][0])
						song_desface = int(temp/1000)
						
						music.play(start=song_desface)
					
				# Ctrl + Flecha Izquierda: Retroceder 10 segundos de la Cancion.
				elif evento.key == 276 and evento.mod == 64:
					if l_canciones_activas:
						song_desface -= 10
						if song_desface < 0: song_desface = 0
						
						temp = music.get_pos()
						temp += song_desface*1000
						
						if temp < 0: temp = 0
						
						music.stop()
						music.load(playlist[song_pos][0])
						song_desface = int(temp/1000)
						
						music.play(start=song_desface)
					
				# Ctrl + Shift + L: Limpiar Pantalla.
				elif evento.key == 108 and evento.mod == 65:				# mod = 64 = Ctrl
					l_comandos = []
				
				# Ctrl + Shift + '-': Volumen - 10%
				elif evento.key ==  47 and evento.mod == 65:				# mod = 64 = Ctrl
					if song_vol > 0: song_vol -= 10
					if song_vol < 0: song_vol = 0
					music.set_volume(song_vol/100)
					s_song_vol = True
					s_song_vol_ticks = 0
					song_vol_pres_min = True
					
				# Ctrl + Shift + '+': Volumen + 10%
				elif evento.key ==  93 and evento.mod == 65:				# mod = 64 = Ctrl
					if song_vol < 100: song_vol += 10
					if song_vol > 100: song_vol = 100
					music.set_volume(song_vol/100)
					s_song_vol = True
					s_song_vol_ticks = 0
					song_vol_pres_plus = True
					
				# ~ print(evento)
				
				# Deteccion de Caracteres En Consola.
				if vista_actual == l_vistas['Consola'] or vista_actual == l_vistas['Login'] and not login_new:
					if len(Comando) < pos_limit and press_Fx == False:
						
						# Se actualizan los valores por si se presiono alguna de las siguientes teclas.
						p_pos += 1
						k_char = True
						
						# Inserta un caracter en la posicion p_pos del Comando.
						temp = CARACTERES if vista_actual == l_vistas['Consola'] else LOGIN_CARACTERES
						if not evento.unicode == '' and evento.unicode in temp: Comando = i_let(Comando, evento.unicode, p_pos)
						else:
							# Si no, se restablecen los valores, significa que no se presiono ninguna de las teclas anteriores a partir del ultimo IF.
							p_pos -= 1
							k_char = False
						
				#=================================================================================
				
			elif evento.type == pygame.KEYUP:
				
				song_vol_pres_min = False
				song_vol_pres_plus = False
				
				if vista_actual == l_vistas['Consola'] or vista_actual == l_vistas['Login']:
					# Al soltar cualquier tecla.
					k_down = False
					k_back = False
					k_del  = False
					k_char = False
					k_izq  = False
					k_der  = False
					k_arr  = False
					k_aba  = False
					k_wait = 0
					exe = False
					
					if evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
					or evento.key == pygame.K_CAPSLOCK:
						a_shift = False if a_shift else True
		
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		
		if vista_actual == l_vistas['Login']:
			
			screen.blit(BGimg_Login, (0, 0))		# Carga la imagen de Fondo. Limpiando todo lo anterior en pantalla.
			
			if login_list == []:
				if os.path.exists(DBName):
					db = Database(DBName)
					login_list = [[data[0],data[1]] for data in db.getData('User','user, pass')]
					db.con.close()
					print(login_list)
			
			if k_down:
				if not (k_wait > 0 and k_wait < 30) \
				and len(Comando) > 0 and p_pos < pos_limit:
					
					if (k_wait % T_rep) == 0 and Comando[-1] in CARACTERES:
						if k_back:
							if p_pos > 0:
								Comando = Comando[:p_pos-1]+Comando[p_pos:]
								p_pos -= 1
						elif k_del:
							if p_pos < len(Comando):
								Comando = Comando[:p_pos]+Comando[p_pos+1:]
						elif k_izq:
							if p_pos > 0: p_pos -= 1
						elif k_der:
							if p_pos < len(Comando): p_pos += 1
						else:
							if k_char:						# Mientras se este presionado una letra, un numero o un espacio, se seguira agregando caracteres.
								if len(Comando) < pos_limit:
									Comando = Comando[:p_pos] + Comando[p_pos-1] + Comando[p_pos:]
									p_pos += 1
				
				k_wait += 1
			
			# ~ # Linea Guia, Centro de Pantalla. En X:
			# ~ pygame.draw.line (screen,VERDE_C,(0,RESOLUCION[s_res][1]//2), (RESOLUCION[s_res][0],RESOLUCION[s_res][1]//2))
			
			# ~ # Linea Guia, Centro de Pantalla. En Y:
			# ~ pygame.draw.line (screen,VERDE_C,(RESOLUCION[s_res][0]//2,0), (RESOLUCION[s_res][0]//2,RESOLUCION[s_res][1]))
				
			tam_f = 16	# Tamanio de Fuente.
			
			text = TITULO + ' ' + __version__
			text_pos = [10, RESOLUCION[s_res][1] - 25]
			rect_opaco(screen, [text_pos[0], text_pos[1], int(len(text)*tam_f/4)*2, tam_f], COLOR['Negro'], 50)
			dibujarTexto(text, text_pos, FUENTES['Inc-R 12'], COLOR['Verde Claro'])	# Dibuja texto en Pantalla.
			
			text = str(datetime.now())[-15:-7]									# Hora Actual.
			text_pos = [RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4), 20]	# Centro de Pantalla.
			rect_opaco(screen, [text_pos[0], text_pos[1], int(len(text)*tam_f/4)*2, tam_f], COLOR['Negro'], 50)
			dibujarTexto(text, text_pos, FUENTES['Inc-R '+str(tam_f)], COLOR['Gris'])	# Dibuja texto en Pantalla.
			
			# Usuario: =================================================
			text_color = VERDE_C if login_pos == 1 else VERDE
			text = 'Usuario:'
			text_pos = [
				RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118,
				RESOLUCION[s_res][1]//3
			]
			dibujarTexto(text, text_pos, FUENTES['Inc-R '+str(tam_f)], text_color)	# Dibuja texto en Pantalla.
			rect_pos1 = [
				text_pos[0],
				text_pos[1] + 25,
				(int(len(text)*tam_f/4) + 118) * 2, 30
			]
			round_rect(screen, rect_pos1, COLOR['VF'], 3, 1, (*COLOR['VS'], 50))
			# ==========================================================
			
			# Boton Lista Usuarios =====================================
			rect_pos_user_list = [ rect_pos1[0]+rect_pos1[2] + 20, rect_pos1[1], 30, 30 ]
			rect_pos_user_list_line = [ 
				[ rect_pos_user_list[0]+5,  rect_pos_user_list[1]+10 ],
				[ rect_pos_user_list[0]+15, rect_pos_user_list[1]+20 ],
				[ rect_pos_user_list[0]+25, rect_pos_user_list[1]+10 ],
				[ rect_pos_user_list[0]+15, rect_pos_user_list[1]+20 ],
				[ rect_pos_user_list[0]+5,  rect_pos_user_list[1]+10 ],
				[ rect_pos_user_list[0]+25, rect_pos_user_list[1]+10 ],
			]
			# Recuadro, lista de Usuarios:
			round_rect(screen, rect_pos_user_list, COLOR['VF'], 3, 1, (*COLOR['Negro'], 200))
			pygame.draw.line(screen, COLOR['Gris'], rect_pos_user_list_line[0], rect_pos_user_list_line[1], 2)
			pygame.draw.line(screen, COLOR['Gris'], rect_pos_user_list_line[2], rect_pos_user_list_line[3], 2)
			pygame.draw.line(screen, COLOR['Gris'], rect_pos_user_list_line[4], rect_pos_user_list_line[5], 1)
			
			if login_list_active:
				if login_list:
					temp = 0
					for u, p in login_list:
						u = len(u)
						if u > temp: temp = u
					rect_ul = [
						(RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118) + ((int(len(text)*tam_f/4) + 118) * 2) + 50,
						RESOLUCION[s_res][1]//3 + 25,
						(int(temp*tam_f/2)+30), 30
					]
					login_rect_user_list = []
					for i, (user, passwd) in enumerate(login_list):
						rect_temp = [rect_ul[0]+2, rect_ul[1]+(30*i), rect_ul[2], rect_ul[3]-2]
						login_rect_user_list.append((user, passwd, rect_temp))
						round_rect(screen, rect_temp, COLOR['VF'], 3, 1, (*COLOR['Negro'], 200))
						dibujarTexto(user, [rect_ul[0]+15, rect_ul[1] + 5 + (30 * i)], FUENTES['Inc-R '+str(tam_f)], VERDE_C)	# Dibuja texto en Pantalla.
				else:
					temp = 'No hay usuarios registrados...'
					rect_ul = [
						(RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118) + ((int(len(text)*tam_f/4) + 118) * 2) + 50,
						 RESOLUCION[s_res][1]//3 + 25,
						(int(len(temp)*tam_f/2)+30), 30
					]
					round_rect(screen, rect_ul, COLOR['VF'], 3, 1, (*COLOR['Negro'], 100))
					dibujarTexto(temp, [rect_ul[0]+15, rect_ul[1] + 5], FUENTES['Inc-R '+str(tam_f)], VERDE_C)	# Dibuja texto en Pantalla.
			# ==========================================================
			
			# Password: ================================================
			text_color = VERDE_C if login_pos == 2 and not login and not login_new else VERDE
			text2 = 'Contraseña:'
			text_pos = [
				RESOLUCION[s_res][0]//2 - int(len(text)*tam_f/4) - 118,
				RESOLUCION[s_res][1]//3 + 70
			]
			dibujarTexto(text2, text_pos, FUENTES['Inc-R '+str(tam_f)], text_color)	# Dibuja texto en Pantalla.
			rect_pos2 = [
				text_pos[0],
				text_pos[1] + 25,
				(int(len(text)*tam_f/4) + 118) * 2, 30
			]
			round_rect(screen, rect_pos2, COLOR['VF'], 3, 1, (*COLOR['VS'], 50))
			# ==========================================================
			
			# Boton Mostrar/Ocultar Password ===========================
			rect_pos_show_pass = [ rect_pos2[0]+rect_pos2[2] + 20, rect_pos2[1], 30, 30 ]
			temp = 150 if not login_show_pass else 200
			round_rect(screen, rect_pos_show_pass, COLOR['VF'], 3, 1, (*COLOR['Verde'], temp))
			screen.blit(btn_show_pass.image, rect_pos_show_pass)
			rect_pos_show_pass_line = [
				[ rect_pos_show_pass[0]+24, rect_pos_show_pass[1]+5  ],
				[ rect_pos_show_pass[0]+5,  rect_pos_show_pass[1]+24 ]
			]
			if not login_show_pass:
				pygame.draw.line(screen, COLOR['Negro'], rect_pos_show_pass_line[0], rect_pos_show_pass_line[1], 3)
			# ==========================================================
			
			tam_f = 18
			
			if not login:
				pos = int(p_pos*((tam_f)/2))
				rect_pos = rect_pos1 if login_pos == 1 else rect_pos2
				temp = [[rect_pos[0]+6+pos, rect_pos[1]+4], [rect_pos[0]+6+pos, rect_pos[1]+25]]
				temp2 = [rect_pos[0]+5, rect_pos[1]+5]
				if ticks < 30 and not login_new: pygame.draw.line(screen, COLOR['Verde'], temp[0], temp[1], 2)		# Dibuja el puntero en pantalla.
				if not login_show_pass and login_pos == 2:
					dibujarTexto('*'*len(Comando), temp2, FUENTES['Inc-R '+str(tam_f)], VERDE)	# Dibuja texto en Pantalla.
				else:
					dibujarTexto(Comando, temp2, FUENTES['Inc-R '+str(tam_f)], VERDE)	# Dibuja texto en Pantalla.
			
			# Dibuja en Pantalla el Usuario si ya se agrego el texto.
			if username and login_pos == 2 or login or login_new:
				dibujarTexto(username, [rect_pos1[0]+5, rect_pos1[1]+5], FUENTES['Inc-R '+str(tam_f)], COLOR['VF'])	# Dibuja texto en Pantalla.
			if password and login_pos == 1 or login or login_new:
				if not login_show_pass:
					dibujarTexto('*'*len(password), [rect_pos2[0]+5, rect_pos2[1]+5], FUENTES['Inc-R '+str(tam_f)], COLOR['VF'])	# Dibuja texto en Pantalla.
				else:
					dibujarTexto(password, [rect_pos2[0]+5, rect_pos2[1]+5], FUENTES['Inc-R '+str(tam_f)], COLOR['VF'])	# Dibuja texto en Pantalla.
			
			if login_error:
				text = 'Contraseña Incorrecta'
				carga_pos  = [RESOLUCION[s_res][0]//2-int(len(text)*(tam_f)/4), (RESOLUCION[s_res][1]//2)+10]
				carga_pos2 = [carga_pos[0]-5, carga_pos[1]-5, int(len(text)*(tam_f)/4)*2 + 15, 30]
				rect_opaco(screen, carga_pos2, COLOR['Rojo'], 120)
				dibujarTexto(text, carga_pos, FUENTES['Inc-R 18'], COLOR['Blanco'])	# Dibuja texto en Pantalla.
				if temporizer(1.5): login_error = False
			elif login_new:
				rect_pos_login_new = [ RESOLUCION[s_res][0]//2 - 150, int((RESOLUCION[s_res][1]//2)+40), 300, 160 ]
				round_rect(screen, rect_pos_login_new, COLOR['VF'], 3, 1, (*COLOR['VS'], 100))
				texto1 = 'No existe el usuario'
				texto2 = 'Desea crearlo?'
				texto3 = 'Cancelar'
				texto4 = 'Aceptar'
				dibujarTexto(texto1,   [RESOLUCION[s_res][0]//2 - int(len(texto1)*(tam_f)/4),   rect_pos_login_new[1]+15], FUENTES['Inc-R 18'], COLOR['Gris'])	# Dibuja texto en Pantalla.
				dibujarTexto(username, [RESOLUCION[s_res][0]//2 - int(len(username)*(tam_f)/4), rect_pos_login_new[1]+45], FUENTES['Inc-R 18'], COLOR['Blanco'])	# Dibuja texto en Pantalla.
				dibujarTexto(texto2,   [RESOLUCION[s_res][0]//2 - int(len(texto2)*(tam_f)/4),   rect_pos_login_new[1]+75], FUENTES['Inc-R 18'], COLOR['Gris'])	# Dibuja texto en Pantalla.
				# Botones Cancelar y Aceptar:
				rect_pos_btn_cancel = [RESOLUCION[s_res][0]//2 - 130, int((RESOLUCION[s_res][1]//2)+150), 100, 30]
				rect_pos_btn_accept = [RESOLUCION[s_res][0]//2 + 30, int((RESOLUCION[s_res][1]//2)+150), 100, 30]
				color1 = COLOR['Verde'] if login_btn_pos == 2 else COLOR['Verde Claro']
				color2 = COLOR['Verde Claro'] if login_btn_pos == 2 else COLOR['Verde']
				dibujarTexto(texto3, [ rect_pos_btn_cancel[0]+15, rect_pos_btn_cancel[1]+5 ], FUENTES['Inc-R 18'], color1)	# Dibuja texto en Pantalla.
				dibujarTexto(texto4, [ rect_pos_btn_accept[0]+20, rect_pos_btn_accept[1]+5 ], FUENTES['Inc-R 18'], color2)	# Dibuja texto en Pantalla.
				round_rect(screen, rect_pos_btn_cancel, COLOR['VF'], 3, 1, (*COLOR['Verde'], 100))
				round_rect(screen, rect_pos_btn_accept, COLOR['VF'], 3, 1, (*COLOR['Verde'], 100))
				
			# Conecta la cuenta:
			if username and password and not login_carga and login:
				console = None
				console = Console(username, password, 'Odin.Dis_'+__version__)
				threading.Thread(target=dbConnectionThread).start()
				login_carga = True
			
			if login_carga:
				# ~ tam_f = 16
				temp = ' .'*(ticks//19)
				text = 'Cargando'
				carga_pos  = [RESOLUCION[s_res][0]//2-int(len(text+' '*6)*tam_f/4)-5, RESOLUCION[s_res][1]//2-10]
				carga_pos2 = [carga_pos[0]-5, carga_pos[1]-5, int(len(text)*tam_f/4)*4+10, 30]
				rect_opaco(screen, carga_pos2, COLOR['Negro'])
				dibujarTexto(text+temp, carga_pos, FUENTES['Inc-R 18'], COLOR['Gris'])	# Dibuja texto en Pantalla.
				if temporizer(2) and db_con_thread_finish:
					vista_actual = l_vistas['Consola']					# Vista Actual.
					Comando = ''
					p_pos = 0
					db_con_thread_finish = False
		else:
			
			# Logica de Linea de Comandos
			if vista_actual == l_vistas['Consola']:
				if k_down:
					if not (k_wait > 0 and k_wait < 30) \
					and len(Comando) > 0 and p_pos < pos_limit:
						
						if (k_wait % T_rep) == 0 and Comando[-1] in CARACTERES:
							if k_back:
								if p_pos > 0:
									Comando = Comando[:p_pos-1]+Comando[p_pos:]
									p_pos -= 1
							elif k_del:
								if p_pos < len(Comando):
									Comando = Comando[:p_pos]+Comando[p_pos+1:]
							elif k_izq:
								if p_pos > 0: p_pos -= 1
							elif k_der:
								if p_pos < len(Comando): p_pos += 1
							elif k_aba and (k_wait % (T_rep*2)) == 0:
								if cache_pos > 0: cache_pos -= 1
								if cache_com[cache_pos] == '' and not cache_pos == 0:
									cache_com.pop(cache_pos)
									cache_pos -= 1
								Comando = cache_com[cache_pos]
								p_pos = len(Comando)
							elif k_arr and (k_wait % (T_rep*2)) == 0:		# <---- <---- <---- <---- <---- <---- <---- Pendiente, revisar, poner pocos caracteres, llenar 1 a tope, agregar otros pocos y probar.
								if cache_pos < len(cache_com)-1: cache_pos += 1
								if cache_com[cache_pos] == '': cache_com.pop(cache_pos)
								Comando = cache_com[cache_pos]
								p_pos = len(Comando)
							else:
								if k_char:						# Mientras se este presionado una letra, un numero o un espacio, se seguira agregando caracteres.
									if len(Comando) < pos_limit:
										Comando = Comando[:p_pos] + Comando[p_pos-1] + Comando[p_pos:]
										p_pos += 1
					
					k_wait += 1
			
			# Aumento de volumen, cuando se deja presionado
			if k_down:
				# Se espera 3/4 de segundo.
				if not (k_wait > 0 and k_wait < 45) \
				and (song_vol_pres_min or song_vol_pres_plus) \
				and (song_vol > 0 and song_vol < 100):
					
					if k_wait % 2 == 0:
						
						if song_vol_pres_min: song_vol -= 1
						elif song_vol_pres_plus: song_vol += 1
						
						s_song_vol = True
						s_song_vol_ticks = 0
						
						music.set_volume(song_vol/100)
					
				k_wait += 1
			
			#=====================================================================================================================================================
			#=====================================================================================================================================================
			#=====================================================================================================================================================
			
			screen.blit(BGimg_General, (0, 0))	# Se Carga La Imagen De Fondo.
			
			#===================================================================================================
			#===================================================================================================
			#===================================================================================================
			
			if not s_full:	# Dibuja un margen en la pantalla.
				pygame.draw.rect(screen, VERDE,  [0, 0, RESOLUCION[s_res][0], RESOLUCION[s_res][1]], 1)	# Margen de Pantalla.
			
			#===================================================================================================
			# Dibujar Iconos
			
			for i, btn in enumerate(l_icons):
				
				i  += 1
				i_y = 10
				d   = 4
				dd  = d*2
				
				if i > 10:
					i_y += btn_y + dd + 4
					i=i%10
				
				i_x = RESOLUCION[s_res][0]-btn_x*i-12*i
				
				rect_opaco(screen, [i_x-d, i_y-d, btn_x+dd, btn_y+dd], AZUL_C, 220)
				pygame.draw.rect(screen, AZUL,           [i_x-d,   i_y-d,   btn_x+dd,   btn_y+dd],   3)			# Recuadro de Icono.
				pygame.draw.rect(screen, AZUL_C,         [i_x-d,   i_y-d,   btn_x+dd,   btn_y+dd],   1)			# Recuadro de Icono.
				pygame.draw.rect(screen, COLOR['Negro'], [i_x-1-d, i_y-1-d, btn_x+2+dd, btn_y+2+dd], 1)			# Recuadro de Icono.
				btn_pos = ( i_x, i_y )
				# ~ btn.resize(btn_x, btn_y)
				screen.blit(btn.image, btn_pos)
			
			#===================================================================================================
			
			if vista_actual == l_vistas['Consola']:
				
				rect_opaco(screen, t_con)							# Ventana de Consola.
				
				# ~ pygame.draw.rect(screen, COLOR['Negro'], t_con, 0)	# Ventana de Consola.
				pygame.draw.rect(screen, VERDE, t_con, 2)			# Margen de Consola.
				pygame.draw.rect(screen, VERDE, l_con, 1)			# Dibuja linea de Consola.
				
				if p_pos > pos_limit: p_pos = pos_limit
				
				p_puntero = u_puntero(con, l_con, len(Prefijo), p_pos)
				
				if ticks < 30: pygame.draw.line(screen, COLOR['Gris'], p_puntero[0], p_puntero[1], 2)		# Dibuja el puntero en pantalla.
				
				temp_y, temp_x = t_con[1], t_con[2]
				temp = console.sysname
				dibujarTexto(temp, [temp_x-(len(temp)*6), temp_y+2], FUENTES['Inc-R 12'], VERDE_C)
				
				#===================================================================================================
					
				# Si se activa un Comando Lo Ejecuta.
				if exe:
					if console.validate(Comando):
						
						textos = console.execute(Comando)
						
						if textos == None:
							temp_pos = l_comandos.pop()[1]
							l_comandos.append((Prefijo+' '+Comando, temp_pos))
							textos = []
						
						temp = textos[:]
						for x in temp:							# Aplica los saltos de linea '\n' que esten en el texto.
							if x == '' or x == 0: continue
							else:
								temp = x.split('\n')
								if len(temp) > 1:
									textos = temp
						
						temp = textos[:]
						for i, x in enumerate(temp):			# Aplica salto de linea al desbordar la ventana.
							if x == '' or x == 0: continue
							else:
								sT = splitText(x)
								t1 = textos[:i]
								t1.extend(sT)
								t1.extend(textos[i+1:])
								textos = t1
								break
						
						l_comandos = add_comand(l_comandos, textos)
						
						if Comando == 'exit':
							
							# ~ threading.Thread(target=saveThread).start()
							
							temp = [
								str(l_canciones_activas), str(l_comandos),
								str(l_com_ps), str(con_tam_buffer)
							]
							
							db = Database(DBName)
							db.updateUserConfig(console.username, temp)
							db.con.commit()
							db.con.close()
							
							vista_actual = l_vistas['Login']
							
							l_canciones_activas = []
							
							segundos   = 0			# Contador de Tiempo, 1 seg por cada 60 Ticks.
							ticks      = 0			# Contador de Ticks.
							Comando    = ''			# Comando en linea actual.
							l_comandos = []			# Lista de comandos ejecutados.
							l_com_ps   = 0			# Poicion actual de lista de comandos ejecutados mostrados, 0 equivale a los mas recientes.
							p_pos      = 0			# Posicion del Puntero, para manipular en que posicion estara en la cadena 'Comando'. p_pos = 5 significaria entonces que estara el puntero en el caracter 5.
							
							# Booleanos:
							c_res   = False			# Cambio de Resolucion.
							
							s_full_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
							s_shot_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
							s_song_vol_ticks = 0			# Indica el tiempo en ticks que se mostrara un texto.
							
							# Cache de comandos para las teclas de Flecha Arriba y Abajo.
							cache_com = []
							cache_pos = 0
							
							#===================================================================
							# Variables de la Musica:
							song_stop          = False
							song_fade_ticks    = 0
							song_desface       = 0
							
							#===================================================================
							# Login Data:
							console_name = 'Odin.Dis_'+__version__
							username    = ''
							password    = ''
							login_pos   = 1
							login_vista = 0
							login_list_active = False
							login_show_pass = False
							login_carga = False
							login_list = []
							login = False
							
						elif Comando == 'cls':  l_comandos = []
						elif Comando == 'save': save_game = True
						elif Comando.split(' ')[0] == 'cd':
							Prefijo = console.actualPath() + ' '											# Actualiza el Path
							pos_limit = ( RESOLUCION_CMD[s_res][0]-30 - (len(Prefijo)*(T_pix))) // T_pix	# Limite de letras en linea de comandos.
					
					Comando = ''
					exe = False
					l_comandos = l_comandos[con_tam_buffer*-1:]
				
				#===================================================================================================
				
				# limita la cantidad de lineas que se mostraran en consola.
				if l_com_ps > 0:
					temp = l_comandos[-l_com_lim-l_com_ps:(l_com_ps*-1)]
				else:
					temp = l_comandos[-l_com_lim:]
				
				#===================================================================================================
				# Mostrara texto en consola. Rojo si no es valido o Verde si es correcto.
				
				error = ': No es un Comando Valido.'
				
				for i, (com, pos) in enumerate(temp):	# Dibuja la lista de comandos ejecutados.
					
					p_texto = [ l_con[0]+5, l_con[1] - ((len(temp)-i)*T_pix_y) -2 ]		# Posicion del texto.
					
					if not com[-2:] == '> ':
						
						if com: valid = console.validate(com.split(' ')[1])		# Si el comando es valido sera igual a True.
						else: valid = True										# Si la linea esta vacia '' en automatico sera True.
						
						# Validamos que sea un comando valido y que sus lineas correspondientes tambien se muestren como validas.
						temp_col = VERDE_C if (valid or com[0] == ' ') else COLOR['Rojo Claro']
						
						if com[:17] == 'Faltan Argumentos' or com[:3] == 'No ': pass
						elif valid or com[0] == ' ': pass
						elif len(com+error) <= pos_limit+len(Prefijo)+1:
							com = com+error
						else:
							com = com[:(pos_limit+len(Prefijo)-len(error)-2)]+'...'+error
						
						try:
							if com.split(' ')[0][-1] == '>':
								recuadro = [p_texto[0]-5, p_texto[1]+2, RESOLUCION_CMD[s_res][0]-20, 13 ]
								rect_opaco(screen, recuadro, COLOR['VS'])
								pygame.draw.rect(screen, COLOR['VN'], recuadro, 1)
						except:
							pass
					else:
						temp_col = VERDE_C
						recuadro = [p_texto[0]-5, p_texto[1]+2, RESOLUCION_CMD[s_res][0]-20, 13 ]
						rect_opaco(screen, recuadro, COLOR['VS'])
						pygame.draw.rect(screen, COLOR['VN'], recuadro, 1)
					
					dibujarTexto(com, p_texto, FUENTES[Font_def], temp_col)			# Imprime el texto en consola.
					
				#===================================================================================================
				# Dibuja el texto en la linea de comandos
				dibujarTexto(Prefijo+Comando[:pos_limit_r-len(Prefijo)+1], p_letra, FUENTES[Font_def], VERDE_C)	# Dibuja lo que vas escribiendo.
				#===================================================================================================
			
			#===================================================================================================
			
			elif vista_actual == l_vistas['Ajustes']:
				
				# Dibuja los textos en pantalla.
				
				#======================================================================================================================
				# Mitad Izquierda.
				#======================================================================================================================
				
				#======================================================================================================================
				# Recuadro: Mitad Izquierda. Musica.
				ajust_pos_y = 3
				# ~ recuadro  = [ajust_init_x, ajust_init_y*ajust_pos_y, RESOLUCION_CMD[s_res][0]-160, RESOLUCION_CMD[s_res][1]-180]
				recuadro  = [ajust_init_x, ajust_init_y*ajust_pos_y, 540, RESOLUCION_CMD[s_res][1]-180]
				rect_opaco(screen, recuadro, COLOR['VS'])
				pygame.draw.rect(screen, VERDE, recuadro, 1)
				
				# Recuadro sobre texto principal
				ajust_pos_y += 1
				recuadro2 = [recuadro[0]+15, recuadro[1]+10, 290, 20]
				rect_opaco(screen, recuadro2, COLOR['VS'])
				pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
				dibujarTexto('Lista de Canciones Disponibles:', [recuadro[0]+20, 40*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
				
				# Todas las canciones disponibles:
				ljust = 45
				combinaciones = [
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
				ajust_pos_y += 1
				# Dibuja en pantalla cada uno de los textos, con un recuadro ajustado a la linea de texto.
				for i, comb in enumerate(combinaciones):
					if i == 1: ajust_pos_y += 1
						
					ajust_pos_y += 1
					if len(comb) > 64:
						# ~ recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, RESOLUCION_CMD[s_res][0]-200, 45]
						recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, 500, 45]
						rect_opaco(screen, recuadro2, COLOR['VS'])
						pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
						comb_p1 = '_'
						comb_pos = 64
						while comb_p1[:comb_pos][-1] != ' ':
							comb_pos -= 1
							comb_p1 = comb[:comb_pos]
						comb_p2 = ' '*(len(comb_p1.split(':')[0])+2)+comb[comb_pos:]
						dibujarTexto(comb_p1, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
						ajust_pos_y += 1
						dibujarTexto(comb_p2, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
					else:
						# ~ recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, RESOLUCION_CMD[s_res][0]-200, 20]
						recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, 500, 20]
						rect_opaco(screen, recuadro2, COLOR['VS'])
						pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
						dibujarTexto(comb, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
					
					if i >= 1:
						# Imprime recuadro de checkbox:
						clic_music_checkbox(evento, recuadro[0]+30, 50+25*ajust_pos_y, i-1)
				#======================================================================================================================
				
				#======================================================================================================================
				# Resolucion Actual
				ajust_pos_y = 2
				texto = 'Resolución: '
				rect_opaco(screen, [ajust_init_x, ajust_init_y*ajust_pos_y, 210, ajust_v_tamY-10], COLOR['VS'])						# Color de Fondo a Resolucion de Consola actual.
				pygame.draw.rect(screen, VERDE, [ajust_init_x, ajust_init_y*ajust_pos_y, 210, ajust_v_tamY-10], 1)							# Contorno a Resolucion de Consola actual.
				dibujarTexto(texto+(str(RESOLUCION[s_res][0])+'x'+str(RESOLUCION[s_res][1])).rjust(9),
								[ajust_init_x+10, ajust_init_y*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)									# Resolucion de Consola actual.
				
				if c_res:
					
					rect_opaco(screen, [ajust_init_x+110, ajust_init_y*ajust_pos_y-5, ajust_v_tamX-5, 30*len(RESOLUCION)], COLOR['VN'])		# Color de Fondo de Ventana de Resolucion.
					pygame.draw.rect(screen, VERDE, [ajust_init_x+110, ajust_init_y*ajust_pos_y-5, ajust_v_tamX-5, 30*len(RESOLUCION)], 1)			# Contorno de Ventana de Resolucion.
					
					for i in range(1, len(RESOLUCION)):
						rect_opaco(screen, [ajust_init_x+115, ajust_init_y*ajust_pos_y+(ajust_v_tamY*i), ajust_v_tamX-15, 20], COLOR['VN'])		# Color de Fondo de Ventana de Resolucion.
						pygame.draw.rect(screen, VERDE, [ajust_init_x+115, ajust_init_y*ajust_pos_y+(ajust_v_tamY*i), ajust_v_tamX-15, 20], 1)		# Recuedro individual de cada Resolucion de Consola.
						temp_texto = str(RESOLUCION[(s_res+i)%len(RESOLUCION)][0])+'x'
						temp_texto += str(RESOLUCION[(s_res+i)%len(RESOLUCION)][1])
						temp_texto = temp_texto.rjust(9)
						dibujarTexto(temp_texto, [ajust_init_x+120, ajust_init_y*ajust_pos_y+(ajust_v_tamY*i)], FUENTES['Inc-R 18'], VERDE_C)		# Imprime el texto.
				#===================================================================================================
				
				#======================================================================================================================
				# Tiempo Transcurrido:
				ajust_pos_y = 1
				recuadro  = [ajust_init_x, ajust_init_y*ajust_pos_y, 275, 20]
				contenido = [recuadro[0]+5, recuadro[1]]
				rect_opaco(screen, recuadro, COLOR['VN'])
				pygame.draw.rect(screen, VERDE, recuadro, 1)
				dibujarTexto('Tiempo Transcurrido: '+normalizeTime(segundos*1000), contenido, FUENTES['Inc-R 18'], VERDE_C)
				#======================================================================================================================
				
				#======================================================================================================================
				# Mitad Derecha.
				#======================================================================================================================
				
				plus_der = 600
				
				#======================================================================================================================
				# Desplazamiento de Scroll:
				ajust_pos_y = 2
				recuadro  = [ajust_init_x+plus_der, ajust_init_y*ajust_pos_y, 335, 20]
				contenido = [recuadro[0]+5, recuadro[1]]
				rect_opaco(screen, recuadro, COLOR['VN'])
				pygame.draw.rect(screen, VERDE, recuadro, 1)
				dibujarTexto('Cantidad de Desplante de Scroll: '+str(cant_scroll), contenido, FUENTES['Inc-R 18'], VERDE_C)
				#======================================================================================================================
				
				#======================================================================================================================
				# Tamanio de Buffer:
				ajust_pos_y = 1
				recuadro  = [ajust_init_x+plus_der, ajust_init_y*ajust_pos_y, 335, 20]
				contenido = [recuadro[0]+5, recuadro[1]]
				rect_opaco(screen, recuadro, COLOR['VN'])
				pygame.draw.rect(screen, VERDE, recuadro, 1)
				dibujarTexto('Tamaño de Buffer de la Terminal: '+str(con_tam_buffer), contenido, FUENTES['Inc-R 18'], VERDE_C)
				#======================================================================================================================
				
			#===================================================================================================
			
			elif vista_actual == l_vistas['Atajos']:
				
				# Dibuja los textos en pantalla.
				#======================================================================================================================
				# Combinaciones de Teclas:
				
				# Recuadro General: Mitad Izquierda.
				ajust_pos_y = 1
				recuadro  = [ajust_init_x, ajust_init_y*ajust_pos_y, RESOLUCION_CMD[s_res][0]-30, RESOLUCION_CMD[s_res][1]-80]
				rect_opaco(screen, recuadro, COLOR['VS'])
				pygame.draw.rect(screen, VERDE, recuadro, 1)
				
				# Recuadro sobre texto principal
				ajust_pos_y += 1
				recuadro2 = [recuadro[0]+15, 80, 225, 20]
				rect_opaco(screen, recuadro2, COLOR['VS'])
				pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
				dibujarTexto('Combinaciones de Teclas:', [recuadro[0]+20, 40*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
				
				# Todas las combinaciones posibles de Teclas:
				combinaciones = [
							'Esc: Para Cerrar el Juego.',
							'F10: Captura de Pantalla.',
							'F11: Poner/Quitar Pantalla Completa.',
							'Ctrl + F: Poner/Quitar Pantalla Completa.',
							'Ctrl + P: Captura de Pantalla.',
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
				
				# Dibuja en pantalla cada uno de los textos, con un recuadro ajustado a la linea de texto.
				for comb in combinaciones:
					ajust_pos_y += 1
					if len(comb) > 64:
						recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, RESOLUCION_CMD[s_res][0]-70, 45]
						rect_opaco(screen, recuadro2, COLOR['VS'])
						pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
						comb_p1 = '_'
						comb_pos = 64
						while comb_p1[:comb_pos][-1] != ' ':
							comb_pos -= 1
							comb_p1 = comb[:comb_pos]
						comb_p2 = ' '*(len(comb_p1.split(':')[0])+2)+comb[comb_pos:]
						dibujarTexto(comb_p1, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
						ajust_pos_y += 1
						dibujarTexto(comb_p2, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
					else:
						recuadro2 = [recuadro[0]+30, 50+25*ajust_pos_y, RESOLUCION_CMD[s_res][0]-70, 20]
						rect_opaco(screen, recuadro2, COLOR['VS'])
						pygame.draw.rect(screen, COLOR['VN'], recuadro2, 1)
						dibujarTexto(comb, [recuadro[0]+40, 50+25*ajust_pos_y], FUENTES['Inc-R 18'], VERDE_C)
				
				#======================================================================================================================
			
			#===================================================================================================
			
			# Imprimir los Datos de Soundtrack.
			if l_canciones_activas:
				temp = [RESOLUCION[s_res][0]-440, RESOLUCION[s_res][1]-23, 435, 19]
				rect_opaco(screen, temp, COLOR['Negro'], 125)
				song_data = playlist[song_pos][2]['By']+' - '+playlist[song_pos][2]['Song']
				song_data = song_data.rjust(40)
				temp = song_time[3:] if not song_time[3:] == '59:59' else '00:00'
				dibujarTexto(song_data+'    Transcurrido: '+ temp + ' - ' + playlist[song_pos][2]['Duration'][3:],
					[RESOLUCION[s_res][0]-440, RESOLUCION[s_res][1]-20], FUENTES['Inc-R 12'], COLOR['Verde Claro'])
			else:
				temp = [RESOLUCION[s_res][0]-440, RESOLUCION[s_res][1]-23, 435, 19]
				rect_opaco(screen, temp, COLOR['Negro'], 125)
				song_data = ' - '
				song_data = song_data.rjust(40)
				dibujarTexto(song_data+'    Transcurrido: 00:00 - 00:00',
					[RESOLUCION[s_res][0]-440, RESOLUCION[s_res][1]-20], FUENTES['Inc-R 12'], COLOR['Verde Claro'])
			#===================================================================================================
			
			# Si se cambia de cancion: Esto es para hacer efecto de Fadeout, el sonido disminuye lentamente.
			if song_change_down or song_change_up:
				
				if song_fade_ticks == 60*song_fade_secs:
					music.stop()
					music.load(playlist[song_pos][0])
					music.play()
					song_fade_ticks = 0
					song_change_down = False
					song_change_up = False
				
				song_fade_ticks += 1
			
			# Dibuja en Pantalla un mensaje cuando se pone en pantalla completa.
			elif s_full and s_full_ticks < 300:
				if s_fullF:
					s_full_ticks = dibujarTextoTemporal(s_full_ticks, 'No Puedes Salir de Pantalla Completa Con la Resolucion Máxima', 300, False)
					if s_full_ticks == 0:
						s_fullF = False
				else:
					s_full_ticks = dibujarTextoTemporal(s_full_ticks, 'Presione Ctrl+F o F11 Para Salir de Pantalla Completa', 300, False)
			
			# Dibuja en Pantalla un mensaje cuando se modifica el volumen.
			elif s_song_vol:
				s_song_vol_ticks = dibujarTextoTemporal(s_song_vol_ticks, 'Volumen: '+str(song_vol)+'%'+(' Mute' if song_vol == 0 else ''), 50)
				if s_song_vol_ticks == 0:
					s_song_vol = False
			
			#===================================================================================================
			#===================================================================================================
			#===================================================================================================
			
			# Actualiza la Base de Datos
			# ~ if segundos % 300 == 0 and ticks == 0:
				# ~ threading.Thread(target=saveThread).start()
			
			if game_over or save_game or (segundos % 60 == 0 and ticks == 0):
				# Ejemplo de Hilos:
				# ~ x = threading.Thread(target=thread_function, args=(1,2,))
				# ~ x.start()
				threading.Thread(target=saveThread).start()
				save_game = False
		
		# Dibuja en Pantalla un mensaje cuando se toma una Captura.
		if s_shot:
			s_shot_ticks = dibujarTextoTemporal(s_shot_ticks, 'Captura de Pantalla', 77)
			if s_shot_ticks == 0:
				s_shot = False
		
		if ticks == 60:
			segundos = getGlobalTime(1)		# Devuelve tiempo en SS.
			ticks = 0
		
		pygame.display.flip()		# Actualiza Los Datos En La Interfaz.
		clock.tick(60)
	
	pygame.quit()

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

# Constantes Globales: =================================================
FUENTES = {}

COLOR  = {
		  'Blanco':   (255, 255, 255), 'Negro':       (  0,   0,   0),
		  'Gris':     (189, 189, 189), 'Gris Claro':  (216, 216, 216),
		  'Rojo':     (255,   0,   0), 'Rojo Claro':  (255,  50,  50),
		  'Verde':    (  4, 180,   4), 'Verde Claro': (  0, 255,   0),
		  'Azul':     ( 20,  80, 240), 'Azul Claro':  ( 40, 210, 250),
		  'VS':       ( 24,  25,  30), 'VN':          (  0,  50,  30),
		  'VC':       (  0,  75,  30), 'VF':          (  0, 100,  30),
		  'Amarillo': (255, 255,   0), 'Naranja':     (255, 120,   0),
		  'Morado':   ( 76,  11,  95), 'Purpura':     ( 56,  11,  97)
		 }	# Diccionario de Colores.

resoluciones = [
		# ~ ( 720,  480),	# 480p. Tamaño de La Ventana, Ancho (640) y Alto  (480).
		(1280,  720),	# 720p
		(1366,  768),
		(1600,  900),	# 1080p Escalado 125%
		(1920, 1080)	# 1080p
		#(2560, 1600)	# Resolucion Maxima, Este es el tamaño Original de la imagen del Fondo.
	]

RESOLUCION = []
size = get_screen_size()

for i, (x, y) in enumerate(resoluciones):
	if size[0] > x and size[1] > y:
		RESOLUCION.append(resoluciones[i])

if size <= resoluciones[-1]: RESOLUCION.append(size)

px = .5
py = 1

RESOLUCION_CMD = [	
		(int(RESOLUCION[i][0]*px), int(RESOLUCION[i][1]*py))
		for i in range(len(RESOLUCION))
	]

# Esta es la lista de caracteres que permiten ser multiplicados al dejar la tecla presionada.
CARACTERES  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz'
CARACTERES += '1234567890' + 'º\'¡+ç,.-<' + 'ª!"·$%&/()=?¿*Ç;:_>'
CARACTERES += '\\|@#~€¬[]{} '

LOGIN_CARACTERES  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOGIN_CARACTERES += 'abcdefghijklmnopqrstuvwxyz'
LOGIN_CARACTERES += '1234567890' + '-_'

s_res     = -2								# Seleccion de Resolucion Por defecto. -2: la penultima Resolucion agregada.
T_pix     = 7								# Tamaño de Pixeles entre cada letra en linea de comandos.
T_pix_y   = T_pix*2							# Tamaño de Pixeles entre cada salto de linea en la linea de comandos.
T_rep     = 3								# Tiempo de repeticion entre caracteres al dejar tecla presionada.
Font_tam  = 14								# Para hacer manipulación del tamaño de algunos textos en pantalla.
Font_def  = 'Inc-R '+str(Font_tam)			# Fuente por defecto y tamaño de Fuente.

l_vistas = {
	'Login':   0,
	'Consola': 1,
	'Ajustes': 2,
	'Atajos':  3,
}

DBName = 'odin/dystopia.odin'

# Variables Globales: ==================================================

screen = None				# Objeto Que Crea La Ventana.
btn_x, btn_y = 40, 40		# Proporciones de los botones.
l_comandos = []
l_canciones_activas = []
music_checkbox_down = False
global_time_init = 0
temporizer_init = 0
db_con_thread_finish = False

l_comandos = []			# Lista de comandos ejecutados.
l_com_ps   = 0			# Poicion actual de lista de comandos ejecutados mostrados, 0 equivale a los mas recientes.
con_tam_buffer = 150	# Tamanio de buffer de consola.


db = None									# Conexion a la Base de Datos.
l_com_lim   = None							# Limite de lineas en consola
pos_limit   = 32							# Limite de letras en linea de comandos.
pos_limit_r = None							# Limite Real de letras en linea de comandos. 
console = None
Prefijo = None								# Simbolo de prefijo para comandos.


vista_actual = l_vistas['Login']	# Vista Inicial.

debug = True

# Conecta Direto a Consola:
# ~ console = Console('Eny', 'xD', 'Odin.Dis_'+__version__)
# ~ dbConnectionThread()
# ~ vista_actual = l_vistas['Consola']	# Vista Actual.

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

if __name__ == "__main__":
	
	main()
