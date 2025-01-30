import os, sys, time,pyautogui, asyncio, json,cv2, subprocess
import  numpy as np

from PIL import Image
from datetime import datetime
from img2pdf import convert
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *

err_FILE = open("stdout.txt","r+",encoding="UTF-8")
if os.path.exists("./system.json"):
    pass
else:
    err_FILE.write("kaynak dosya bulunamadı")
    backup = '{"res_mode":false,"resulation_up": 4,"CUR_UI": "vertical.ui","AI": "cpu","UI_DIR": "./UI/","OP_PATH": "./data/","IM_PATH":"./data/im/","PDF_PATH": "./created","Version": "1.1 NIGHT"}'
    open("./system.json","a").write(backup)
    err_FILE.write("sistem ayar dosyası oluşturuldu")

try:
    with open('system.json', 'r') as f:
        data = json.load(f)

except FileNotFoundError:
    err_FILE.write("Dosya bulunamadı.")
except json.JSONDecodeError:
    err_FILE.write("JSON verileri hatalı.")
global clickmemory

UI_PATH = data['UI_DIR']
UI_MODE = data['CUR_UI']
OP_PATH = data['OP_PATH']
RES_UP = data['resulation_up']
RES_MODE = data['res_mode']
clickmemory = {
    "x1":0,
    "x2":0,
    "y1":0,
    "y2":0,
    "cx":0,
    "cy":0
}
if not os.path.exists(OP_PATH):
    os.mkdir(OP_PATH)
if not os.path.exists(OP_PATH+'pre'):
    os.mkdir(OP_PATH+'pre')
