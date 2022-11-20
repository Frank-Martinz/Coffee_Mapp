import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3


class Coffee_Mapp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.add_funcs_to_buttons()
        self.fill_table()

    def add_funcs_to_buttons(self):
        self.find_btn.clicked.connect(self.fill_table)
        self.name_edit.textChanged.connect(self.fill_table)

    def find_coffee_in_bd(self):
        name = self.name_edit.text()

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute(f'''SELECT * FROM Info WHERE title LIKE '{name.capitalize()}%' ''').fetchall()

        cur.close()

        return result

    def fill_table(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(0, 25)
        self.tableWidget.setColumnWidth(1, 130)
        self.tableWidget.setColumnWidth(2, 140)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 170)
        self.tableWidget.setColumnWidth(5, 60)
        self.tableWidget.setColumnWidth(6, 140)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Молотый/В зернах',
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])

        info = self.find_coffee_in_bd()

        for en, i in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for e, item in enumerate(i):
                self.tableWidget.setItem(en, e, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cfm = Coffee_Mapp()
    cfm.show()
    sys.exit(app.exec_())