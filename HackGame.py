

import pygame

from win32api import GetKeyState
from win32con import VK_CAPITAL

TITULO  = 'Hack Game'
__version__ = 'v1.0.0'

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

def load_image(filename, transparent=False):
	
	global Error
	
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

def u_puntero(con, l_con, p_pos):
	
	p_p_pos = ((p_pos+2)*T_pix)
	puntero = [
			[ l_con[0]+5 + p_p_pos, l_con[1]+5 ],
			[ l_con[0]+5 + p_p_pos, l_con[1]+con['L_y']-5 ]
		]
	
	return puntero

#===================================================================================================

#===================================================================================================

def main():
	
	global screen
	
	# Inicializaciones =================================================
	
	screen = pygame.display.set_mode(DIMENCIONES)	# Objeto Que Crea La Ventana.	# Objeto Que Crea La Ventana.
	BGimg  = load_image('images/fondo-negro.jpg')	# Carga el Fondo de la Ventana.
	Icono  = pygame.image.load('images/Icon.png')	# Carga el icono del Juego.
	
	pygame.display.set_icon(Icono)						# Agrega el icono a la ventana.
	pygame.display.set_caption(TITULO+' '+__version__)	# Titulo de la Ventana del Juego.
	
	pygame.init()									# Inicia El Juego.
	pygame.mixer.init()								# Inicializa el Mesclador.
	
	
	FUENTES = {
		   'Inc-R 16':pygame.font.Font("fuentes/Inconsolata-Regular.ttf", 16),
		   'Retro 16':pygame.font.Font("fuentes/Retro Gaming.ttf", 16),
		   'Wendy 18':pygame.font.Font("fuentes/Wendy.ttf", 18)
		  }

	# Variables ========================================================
	
	game_over = False				# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()		# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	tamanio_fuente = 16				# Constante, para hacer manipulación del tamaño de algunas letras y en la matriz
									# para tener un margen correcto y otras cosas más.
	
	segundos = 0		# Contador de Tiempo, 1 seg por cada 60 Ticks.
	ticks    = 0		# Contador de Ticks.
	Prefijo  = '> '		# Simbolo de prefijo para comandos.
	Comando  = ''		# Comando en linea actual.
	l_comandos = []		# Lista de comandos ejecutados.
	l_com_ps = 0		# Poicion actual de comandos ejecutados mostrados, 0 equivale a los mas recientes.
	
	# Dimensiones de Consola:
	# P = Punto inicial. T = Tamaño. M = Margen. L = linea
	con = {
		'P_x':30,  'P_y':30,
		'L_y':30,  'L_x':None,
		'T_x':DIMENCIONES[0]-60,
		'T_y':DIMENCIONES[1]-60,
		'T_m':5
	}
	
	con['L_x'] = con['T_x'] - ( con['T_m']*2 )	# Agrega los valores para L_x.
	
	t_con = [ con['P_x'], con['P_y'], con['T_x'], con['T_y'] ]
	l_con = [
		con['P_x']+con['T_m'],
		con['P_y']+con['T_y']-con['L_y']-con['T_m'],
		con['L_x'],
		con['L_y']
	]
	
	p_pos   = 0
	
	l_p_pos = (p_pos*T_pix)
	p_letra = [ l_con[0]+5 + l_p_pos, l_con[1]+5 ]
	
	a_shift = False if GetKeyState(VK_CAPITAL) == 0 else True	# Saber si esta activo el Bloq. Mayus.
	k_down = False
	k_back = False
	k_wait = 0
	
	#===================================================================
	
	# Inicio Del Juego:
	while game_over is False:
		
		ticks += 1
		
		# Chequeo Constante de Eventos del Teclado:
		events = pygame.event.get()
		
		for evento in events:
			
			# ~ print(pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
			# ~ print(evento.type)
			
			if evento.type == pygame.QUIT: game_over = True		# Si Se Presiona El Botón Cerrar, Cerrara El Juego.
			
			elif evento.type == pygame.MOUSEBUTTONDOWN:		# Manipulación del Mouse.
				
				# evento.button:
				# Clic  Izq = 1 - Clic  Cen = 2 - Clic Der = 3
				# Rueda Arr = 4 - Rueda Aba = 5
				
				if evento.button == 4 and l_com_ps < len(l_comandos):
					l_com_ps += 1
				elif evento.button == 5 and l_com_ps > 0:
					l_com_ps -= 1
					
			elif evento.type == pygame.KEYDOWN:		# Manipulación del Teclado.
				
				k_down = True
				k_wait = 1
				
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				if evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
				or evento.key == pygame.K_CAPSLOCK:
					a_shift = False if a_shift else True
				
				# ~ if   evento.key == pygame.K_LEFT  or evento.key == pygame.K_a:
				# ~ elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
				# ~ elif evento.key == pygame.K_UP    or evento.key == pygame.K_w:
				# ~ elif evento.key == pygame.K_DOWN  or evento.key == pygame.K_s:
				
				# ~ if evento.key == pygame.K_BACKSPACE or evento.key == pygame.K_DELETE:
				# ~ elif evento.key == pygame.K_PERIOD or evento.key == pygame.K_KP_PERIOD:
				# ~ if   evento.key == pygame.K_0 or evento.key == pygame.K_KP0:
				
				if evento.key == pygame.K_BACKSPACE or evento.key == pygame.K_DELETE:
					
					Comando = Comando[:-1]
					k_back  = True
					
					if p_pos > 0: p_pos -= 1
				
				if evento.key == pygame.K_RETURN:
					
					if not Comando == '':
						
						l_comandos.append((Comando, len(l_comandos)))
						Comando = ''
						p_pos = 0
					
				if p_pos < pos_limit:
					
					p_pos += 1
					if evento.key == pygame.K_SPACE: Comando += ' '
					# Minusculas y Mayusculas:
					elif evento.key == pygame.K_a: Comando += ('A' if a_shift else 'a')
					elif evento.key == pygame.K_b: Comando += ('B' if a_shift else 'b')
					elif evento.key == pygame.K_c: Comando += ('C' if a_shift else 'c')
					elif evento.key == pygame.K_d: Comando += ('D' if a_shift else 'd')
					elif evento.key == pygame.K_e: Comando += ('E' if a_shift else 'e')
					elif evento.key == pygame.K_f: Comando += ('F' if a_shift else 'f')
					elif evento.key == pygame.K_g: Comando += ('G' if a_shift else 'g')
					elif evento.key == pygame.K_h: Comando += ('H' if a_shift else 'h')
					elif evento.key == pygame.K_i: Comando += ('I' if a_shift else 'i')
					elif evento.key == pygame.K_j: Comando += ('J' if a_shift else 'j')
					elif evento.key == pygame.K_k: Comando += ('K' if a_shift else 'k')
					elif evento.key == pygame.K_l: Comando += ('L' if a_shift else 'l')
					elif evento.key == pygame.K_m: Comando += ('M' if a_shift else 'm')
					elif evento.key == pygame.K_n: Comando += ('N' if a_shift else 'n')
					elif evento.key == pygame.K_o: Comando += ('O' if a_shift else 'o')
					elif evento.key == pygame.K_p: Comando += ('P' if a_shift else 'p')
					elif evento.key == pygame.K_q: Comando += ('Q' if a_shift else 'q')
					elif evento.key == pygame.K_r: Comando += ('R' if a_shift else 'r')
					elif evento.key == pygame.K_s: Comando += ('S' if a_shift else 's')
					elif evento.key == pygame.K_t: Comando += ('T' if a_shift else 't')
					elif evento.key == pygame.K_u: Comando += ('U' if a_shift else 'u')
					elif evento.key == pygame.K_v: Comando += ('V' if a_shift else 'v')
					elif evento.key == pygame.K_w: Comando += ('W' if a_shift else 'w')
					elif evento.key == pygame.K_x: Comando += ('X' if a_shift else 'x')
					elif evento.key == pygame.K_y: Comando += ('Y' if a_shift else 'y')
					elif evento.key == pygame.K_z: Comando += ('Z' if a_shift else 'z')
					# Numeros:
					elif evento.key == pygame.K_0: Comando += '0'
					elif evento.key == pygame.K_1: Comando += '1'
					elif evento.key == pygame.K_2: Comando += '2'
					elif evento.key == pygame.K_3: Comando += '3'
					elif evento.key == pygame.K_4: Comando += '4'
					elif evento.key == pygame.K_5: Comando += '5'
					elif evento.key == pygame.K_6: Comando += '6'
					elif evento.key == pygame.K_7: Comando += '7'
					elif evento.key == pygame.K_8: Comando += '8'
					elif evento.key == pygame.K_9: Comando += '9'
					else: p_pos -= 1
				
			elif evento.type == pygame.KEYUP:
				
				k_down = False
				k_back = False
				k_wait = 0
				
				if evento.key == pygame.K_RSHIFT or evento.key == pygame.K_LSHIFT \
				or evento.key == pygame.K_CAPSLOCK:
					a_shift = False if a_shift else True
		
		if k_down:
			if not (k_wait > 0 and k_wait < 30) and len(Comando) > 0 and p_pos < pos_limit:
				if (k_wait % T_rep) == 0 and Comando[-1] in LETRAS:
					if k_back:
						Comando = Comando[:-1]
						if p_pos > 0: p_pos -= 1
					else:
						if not a_shift:				# Mientras no este precionado los shifts o bloq. mayus, seguira agregando caracteres.
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
		if l_com_ps > 0:
			temp = l_comandos[-l_com_lim-l_com_ps:(l_com_ps*-1)]
		else:
			temp = l_comandos[-l_com_lim:]
		
		for i, (com, pos) in enumerate(temp):	# Dibuja la lista de comandos ejecutados.
			p_texto = [ l_con[0]+5 + l_p_pos, l_con[1]+5 - ((len(temp)-i)*24) ]
			dibujarTexto(str(pos+1).zfill(2)+' '+com, p_texto, FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
		dibujarTexto('Tiempo Transcurrido: '+str(segundos), [con['P_x'], 10], FUENTES['Wendy 18'], COLOR['Verde Claro'])
		dibujarTexto(Prefijo+Comando, p_letra, FUENTES['Inc-R 16'], COLOR['Verde Claro'])
		
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
		  'Blanco':		(255, 255, 255),	'Negro':		(  0,   0,   0),
		  'Gris':		(189, 189, 189),	'Gris Claro':	(216, 216, 216),
		  'Rojo':		(255,   0,   0),	'Rojo Claro':	(255,  50,  50),
		  'Verde':		(  4, 180,   4),	'Verde Claro':	(  0, 255,   0),
		  'Azul':		( 20,  80, 240),	'Azul Claro':	( 40, 210, 250),
		  'Amarillo':	(255, 255,   0),	'Naranja':		(255, 120,   0),
		  'Morado':		( 76,  11,  95),	'Purpura':		( 56,  11,  97),
		  'Fondo':		( 24,  25,  30),	'Seleccion':	(220, 200,   0)
		 }	# Diccionario de Colores.

# ~ DIMENCIONES = (1280, 720)		# Tamaño de La Ventana, Ancho (1120) y Alto (600).
DIMENCIONES = (720, 480)		# Tamaño de La Ventana, Ancho (1120) y Alto (600).
LETRAS = [
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
		'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		' ',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
	]

T_pix = 8		# Tamaño de Pixeles entre cada letra en linea de comandos. 
T_rep = 3		# Tiempo de repeticion entre caracteres al dejar tecla presionada.
pos_limit = (DIMENCIONES[0] - 100) // T_pix
l_com_lim = ((DIMENCIONES[1] - 80) // 24)

print(l_com_lim)

# Variables Globales: ==================================================

screen = None					# Objeto Que Crea La Ventana.

#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================

if __name__ == "__main__":
	
	main()
