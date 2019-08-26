import os
import requests
from PySide2.QtCore import Qt, QItemSelectionModel, QByteArray, QBuffer, QIODevice
from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListView, QApplication
from PySide2.QtGui import QPixmap, QStandardItemModel, QStandardItem, QMovie
from MIYU.Yankers import randomImgurResponse, randomImgurResponses

class Image:
    url = Qt.DisplayRole
    image = Qt.UserRole+1
    response = Qt.UserRole+2

class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self._linkHistoryModel = QStandardItemModel()
        self._linkHistoryView = QListView()
        self._viewer = QLabel()

        self._linkHistoryView.setFixedWidth(200)
        self._linkHistoryView.setModel(self._linkHistoryModel)

        self.setLayout(QHBoxLayout())
        self._innerLayout = QVBoxLayout()
        self.layout().addWidget(self._linkHistoryView)
        self.layout().addLayout(self._innerLayout)
        self._innerLayout.addWidget(self._viewer, alignment=Qt.AlignCenter)
        self._linkHistoryView.selectionModel().selectionChanged.connect(self._updateViewer)

        self._newImage(randomImgurResponse())

    def _updateViewer(self, selected, deselected):
        # Updates viewer
        index = selected.indexes()[0]
        response = index.data(role=Image.response)
        if not index.data(role=Image.image):
            pixmap = self._makeImage(response)
            self._linkHistoryModel.setData(index, pixmap, role=Image.image)
        
        # if response.headers['Content-Type'] == 'image/gif': #TODO: Find out why QMovie crashes with start()
        #     movie = index.data(role=Image.image)
        #     self._viewer.setMovie(movie)
        #     movie.start()
        # else:
        self._viewer.setPixmap(index.data(role=Image.image))

    def _saveImage(self, response=None):
        # Saves the given response if any, else uses the image stored in the currently selected index
        if response:
            name, data = response.url.rsplit('/', 1)[-1], response.content
        else:
            item = self._linkHistoryView.selectionModel().selectedIndexes()[0]
            name = item.data(role=Image.url).rsplit('/', 1)[-1]
            data = item.data(role=Image.response).content
        saveDirectory = './images'
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
        saveDirectory += '/' + name
        with open(saveDirectory, 'wb') as f:
            f.write(data)

    def _makeImage(self, response, maxWidth=700, maxHeight=700):
        # Makes an image for the given response
        # if response.headers['Content-Type'] == 'image/gif':
        #     byteArray = QByteArray(response.content)
        #     buffer = QBuffer(byteArray)
        #     buffer.open(QIODevice.ReadOnly)
        #     mov = QMovie(buffer, b'GIF')
        #     mov.setCacheMode(QMovie.CacheAll)
        #     mov.setSpeed(100)
        #     return mov

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        width, height = pixmap.width(), pixmap.height()
        if width > height and width > maxWidth:
            dx = maxWidth / width
            width = min(width, maxWidth)
            height *= dx
        elif height > width and height > maxHeight:
            dy = maxHeight / height
            height = min(height, maxHeight)
            width *= dy
        elif height == width:
            width = height = maxWidth
        scaled = pixmap.scaled(width, height, transformMode=Qt.SmoothTransformation)

        return scaled

    def _makeItem(self, response, defer=False):
        # Creates an image item from the given response
        item = QStandardItem()
        item.setData(response.url, role=Image.url)
        item.setData(response, role=Image.response)
        if not defer:
            item.setData(self._makeImage(response), role=Image.image)
        
        return item

    def _newImage(self, response, defer=False):
        # Creates a new image item, adds it to the model, then updates the view
        item = self._makeItem(response, defer=defer)
        self._linkHistoryModel.appendRow(item)
        self._linkHistoryView.selectionModel().select(self._linkHistoryModel.indexFromItem(item), QItemSelectionModel.ClearAndSelect)

        return item

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._newImage(randomImgurResponse(), defer=True)
        elif event.button() == Qt.RightButton:
            self._saveImage()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_R:
            for response in randomImgurResponses(10000):
                # newImageItem = self._newImage(response)
                # QApplication.processEvents()
                self._saveImage(response)