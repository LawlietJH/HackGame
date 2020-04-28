
# By: LawlietJH
# Odyssey in Dystopia

from datetime import datetime
from .helps import Helps

import threading
import sqlite3
import random
import os

#=======================================================================

TITULO      = 'Odyssey in Dystopia'	# Nombre
__version__ = 'v1.2.5'				# Version
__author__  = 'LawlietJH'			# Desarrollador

#=======================================================================
#=======================================================================
#=======================================================================



class Database:
	
	# verb:
	# 0 = No Muestra Nada.
	# 1 = Muestra mensaje de tabla cargada.
	# 2 = Muestra mensaje de tabla cargada y muestra la Query completa.
	
	def __init__(self, DBName):
		
		self.db_name = DBName
		self.con = sqlite3.connect(DBName)
		self.cur = self.con.cursor()
	
	def randomIP(self, types=0):
		
		# types: 0 = Publica, 1 = Privada
		
		if types == 0:
			ip = [str(random.randint(1, 255)) for _ in range(4)]
		else:
			ip = ['192','168','1',str(random.randint(1, 255))]
		
		ip = '.'.join(ip)
		return ip
	
	def freeQuery(self, query, verb=0):
		
		self.cur.executescript(query)
		
		if verb > 0: print(query)
	
	def createTable(self, name, data, fore=[], verb=0):
		
		atrs = ''
		for key, val in data.items(): atrs += '    ' + key + ' ' + val + ',\n'
		atrs = atrs[:-2]
		
		foreK = ''
		for t in fore:
			foreK += ',\n    FOREIGN KEY({1}) REFERENCES {0}({1})'.format(t, 'id'+t)
		
		base  = 'CREATE TABLE IF NOT EXISTS'
		query = '{0} {1} (\n{2}{3}\n);'.format(base, name, atrs, foreK)
		
		self.cur.execute(query)
		
		if verb > 0: print('\n Table \'{}\' loaded successfully.'.format(name))
		if verb > 1: print('\n' + query + '\n')
	
	def insertData(self, table, keys, values, verb=0):
		
		types = ''
		l_val = len(values[0])
		keys  = ', '.join(keys)
		
		base  = 'INSERT INTO {}'.format(table)
		
		types = '?,'*l_val
		types = types[:-1]
		
		query = '{}({}) VALUES ({});'.format(base, keys, types)
		
		self.cur.executemany(query, values)
		
		if verb > 0:
			print('\n Data in \'{}\' loaded successfully.'.format(table))
		if verb > 1:
			print('\n' + query + '\n')
			for v in values: print(v)
	
	def getData(self, table, types='*', where='', c=0, verb=0):
		
		if type(types) == list: types = ', '.join(types)
		
		base  = 'SELECT {} FROM {}'.format(types, table)
		where = (' WHERE '+where if where else '')
		query = '{}{};'.format(base, where)
		try:
			self.cur.execute(query)
		except:
			return None
		if c == 0:
			rows = self.cur.fetchall()
		elif c == 1:
			rows = self.cur.fetchone()
			try:
				if len(rows) == 1: rows = rows[0]
			except:
				pass
				# ~ if rows == None: print('\n Nothing Here...')
		else:
			rows = self.cur.fetchmany(c)
		
		if verb > 0:
			print('\n \'{}\' Information displayed successfully.'.format(table))
		elif verb > 1:
			print('\n' + query + '\n')
		
		return rows
	
	def updateData(self, table, update, where='', verb=0):
		
		l = ['{}={}'.format(row, up) for row, up in update]
		s = ', '.join(l)
		base  = 'UPDATE {}'.format(table)
		setr  = 'SET ' + s
		where = 'WHERE {}'.format(where) if where else ''
		
		query = '{} {} {};'.format(base, setr, where)
		# ~ print(query)
		self.con.execute(query)
		
		if verb > 0: print('\n Table \'{}\' updated successfully.'.format(table))
		if verb > 1: print('\n' + query + '\n')
	
	def updateUserConection(self, user, verb=0):
		
		query  = ['User', 'idUser', 'user = "{}"'.format(user)]
		idUser = str(self.getData(*query, c=1))
		
		setr = [('lastCon',"datetime('now','localtime')")]
		self.updateData('User', setr, 'idUser = '+idUser)
		self.con.commit()
		
		if verb > 0:
			t = self.getData('User','lastCon','idUser='+idUser, c=1)
			print('\n User \'{}\' last connection '.format(user)+\
			'updated successfully at: {}'.format(t))
	
	# Actualiza la Fila seleccionada del Usuario con los Datos Nuevos.
	def updateUserFile(self, data, elements, con, verb=0):
		# Ejemplos:
		# data = [('permiso','new data'),('content','new content')]
		# elements = [ch.element, ch.path_r]
		
		user = con.username
		data_origin = con.getChildData(elements[0], elements[1])
		
		query  = ['User', 'idUser', 'user = "{}"'.format(user)]
		idUser = str(self.getData(*query, c=1))
		
		elems   = ['nodeP', 'element', 'permiso', 'content', 'path']
		changes = data_origin[:]
		for origin, new in data:
			changes[elems.index(origin)] = new
		
		setr = [
			(elems[0], '"'+changes[0]+'"'),
			(elems[1], '"'+changes[1]+'"'),
			(elems[2], '"'+changes[2]+'"'),
			(elems[3], '"'+changes[3]+'"'),
			(elems[4], '"'+changes[4]+'"')
		]
		
		where  = 'idUser = '+idUser
		where += ' AND nodeP="'+data_origin[0]+'"'
		where += ' AND element="'+data_origin[1]+'"'
		where += ' AND permiso="'+data_origin[2]+'"'
		where += ' AND content="'+data_origin[3]+'"'
		where += ' AND path="'+data_origin[4]+'"'
		
		self.updateData('UserFiles', setr, where, verb=verb)
		
		if verb > 0:
			print('\n UserFiles \'{}\' updated successfully.'.format(data_origin[1]))
	
	# Elimina Todas las Filas del Usuario y las Vuelve a Crear Actualizadas.
	def updateUserFilesAll(self, con, verb=0):
		
		user = con.username
		
		query  = ['User', 'idUser', 'user = "{}"'.format(user)]
		idUser = str(self.getData(*query, c=1))
		
		elems   = ['nodeP', 'element', 'permiso', 'content', 'path']
		
		query = 'DELETE FROM UserFiles WHERE idUser='+idUser
		self.freeQuery(query, verb)
		
		files = con.getAllChilds(raw=True)
		data = [# Tabla,  Campos de la Tabla:
			'UserFiles', ['idUser','nodeP','element','permiso','content','path'],
			[	# Datos a cargar
				[
					idUser,
					vals['nodeP'],
					vals['element'],
					vals['permiso'],
					vals['content'],
					key
					
				] for key, vals in files.items()
			]
		]
		
		self.insertData(*data, verb=verb)
		
		if verb > 0:
			print('\n UserFiles \'{}\' updated successfully.'.format(user))
	
	def updateUserConfig(self, user, lis, verb=0):
		
		query  = ['User', 'idUser', 'user = "{}"'.format(user)]
		idUser = str(self.getData(*query, c=1))
		
		elems = [
			'song_vol',
			'song_pos',
			'l_canciones_activas',
			'l_comandos', 
			'l_com_ps',
			'con_tam_buffer',
			'cant_scroll'
		]
		
		lc_pos = elems.index('l_comandos')
		
		# ~ lis[lc_pos] = lis[lc_pos].replace('"',"___").replace("'","__")
		lis[lc_pos] = Helps.encode_bz2(lis[lc_pos])			# Comprime el texto con el Cifrado BZ2 y luego lo convierte a Hexadecimal.
		
		setr = [
			(elems[0], lis[0]),
			(elems[1], lis[1]),
			(elems[2], '"'+lis[2]+'"'),
			(elems[3], '"'+lis[3]+'"'),
			(elems[4], lis[4]),
			(elems[5], lis[5]),
			(elems[6], lis[6])
		]
		
		where  = 'idUser = '+idUser
		
		self.updateData('UserConfig', setr, where, verb=verb)
		
		if verb > 0:
			print('\n UserConfig \'{}\' updated successfully.'.format(user))
		elif verb > 1:
			print(lis)
	
	def orderUserFiles(self, verb=0):
		
		query = '''
			DROP TABLE IF EXISTS Temporal;
			CREATE TABLE Temporal AS SELECT * FROM UserFiles;
			DROP TABLE IF EXISTS UserFiles;
			CREATE TABLE IF NOT EXISTS UserFiles (
				idUserFiles INTEGER PRIMARY KEY AUTOINCREMENT,
				idUser INTEGER NOT NULL,
				nodeP TEXT NOT NULL,
				element TEXT NOT NULL,
				permiso TEXT NOT NULL,
				content TEXT NOT NULL,
				path TEXT NOT NULL,
				FOREIGN KEY(idUser) REFERENCES User(idUser)
			);
			INSERT INTO UserFiles (idUser, nodeP, element, permiso, content, path)
				SELECT idUser, nodeP, element, permiso, content, path 
				FROM Temporal ORDER BY idUser;
			DROP TABLE Temporal;
		'''
		
		self.freeQuery(query, verb)
	
	def createUser(self, con, verb=0):
		
		temp = [
			['logs', 'connection 2020-01-25_01-48-26.241195.log', '-r--', 'Connection 2020-01-25_01-48-26.241195', '010'],
			['logs', con.createLogFile('connection'), '-r--', con.createLogFile('Connection')[:-4], '011'],
			['bin', 'nueva', 'drwx', 'folder', '1000'],
			['config', 'chmod.txt', '-r--', Helps.Content.chmod, '000'],
			['config', 'permisos.txt', '-r--', Helps.Content.permisos, '001'],
			['bin', 'scan.exe', '-rwx', con.binary(), '1001']
		]
		con.fileSystemUpdate(temp)
		
		self.loadTables(verb)
		
		#===============================
		# Agregar Datos Base en la Tabla User:
		
		files = con.getAllChilds(raw=True)
		# ~ for key, val in con.getAllChilds().items():
			# ~ print(key, val)
		
		data = [
			# Tabla, Campos de la Tabla:
			'User', ['user','pass'],
			[	# Datos a cargar
				[con.username, con.password]
			]
		]
		self.insertData(*data, verb)
		
		idUser = self.getData('User','idUser','user="'+con.username+'"', c=1)
		# Agregar Datos Base en la Tabla User:
		datas = [
			[
				'System', # Tabla
				# Campos de la Tabla:
				['idUser','OS','USERNAME','COMPUTERNAME','NUMBER_OF_PROCESSORS',
				 'PROCESSOR_ARCHITECTURE','PROGRAMDATA','SESSIONNAME'],
				[	# Datos a cargar:
					[
						idUser,
						os.environ['OS'],
						os.environ['USERNAME'],
						os.environ['COMPUTERNAME'],
						os.environ['NUMBER_OF_PROCESSORS'],
						os.environ['PROCESSOR_ARCHITECTURE'],
						os.environ['PROGRAMDATA'],
						os.environ['SESSIONNAME']
					]
				]
			],[
				# Tabla, Campos de la Tabla:
				'Data', ['idUser','seed','ipPublic','ipPrivate'],
				[	# Datos a cargar
					[idUser, files['2']['content'], self.randomIP(0), self.randomIP(1)]
				]
			],[# Tabla, Campos de la Tabla:
				'UserFiles', ['idUser','nodeP','element','permiso','content','path'],
				[	# Datos a cargar
					[
						idUser,
						vals['nodeP'],
						vals['element'],
						vals['permiso'],
						vals['content'],
						key
						
					] for key, vals in files.items()
				]
			],[# Tabla, Campos de la Tabla:
				'UserConfig', ['idUser', 'song_vol', 'song_pos',
					'l_canciones_activas', 'l_comandos',
					'l_com_ps', 'con_tam_buffer', 'cant_scroll'],
				[	# Datos a cargar
					[ idUser, 20, 0, '[]', Helps.encode_bz2('[]'), 0, 150, 3 ]
				]
			]
		]
		
		for data in datas: self.insertData(*data, verb)
		
		self.con.commit()
		
		print('\n New User Create: '+con.username)
		
		return con
	
	def deleteUserAccount(self, username, verb=0):
		
		idUser = self.getData('User','idUser','user="'+username+'"', c=1)
		idUser = str(idUser)
		
		query  = 'DELETE FROM User          WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM System        WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM Data          WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM BotNet        WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM UserFiles     WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM HistoricalLog WHERE idUser='+idUser+';\n'
		query += 'DELETE FROM UserConfig    WHERE idUser='+idUser+';\n'
		
		self.freeQuery(query, verb)
	
	def loadTables(self, verb=0):
		
		datas = [
			[
				'User', {
				'idUser' :'INTEGER PRIMARY KEY AUTOINCREMENT',
				'user'   :'TEXT NOT NULL',
				'pass'   :'TEXT NOT NULL',
				'created':"DATETIME DEFAULT (datetime('now','localtime'))",
				'lastCon':"DATETIME DEFAULT (datetime('now','localtime'))"
				}, []
			],[
				'LenTables', {
				'idLenTables':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'tableName'  :'TEXT NOT NULL',
				'tableLen'   :'INTEGER NOT NULL'
				}, []
			],[
				'System', {
				'idSystem':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'  :'INTEGER NOT NULL',
				'OS'                    :'TEXT NOT NULL',
				'USERNAME'              :'TEXT NOT NULL',
				'COMPUTERNAME'          :'TEXT NOT NULL',
				'NUMBER_OF_PROCESSORS'  :'TEXT NOT NULL',
				'PROCESSOR_ARCHITECTURE':'TEXT NOT NULL',
				'PROGRAMDATA'           :'TEXT NOT NULL',
				'SESSIONNAME'           :'TEXT NOT NULL'
				}, ['User']
			],[
				'Data', {
				'idData'   :'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'   :'INTEGER NOT NULL',
				'seed'     :'TEXT NOT NULL',
				'ipPublic' :'TEXT NOT NULL',
				'ipPrivate':'TEXT NOT NULL'
				}, ['User']
			],[
				'BotNet', {
				'idBotNet':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'  :'INTEGER NOT NULL',
				'ipBot'   :'TEXT NOT NULL'
				}, ['User']
			],[
				'UserFiles', {
				'idUserFiles':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'     :'INTEGER NOT NULL',
				'nodeP'      :'TEXT NOT NULL',
				'element'    :'TEXT NOT NULL',
				'permiso'    :'TEXT NOT NULL',
				'content'    :'TEXT NOT NULL',
				'path'       :'TEXT NOT NULL'
				}, ['User']
			],[
				'HistoricalLog', {
				'idHistoricalLog':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'         :'INTEGER NOT NULL',
				'command'        :'TEXT NOT NULL',
				'content'        :'TEXT NOT NULL',
				'path'           :'TEXT NOT NULL',
				'created'        :"DATETIME DEFAULT (datetime('now','localtime'))"
				}, ['User']
			],[
				'UserConfig', {
				'idUserConfig'       :'INTEGER PRIMARY KEY AUTOINCREMENT',
				'idUser'             :'INTEGER NOT NULL',
				'song_vol'           :'INTEGER NOT NULL',
				'song_pos'           :'INTEGER NOT NULL',
				'l_canciones_activas':'TEXT NOT NULL',
				'l_comandos'         :'TEXT NOT NULL',
				'l_com_ps'           :'INTEGER NOT NULL',
				'con_tam_buffer'     :'INTEGER NOT NULL',
				'cant_scroll'        :'INTEGER NOT NULL',
				}, ['User']
			]
		]
		
		for data in datas: self.createTable(*data, verb)



