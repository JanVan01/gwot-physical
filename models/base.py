import psycopg2.extras
from pprint import pformat

class BaseModel(object):

	def __init__(self, db, attrs = []):
		self.db = db
		self.attrs = attrs
		
	def __repr__(self):
		if len(self.attrs) == 0:
			return super().__repr__()

		data = {}
		for attr in self.attrs:
			data[attr] = getattr(self, attr)
		
		return self.__module__ + '.' + self.__class__.__name__ + ':' + pformat(data)
		
	def from_dict(self, dict):
		return
	
	def create(self):
		return
	
	def read(self):
		return
	
	def update(self):
		return
	
	def delete(self):
		return
		
	
class BaseMultiModel(object):

	def __init__(self, db):
		self.db = db
	
	def to_object_list(self, list):
		collection = []
		if list is not None:
			for entry in list:
				obj = self.to_object(entry)
				if obj is not None:
					collection.append(obj)
		return collection
	
	def to_object(self, data):
		obj = self.create()
		obj.from_dict(data)
		return obj

	def get(self, pk):
		obj = self.create(pk)
		if obj.read():
			return obj
		else:
			return None
	
	def create(self, pk = None):
		return None
		
	def _get_all(self, query, params = None):
		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute(query, params)
		if cur.rowcount > 0:
			return self.to_object_list(cur.fetchall())
		else:
			return []
	
	def _get_one(self, query, params = None):
		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute(query, params)
		if cur.rowcount > 0:
			return self.to_object(cur.fetchone())
		else:
			return None