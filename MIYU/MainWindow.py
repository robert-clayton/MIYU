import os
import requests
from PySide2.QtCore import Qt, QItemSelectionModel
from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListView, QApplication
from PySide2.QtGui import QPixmap, QStandardItemModel, QStandardItem
from MIYU.Yankers import randomImgurResponse, randomImgurResponses

class Image:
    url = Qt.DisplayRole
    image = Qt.UserRole+1
    data = Qt.UserRole+2

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
        self._viewer.setPixmap(index.data(role=Image.image))

    def _saveImage(self, response=None):
        # Saves the given response if any, else uses the image stored in the currently selected index
        if response:
            name, data = response.url.rsplit('/', 1)[-1], response.content
        else:
            item = self._linkHistoryView.selectionModel().selectedIndexes()[0]
            name = item.data(role=Image.url).rsplit('/', 1)[-1]
            data = item.data(role=Image.data)
        saveDirectory = './images'
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
        saveDirectory += '/' + name
        with open(saveDirectory, 'wb') as f:
            f.write(data)

    def _makeItem(self, response, maxWidth=700, maxHeight=700):
        # Creates an image item from the given url
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
        
        # Make item
        item = QStandardItem()
        item.setData(response.url, role=Image.url)
        item.setData(response.content, role=Image.data)
        item.setData(scaled, role=Image.image)
        
        return item

    def _newImage(self, response):
        # Creates a new image item, adds it to the model, then updates the view
        item = self._makeItem(response)
        self._linkHistoryModel.appendRow(item)
        self._linkHistoryView.selectionModel().select(self._linkHistoryModel.indexFromItem(item), QItemSelectionModel.ClearAndSelect)

        return item

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._newImage(randomImgurResponse())
        elif event.button() == Qt.RightButton:
            self._saveImage()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_R:
            for response in randomImgurResponses(10000):
                # newImageItem = self._newImage(response)
                # QApplication.processEvents()
                self._saveImage(response)