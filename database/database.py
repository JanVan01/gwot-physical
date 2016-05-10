import psycopg2
import psycopg2.extras

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='data' user='postgres' host='localhost' password='elephants<3oranges'")
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

    def get_last_measurement(self, filter):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        filterSql = self.build_filter(filter, "WHERE")
        cur.execute("SELECT * FROM Measurements " + filterSql + " ORDER BY id DESC LIMIT 1")
        return cur.fetchone();
    
    def get_measurement_list(self, filter):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        filterSql = self.build_filter(filter, "WHERE")
        cur.execute("SELECT * FROM Measurements " + filterSql + " ORDER BY id")
        return cur.fetchall();
    
    def get_min_measuremen(self, filter):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        filterSql = self.build_filter(filter, "WHERE")
        cur.execute("SELECT * FROM Measurements " + filterSql + " ORDER BY value ASC LIMIT 1")
        return cur.fetchone();
    
    def get_max_measurement(self, filter):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        filterSql = self.build_filter(filter, "WHERE")
        cur.execute("SELECT * FROM Measurements " + filterSql + " ORDER BY value DESC LIMIT 1")
        return cur.fetchone();
    
    def get_location_list(self):
        cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM Locations ORDER BY id")
        return cur.fetchall();

    def build_filter(self, args, prefix):
        conditions = []

        if args['outliers'] == 0:
            conditions.append("quality > 0.5") # ToDo: What is a good quality?

# ToDo
#        if args['start'] != None:
#            conditions.append("datetime >= " + args['start'])


#        if args['end'] != None:
#            conditions.append("datetime <= " + args['end'])

        if args['location'] != None:
            conditions.append("location = " + args['location'])

#        if args['coordinates'] != None:
#            conditions.append("location = " + args['coordinates'])
        
        if len(conditions) > 0:
            op = " AND ";
            return prefix + " " + op.join(conditions)
        else:
            return ""
        
        
