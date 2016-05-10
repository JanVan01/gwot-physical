import psycopg2
import psycopg2.extras

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='data' user='postgres' host='localhost' password=''")
            self.connection.autocommit = True # We might want to remove that and switch to transactions
        except:
            self.connection = None
            print "I am unable to connect to the database.\n"
    
    def save_measurement(self, value, location):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("INSERT INTO Measurements (value, location) VALUES (%s, %s) RETURNING id", (value, location)) # Datetime is added by PostgreSQL
        last_id = cur.fetchone()['id'];
        cur.execute("SELECT * FROM Measurements WHERE id = %s", [last_id])
        data = cur.fetchone();
        return data;

    def get_last_measurement(self):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM Measurements ORDER BY id DESC LIMIT 1")
        return cur.fetchone();
    
    def get_measurement_list(self):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM Measurements ORDER BY datetime, id")
        return cur.fetchall();
    
    def get_min_measuremen(self):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM Measurements ORDER BY value ASC LIMIT 1")
        return cur.fetchone();
    
    def get_max_measurement(self):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM Measurements ORDER BY value DESC LIMIT 1")
        return cur.fetchone();