if not os.path.exists(OP_PATH + 'im'):
    os.mkdir(OP_PATH + 'im')
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_PATH + UI_MODE, self)
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

        self.start_sistem = QShortcut(QKeySequence("Ctrl+4"), self)
        self.start_sistem.activated.connect(self.operation_started)

        self.start_sistem_pdf = QShortcut(QKeySequence("Ctrl+5"), self)
        self.start_sistem_pdf.activated.connect(self.create_pdf)

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
    def update_saveloca(self):
        text = f"X1:{clickmemory['x1']}\nY1:{clickmemory['y1']} \nX2:{clickmemory['x2']} \nY2:{clickmemory['y2']}\nCX:{clickmemory['cx']}\nCY:{clickmemory['cy']}"
        self.locations.setText(text)
    def saveloca1(self):
        clickmemory["x1"] = Current_X
        clickmemory["y1"] = Current_Y
        self.update_saveloca()
    def saveloca2(self):

        clickmemory["x2"] = Current_X
        clickmemory["y2"] = Current_Y
        self.update_saveloca()

    def saveloca3(self):
        clickmemory["cx"] = Current_X
        clickmemory["cy"] = Current_Y
        self.update_saveloca()
    def helpwin(self):
        self.secwin = helpwin()
        self.secwin.show()

    def clicktest(self):
        sector_x, sector_y = clickmemory["cx"], clickmemory["cy"]
        pyautogui.click(sector_x, sector_y)

    def click_located(self):
        sector_x, sector_y = clickmemory["cx"], clickmemory["cy"]
        pyautogui.click(sector_x, sector_y)

    def sstest(self):
        global TestFile
        dates = datetime.now()
        # year month day hours munites second ms
        filename = OP_PATH + 'im/' + dates.strftime("%Y%m%d%H%M%S%f") + ".png"
        TestFile = filename
        x1, y1, x2, y2 = clickmemory["x1"], clickmemory["y1"], clickmemory["x2"], clickmemory["y2"]

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

        self.secwin = ShowTestIm()
        self.secwin.show()


    def take_screenshot(self):
        dates = datetime.now()
        # year month day hours munites second ms
        filename = OP_PATH + 'im/' + dates.strftime("%Y%m%d%H%M%S%f") + ".png"
        x1, y1, x2, y2 = clickmemory["x1"], clickmemory["y1"], clickmemory["x2"], clickmemory["y2"]

        left, top, width, height = 0, 0, 0, 0
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

    async def process_images(self):  # Make this an async function
        delay = int(self.delay.text())
        repeat = int(self.pagecount.text())  # Corrected typo: repaet to repeat
        counter = 1

        delay = max(1, delay)  # Simplified: max() returns the larger of the two values
        repeat = max(1, repeat)  # Simplified: max() returns the larger of the two values
        x1, y1, x2, y2 = clickmemory["x1"], clickmemory["y1"], clickmemory["x2"], clickmemory["y2"]

        left, top, width, height = 0, 0, 0, 0
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

        while counter <= repeat:

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Generate timestamp only once per loop
            image_path = os.path.join(OP_PATH, 'im', f"{timestamp}.png")  # Use os.path.join and f-strings
            output_path = os.path.join(OP_PATH, 'im', f"Cozelti_UPG_{timestamp}.png")  # Use os.path.join and f-strings

            take_snapshot = pyautogui.screenshot(region=(left, top, width, height))

            # Efficient conversion and color correction
            numpy_image = np.array(take_snapshot.convert("RGB"))

            if numpy_image is None or numpy_image.size == 0:
                err_FILE.write("Error: Could not convert screenshot to NumPy array.")
                break  # Exit the loop if screenshot fails.

            # Boyutlandırma (Conditional and efficient)
            if RES_UP != 1 and RES_UP > 0:
                height, width = numpy_image.shape[:2]
                new_size = (int(width * RES_UP), int(height * RES_UP))
                numpy_image = cv2.resize(numpy_image, new_size, interpolation=cv2.INTER_LANCZOS4)

            # Keskinleştirme (Conditional, consider removing if not essential)
            kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened_image = cv2.filter2D(numpy_image, -1, kernel_sharpening)

            # Pikselleşmeyi azaltma (Denoising)
            denoised_image = cv2.fastNlMeansDenoisingColored(sharpened_image, None, 10, 10, 7, 21)

            cv2.imwrite(output_path, denoised_image)  # Save directly to the final path.
            # os.remove(image_path)  # Remove the original screenshot (optional, if disk space is a concern)

            self.click_located()  # Keep this line to be executed in each loop

            await asyncio.sleep(delay)  # Await the delay.

            percent = int((counter / repeat) * 100)
            self.progress.setValue(percent)
            counter += 1

        self.progress.setValue(100)

        msgBox = QMessageBox()
        msgBox.information(self, "z-book scanning ended",
                           f"Your image files are created from {repeat} pages.")
    async def async_operation_started(self):
        if RES_MODE == True:
            syspath = OP_PATH + 'pre/'
        else:
            syspath = OP_PATH + 'im/'
        for a in os.listdir(syspath):
            os.remove(syspath + a)
        delay = int(self.delay.text())
        repaet = int(self.pagecount.text())
        counter = 1
        if delay <= 0:
            delay = 1
        if repaet <= 0:
            repaet = 1

        while counter <= repaet:
            dates = datetime.now()
            # year month day hours munites second ms
            filename = syspath + dates.strftime("%Y%m%d%H%M%S%f") + ".png"
            x1, y1, x2, y2 = clickmemory["x1"], clickmemory["y1"], clickmemory["x2"], clickmemory["y2"]

            left, top, width, height = 0, 0, 0, 0
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
            self.click_located()
            await asyncio.sleep(delay)
            if RES_MODE == True:
                percent = int(((counter/repaet)*100)/2)
                self.progress.setValue(percent)
            else:
                self.progress.setValue(int((counter/repaet)*100))

            counter += 1
        if RES_MODE == True:

            self.progress.setValue(50)
        else:
            self.progress.setValue(100)


    def operation_started(self):
        asyncio.run(self.operate_AI())

    async def operate_AI(self):
        m1 = asyncio.create_task(self.async_operation_started())
        await m1
        if RES_MODE == True:
            m2 = asyncio.create_task(self.AI_Operate())
            await m2
    async def AI_Operate(self):

        for a in os.listdir(OP_PATH + 'im/'):
            os.remove(OP_PATH + 'im/' + a)
        files = os.listdir(OP_PATH + "pre/")
        pre = 50
        c = 0
        for i in files:

            dates = datetime.now()

            image = cv2.imread(OP_PATH + "pre/"+i)

            # Boyutlandırma: Oranları koruyarak boyutu iki katına çıkar
            height, width = image.shape[:2]
            new_size = (width * RES_UP, height * RES_UP)
            resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)

            # Keskinleştirme (Sharpening) maskesi oluşturma
            kernel_sharpening = np.array([[-1, -1, -1],
                                          [-1, 9, -1],
                                          [-1, -1, -1]])

            # Keskinleştirme filtresi uygula
            sharpened_image = cv2.filter2D(resized_image, -1, kernel_sharpening)

            # Pikselleşmeyi azaltma (Denoising)
            denoised_image = cv2.fastNlMeansDenoisingColored(sharpened_image, None, 10, 10, 7, 21)
            out = OP_PATH + 'im/' + "Cozelti_UPG_" + dates.strftime("%Y%m%d%H%M%S%f") + ".png"

            # Kaydetme (isteğe bağlı)
            cv2.imwrite(out, denoised_image)
            c+=1
            if RES_MODE == True:
                self.progress.setValue(pre + int(((c / len(files) * 100) / 2)))
            else:
                self.progress.setValue(pre + int((c / len(files) * 100)))

        self.progress.setValue(100)

        msgBox = QMessageBox()
        msgBox.information(self, "z-book scanning ended",
                           "Your image files already created from that z book " + str(c) + ' pages')


    async def async_create_pdf(self):
        pathx = OP_PATH + "im/"
        file = os.listdir(pathx)
        imlist = []
        for i in file:
            imlist.append(pathx + i)
        if len(imlist) >= 0:
            filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            with open("exported_cozelti_software_" + filename + ".pdf", "wb") as f:
                f.write(convert(imlist))

            msgBox = QMessageBox()
            msgBox.information(self, "pdf creation ended", "Your image files already converted to pdf")
            for a in os.listdir(OP_PATH + 'im/'):
                os.remove(OP_PATH + 'im/' + a)
        else:
            msgBox = QMessageBox()
            msgBox.warning(self, "pdf creation error", "Your image files didn't found in ./data/im/")
    def create_pdf(self):
        asyncio.run(self.async_create_pdf())
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
            "CTRL+1 for first location[X1:Y1]\nCTRL+2 for second location[X2:Y2]\nCTRL+3 for click location[Mx:My]\nCTRL+T for testing clicking\nCTRL+S for testing snapshot\nCTRL+4 Start system\nCTRL+5 to PDF")

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