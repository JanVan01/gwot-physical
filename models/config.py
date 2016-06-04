import configparser


class ConfigManager:
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../data/config.ini')

    def save_config(self):
        with open('config.ini', 'w') as c:
            self.config.write(c)

    def reset_default(self):
        self.config['Config'] = self.config['Default']
        self.save_config()

    def get_name(self):
        return self.config['Config']['name']

    def set_name(self, name):
        self.config['Config']['name'] = name
        self.save_config()

    def get_lat(self):
        return float(self.config['Config']['lat'])

    def set_lat(self, lat):
        try:
            self.config['Config']['lat'] = float(lat)
            self.save_config()
        except ValueError:
            raise

    def get_lon(self):
        return float(self.config['Config']['lon'])

    def set_lon(self, lon):
        try:
            self.config['Config']['lon'] = float(lon)
            self.save_config()
        except ValueError:
            raise

    def get_height(self):
        return float(self.config['Config']['height'])

    def set_height(self, height):
        try:
            self.config['Config']['height'] = float(height)
            self.save_config()
        except ValueError:
            raise

    def get_interval(self):
        return int(self.config['Config']['interval'])

    def set_interval(self, interval):
        try:
            self.config['Config']['interval'] = int(interval)
            self.save_config()
        except ValueError:
            raise

    def get_password(self):
        return self.config['Config']['password']

    def set_password(self, pw):
        self.config['Config']['password'] = pw
        self.save_config()
