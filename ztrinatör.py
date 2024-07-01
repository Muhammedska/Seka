import os
import sys
import time
import pyautogui

from datetime import datetime
from img2pdf import convert
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.stdout = open('stdout.txt', 'w+', encoding="utf-8")

global UI_PATH, OP_PATH, SAVE_PATH, Current_X, Current_Y, TestFile

UI_PATH = "./UI/"
OP_PATH = "./data/"
SAVE_PATH = ""
Current_X = 0
Current_Y = 0
TestFile = ""
if os.path.isdir(OP_PATH) == False:
    os.mkdir(OP_PATH)
if os.path.isdir(OP_PATH + 'im/') == False:
    os.mkdir(OP_PATH + 'im/')

for a in os.listdir(OP_PATH+'im/'):
    os.remove(OP_PATH+'im/'+a)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_PATH + 'zmain.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.h = QtWidgets.QDesktopWidget().screenGeometry().height()
        self.w = QtWidgets.QDesktopWidget().screenGeometry().width()

        self.loca1 = QShortcut(QKeySequence("Ctrl+1"), self)
        self.loca1.activated.connect(self.saveloca1)

        self.loca2 = QShortcut(QKeySequence("Ctrl+2"), self)
        self.loca2.activated.connect(self.saveloca2)

        self.loca3 = QShortcut(QKeySequence("Ctrl+3"), self)
        self.loca3.activated.connect(self.saveloca3)

        self.click_test = QShortcut(QKeySequence("Ctrl+T"), self)
        self.click_test.activated.connect(self.clicktest)

        self.snapshot_test = QShortcut(QKeySequence("Ctrl+S"), self)
        self.snapshot_test.activated.connect(self.sstest)

        self.help.clicked.connect(self.helpwin)
        self.start.clicked.connect(self.operation_started)
        self.convert.clicked.connect(self.create_pdf)

        self.setMouseTracking(True)
        self.installEventFilter(self)

        # Create a timer to update the cursor position periodically
        self.timer = QTimer(self)
        self.timer.setInterval(1)  # Update every 100 milliseconds
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start()

    def update_cursor_position(self):
        global Current_Y, Current_X

        x = QCursor.pos().x()
        y = QCursor.pos().y()
        Current_X = x
        Current_Y = y
        self.mouselocation.setText(f"X: {x} , Y: {y}")

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseMove and
                event.buttons() == Qt.NoButton):
            pos = event.pos()
            self.mouselocation.setText(' %d : %d ' % (pos.x(), pos.y()))
            print()
        return QWidget.eventFilter(self, source, event)

    def mouseMoveEvent(self, event):
        x = QCursor.pos().x()
        y = QCursor.pos().y()

        self.mouselocation.setText(f"({x}, {y})")

    def saveloca1(self):

        self.x_loca_1.setText(str(Current_X))
        self.y_loca_1.setText(str(Current_Y))

    def saveloca2(self):

        self.x_loca_2.setText(str(Current_X))
        self.y_loca_2.setText(str(Current_Y))

    def saveloca3(self):

        self.m_loca_x.setText(str(Current_X))
        self.m_loca_y.setText(str(Current_Y))

    def helpwin(self):
        self.secwin = helpwin()
        self.secwin.show()

    def clicktest(self):
        sector_x, sector_y = int(self.m_loca_x.text()), int(self.m_loca_y.text())
        pyautogui.click(sector_x, sector_y)

    def click_located(self):
        sector_x, sector_y = int(self.m_loca_x.text()), int(self.m_loca_y.text())
        pyautogui.click(sector_x, sector_y)

    def sstest(self):
        global TestFile
        dates = datetime.now()
        # year month day hours munites second ms
        filename = OP_PATH + 'im/' + dates.strftime("%Y%m%d%H%M%S%f") + ".png"
        TestFile = filename
        x1, y1, x2, y2 = int(self.x_loca_1.text()), int(self.y_loca_1.text()), int(self.x_loca_2.text()), int(
            self.y_loca_2.text())

        self.progressout.appendPlainText(str(x1) + ' / ' + str(x2) + ' - ' + str(y1) + ' / ' + str(y2))
        self.progressout.appendPlainText('filename : ' + filename)
        self.progressout.appendPlainText('\n--\n')
        self.progressout.appendPlainText('snapshot test')
        left, top, width, height = 0,0,0,0
        if y1 > y2:
            top = y2
        if y2 > y1:
            top = y1
        if y1 == y2:
            top = y1

        if (y1 - y2) < 0:
            height = 0 - (y1 - y2)
        if (y1 - y2) >= 0:
            height = (y1 - y2)

        if x1 > x2:
            left = x2
        if x2 > x1:
            left = x1
        if x1 == x2:
            left = x1

        if (x1 - x2) < 0:
            width = 0 - (x1 - x2)
        if (x1 - x2) >= 0:
            width = (x1 - x2)
        self.progressout.appendPlainText(str(left)+' - '+ str(top)+' - '+ str(width)+' - '+ str(height))
        # screenshot = pyautogui.screenshot(region=())
        take_snapshot = pyautogui.screenshot(region=(left, top, width, height))
        take_snapshot.save(filename)

        self.secwin = ShowTestIm()
        self.secwin.show()

        self.progressout.appendPlainText('\n--\n')

    def take_screenshot(self):
        dates = datetime.now()
        # year month day hours munites second ms
        filename = OP_PATH + 'im/' + dates.strftime("%Y%m%d%H%M%S%f") + ".png"
        x1, y1, x2, y2 = int(self.x_loca_1.text()), int(self.y_loca_1.text()), int(self.x_loca_2.text()), int(
            self.y_loca_2.text())

        left, top, width, height = 0,0,0,0
        if y1 > y2:
            top = y2
        if y2 > y1:
            top = y1
        if y1 == y2:
            top = y1

        if (y1 - y2) < 0:
            height = 0 - (y1 - y2)
        if (y1 - y2) >= 0:
            height = (y1 - y2)

        if x1 > x2:
            left = x2
        if x2 > x1:
            left = x1
        if x1 == x2:
            left = x1

        if (x1 - x2) < 0:
            width = 0 - (x1 - x2)
        if (x1 - x2) >= 0:
            width = (x1 - x2)
        # screenshot = pyautogui.screenshot(region=())
        take_snapshot = pyautogui.screenshot(region=(left, top, width, height))
        take_snapshot.save(filename)

    def operation_started(self):
        delay = int(self.delay.text())
        repaet = int(self.pagecount.text())
        counter = 1
        if delay <= 0:
            delay = 1
        if repaet <= 0:
            repaet = 1

        while counter <= repaet:
            self.progressout.appendPlainText(str(counter) + ' / ' + str(repaet))

            self.take_screenshot()
            time.sleep(delay)
            self.click_located()
            self.progressout.appendPlainText('\n')
            self.progressout.appendPlainText('snapshot taken')
            self.progressout.appendPlainText('\n')

            counter += 1
        msgBox = QMessageBox()
        msgBox.information(self, "z-book scanning ended", "Your image files already created from that z book "+str(repaet)+' pages')

        self.progressout.appendPlainText('progress finished')
        self.progressout.appendPlainText('\n======\n')

    def create_pdf(self):
        pathx = OP_PATH+"im/"
        file = os.listdir(pathx)
        imlist = []
        for i in file:
            imlist.append(pathx+i)
        if len(imlist)>=0:
            filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            with open("exported_cozelti_software_"+filename+".pdf", "wb") as f:
                f.write(convert(imlist))

            msgBox = QMessageBox()
            msgBox.information(self,"pdf creation ended","Your image files already converted to pdf")
            for a in os.listdir(OP_PATH + 'im/'):
                os.remove(OP_PATH + 'im/' + a)
        else:
            msgBox = QMessageBox()
            msgBox.warning(self, "pdf creation error", "Your image files didn't found in ./data/im/")




