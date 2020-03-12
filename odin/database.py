
# By: LawlietJH
# Odyssey in Dystopia

from datetime import datetime
from .helps import Helps

import threading
import sqlite3
import random
import os

TITULO  = 'Odyssey in Dystopia'
__version__ = 'v1.2.1'

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
		
		self.cur.execute(query)
		if c == 0:
			rows = self.cur.fetchall()
		elif c == 1:
			rows = self.cur.fetchone()
			if len(rows) == 1: rows = rows[0]
		else:
			rows = self.cur.fetchmany(c)
		
		if verb > 0:
			print('\n \'{}\' Information displayed successfully.'.format(table))
		elif verb > 1:
			print('\n' + query + '\n')
		
		return rows
	
	def updateData(self, table, update, where='', verb=0):
		
		base  = 'UPDATE {}'.format(table)
		setr  = 'SET ' + ', '.join(['{}={}'.format(row, up) for row, up in update])
		where = 'WHERE {}'.format(where) if where else ''
		
		query = '{} {} {};'.format(base, setr, where)
		
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
	
	def updateUserFiles(self, data, con, elements, verb=0):
		
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
		
		self.updateData('UserFiles', setr, where)
		
		if verb > 0:
			print('\n UserFiles \'{}\' updated successfully.'.format(data_origin[1]))
	
	def loadTables(self, verb=0):
		
		datas = [
			[
				'LenTables', {
				'idLenTables':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'tableName'  :'TEXT NOT NULL',
				'tableLen'   :'INTEGER NOT NULL'
				}, []
			],[
				'System', {
				'idSystem':'INTEGER PRIMARY KEY AUTOINCREMENT',
				'OS'                    :'TEXT NOT NULL',
				'USERNAME'              :'TEXT NOT NULL',
				'COMPUTERNAME'          :'TEXT NOT NULL',
				'NUMBER_OF_PROCESSORS'  :'TEXT NOT NULL',
				'PROCESSOR_ARCHITECTURE':'TEXT NOT NULL',
				'PROGRAMDATA'           :'TEXT NOT NULL',
				'SESSIONNAME'           :'TEXT NOT NULL'
				}, []
			],[
				'User', {
				'idUser' :'INTEGER PRIMARY KEY AUTOINCREMENT',
				'user'   :'TEXT NOT NULL',
				'pass'   :'TEXT NOT NULL',
				'created':"DATETIME DEFAULT (datetime('now','localtime'))",
				'lastCon':"DATETIME DEFAULT (datetime('now','localtime'))"
				}, []
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
				'content'    :'TEXT NOT NULL',
				'permiso'    :'TEXT NOT NULL',
				'path'       :'TEXT NOT NULL'
				}, ['User']
			]
		]
		
		for data in datas: self.createTable(*data, verb)



def initDB(DBName, con):
	
	#===============================
	#======== Odin Database ========
	#===============================
	# Basic Data: ==================
	#===============================
	
	db = None
	verb = 0
	
	if not os.path.exists(DBName):
		
		temp = [
			['logs', 'connection 2020-01-25_01-48-26.241195.log', '-r--', 'Connection 2020-01-25_01-48-26.241195', '010'],
			['logs', con.createLogFile('connection'), '-r--', con.createLogFile('Connection')[:-4], '011'],
			['bin', 'nueva', 'drwx', 'folder', '1000'],
			['config', 'chmod.txt', '-r--', Helps.chmod_content, '000'],
			['config', 'permisos.txt', '-r--', Helps.permisos_content, '001'],
			['bin', 'scan.exe', '-rwx', con.binary(), '1001']
		]
		con.fileSystemUpdate(temp)
		
		db = Database(DBName)
		db.loadTables(verb)
		datas = [
			[
				'LenTables', # Tabla
				# Campos de la Tabla:
				['tableName','tableLen'],
				[	# Datos a cargar:
					['LenTables', 5],
					['System',    7],
					['User',      3],
					['Data',      4],
					['BotNet',    2],
					['UserFiles', 6]
				]
			],[
				'System', # Tabla
				# Campos de la Tabla:
				['OS','USERNAME','COMPUTERNAME','NUMBER_OF_PROCESSORS',
				 'PROCESSOR_ARCHITECTURE','PROGRAMDATA','SESSIONNAME'],
				[	# Datos a cargar:
					[
						os.environ['OS'],
						os.environ['USERNAME'],
						os.environ['COMPUTERNAME'],
						os.environ['NUMBER_OF_PROCESSORS'],
						os.environ['PROCESSOR_ARCHITECTURE'],
						os.environ['PROGRAMDATA'],
						os.environ['SESSIONNAME']
					]
				]
			]
		]
		
		for data in datas: db.insertData(*data, verb)
		
		db.con.commit()
		
		#===============================
		# Agregar Datos Base en la Tabla User:
		
		files = con.getAllChilds()
		# ~ for key, val in files.items():
			# ~ print(key, val)
		
		data = [
			# Tabla, Campos de la Tabla:
			'User', ['user','pass'],
			[	# Datos a cargar
				[con.username,'xD']
			]
		]
		db.insertData(*data, verb)
		
		idUser = db.getData('User','idUser','user="'+con.username+'"', c=1)
		# Agregar Datos Base en la Tabla User:
		datas = [
			[
				# Tabla, Campos de la Tabla:
				'Data', ['idUser','seed','ipPublic','ipPrivate'],
				[	# Datos a cargar
					[1, files['2']['element'], db.randomIP(0), db.randomIP(1)]
				]
			],[# Tabla, Campos de la Tabla:
				'UserFiles', ['idUser','nodeP','element','content','permiso','path'],
				[	# Datos a cargar
					[
						idUser,
						'' if key == '' else ( 'root' if len(key)==1 else (
								con.getChild([int(_) for _ in key[:-1]]).element
							)
						),
						vals['element'],
						vals['content'],
						vals['permiso'],
						key
						
					] for key, vals in files.items()
				]
			]
		]
		
		for data in datas: db.insertData(*data, verb)
		db.con.commit()
		
	else:
		
		db = Database(DBName)
		
		# ~ try:
		user = db.getData('User')
		if not user:
			db.cur.close()
			db = None
			try:
				os.remove(DBName)
				raise TypeError('\nDatos Corruptos: '+DBName+'. Eliminado.')
			except: raise TypeError('\nDatos Corruptos: '+DBName)
		# ~ except:
			# ~ db.cur.close()
			# ~ db = None
			# ~ try:
				# ~ os.remove(DBName)
				# ~ raise TypeError('\nDatos Corruptos: '+DBName+'. Eliminado.')
			# ~ except: raise TypeError('\nDatos Corruptos: '+DBName)
	
	if db:
		
		# ~ verb = 0
		
		# ~ print('\n User:', db.getData('User', verb=verb))
		
		# Actualizar Ultima Conexion:
		db.updateUserConection(con.username)
		
		# ~ ['bin', 'scan.exe', 'rwx', con.binary()]
		idUser = str(db.getData('User','idUser','user="'+con.username+'"', c=1))
		# Actualizar los Datos de Consola desde la DB.
		temp = [
			[ v[2], v[3], v[5], v[4], v[6] ] for v in db.getData('UserFiles', where='idUser='+idUser)
		]
		
		temp.pop(0)
		con.system = []
		con.fileSystemUpdate(temp)
		
	return db, con

# ~ from helps import Helps
# ~ from consola import Console
# ~ console = Console('Eny', 'xD')
# ~ initDB('dystopia.odin', console)
