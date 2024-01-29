
import csv
import os

#TODO ottimizzare la classe usando np array piuttosto che list
class Signal(object):
    def __init__(self, filePath = 'signal.csv', objectName = 'signal', len = 10000, flSavePath = True):
        self._signal = []
        self._objectName = objectName
        self._file = ''
        self._flSavePath = flSavePath
        self.setPath(filePath)
        self._len = len


    @property
    def file(self):
        return os.path.abspath(self._file)
#overload il metodo da un file
    def buildSignal(self, newData):
        self._signal = self._signal + [int(e) for e in newData]
        savingStatus = True
        if len(self._signal) > self._len:
            savingStatus = self.save()
            if savingStatus:
                self._signal = []
        return savingStatus

    def save(self):
        if self._flSavePath:
            try:
                f = open(self._file, 'r+')
                writer = csv.writer(f)
                for r in self._signal:
                    writer.writerows([[r]])
                f.close()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return True
    def getSignal(self, unsafe = False):
        if unsafe and self._flSavePath:
            with open(self._file, newline='') as f:
                reader = csv.reader(f)
                self._signal = [float(e[0]) for e in list(reader)]
        return self._signal

    def rmvMean(self):
        m = sum(self._signal) / len(self._signal)
        filtered = [e - m for e in self._signal]
        return filtered

    def clear(self):
        if self._flSavePath:
            with open(self._file, 'w'):
                pass
        self._signal = []

    def setPath(self, newPath):
        if self._flSavePath:
            try:
                self._file = newPath
                path = os.path.dirname(self._file)
                if path != '':
                    os.makedirs(os.path.dirname(self._file), exist_ok=True)
                if not os.path.exists(self._file):
                    with open(self._file, 'w'):
                        pass
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return True


if __name__ == "__main__":
    s = Signal(flSavePath=False)
    prova = [1, 2, 3, 4]
    for i in range(4):
        s.buildSignal(prova)
    print('segnale')
    print(s.getSignal(unsafe=True))