class ShowTestIm(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        global TestFile
        self.h = QtWidgets.QDesktopWidget().screenGeometry().height()
        self.w = QtWidgets.QDesktopWidget().screenGeometry().width()
        self.setGeometry(int((self.w - 256) / 2), int((self.h - 256) / 2), 256, 256)
        self.setWindowIcon(QIcon(UI_PATH + "img/ztrinatör.png"))
        self.setWindowTitle('image test showing')
        layout = QVBoxLayout()
        self.pixmap = QPixmap(TestFile)

        self.label = QLabel("Another Window % d")
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)

        # Widget'ın boyutunu ayarlayın (genişlik veya yükseklik sabitlenebilir)
        self.label.resize(256, 256)  # 200 genişlik, 100 yükseklik
        self.label.setMaximumSize(256, 256)

        layout.addWidget(self.label)
        self.setLayout(layout)
        file_path = TestFile  # Replace with the actual file path

        try:
            os.remove(file_path)
            print("File deleted successfully!")
        except FileNotFoundError:
            print("File not found!")
        except PermissionError:
            print("You don't have permission to delete the file.")
        except OSError as e:
            print(f"Error deleting file: {e}")


class helpwin(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()

        self.h = QtWidgets.QDesktopWidget().screenGeometry().height()
        self.w = QtWidgets.QDesktopWidget().screenGeometry().width()
        self.setGeometry(int((self.w - 200) / 2), int((self.h - 200) / 2), 256, 256)
        self.setWindowIcon(QIcon(UI_PATH + "img/ztrinatör.png"))
        self.setWindowTitle('help')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()

        self.label = QLabel(
            "CTRL+1 for first location[X1:Y1]\nCTRL+2 for second location[X2:Y2]\nCTRL+3 for click location[Mx:My]\nCTRL+T for testing clicking\nCTRL+S for testing snapshot\n")

        # Widget'ın boyutunu ayarlayın (genişlik veya yükseklik sabitlenebilir)
        self.label.setGeometry(0, 0, 256, 256)  # 200 genişlik, 100 yükseklik
        self.label.setMaximumSize(256, 256)

        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
