import json


class ConfigurationHandler:
    @staticmethod
    def saveConfiguration(filePath, parameter, newValue):
        try:
            with open(filePath, 'r') as f:
                config = json.load(f)
            with open(filePath, 'w') as f:
                config[parameter] = newValue
                print(config)
                json.dump(config, f)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def getConfiguration(filePath):
        config = {}
        try:
            with open(filePath, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(e)
        return config

    @staticmethod
    def saveConfigurations(filePath, config):
        try:
            with open(filePath, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            print(e)
            return False
