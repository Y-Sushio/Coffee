from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QButtonGroup
from additionally_win import Ui_additional_window
from Coffee import Ui_Coffee
from sys import exit
import sqlite3


class AdditionallyWin(QWidget, Ui_additional_window):
    def __init__(self, parent, title, *args, **kwargs):
        super(AdditionallyWin, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.parent_win = parent
        self.title = title
        self.setWindowTitle(self.title)

        if self.title == "Удалить":
            self.taste_edit.setText("Данное поле можно не заполнять")
            self.exit_button.setText("Для подтверждения удаления заполните соответсвующие поля")
        elif self.title == "Редактировать":
            self.exit_button.setText("Введите нужный ID и выставьте новые значения полей")

        self.grade_flag = ""
        self.grade_buttons = QButtonGroup()
        self.grade_buttons.addButton(self.arabic_button)
        self.grade_buttons.addButton(self.liberica_button)
        self.grade_buttons.addButton(self.robust_button)
        self.grade_buttons.addButton(self.excelsa_button)
        self.grade_buttons.buttonClicked.connect(self.__grade_buttons__)

        self.degree_flag = ""
        self.degree_buttons = QButtonGroup()
        self.degree_buttons.addButton(self.weak_button)
        self.degree_buttons.addButton(self.medium_button)
        self.degree_buttons.addButton(self.strong_button)
        self.degree_buttons.buttonClicked.connect(self.__degree_buttons__)

        self.grind_flag = ""
        self.grind_buttons = QButtonGroup()
        self.grind_buttons.addButton(self.grind_true_button)
        self.grind_buttons.addButton(self.grind_false_button)
        self.grind_buttons.buttonClicked.connect(self.__grind_buttons__)

        self.exit_button.clicked.connect(self.__exit_button__)

    def __grade_buttons__(self, button):
        self.grade_flag = button.text()

    def __degree_buttons__(self, button):
        self.degree_flag = button.text()

    def __grind_buttons__(self, button):
        self.grind_flag = button.text()

    def __exit_button__(self):
        if self.grind_flag != "" and self.degree_flag != "" and self.degree_flag != "":
            if self.title == "Добавить":
                try:
                    with sqlite3.connect("coffee.sqlite") as data_base:
                        data_base.cursor().execute("""INSERT INTO Coffee VALUES
                        (?, ?, ?, ?, ?, ?, ?)""", (int(self.id_edit.text()), self.grade_flag, self.degree_flag,
                                                   1 if self.grind_flag == "Молотый" else 0, self.taste_edit.text(),
                                                   float(self.price_edit.text()), float(self.volume_edit.text())))

                    self.parent_win.base_table()

                    self.close()
                except Exception:
                    self.exit_button.setText("Непредвиденная ошибка!")
            elif self.title == "Удалить":
                flag = False
                try:
                    with sqlite3.connect("coffee.sqlite") as data_base:
                        info = data_base.cursor().execute("""SELECT * FROM Coffee
                        WHERE ID = ?""", (int(self.id_edit.text()),)).fetchall()[0]

                        if not len(info) or info[1] != self.grade_flag or info[2] != self.degree_flag or info[
                            3] != {"Молотый": 1, "Зёрна": 0}[self.grind_flag] or info[5] != float(
                            self.price_edit.text()) or info[6] != float(self.volume_edit.text()):
                            self.exit_button.setText("Несоответсвует указанная информация!")
                        else:
                            flag = True

                            data_base.cursor().execute("""DELETE FROM Coffee
                            WHERE ID = ?""", (int(self.id_edit.text()),))

                    if flag:
                        self.parent_win.base_table()

                        self.close()
                except Exception:
                    self.exit_button.setText("Непредвиденная ошибка!")
            else:
                try:
                    with sqlite3.connect("coffee.sqlite") as data_base:
                        data_base.cursor().execute("""UPDATE Coffee set
                        Grade = ?,
                        DegreeRoasting = ?,
                        Grind = ?,
                        Taste = ?,
                        Price = ?,
                        Volume = ?
                        WHERE ID = ?""", (self.grade_flag, self.degree_flag,
                                          1 if self.grind_flag == "Молотый" else 0,
                                          self.taste_edit.text(), float(self.price_edit.text()),
                                          float(self.volume_edit.text()), int(self.id_edit.text())))

                        data_base.commit()

                    self.parent_win.base_table()

                    self.close()
                except Exception:
                    print(str(Exception))
                    self.exit_button.setText("Непредвиденная ошибка!")
        else:
            self.exit_button.setText("Заполните обязательные поля!")


class Coffee(QMainWindow, Ui_Coffee):
    def __init__(self, *args, **kwargs):
        super(Coffee, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.arabic_button.clicked.connect(self.__radio_button__)
        self.liberica_button.clicked.connect(self.__radio_button__)
        self.excelsa_button.clicked.connect(self.__radio_button__)
        self.robust_button.clicked.connect(self.__radio_button__)

        self.add_button.clicked.connect(self.__button__)
        self.edit_button.clicked.connect(self.__button__)
        self.delete_button.clicked.connect(self.__button__)

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

        self.base_table()

    def __radio_button__(self):
        with sqlite3.connect("coffee.sqlite") as data_base:
            list_info = data_base.cursor().execute("""SELECT * FROM Coffee
            WHERE Grade = ?""", (self.sender().text(),)).fetchall()

        self.table.setRowCount(len(list_info))

        for index_y in range(0, len(list_info), 1):
            for index_x in range(0, 7, 1):
                if index_x == 3:
                    self.table.setItem(index_y, index_x,
                                       QTableWidgetItem("Зёрна" if list_info[index_y][3] == 0 else "Молотый"))
                else:
                    self.table.setItem(index_y, index_x, QTableWidgetItem(str(list_info[index_y][index_x])))

        self.statusbar.showMessage(f"Всего {len(list_info)} записей")

    def __button__(self):
        if self.sender().text() == "Добавить Запись":
            self.child = AdditionallyWin(self, "Добавить")

            self.child.show()
        elif self.sender().text() == "Удалить Запись":
            self.child = AdditionallyWin(self, "Удалить")

            self.child.show()
        else:
            self.child = AdditionallyWin(self, "Редактировать")

            self.child.show()

    def base_table(self):
        with sqlite3.connect("coffee.sqlite") as data_base:
            list_info = data_base.cursor().execute("SELECT * FROM Coffee").fetchall()

        self.table.setRowCount(len(list_info))

        for index_y in range(0, len(list_info), 1):
            for index_x in range(0, 7, 1):
                if index_x == 3:
                    self.table.setItem(index_y, index_x,
                                       QTableWidgetItem("Зёрна" if list_info[index_y][3] == 0 else "Молотый"))
                else:
                    self.table.setItem(index_y, index_x, QTableWidgetItem(str(list_info[index_y][index_x])))

        self.statusbar.showMessage(f"Всего {len(list_info)} записей")


if __name__ == '__main__':
    application = QApplication([])

    window = Coffee()
    window.show()

    exit(application.exec_())
