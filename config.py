import configparser


class ConfigManager:
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def saveConfig(self):
        with open('config.ini', 'w') as c:
            self.config.write(c)

    def resetDefault(self):
        self.config['Config'] = self.config['Default']
        self.saveConfig()

    def getName(self):
        return self.config['Config']['name']

    def setName(self, name):
        self.config['Config']['name'] = name
        self.saveConfig()

    def getLat(self):
        return float(self.config['Config']['lat'])

    def setLat(self, lat):
        try:
            self.config['Config']['lat'] = float(lat)
            self.saveConfig()
        except ValueError:
            raise

    def getLon(self):
        return float(self.config['Config']['lon'])

    def setLon(self, lon):
        try:
            self.config['Config']['lon'] = float(lon)
            self.saveConfig()
        except ValueError:
            raise

    def getHeight(self):
        return float(self.config['Config']['height'])

    def setHeight(self, height):
        try:
            self.config['Config']['height'] = float(height)
            self.saveConfig()
        except ValueError:
            raise

    def getInterval(self):
        return int(self.config['Config']['interval'])

    def setInterval(self, interval):
        try:
            self.config['Config']['interval'] = int(interval)
            self.saveConfig()
        except ValueError:
            raise

    def setPassword(self, pw):
        self.config['Config']['password'] = pw
        self.saveConfig()
