
# By: LawlietJH
# Odyssey in Dystopia

TITULO  = 'Odyssey in Dystopia'		# Nombre
__version__ = 'v1.2.3'				# Version

class Helps:
	
	'''
	Las computadoras tienen el poder y el poder lo tienes tú.
	La conexión entre el bien y el mal existe más allá de unos y ceros.
	Unos y ceros, prediciendo el futuro.
	'''
	
	help_content = '''

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
	
	permisos_content = '''
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

	chmod_content = '''
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
	
	save_content = '''
 Este comando permite Guardar la partida actual.
	'''
	
	cls_content = '''
 Este comando permite vaciar el Buffer de consola,
 eliminando los datos cargados y restaurando la
 pantalla a su estado original.
	'''
	
	exit_content = '''
 Este comando permite cerrar la sesión actual.
	'''
	
	


