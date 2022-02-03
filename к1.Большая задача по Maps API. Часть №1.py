from PIL import Image
import sys
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from io import BytesIO


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 300, 300)
        uic.loadUi('ui/map.ui', self)
        self.start_button.clicked.connect(self.start)
        self.scale = 0
        self.longitude = 0.0
        self.lattitude = 0.0

        ## Изображение
       # ask = 'Выбрать картинку'
        #self.fileName = 'image.png'
        # self.fname = QFileDialog.getOpenFileName(self, ask, '')[0]
        ##self.fname = 'D:\\tmp\\image2.png'
        #self.loadPixmap(self.fname)

    def loadPixmap(self, fname):
        self.pixmap = QPixmap(fname)
        self.im = Image.open(fname)
        self.pixels = self.im.load()  # список с пикселями
        self.x, self.y = self.im.size
        self.label_map.resize(self.x, self.y)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.label_map.setPixmap(self.pixmap)
        self.label_map.repaint()

    def start(self):
        self.scale = int(self.scale_LineEdit.text())
        self.lattitude = float(self.lattitude_LineEdit.text())
        self.longitude = float(self.longitude_LineEdit.text())

        map_params = {
            "ll": ",".join([str(self.longitude), str(self.lattitude)]),
            "l": "map",
            "z": str(self.scale)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        Image.open(BytesIO(
            response.content)).save("image.png")
        self.loadPixmap('image.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())