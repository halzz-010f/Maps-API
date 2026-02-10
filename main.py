import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from io import BytesIO


class FirstTask(QMainWindow):
    def __init__(self):
        super(FirstTask, self).__init__()
        uic.loadUi('ui/task1_map.ui', self)
        self.update_button.clicked.connect(self.on_update_clicked)

    def on_update_clicked(self):
        lat = self.lat_input.text().strip()
        lon = self.lon_input.text().strip()
        zoom = self.zoom_input.value()

        if not lat or not lon:
            print("Ошибка: введите широту и долготу!")
            return

        url = f"https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z={zoom}&l=map&size=541,450"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = BytesIO(response.content)
            image = QImage()
            if image.loadFromData(data.getvalue()):
                pixmap = QPixmap.fromImage(image)
                self.map_label.setPixmap(pixmap)
            else:
                print("Ошибка: не удалось загрузить изображение из данных")
        else:
            print(f"Ошибка загрузки карты: HTTP {response.status_code}")

def main():
    app = QApplication(sys.argv)
    window = FirstTask()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
