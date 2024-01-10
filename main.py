from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QButtonGroup
from Coffee import Ui_Coffee
from sys import exit
import sqlite3


class Coffee(QMainWindow, Ui_Coffee):
    def __init__(self, *args, **kwargs):
        super(Coffee, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.arabic_button.clicked.connect(self.__radio_button__)
        self.liberica_button.clicked.connect(self.__radio_button__)
        self.excelsa_button.clicked.connect(self.__radio_button__)
        self.robust_button.clicked.connect(self.__radio_button__)

        self.table.setColumnCount(7)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 250)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 200)

        self.table.setHorizontalHeaderLabels(
            ["ID", "Сорт", "Степень обжарки", "Молотый/Зёрна", "Вкус", "Стоимость", "Объём"])

        with sqlite3.connect("coffee.sqlite") as data_base:
            cursor = data_base.cursor()

            list_info = cursor.execute("SELECT * FROM Coffee").fetchall()

        self.table.setRowCount(len(list_info))

        for index_y in range(0, len(list_info), 1):
            for index_x in range(0, 7, 1):
                if index_x == 3:
                    self.table.setItem(index_y, index_x,
                                       QTableWidgetItem("Зёрна" if list_info[index_y][3] == 0 else "Молотый"))
                else:
                    self.table.setItem(index_y, index_x, QTableWidgetItem(str(list_info[index_y][index_x])))

        self.statusbar.showMessage(f"Всего {len(list_info)} записей")

    def __radio_button__(self):
        with sqlite3.connect("coffee.sqlite") as data_base:
            cursor = data_base.cursor()

            list_info = cursor.execute("""SELECT * FROM Coffee
            WHERE Grade = ?""", (self.sender().text(),)).fetchall()

        self.table.setRowCount(len(list_info))

        for index_y in range(0, len(list_info), 1):
            for index_x in range(0, 7, 1):
                if index_x == 3:
                    self.table.setItem(index_y, index_x,
                                       QTableWidgetItem("Зёрна" if list_info[index_y][3] == 0 else "Молотый"))
                else:
                    self.table.setItem(index_y, index_x, QTableWidgetItem(str(list_info[index_y][index_x])))

        self.statusbar.showMessage(f"Найдено {len(list_info)} записей")


if __name__ == '__main__':
    application = QApplication([])

    window = Coffee()
    window.show()

    exit(application.exec_())
