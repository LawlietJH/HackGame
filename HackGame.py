

import keyboard
import pygame						# python -m pip install pygame
import ctypes

from win32api import GetKeyState	# python -m pip install pywin32
from win32con import VK_CAPITAL		# python -m pip install pywin32

TITULO  = 'Hack Game'
__version__ = 'v1.0.4'

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

def get_screen_size():
    user32 = ctypes.windll.user32
    screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screenSize

def load_image(filename, transparent=False):
	
	try: image = pygame.image.load(filename)
	except pygame.error as message: raise SystemError
	
	image = image.convert()
	
	if transparent:
		
		color = image.get_at((0,0))
		image.set_colorkey(color, RLEACCEL)
		
	return image

#===================================================================================================

def dibujarTexto(texto, posicion, fuente, color):		# Dibuja Texto En Pantalla.
	
	Texto = fuente.render(texto, 1, color)		# Se Pasa El Texto Con La Fuente Especificada.
	screen.blit(Texto, posicion)				# Se Dibuja En Pantalla El Texto en la Posición Indicada.

#===================================================================================================

def u_puntero(con, l_con, p_pos):	# Actualizar puntero. U = Update.
	
	p_p_pos = ((p_pos+2)*T_pix)		# Posicion de Puntero en Pixeles.
	puntero = [
			[ l_con[0]+5 + p_p_pos, l_con[1]+5 ],				# Posicion Inicial en X
			[ l_con[0]+5 + p_p_pos, l_con[1]+con['L_y']-5 ]		# Posicion Inicial en Y
		]
	
	return puntero

def i_let(t, c, p):		# Insertar letra. T = Texto, C = Caracter, P = Posicion
	t = t[:p-1] + c + t[p-1:]		# Se agrega el texto desde el inicio hasta la posicion p -1, agrega el nuevo caracter en dicha posicion y se agrega el resto desde p -1.
	return t

def add_comand(l_comandos, textos):	# Inserta Comandos a la Lista
	cont = l_comandos[-1][1]
	for t in textos: l_comandos.append((' '+t, cont))
	return l_comandos

#===================================================================================================

