from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel

class ImageElement:
    url = Qt.DisplayRole
    image = Qt.UserRole+1
    response = Qt.UserRole+2

class ImageModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
    
    def __iter__(self):
        for idx in xrange(self.rowCount()):
            yield self.index(idx, 0)

    def iterPersist(self):
        for idx in xrange(self.rowCount()):
            yield QPersistentModelIndex(self.index(idx, 0))