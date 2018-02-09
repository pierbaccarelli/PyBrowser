import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from bs4 import BeautifulSoup


def render(url):
    """Outputs pure HTML from a url"""

    class Render(QWebEngineView):
        def __init__(self, url):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            # self.setHtml(html)
            self.load(QUrl(url))
            self.app.exec_()

        def _loadFinished(self, result):
            # This is an async call, you need to wait for this
            # to be called before closing the app
            self.page().toHtml(self._callable)

        def _callable(self, data):
            self.html = data
            # Data has been stored, it's safe to quit the app
            self.app.quit()

    return Render(url).html


class Ui_MainWindow(object):

    def __init__(self):
        self.html = None
        self.url = "http://www.facebook.com/"

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # MAIN WINDOW

        # CREATE CENTRAL WIDGET
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # CREATE GRID LAYOUT
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # CREATE WEB VIEW
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        # ON LOAD FINISHED, RETURN SOURCE
        self.webView.loadFinished.connect(self.return_source)
        # SET URL OF PAGE
        self.webView.setUrl(QtCore.QUrl(self.url))
        self.webView.setObjectName("webView")

        # ADD WEB VIEW TO GRID LAYOUT
        self.gridLayout.addWidget(self.webView)

        # SET MAIN WINDOW CENTRAL WIDGET TO SELF.CENTRALWIDGET
        MainWindow.setCentralWidget(self.centralwidget)

        # CREATE TOOLBAR
        self.locationEdit = QLineEdit(MainWindow)
        self.locationEdit.setSizePolicy(QSizePolicy.Expanding,
                                        self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.change_location)

        toolBar = MainWindow.addToolBar("Navigation")
        toolBar.addAction(self.webView.pageAction(QWebEnginePage.Back))
        toolBar.addAction(self.webView.pageAction(QWebEnginePage.Forward))
        toolBar.addAction(self.webView.pageAction(QWebEnginePage.Reload))
        toolBar.addAction(self.webView.pageAction(QWebEnginePage.Stop))
        toolBar.addWidget(self.locationEdit)

        viewMenu = MainWindow.menuBar().addMenu("&Tools")
        viewSourceAction = QAction("Source Scan", MainWindow)
        viewSourceAction.triggered.connect(self.return_source)
        viewMenu.addAction(viewSourceAction)

        # ADD STATUS BAR TO MAIN WINDOW
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # RETRANSLATE UI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_location(self):
        self.url = QUrl.fromUserInput(self.locationEdit.text())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def return_source(self):
        # print(html)
        print("render btn pressed")
        html = self.webView.page().toHtml(self._callable)

    def _callable(self, data):
        self.html = data
        print(self.html)
        print("-----HTML OUTPUTTED-----")
        self.beautiful_soup()

    def beautiful_soup(self):
        print("Reading HTML...")
        soup = BeautifulSoup(self.html, 'html.parser')
        print('title is %r' % soup.select_one('title').text)

        links = 0
        for link in soup.find_all('a'):
            links += 1

        s = "Links: "
        print(s + str(links))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

