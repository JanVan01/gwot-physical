import psycopg2.extras
from models.base import BaseModel, BaseMultiModel

class Location(BaseModel):

	def __init__(self, db, id = None):
		super().__init__(db, ['id', 'name', 'lon', 'lat', 'height'])
		self.id = id
		self.name = None
		self.lon = None
		self.lat = None
		self.height = None

	def from_dict(self, dict):
		self.set_id(dict['id'])
		self.set_name(dict['name'])
		self.set_position(dict['lon'], dict['lat'])
		self.set_height(dict['height'])

	def create(self):
		if self.lon is None or self.lat is None or self.height is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("INSERT INTO Locations (name, geom, height) VALUES (%s, ST_GeomFromText(%s, 4326), %s) RETURNING id", [self.name, self.get_point_wkt(), self.height])
		data = cur.fetchone()
		self.id = data['id']
		if self.id > 0:
			return True
		else:
			return False

	def read(self):
		if self.id is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("SELECT *, ST_X(geom) AS lon, ST_Y(geom) AS lat FROM Locations WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False

	def update(self):
		if self.id is None or self.lon is None or self.lat is None or self.height is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("UPDATE Locations SET name = %s, geom = ST_GeomFromText(%s, 4326), height = %s WHERE id = %s", [self.name, self.get_point_wkt(), self.height, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False

	def delete(self):
		if self.id is None:
			return False

		cur = self.db.cursor()
		cur.execute("DELETE FROM Locations WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.id = None
			return True
		else:
			return False

	def get_id(self):
		return self.id

	def set_id(self, id):
		self.id = id

	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_position(self):
		return {
			'lon': self.lon,
			'lat': self.lat
		}

	def get_point_wkt(self):
		return "POINT(" + str(self.lon) + " " + str(self.lat) + ")"

	def get_longitude(self):
		return self.lon

	def get_latitude(self):
		return self.lat

	def set_position(self, lon, lat):
		self.lon = lon
		self.lat = lat

	def get_height(self):
		return self.height

	def set_height(self, height):
		self.height = height


class Locations(BaseMultiModel):

	def __init__(self, db):
		super().__init__(db)

	def create(self, pk = None):
		return Location(self.db, pk)

	def get_all(self):
		return self._get_all("SELECT *, ST_X(geom) AS lon, ST_Y(geom) AS lat FROM Locations ORDER BY id")
