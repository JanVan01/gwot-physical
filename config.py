import configparser

#TODO fix datatype errors when getting stuff that is not a number


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
        self.config['Config']['lat'] = lat
        self.saveConfig()

    def getLon(self):
        return float(self.config['Config']['lon'])

    def setLon(self, lon):
        self.config['Config']['lon'] = lon
        self.saveConfig()

    def getHeight(self):
        return float(self.config['Config']['height'])

    def setHeight(self, height):
        self.config['Config']['height'] = height
        self.saveConfig()

    def getInterval(self):
        return int(self.config['Config']['interval'])

    def setInterval(self, interval):
        self.config['Config']['interval'] = interval
        self.saveConfig()

    def setPassword(self, pw):
        self.config['Config']['password'] = pw
        self.saveConfig()
