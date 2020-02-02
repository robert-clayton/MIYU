import requests
import string
import random
from PySide2.QtCore import QObject, QThread, Signal, QSettings

class _AsyncRequestManager(QObject):
    totalRequestsChanged = Signal(int)
    finishedRequestsChanged = Signal(int)
    activeRequestsChanged = Signal(int)
    responseReceived = Signal(object)
    badResponseReceived = Signal(object)

    def __init__(self):
        super().__init__()
        self._activeRequests = []
        self._totalRequests = QSettings().value('managers/totalRequests', 0)
        self._finishedRequests = QSettings().value('managers/finishedRequests', 0)

    def downloadRequest(self, url=None, random=False):
        newRequest = _Request(url=url, random=random)
        self._activeRequests.append(newRequest)
        self._totalRequests += 1

        self.totalRequestsChanged.emit(self._totalRequests)
        self.activeRequestsChanged.emit(len(self._activeRequests))
        newRequest.responseReceived.connect(self._handleResponse)
        newRequest.done.connect(self._handleRequestFinished)
        newRequest.start()
    def _handleResponse(self, response):
        if response.ok:
            self.responseReceived.emit(response)
        else:
            self.badResponseReceived.emit(response)

    def _handleRequestFinished(self, request):
        self._finishedRequests += 1
        self.finishedRequestsChanged.emit(self._finishedRequests)
        self._activeRequests.remove(request)
        self.activeRequestsChanged.emit(len(self._activeRequests))

class _Request(QThread):
    responseReceived = Signal(object)
    done = Signal(object)

    def __init__(self, url=None, random=False):
        super().__init__()
        self._random = random
        self._url = url

    def run(self):
        if not self._random:
            response = requests.get(self._url)
        else:
            chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
            while True:
                randString = ''.join(random.choice(chars) for _ in range(5))
                url = f'http://i.imgur.com/{randString}.png'
                response = requests.get(url)
                contentType = response.headers['Content-Type']
                if len(response.content) != 503:
                    if contentType == 'image/jpeg':
                        response.url = url.replace('png', 'jpg')
                        break
                    elif contentType == 'image/gif':
                        response.url = url.replace('png', 'gif')
                        break

        self.responseReceived.emit(response)
        self.done.emit(self)
        

AsyncRequestManager = _AsyncRequestManager()