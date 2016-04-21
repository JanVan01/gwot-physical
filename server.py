import time
from flask import Flask
from sensor import sensor


app = Flask(__name__)


@app.route('/api/data/trigger')
def trigger():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()) + '  :  ' + str(sensor.trigger_reading())

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
