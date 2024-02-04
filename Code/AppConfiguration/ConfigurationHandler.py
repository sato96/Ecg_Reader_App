import json
import ipaddress


class ConfigurationHandler:
    @staticmethod
    def saveConfiguration(filePath, parameter, newValue):
        conf = configuration(filePath, "generalConfigurations")
        response = conf.setParam(parameter, newValue)
        return response

    @staticmethod
    def getConfiguration(filePath, parameter):
        conf = configuration(filePath, "generalConfigurations")
        config = conf.getParam(parameter)
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

class configuration(object):
    def __init__(self, path, typo = "root"):
        self._path = path
        self._typo = typo
        with open(self._path, 'r') as f:
            if typo != 'root':
                self._conf = json.load(f)[typo]
            else:
                self._conf = json.load(f)[typo]
    @property
    def typo(self):
        return self._typo

    def setParam(self, param, newvalue):
        beSet = self.getParam(param, False)
        if self._checkValueType(beSet["type"], newvalue):
            beSet['value'] = newvalue
            index = [i for i,_ in enumerate(self._conf) if _['code'] == param][0]
            self._conf[index] = beSet
            response = self._save()
        else:
            response = False
        return response
    def _save(self):
        try:
            with open(self._path, 'r') as f:
                db = json.load(f)
            if self._typo != 'root':
                db[self._typo] = self._conf
            else:
                db.update(self._conf)
            with open(self._path, 'w') as f:
                json.dump(db, f, indent=4)
            return True
        except Exception as e:
            print(e)
            return False

    def _checkValueType(self, typo, value):
        if typo == "ip":
            try:
                valList = value.split(':')
                ipaddress.ip_address(valList[0])
                response = True
            except:
                response = False
        elif typo == value.__class__.__name__:
            response = True
        else:
            response = False
        return response

    def getParam(self, param = None, onlyValue = True):
        if param is not None:
            result = list(filter(lambda c: c['code'] == param, self._conf))[0]
            result = result['value'] if onlyValue else result
        else:
            result = self._conf
        return result

    def setInt(self):
        pass

