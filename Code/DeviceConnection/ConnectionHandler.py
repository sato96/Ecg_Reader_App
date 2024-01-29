
import socket
import threading
from Code.SignalProcessing.Signal import Signal
import time
class SocketConnection(object):
    def __init__(self, host, port, saveDir):
        self.host = host
        self.port = port
        self._isRecording = False
        self._buffer = Signal(flSavePath=False)
        self._signal = Signal()
        self._saveDir = saveDir

    def _record(self):
        name = self._saveDir + 'ecg_' + str(time.time()).replace('.', '_') + '.csv'
        self._signal.setPath(name)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(
                b'GET /ecg HTTP/1.1\r\nHost:' + self.host.encode() + b'\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n')
            while self._isRecording:
                data = s.recv(1024)
                a = data
                d = a.decode().split('\n')
                print(d)
                d.remove('')
                self._signal.buildSignal(d)
                self._buffer.buildSignal(d)
                #build un buffer signal e puliscilo ogni 250 campioni
    def stopRecording(self):
        if self._isRecording:
            self._isRecording = False

    def startRecording(self):
        if not self._isRecording:
            self._isRecording = True
            t0 = threading.Thread(target=self._record)
            t0.start()

    def getSignal(self):
        self._signal.save()
        return self._signal

    def getBuffer(self):
        tmp = self._buffer.getSignal(unsafe=True)
        self._buffer.clear()
        return tmp



