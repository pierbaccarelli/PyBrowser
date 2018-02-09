from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from bs4 import BeautifulSoup
import time

class MainWindow(QMainWindow):
    def __init__(self, url):
        super(MainWindow, self).__init__()

        self.progress = 0
        self.html = None
        self.start_time = time.time()

        self.view = QWebEngineView(self)
        self.view.load(url)
        self.view.loadFinished.connect(self.finish_loading)
        self.view.titleChanged.connect(self.adjust_title)
        self.view.loadProgress.connect(self.set_progress)

        self.locationEdit = QLineEdit(self)
        self.locationEdit.setSizePolicy(QSizePolicy.Expanding,
                                        self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.change_location)

        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Back))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Forward))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Reload))
        toolBar.addAction(self.view.pageAction(QWebEnginePage.Stop))
        toolBar.addWidget(self.locationEdit)

        viewMenu = self.menuBar().addMenu("&Tools")
        viewSourceAction = QAction("Source Scan", self)
        viewSourceAction.triggered.connect(self.return_source)
        viewMenu.addAction(viewSourceAction)

        self.setCentralWidget(self.view)

    def adjust_location(self):
        self.locationEdit.setText(self.view.url().toString())

    def change_location(self):
        url = QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()

    def adjust_title(self):
        if 0 < self.progress < 100:
            self.setWindowTitle("%s (%s%%)" % (self.view.title(), self.progress))
        else:
            self.setWindowTitle(self.view.title())

    def set_progress(self, p):
        self.progress = p
        self.adjust_title()

    def started_loading(self):
        print("new page loading...")

    def finish_loading(self):
        self.progress = 100
        self.adjust_title()
        self.adjust_location()
        self.return_source()

    def return_source(self):
        html = self.view.page().toHtml(self._callable)

    def _callable(self, data):
        self.html = data
        self.beautiful_soup()

    def beautiful_soup(self):
        print("Scanning HTML...")
        soup = BeautifulSoup(self.html, 'html.parser')
        print('title is %r' % soup.select_one('title').text)

        links = 0
        for link in soup.find_all('a'):
            links += 1

        s = "Links: "
        print(s + str(links))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        url = QUrl(sys.argv[1])
    else:
        url = QUrl('http://www.facebook.com/')

    browser = MainWindow(url)
    browser.show()

    sys.exit(app.exec_())