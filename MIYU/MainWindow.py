import os
import requests
from PySide2.QtCore import Qt, QItemSelectionModel
from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListView
from PySide2.QtGui import QPixmap, QStandardItemModel, QStandardItem
from MIYU.Yankers import randomImage

class Image:
    url = Qt.DisplayRole
    image = Qt.UserRole+1
    scaled = Qt.UserRole+2
    data = Qt.UserRole+3

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

        self._newImage()

    def _updateViewer(self, selected, deselected):
        # Updates viewer
        self._viewer.setPixmap(selected.indexes()[0].data(role=Image.scaled))

    def _saveImage(self):
        # Saves the image stored in the currently selected index
        item = self._linkHistoryView.selectionModel().selectedIndexes()[0]
        saveDirectory = './images'
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
        saveDirectory += '/' + item.data(role=Image.url).rsplit('/', 1)[-1]
        with open(saveDirectory, 'wb') as f:
            f.write(item.data(role=Image.data))

    def _newImage(self, maxWidth=700, maxHeight=700):
        # Creates a new image item, adds it to the model, then updates the view
        url = randomImage()
        data = requests.get(url).content
        pixmap = QPixmap()
        pixmap.loadFromData(data)

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
        item.setData(url, role=Image.url)
        item.setData(data, role=Image.data)
        item.setData(pixmap, role=Image.image)
        item.setData(scaled, role=Image.scaled)

        # Add to model and select in the selection model
        self._linkHistoryModel.appendRow(item)
        self._linkHistoryView.selectionModel().select(self._linkHistoryModel.indexFromItem(item), QItemSelectionModel.ClearAndSelect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._newImage()
        elif event.button() == Qt.RightButton:
            self._saveImage()
