

from os import path, mkdir, environ

from consola import Console

import keyboard
import pygame						# python -m pip install pygame
import ctypes

from win32api import GetKeyState	# python -m pip install pywin32
from win32con import VK_CAPITAL		# python -m pip install pywin32

TITULO  = 'Hack Game'
__version__ = 'v1.1.3'

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

class Boton(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Botones.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
		self.x = self.image.get_width()
		self.y = self.image.get_height()
		
	def getSize(self):
		return self.x, self.y
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		self.x = TX
		self.y = TY
		self.image = pygame.transform.scale(self.image, (TX, TY))

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
	for text in textos: l_comandos.append((plus+text, cont))
	return l_comandos

def clic_boton(screen, pos, rec=0):	# Detecta un Clic en las coordenadas de un boton, contando la posicion de botones derecha a izquierda.
	
	x_pos = RESOLUCION[s_res][0]-btn_x-10*(rec+1)-btn_x*rec
	x, y  = pos
	
	if x > x_pos and x < x_pos + btn_x:
		if y > 10 and y < btn_y+10:
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

def printTFiles(t_files):
	
	global l_comandos
	
	if len(l_comandos) > 0:
		cont = l_comandos[-1][1]+1
		l_comandos.append((Prefijo, cont))
	else:
		l_comandos.append((Prefijo, 1))
	
	l_comandos = add_comand(l_comandos, [''] + t_files + [''])

#===================================================================================================
#===================================================================================================
#===================================================================================================

def main():
	
	global screen, s_res, pos_limit, pos_limit_r, l_com_lim, FUENTES, Prefijo, l_comandos
	
	# Inicializaciones =================================================
	
	ss_x, ss_y = get_screen_size()
	s_x = ss_x//2-RESOLUCION[s_res][0]//2
	s_y = ss_y//2-RESOLUCION[s_res][1]//2
	
	# ~ print(ss_x, ss_y, RESOLUCION[s_res], s_x, s_y)
	
	environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(s_x, s_y)
	
	screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
	screen.fill(COLOR['Negro'])									# Rellena el Fondo de Negro.
	
	BGimg  = load_image('images/background.bmp')				# Carga el Fondo de la Ventana.
	BGimg = pygame.transform.scale(BGimg, RESOLUCION[s_res])	# Cambia la resolucion de la imagen.
	
	Icono  = pygame.image.load('images/Icon.png')				# Carga el icono del Juego.
	
	btn_ajustes = Boton('images/Ajustes.bmp')					# Boton de Ajustes.
	btn_consola = Boton('images/Consola.bmp')					# Boton de Consola.
	btn_atajos  = Boton('images/Atajos.bmp')					# Boton de Consola.
	
	l_icons = [btn_ajustes, btn_atajos]							# Lista actual de iconos a imprimir.
	
	pygame.display.set_icon(Icono)								# Agrega el icono a la ventana.
	pygame.display.set_caption(TITULO+' '+__version__)			# Titulo de la Ventana del Juego.
	
	pygame.init()												# Inicia El Juego.
	pygame.mixer.init()											# Inicializa el Mesclador.
	
	FUENTES = {
		   'Inc-R 18':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 18),
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
	
	l_vistas = {
			'Consola': 1,
			'Ajustes': 2
		}
	
	vista_actual = l_vistas['Consola']	# Vista Actual.
	
	game_over = False				# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()		# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	
	segundos = 0		# Contador de Tiempo, 1 seg por cada 60 Ticks.
	ticks    = 0		# Contador de Ticks.
	Comando  = ''		# Comando en linea actual.
	l_comandos = []		# Lista de comandos ejecutados.
	l_com_ps = 0		# Poicion actual de lista de comandos ejecutados mostrados, 0 equivale a los mas recientes.
	p_pos    = 0	# Posicion del Puntero, para manipular en que posicion estara en la cadena 'Comando'. p_pos = 5 significaria entonces que estara el puntero en el caracter 5.
	
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
	
	s_full_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
	s_shot_ticks = 0				# Indica el tiempo en ticks que se mostrara un texto.
	
	# Cache de comandos para las teclas de Flecha Arriba y Abajo.
	cache_com = []
	cache_pos = 0
	
	t_files_ini = ''
	t_files_pos = 0			# Posicion Temporal de Seleccion de Archivo al pulsar TAB.
	
	#===================================================================
	
	# Inicio Del Juego:
	while game_over is False:
		
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
					
					if vista_actual == l_vistas['Consola']:
						
						if clic_boton(screen, evento.pos, 0):
							vista_actual = l_vistas['Ajustes']	# Detecta si se presiono el primer boton.
							l_icons.pop(0)
							l_icons.insert(0, btn_consola)
						
					elif vista_actual == l_vistas['Ajustes']:
						
						if clic_boton(screen, evento.pos, 0):
							vista_actual = l_vistas['Consola']	# Detecta si se presiono el primer boton.
							l_icons.pop(0)
							l_icons.insert(0, btn_ajustes)
						
						v_tamX, v_tamY = 110, 30
						temp_x, temp_y = 25, 60
						
						if x > temp_x and x < temp_x+215:
							
							if y > temp_y and y < temp_y+v_tamY-10: c_res = False if c_res else True
							
							if c_res:
								for i in range(1, len(RESOLUCION)):
									if x > temp_x+115 and x < temp_x+v_tamX+100 \
									and y > temp_y+(v_tamY*i) and y < 20+temp_y+(v_tamY*i):
										s_res = ((s_res+i)%len(RESOLUCION))
										
										if s_full: screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
										else:
											if (ss_x, ss_y) == RESOLUCION[s_res]:
												s_full = True
												screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
												s_full_ticks = 0
											else:
												s_x = ss_x//2-RESOLUCION[s_res][0]//2
												s_y = ss_y//2-RESOLUCION[s_res][1]//2
												environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(s_x, s_y)
												screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
												
										BGimg = load_image('images/background.bmp')											# Carga el Fondo de la Ventana.
										BGimg = pygame.transform.scale(BGimg, RESOLUCION[s_res])							# Cambia la resolucion de la imagen.
										
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
						
				if evento.button == 4:
					if vista_actual == l_vistas['Consola']:
						# Si la posicion en lista de comandos es menor que la cantidad de lineas de comandos
						if l_com_ps < len(l_comandos):
							# Si la cantidad de lineas en lista de comandos es mayor al limite de lineas de comandos en pantalla
							# Y si la suma de posicion + el limite es menor a la cantidad de comandos, significa que por encima hay mas lineas de texto.
							# En resumen, Detecta si hay mas texto por encima 
							if len(l_comandos) > l_com_lim and (l_com_ps + l_com_lim) < len(l_comandos):
								# Y Permite desplazarse hacia arriba linea por linea, hasta que no haya mas encima.
								l_com_ps += 1
					
				elif evento.button == 5:
					if vista_actual == l_vistas['Consola']:
						if l_com_ps > 0:	# Mientras haya lineas debajo permite dezplazarse.
							l_com_ps -= 1
			
			#=================================================================================
			
			elif evento.type == pygame.KEYDOWN:		# Manipulación del Teclado.
				if vista_actual == l_vistas['Consola']:
					# Al presionar cualquier tecla.
					k_down = True
					k_wait = 1
				
				#=================================================================================
				
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				
				#=================================================================================
				# Teclas Bloq Mayus, y las teclas Shift izquerdo y derecho.
				elif evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
				or evento.key == pygame.K_CAPSLOCK:
					if vista_actual == l_vistas['Consola']:
						a_shift = False if a_shift else True
				
				#=================================================================================
				# Felchas de direcciones
				elif evento.key == pygame.K_LEFT:
					if vista_actual == l_vistas['Consola']:
						if p_pos > 0: p_pos -= 1
						k_izq = True
					
				elif evento.key == pygame.K_RIGHT:
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
							# ~ elif cache_com[cache_pos] == '':
								# ~ cache_com.pop(cache_pos)		# Elimina los que sean cadenas vacias.
								# ~ cache_pos -= 1
							
							Comando = cache_com[cache_pos][:pos_limit_r-len(Prefijo)+1]
							p_pos = len(Comando)
							
							# ~ print(cache_com)
					
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
					if vista_actual == l_vistas['Consola']:
						if p_pos > 0:
							Comando = Comando[:p_pos-1]+Comando[p_pos:]
							p_pos  -= 1
							k_back  = True
				
				elif evento.key == pygame.K_DELETE:
					if vista_actual == l_vistas['Consola']:
						if p_pos < len(Comando):
							Comando = Comando[:p_pos]+Comando[p_pos+1:]
							k_del   = True
				
				#=================================================================================
				# Acciones al Presionar ENTER.
				elif evento.key == pygame.K_RETURN:
					if vista_actual == l_vistas['Consola']:
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
				xD = False
				# Ctrl + P o F10 para tomar una Captura de Pantalla.
				if evento.key == pygame.K_p and evento.mod == 64 or evento.key == pygame.K_F10:
					
					s_n = 1
					s_folder = 'screenshots/'
					s_path = s_folder+'screenshot_001.jpg'
					
					if not path.isdir(s_folder): mkdir(s_folder)
					
					while path.exists(s_path):
						s_n += 1
						s_path = s_folder+'screenshot_{}.jpg'.format(str(s_n).zfill(3))
					
					pygame.image.save(screen, s_path)
					
					s_shot_ticks = 0
					s_shot = True
					xD = True
				
				# Ctrl + F o F11 para poner Pantalla Completa.
				elif evento.key == pygame.K_f and evento.mod == 64 or evento.key == pygame.K_F11:
					
					if s_full:
						
						if (ss_x, ss_y) == RESOLUCION[s_res]:
							s_fullF = True
						else:
							screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
							s_x = ss_x//2-RESOLUCION[s_res][0]//2
							s_y = ss_y//2-RESOLUCION[s_res][1]//2
							# ~ print(ss_x, ss_y, s_res, RESOLUCION[s_res], s_x, s_y)
							environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(s_x, s_y)					# <---- <---- <---- <---- <---- <---- <---- Bugs de Resolucion, Cambiar a maxima Resolucion, luego cabiar a cualquier otra y presionar F11, no se ajusta correctamente.
							screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.NOFRAME)			# Objeto Que Crea La Ventana.
							s_full = False
					else:
						screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
						s_full = True
					
					s_full_ticks = 0
					xD = True
				
				#=================================================================================
				# Deteccion de Caracteres En Consola.
				elif evento.unicode == '\t':
					
					if t_files_ini == '' and t_files_pos == 0:
						
						t_files_ini = Comando.split(' ')
						
						if len(t_files_ini) >= 2:
							
							t_files = [ ( (str(x) + ('/' if not '.' in str(x)[-5:] else ''))
								if str(x).startswith(t_files_ini[1]) else '') for x in console.getChilds() ]
							
							while '' in t_files: t_files.remove('')
					
					if len(t_files_ini) >= 2:
						
						if t_files_ini[0] == 'cd':
							
							# Listar Carpetas de Niveles Inferiores.
							#===========================================================
							# ~ t_files_path = Comando.split(' ')[1].split('/')
							# ~ while '' in t_files_path: t_files_path.remove('')
							# ~ print([t_files_path])
							# ~ if type(t_files_path) == list and len(t_files_path) > 1:
								# ~ t_files = []
							#===========================================================
							
							t_files = [ ( x if x.endswith('/') else '' ) for x in t_files ]
							while '' in t_files: t_files.remove('')
							
						elif t_files_ini[0] == 'cat':
							
							t_files = [ ( x if not x.endswith('/') else '' ) for x in t_files ]
							while '' in t_files: t_files.remove('')
						
						if t_files:
							
							if len(t_files) == 1:
								t_name = t_files[t_files_pos]
								if ' ' in t_name:
									Comando = t_files_ini[0] + ' "' + t_name + '"'
								else:
									Comando = t_files_ini[0] + ' '  + t_name
								p_pos = len(Comando)
							else:
								temp = False
								for x in range(len(t_files[0])):
									for y in t_files[1:]:
										if not y.startswith(t_files[0][:x]): temp = True; break
									if temp: x-=1; break
								
								if temp:
									Comando = t_files_ini[0] + ' '  + t_files[0][:x]
									p_pos = len(Comando)
								
								printTFiles(t_files)
					
				if vista_actual == l_vistas['Consola']:
					if len(Comando) < pos_limit and xD == False:
						
						# Se actualizan los valores por si se presiono alguna de las siguientes teclas.
						p_pos += 1
						k_char = True
						
						if evento.unicode != '\t':
							t_files_ini = ''
							t_files_pos = 0
						
						#=================================================================================
						
						# Inserta un espacio en la posicion p_pos del Comando.
						
						# ~ if evento.key == pygame.K_SPACE:   Comando = i_let(Comando, ' ',  p_pos)
						if not evento.unicode == '' and evento.unicode in CARACTERES: Comando = i_let(Comando, evento.unicode,  p_pos)
						else:
							# Si no, se restablecen los valores, significa que no se presiono ninguna de las teclas anteriores a partir del ultimo IF.
							p_pos -= 1
							k_char = False
							
				#=================================================================================
				
			elif evento.type == pygame.KEYUP:
				if vista_actual == l_vistas['Consola']:
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
		
		if vista_actual == l_vistas['Consola']:
			# Logica de Linea de Comandos
			if k_down:
				if not (k_wait > 0 and k_wait < 30) and len(Comando) > 0 and p_pos < pos_limit:
					# ~ print(Comando)
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
									# ~ print(p_pos, [Comando])
									Comando = Comando[:p_pos] + Comando[p_pos-1] + Comando[p_pos:]
									p_pos += 1
				
				k_wait += 1
		
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		
		screen.blit(BGimg, (0, 0))	# Se Carga La Imagen De Fondo.
		
		#===================================================================================================
		#===================================================================================================
		#===================================================================================================
		
		if not s_full:	# Dibuja un margen en la pantalla.
			pygame.draw.rect(screen, VERDE,  [0, 0, RESOLUCION[s_res][0], RESOLUCION[s_res][1]], 1)	# Margen de Pantalla.
		
		#===================================================================================================
		# Dibujar Iconos
		
		for i, btn in enumerate(l_icons):
			
			i += 1
			i_x = RESOLUCION[s_res][0]-btn_x*i-10*i
			
			rect_opaco(screen, [i_x, 10, btn_x, btn_y], AZUL_C, 220)
			pygame.draw.rect(screen, AZUL, [i_x, 10, btn_x, btn_y], 3)								# Recuadro de Icono.
			pygame.draw.rect(screen, AZUL_C, [i_x, 10, btn_x, btn_y], 1)							# Recuadro de Icono.
			pygame.draw.rect(screen, COLOR['Negro'], [i_x-1, 10-1, btn_x+2, btn_y+2], 1)			# Recuadro de Icono.
			btn_pos = ( i_x, 10 )
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
			dibujarTexto('Consola HG'+__version__, [temp_x-100, temp_y+1], FUENTES['Inc-R 12'], VERDE_C)
			
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
					for i, x in enumerate(temp):
						if x == '' or x == 0: continue
						else:
							sT = splitText(x)
							t1 = textos[:i]
							t1.extend(sT)
							t1.extend(textos[i+1:])
							textos = t1
							break
					
					l_comandos = add_comand(l_comandos, textos)
					
					if   Comando == 'exit': game_over = True
					elif Comando == 'cls':  l_comandos = []
					elif Comando.split(' ')[0] == 'cd':
						Prefijo = console.actualPath() + ' '											# Actualiza el Path
						pos_limit = ( RESOLUCION_CMD[s_res][0]-30 - (len(Prefijo)*(T_pix))) // T_pix	# Limite de letras en linea de comandos.
						
				Comando = ''
				exe = False
			
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
					# ~ print([com[:17]], com[:17] == 'Faltan Argumentos') #
					
					if com[:17] == 'Faltan Argumentos' or com[:3] == 'No ': pass
					elif valid or com[0] == ' ': pass
					elif len(com+error) <= pos_limit+len(Prefijo)+1:
						com = com+error
					else:
						com = com[:(pos_limit+len(Prefijo)-len(error)-2)]+'...'+error
				
				else:
					temp_col = VERDE_C
				
				dibujarTexto(com, p_texto, FUENTES[Font_def], temp_col)			# Imprime el texto en consola.
				
			#===================================================================================================
			# Dibuja el texto en la linea de comandos
			dibujarTexto(Prefijo+Comando[:pos_limit_r-len(Prefijo)+1], p_letra, FUENTES[Font_def], VERDE_C)	# Dibuja lo que vas escribiendo.
			
			#===================================================================================================
			
		#===================================================================================================
		elif vista_actual == l_vistas['Ajustes']:
			
			# Dibuja los textos en pantalla.
			pygame.draw.rect(screen, VERDE, [int(RESOLUCION[s_res][0]*.5)-5, 60, 250, 20], 1)
			dibujarTexto('Tiempo Transcurrido: '+str(segundos), [int(RESOLUCION[s_res][0]*.5), 60], FUENTES['Inc-R 18'], VERDE_C)
			
			v_tamX, v_tamY = 110, 30
			temp_x, temp_y = 25, 60
			
			# Resolucion Actual
			rect_opaco(screen, [temp_x, temp_y, 210, v_tamY-10], COLOR['Verde S'])								# Color de Fondo a Resolucion de Consola actual.
			pygame.draw.rect(screen, VERDE, [temp_x, temp_y, 210, v_tamY-10], 1)								# Contorno a Resolucion de Consola actual.
			dibujarTexto('Resolución: '+(str(RESOLUCION[s_res][0])+'x'+str(RESOLUCION[s_res][1])).rjust(9),
							[temp_x+10, temp_y], FUENTES['Inc-R 18'], VERDE_C)									# Resolucion de Consola actual.
			
			if c_res:
				
				rect_opaco(screen, [temp_x+110, temp_y-5, v_tamX-5, 30*len(RESOLUCION)], COLOR['Verde N'])		# Color de Fondo de Ventana de Resolucion.
				pygame.draw.rect(screen, VERDE, [temp_x+110, temp_y-5, v_tamX-5, 30*len(RESOLUCION)], 1)			# Contorno de Ventana de Resolucion.
				
				for i in range(1, len(RESOLUCION)):
					pygame.draw.rect(screen, VERDE, [temp_x+115, temp_y+(v_tamY*i), v_tamX-15, 20], 1)				# Recuedro individual de cada Resolucion de Consola.
					temp_texto = str(RESOLUCION[(s_res+i)%len(RESOLUCION)][0])+'x'
					temp_texto += str(RESOLUCION[(s_res+i)%len(RESOLUCION)][1])
					temp_texto = temp_texto.rjust(9)
					dibujarTexto(temp_texto, [temp_x+120, temp_y+(v_tamY*i)], FUENTES['Inc-R 18'], VERDE_C)			# Imprime el texto.
		
		#===================================================================================================
		# Dibuja en Pantalla un mensaje cuando se toma una Captura.
		if s_shot:
			s_shot_ticks = dibujarTextoTemporal(s_shot_ticks, 'Captura de Pantalla', 77)
			if s_shot_ticks == 0:
				s_shot = False
		
		elif s_full and s_full_ticks < 300:
			if s_fullF:
				s_full_ticks = dibujarTextoTemporal(s_full_ticks, 'No Puedes Salir de Pantalla Completa Con la Resolucion Máxima', 300, False)
				if s_full_ticks == 0:
					s_fullF = False
			else:
				s_full_ticks = dibujarTextoTemporal(s_full_ticks, 'Presione Ctrl+F o F11 Para Salir de Pantalla Completa', 300, False)
			
		#===================================================================================================
		#===================================================================================================
		#===================================================================================================
		
		pygame.display.flip()		# Actualiza Los Datos En La Interfaz.
		
		if ticks == 60:
			segundos += 1
			ticks = 0
			
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
		  'Verde S':  ( 24,  25,  30), 'Verde N':     (  0,  50,  30),
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

