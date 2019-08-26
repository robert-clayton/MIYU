from PySide2.QtWidgets import QApplication
from MIYU.MainWindow import MainWindow

app = QApplication()
window = MainWindow()
window.show()
app.exec_()