import time
import psycopg2
import sys
from flask import Flask
from sensor.sensor import Sensor


app = Flask(__name__)
sensor = Sensor()


@app.route('/api/data/trigger')
def trigger():

        try:
                conn = psycopg2.connect("dbname='data' user='postgres' host='localhost' password='elephants<3oranges'")
                print "Connected!\n"
        except:
                print "I am unable to connect to the database"
        cur = conn.cursor()
        currenttime = time.strftime("%a %d %b %Y %H:%M:%S +0000", time.localtime())
        currentvalue = sensor.trigger_reading()
        cur.execute("INSERT into Measurements (datetime, value) values (\'%s\', %f)" % (currenttime, currentvalue))
        cur.execute("SELECT * FROM Measurements")
        print  cur.fetchall()
        conn.commit()
        return currenttime + '  :  ' + str(currentvalue)


if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')