console = Console('Eny', 'HG'+__version__)
Prefijo = console.actualPath()+' '			# Simbolo de prefijo para comandos.

s_res     = -2								# Seleccion de Resolucion Por defecto. -2: la penultima Resolucion agregada.
T_pix     = 7								# Tamaño de Pixeles entre cada letra en linea de comandos.
T_pix_y   = T_pix*2							# Tamaño de Pixeles entre cada salto de linea en la linea de comandos.
T_rep     = 3								# Tiempo de repeticion entre caracteres al dejar tecla presionada.
Font_tam  = 14								# Para hacer manipulación del tamaño de algunos textos en pantalla.
Font_def  = 'Inc-R '+str(Font_tam)			# Fuente por defecto y tamaño de Fuente.

l_com_lim = ( RESOLUCION_CMD[s_res][1]-45) // T_pix_y							# Limite de lineas en consola
pos_limit = ( RESOLUCION_CMD[s_res][0]-30 - (len(Prefijo)*(T_pix))) // T_pix	# Limite de letras en linea de comandos.
pos_limit_r = ((RESOLUCION_CMD[s_res][0]-30)//T_pix)-1							# Limite Real de letras en linea de comandos. 
console.setConSize(pos_limit_r)													# Se indica el limite de caracteres para consola.

# Variables Globales: ==================================================

screen = None				# Objeto Que Crea La Ventana.
btn_x, btn_y = 40, 40		# Proporciones de los botones.
l_comandos = []

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

if __name__ == "__main__":
	
	main()