#=======================================================================
#=======================================================================
#=======================================================================

def initDB(DBName, con):
	
	#===============================
	#======== Odin Database ========
	#===============================
	# Basic Data: ==================
	#===============================
	
	db = None
	verb = 0
	
	if not os.path.exists(DBName):
		
		db = Database(DBName)
		con = db.createUser(con, verb)
		
		data = [ # Tabla,      Campos de la Tabla:
			'LenTables', ['tableName','tableLen'],
			[	# Datos a cargar:
				['User',          3],
				['LenTables',     5],
				['System',        7],
				['Data',          4],
				['BotNet',        2],
				['UserFiles',     6],
				['HistoricalLog', 6]
			]
		]
		
		db.insertData(*data, verb)
		
	else:
		
		db = Database(DBName)
		user = db.getData('User')
		
		if not user: con = db.createUser(con, verb)
	
	if db:
		
		# ~ verb = 0
		
		# ~ print('\n User:', db.getData('User', verb=verb))
		
		idUser = db.getData('User','idUser','user="'+con.username+'"', c=1)
		
		if idUser:
			
			# Actualizar Ultima Conexion:
			db.updateUserConection(con.username)
			
			# Actualizar los Datos de Consola desde la DB.
			temp = [
				[ v[2], v[3], v[4], v[5], v[6] ]
				for v in db.getData('UserFiles', where='idUser='+str(idUser))
			]
			
			temp.pop(0)
			con.system = []
			con.fileSystemUpdate(temp)
			
			# Actualizar los Datos de Consola desde la DB.
			temp = [*db.getData('UserConfig', where='idUser='+str(idUser), c=1)[2:]]
			# ~ print(temp)
			exec('temp[2] = '+temp[2])
			# ~ exec('temp[3] = '+temp[3].replace('___','"').replace('__',"'"))
			exec('temp[3] = '+Helps.decode_bz2(temp[3]))
			con.temporal = temp
			# ~ print(con.temporal)
		else:
			con = db.createUser(con, verb)
	
	db.con.close()
	
	return con



# ~ from helps import Helps
# ~ from consola import Console
# ~ console = Console('Eny', 'xD')
# ~ initDB('dystopia.odin', console)
