from PySide2.QtWidgets import QApplication
from miyu.Frontend.MainWindow import MainWindow

app = QApplication()
app.setOrganizationName('Ziru\'s Musings')
app.setOrganizationDomain('https://www.zirusmusings.com/')
app.setApplicationName('miyu - My Internet Yanking Unicorn')
window = MainWindow()
window.show()
app.exec_()