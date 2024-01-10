from PyQt5.QtWidgets import QApplication, QMainWindow
from Coffee import Ui_Coffee
from sys import exit


class Coffee(QMainWindow, Ui_Coffee):
    def __init__(self, *args, **kwargs):
        super(Coffee, self).__init__(*args, **kwargs)

        self.setupUi(self)


if __name__ == '__main__':
    application = QApplication([])

    window = Coffee()
    window.show()

    exit(application.exec_())