def main():
	
	global screen, s_res, pos_limit, l_com_lim
	
	# Inicializaciones =================================================
	
	screen = pygame.display.set_mode(RESOLUCION[s_res])	# Objeto Que Crea La Ventana.	# Objeto Que Crea La Ventana.
	BGimg  = load_image('images/fondo-negro.jpg')		# Carga el Fondo de la Ventana.
	Icono  = pygame.image.load('images/Icon.png')		# Carga el icono del Juego.
	
	pygame.display.set_icon(Icono)						# Agrega el icono a la ventana.
	pygame.display.set_caption(TITULO+' '+__version__)	# Titulo de la Ventana del Juego.
	
	pygame.init()									# Inicia El Juego.
	pygame.mixer.init()								# Inicializa el Mesclador.
	
	FUENTES = {
		   'Inc-R 16':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 16),
		   'Inc-R 12':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 12),
		   'Retro 16':pygame.font.Font("fuentes/Retro Gaming.ttf", 16),
		   'Wendy 18':pygame.font.Font("fuentes/Wendy.ttf", 18)
		  }
	
	# Variables ========================================================
	
	l_vistas = {
			'Consola': 1,
			'Ajustes': 2
		}
	
	vista_actual = l_vista['Consola']	# Vista Actual.
	
	game_over = False				# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()		# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	tamanio_fuente = 16				# Constante, para hacer manipulación del tamaño de algunas letras y en la matriz
									# para tener un margen correcto y otras cosas más.
	
	segundos = 0		# Contador de Tiempo, 1 seg por cada 60 Ticks.
	ticks    = 0		# Contador de Ticks.
	Prefijo  = '> '		# Simbolo de prefijo para comandos.
	Comando  = ''		# Comando en linea actual.
	l_comandos = []		# Lista de comandos ejecutados.
	l_com_ps = 0		# Poicion actual de lista de comandos ejecutados mostrados, 0 equivale a los mas recientes.
	p_pos    = 0	# Posicion del Puntero, para manipular en que posicion estara en la cadena 'Comando'. p_pos = 5 significaria entonces que estara el puntero en el caracter 5.
	
	# Dimensiones de Consola:
	# P = Punto inicial. T = Tamaño. M = Margen. L = linea
	con = {
		'P_x':30,  'P_y':30,
		'L_y':30,  'L_x':None,
		'T_x':RESOLUCION_CMD[s_res][0]-60,
		'T_y':RESOLUCION_CMD[s_res][1]-60,
		'T_m':5
	}
	
	con['L_x'] = con['T_x'] - ( con['T_m']*2 )	# Agrega los valores para L_x.
	
	t_con = [ con['P_x'], con['P_y'], con['T_x'], con['T_y'] ]		# Tamanios de Consola
	l_con = [														# Linea de Consola para los comandos
		con['P_x']+con['T_m'],
		con['P_y']+con['T_y']-con['L_y']-con['T_m'],
		con['L_x'],
		con['L_y']
	]
	
	p_letra = [ l_con[0]+5, l_con[1]+5 ]			# Posicion Inicial de texto.
	
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
	s_shot  = False			# Indica si se tomo una captura de pantalla.
	s_text  = 0				# Indica el tiempo en ticks que se mostrara un texto.
	
	# Cache de comandos para las teclas de Flecha Arriba y Abajo.
	cache_com = []
	cache_pos = 0
	
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
					
					v_tamX = 190
					_tempX = RESOLUCION[s_res][0] - RESOLUCION_CMD[s_res][0] + 30	# Espacio sobrante despues del borde de consola, en pixeles.
					_tempX = _tempX - ((_tempX - v_tamX) // 2)						# Sacamos la mitad del espacio sobrante al espacio ocupado por la ventana de resoluciones y se lo restamos para centrarlo.
					
					if x > RESOLUCION[s_res][0]-_tempX+5 and x < RESOLUCION[s_res][0]-25:
						
						if y > 15 and y < 40: c_res = False if c_res else True
						
						for i in range(1, len(RESOLUCION)):
							if y > (i*30)+15 and y < (i*30)+40 and c_res:
								s_res = ((s_res+i)%len(RESOLUCION))
								
								if s_full: screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN)
								else: screen = pygame.display.set_mode(RESOLUCION[s_res])
								
								pos_limit = (RESOLUCION_CMD[s_res][0] - 100) // T_pix
								l_com_lim = (RESOLUCION_CMD[s_res][1] - 100) // T_pix_y
								con = { 'P_x':30,  'P_y':30, 'L_y':30,  'L_x':None, 
										'T_x':RESOLUCION_CMD[s_res][0]-60, 'T_y':RESOLUCION_CMD[s_res][1]-60, 'T_m':5 }					# Dimensiones Generales para la Consola.
								con['L_x'] = con['T_x'] - ( con['T_m']*2 )																# Agrega los valores para L_x.
								t_con = [ con['P_x'], con['P_y'], con['T_x'], con['T_y'] ]												# Tamanios de Consola.
								l_con = [ con['P_x']+con['T_m'], con['P_y']+con['T_y']-con['L_y']-con['T_m'], con['L_x'], con['L_y'] ]	# Linea de Consola para los comandos.
								p_letra = [ l_con[0]+5, l_con[1]+5 ]																	# Posicion Inicial de texto.
								c_res = False
							
					else: c_res = False
							
				# Si la posicion en lista de comandos es menor que la cantidad de lineas de comandos
				if evento.button == 4 and l_com_ps < len(l_comandos):
					# Si la cantidad de lineas en lista de comandos es mayor al limite de lineas de comandos en pantalla
					# Y si la suma de posicion + el limite es menor a la cantidad de comandos, significa que por encima hay mas lineas de texto.
					# En resumen, Detecta si hay mas texto por encima 
					if len(l_comandos) > l_com_lim and (l_com_ps + l_com_lim) < len(l_comandos):
						# Y Permite desplazarse hacia arriba linea por linea, hasta que no haya mas encima.
						l_com_ps += 1
					
				elif evento.button == 5 and l_com_ps > 0:	# Mientras haya lineas debajo permite dezplazarse.
					l_com_ps -= 1
			
			#=================================================================================
			
			elif evento.type == pygame.KEYDOWN:		# Manipulación del Teclado.
				# Al presionar cualquier tecla.
				k_down = True
				k_wait = 1
				
				#=================================================================================
				
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				
				#=================================================================================
				# Teclas Bloq Mayus, y las teclas Shift izquerdo y derecho.
				if evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
				or evento.key == pygame.K_CAPSLOCK:
					a_shift = False if a_shift else True
				
				#=================================================================================
				# Felchas de direcciones
				if   evento.key == pygame.K_LEFT:
					if p_pos > 0: p_pos -= 1
					k_izq = True
					
				elif evento.key == pygame.K_RIGHT:
					if p_pos < len(Comando): p_pos += 1
					k_der = True
					
				elif evento.key == pygame.K_UP:
					if len(cache_com) > 0:
						k_arr = True
						if cache_com[cache_pos] != Comando and cache_pos == 0:
							cache_com.insert(0, Comando)	# Inserta el Comando en la posicion 0 de la lista
						if cache_pos < len(cache_com)-1:    cache_pos += 1					# Aumenta la posicion en 1, o sea, para mostrar uno anterior.
						if cache_com[cache_pos] == '':
							cache_com.pop(cache_pos)		# Elimina los que sean cadenas vacias.
							cache_pos -= 1
						Comando = cache_com[cache_pos]
						p_pos = len(Comando)
					
				elif evento.key == pygame.K_DOWN:
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
				if evento.key == pygame.K_BACKSPACE:
					
					if p_pos > 0:
						Comando = Comando[:p_pos-1]+Comando[p_pos:]
						p_pos  -= 1
						k_back  = True
				
				if evento.key == pygame.K_DELETE:
					
					if p_pos < len(Comando):
						Comando = Comando[:p_pos]+Comando[p_pos+1:]
						k_del   = True
				
				#=================================================================================
				# Acciones al Presionar ENTER.
				if evento.key == pygame.K_RETURN:
					
					if not Comando == '':
						
						l_com_ps = 0
						exe = True
						
						if len(l_comandos) > 0:
							cont = l_comandos[-1][1]+1
							l_comandos.append((str(cont).zfill(2)+' '+Comando, cont))
						else:
							l_comandos.append(('01 '+Comando, 1))
						
						# Si el comando ya existe en Cache, se eliminan todas sus replicas, dejando solo el nuevo en la lista.
						while Comando in cache_com:
							temp_pos = cache_com.index(Comando)
							cache_com.pop(temp_pos)
						
						cache_com.insert(0, Comando)
						cache_pos = 0
						
						p_pos = 0
				
				#=================================================================================
				
				if p_pos < pos_limit:
					
					# Se actualizan los valores por si se presiono alguna de las siguientes teclas.
					p_pos += 1
					k_char = True
					
					#=================================================================================
					# Combinacion de Teclas
					# Ctrl + P o F10 para tomar una Captura de Pantalla.
					if evento.key == pygame.K_p and evento.mod == 64 or evento.key == pygame.K_F10:
						
						from os import path, mkdir
						
						s_n = 1
						s_folder = 'screenshots/'
						s_path = s_folder+'screenshot_001.jpg'
						
						if not path.isdir(s_folder): mkdir(s_folder)
						
						while path.exists(s_path):
							s_n += 1
							s_path = s_folder+'screenshot_{}.jpg'.format(str(s_n).zfill(3))
						
						pygame.image.save(screen, s_path)
						
						s_shot = True
					
					# Ctrl + F o F11 para poner Pantalla Completa.
					elif evento.key == pygame.K_f and evento.mod == 64 or evento.key == pygame.K_F11:
						
						p_pos -= 1
						k_char = False
						
						if s_full:
							screen = pygame.display.set_mode(RESOLUCION[s_res])
							s_full = False
						else:
							screen = pygame.display.set_mode(RESOLUCION[s_res], pygame.FULLSCREEN)
							s_full = True
					
					#=================================================================================
					
					# Inserta un espacio en la posicion p_pos del Comando.
					elif evento.key == pygame.K_SPACE:   Comando = i_let(Comando, ' ',  p_pos)
					elif keyboard.is_pressed('/'):  Comando = i_let(Comando, '/',  p_pos)
					elif keyboard.is_pressed('+'):  Comando = i_let(Comando, '+',  p_pos)
					elif keyboard.is_pressed('-'):  Comando = i_let(Comando, '-',  p_pos)
					elif keyboard.is_pressed('.'):  Comando = i_let(Comando, '.',  p_pos)
					
					# Inserta una letra Mayuscula si a_shift es True, sino una Minuscula en la posicion p_pos del Comando.
					elif evento.key == pygame.K_a: Comando = i_let(Comando, 'A' if a_shift else 'a', p_pos)
					elif evento.key == pygame.K_b: Comando = i_let(Comando, 'B' if a_shift else 'b', p_pos)
					elif evento.key == pygame.K_c: Comando = i_let(Comando, 'C' if a_shift else 'c', p_pos)
					elif evento.key == pygame.K_d: Comando = i_let(Comando, 'D' if a_shift else 'd', p_pos)
					elif evento.key == pygame.K_e: Comando = i_let(Comando, 'E' if a_shift else 'e', p_pos)
					elif evento.key == pygame.K_f: Comando = i_let(Comando, 'F' if a_shift else 'f', p_pos)
					elif evento.key == pygame.K_g: Comando = i_let(Comando, 'G' if a_shift else 'g', p_pos)
					elif evento.key == pygame.K_h: Comando = i_let(Comando, 'H' if a_shift else 'h', p_pos)
					elif evento.key == pygame.K_i: Comando = i_let(Comando, 'I' if a_shift else 'i', p_pos)
					elif evento.key == pygame.K_j: Comando = i_let(Comando, 'J' if a_shift else 'j', p_pos)
					elif evento.key == pygame.K_k: Comando = i_let(Comando, 'K' if a_shift else 'k', p_pos)
					elif evento.key == pygame.K_l: Comando = i_let(Comando, 'L' if a_shift else 'l', p_pos)
					elif evento.key == pygame.K_m: Comando = i_let(Comando, 'M' if a_shift else 'm', p_pos)
					elif evento.key == pygame.K_n: Comando = i_let(Comando, 'N' if a_shift else 'n', p_pos)
					elif evento.key == pygame.K_o: Comando = i_let(Comando, 'O' if a_shift else 'o', p_pos)
					elif evento.key == pygame.K_p: Comando = i_let(Comando, 'P' if a_shift else 'p', p_pos)
					elif evento.key == pygame.K_q: Comando = i_let(Comando, 'Q' if a_shift else 'q', p_pos)
					elif evento.key == pygame.K_r: Comando = i_let(Comando, 'R' if a_shift else 'r', p_pos)
					elif evento.key == pygame.K_s: Comando = i_let(Comando, 'S' if a_shift else 's', p_pos)
					elif evento.key == pygame.K_t: Comando = i_let(Comando, 'T' if a_shift else 't', p_pos)
					elif evento.key == pygame.K_u: Comando = i_let(Comando, 'U' if a_shift else 'u', p_pos)
					elif evento.key == pygame.K_v: Comando = i_let(Comando, 'V' if a_shift else 'v', p_pos)
					elif evento.key == pygame.K_w: Comando = i_let(Comando, 'W' if a_shift else 'w', p_pos)
					elif evento.key == pygame.K_x: Comando = i_let(Comando, 'X' if a_shift else 'x', p_pos)
					elif evento.key == pygame.K_y: Comando = i_let(Comando, 'Y' if a_shift else 'y', p_pos)
					elif evento.key == pygame.K_z: Comando = i_let(Comando, 'Z' if a_shift else 'z', p_pos)
					# Inserta un Numero en la posicion p_pos en Comando.
					elif evento.key == pygame.K_0: Comando = i_let(Comando, '0', p_pos)
					elif evento.key == pygame.K_1: Comando = i_let(Comando, '1', p_pos)
					elif evento.key == pygame.K_2: Comando = i_let(Comando, '2', p_pos)
					elif evento.key == pygame.K_3: Comando = i_let(Comando, '3', p_pos)
					elif evento.key == pygame.K_4: Comando = i_let(Comando, '4', p_pos)
					elif evento.key == pygame.K_5: Comando = i_let(Comando, '5', p_pos)
					elif evento.key == pygame.K_6: Comando = i_let(Comando, '6', p_pos)
					elif evento.key == pygame.K_7: Comando = i_let(Comando, '7', p_pos)
					elif evento.key == pygame.K_8: Comando = i_let(Comando, '8', p_pos)
					elif evento.key == pygame.K_9: Comando = i_let(Comando, '9', p_pos)
					else:
						# Si no, se restablecen los valores, significa que no se presiono ninguna de las teclas anteriores a partir del ultimo IF.
						p_pos -= 1
						k_char = False
				#=================================================================================
				
			elif evento.type == pygame.KEYUP:
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
		
		# Logica de Linea de Comandos
		if k_down:
			if not (k_wait > 0 and k_wait < 30) and len(Comando) > 0 and p_pos < pos_limit:
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
					elif k_arr and (k_wait % (T_rep*2)) == 0:
						if cache_pos < len(cache_com)-1: cache_pos += 1
						if cache_com[cache_pos] == '': cache_com.pop(cache_pos)
						Comando = cache_com[cache_pos]
						p_pos = len(Comando)
					else:
						if k_char:						# Mientras se este presionado una letra, un numero o un espacio, se seguira agregando caracteres.
							Comando += Comando[-1]
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
			pygame.draw.rect(screen, COLOR['Azul'],  [0, 0, RESOLUCION[s_res][0], RESOLUCION[s_res][1]], 1)	# Margen de Pantalla.
			# ~ pygame.draw.rect(screen, COLOR['Verde'], [1, 1, RESOLUCION[s_res][0]-2, RESOLUCION[s_res][1]-2], 1)	# Margen de Pantalla.
		
		pygame.draw.rect(screen, COLOR['Negro'], t_con, 0)	# Ventana de Consola.
		pygame.draw.rect(screen, COLOR['Verde'], t_con, 2)	# Margen de Consola.
		pygame.draw.rect(screen, COLOR['Verde'], l_con, 1)	# Dibuja linea de Consola.
		# ~ pygame.draw.rect(screen, COLOR['Negro'], linea_consola, 0)	# Dibuja linea de Consola.
		# ~ pygame.draw.rect(screen, COLOR['Verde Claro'], linea_consola, 1)	# Dibuja linea de Consola.
		
		# ~ print(l_com_ps)
		p_puntero = u_puntero(con, l_con, p_pos)
		
		if ticks < 30:
			pygame.draw.line(screen, COLOR['Gris'], p_puntero[0], p_puntero[1], 2)
		
		#======================================================================================
		
		# Si se activa un Comando Lo Ejecuta.
		if exe:
			
			if   Comando == 'exit': game_over = True
			elif Comando == 'cls':  l_comandos = []
			elif Comando == 'xD': l_comandos[-1] = (l_comandos[-1][0]+': Hola.', l_comandos[-1][1])
			elif Comando == 'help':
				textos = [
					'',
					'Los Posibles Comandos a Utilizar Son:',
					'',
					'    help    Muestra Este Mensaje de Ayuda.',
					'    exit    Cierra la Consola de Comandos.',
					'    cls     Limpia la Consola de Comandos.',
					''
				]
				l_comandos = add_comand(l_comandos, textos)
				
			Comando = ''
		
		# limita la cantidad de lineas que se mostraran en consola.
		if l_com_ps > 0:
			temp = l_comandos[-l_com_lim-l_com_ps:(l_com_ps*-1)]
		else:
			temp = l_comandos[-l_com_lim:]
		
		# Mostrara texto en consola.
		
		error = ': No es un Comando Valido.'
		
		for i, (com, pos) in enumerate(temp):	# Dibuja la lista de comandos ejecutados.
			# ~ p_texto = [ l_con[0]+5 + l_p_pos, l_con[1]+5 - ((len(temp)-i)*24) ]
			p_texto = [ l_con[0]+5, l_con[1] - ((len(temp)-i)*T_pix_y) ]
			
			# Validamos que sea un comando valido y que sus lineas correspondientes tambien se muestren como validas.
			temp_col = COLOR['Verde Claro'] if (com[3:] in COMANDOS or com[0] == ' ') else COLOR['Rojo Claro']
			com = com if (com[3:] in COMANDOS or com[0] == ' ') else (
				com+error if len(com)+len(error) <= pos_limit else (
					com[:(pos_limit-len(error))]+'...'+error
				)
			)
			
			dibujarTexto(com, p_texto, FUENTES['Inc-R 16'], temp_col)
		
		v_tamX = 190
		_tempX = RESOLUCION[s_res][0] - RESOLUCION_CMD[s_res][0] + 30	# Espacio sobrante despues del borde de consola, en pixeles.
		_tempX = _tempX - ((_tempX - v_tamX) // 2)						# Sacamos la mitad del espacio sobrante al espacio ocupado por la ventana de resoluciones y se lo restamos para centrarlo.
		
		# Dibuja los textos en pantalla.
		dibujarTexto('Tiempo Transcurrido: '+str(segundos), [con['P_x'], 10], FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
		# Resolucion Actual
		pygame.draw.rect(screen, COLOR['Azul Claro'], [RESOLUCION[s_res][0]-_tempX+5, 15, v_tamX-10, 25], 1)
		dibujarTexto('Resolución: '+str(RESOLUCION[s_res][0])+'x'+str(RESOLUCION[s_res][1]), [RESOLUCION[s_res][0]-_tempX+10, 20], FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
		if c_res:
			
			pygame.draw.rect(screen, COLOR['Verde N'], [RESOLUCION[s_res][0]-_tempX,   10, v_tamX,    5+(30*len(RESOLUCION))], 0)	# Ventana de Resolucion.
			pygame.draw.rect(screen, COLOR['Azul'],   [RESOLUCION[s_res][0]-_tempX,   10, v_tamX,    5+(30*len(RESOLUCION))], 1)	# Ventana de Resolucion Contorno.
			pygame.draw.rect(screen, COLOR['Verde S'], [RESOLUCION[s_res][0]-_tempX+5, 15, v_tamX-10, 25], 0)						# Color fondo a Resolucion de Consola actual.
			
			for i in range(len(RESOLUCION)):
				
				color = COLOR['Verde Claro'] if i == 0 else COLOR['Azul Claro']
				
				pygame.draw.rect(screen, color, [RESOLUCION[s_res][0]-_tempX+5, 15+(i*30), v_tamX-10, 25], 1)				# Recuedro individual de cada Resolucion de Consola.
				
				dibujarTexto('Resolución: '+str(RESOLUCION[(s_res+i)%len(RESOLUCION)][0])+'x'+str(RESOLUCION[(s_res+i)%len(RESOLUCION)][1]), [RESOLUCION[s_res][0]-_tempX+10, 20+(30*i)], FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
		dibujarTexto(Prefijo+Comando, p_letra, FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
		#===================================================================================================
		
		if s_shot:
			s_text += 1
			if s_text < 77:
				texto = 'Captura de Pantalla'
				len_t = len(texto)
				t_temp = ((RESOLUCION[s_res][0]//2)-((len_t*T_pix)//2), (RESOLUCION[s_res][1]//2)-(T_pix*2))
				pygame.draw.rect(screen, COLOR['Negro'], [t_temp[0]-5, t_temp[1]-5, (len_t*T_pix)+10, (T_pix*2)+10], 0)	# Resolucion de Consola.
				pygame.draw.rect(screen, COLOR['Azul'], [t_temp[0]-5, t_temp[1]-5, (len_t*T_pix)+10, (T_pix*2)+10], 1)	# Resolucion de Consola.
				dibujarTexto(texto, [t_temp[0], t_temp[1]], FUENTES['Inc-R 16'], COLOR['Verde Claro'])
			else:
				s_text = 0
				s_shot = False
			
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

COLOR  = {
		  'Blanco':   (255, 255, 255), 'Negro':       (  0,   0,   0),
		  'Gris':     (189, 189, 189), 'Gris Claro':  (216, 216, 216),
		  'Rojo':     (255,   0,   0), 'Rojo Claro':  (255,  50,  50),
		  'Verde':    (  4, 180,   4), 'Verde Claro': (  0, 255,   0),
		  'Azul':     ( 20,  80, 240), 'Azul Claro':  ( 40, 210, 250),
		  'Amarillo': (255, 255,   0), 'Naranja':     (255, 120,   0),
		  'Morado':   ( 76,  11,  95), 'Purpura':     ( 56,  11,  97),
		  'Verde S':  ( 24,  25,  30), 'Verde N':     (  0,  50,  30)
		 }	# Diccionario de Colores.

resoluciones = [
		( 640,  480),	# Tamaño de La Ventana, Ancho (640) y Alto  (480).
		( 720,  480),
		( 800,  600),
		(1280,  720),
		(1366,  768),
		(1536,  864),
		(1920, 1080)
	]

RESOLUCION = []
size = get_screen_size()

for i, (x, y) in enumerate(resoluciones):
	if size[0] >= x and size[1] >= y:
		RESOLUCION.append(resoluciones[i])

px = .72
py = .77

RESOLUCION_CMD = [	
		(int(RESOLUCION[i][0]*px), int(RESOLUCION[i][1]*py))
		for i in range(len(RESOLUCION))
	]

CARACTERES = [
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
		'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
		' ', '/', '+', '-', '.'
	]

COMANDOS = ['help', 'exit', 'cls', 'xD: Hola.']

# ~ s_res     = -2		# Seleccion de Resolucion Por defecto. -2: la penultima Resolucion agregada.
s_res     = 0		# Seleccion de Resolucion Por defecto. -2: la penultima Resolucion agregada.
T_pix_y   = 20		# Tamaño de Pixeles entre cada salto de linea en la linea de comandos.
T_pix     = 8		# Tamaño de Pixeles entre cada letra en linea de comandos.
T_rep     = 3		# Tiempo de repeticion entre caracteres al dejar tecla presionada.
pos_limit = (RESOLUCION_CMD[s_res][0] - 100) // T_pix
l_com_lim = (RESOLUCION_CMD[s_res][1] - 100) // T_pix_y

# Variables Globales: ==================================================

screen = None		# Objeto Que Crea La Ventana.

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

if __name__ == "__main__":
	
	main()
