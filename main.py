import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from addEditCoffeeForm import Ui_Add_Dialog
from mainAppForm import Ui_MainWindow
import sqlite3


class Coffee_Mapp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_funcs_to_buttons()
        self.fill_table()

    def add_funcs_to_buttons(self):
        self.find_btn.clicked.connect(self.fill_table)
        self.name_edit.textChanged.connect(self.fill_table)
        self.add_btn.clicked.connect(self.call_AddEditDialog)
        self.edit_btn.clicked.connect(self.call_AddEditDialog)

    def call_AddEditDialog(self):
        self.error_lbl.setText('')
        do = self.sender().text()

        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]

        if len(ids) > 1:
            self.error_lbl.setText('Указано много строк')
            return False
        elif len(ids) == 0 and do != 'Добавить':
            self.error_lbl.setText('Укажите 1 строку, которую хотите изменить')
            return False

        dial = AddEditCoffeeDialog(do, ids)
        dial.exec()

        self.fill_table()

    def find_coffee_in_bd(self):
        name = self.name_edit.text()

        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()

        result = cur.execute(f'''SELECT * FROM Info WHERE title LIKE '{name.capitalize()}%' ''').fetchall()

        cur.close()

        return result

    def fill_table(self):
        self.error_lbl.setText('')
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


class AddEditCoffeeDialog(Ui_Add_Dialog, QDialog):
    def __init__(self, edit_or_add, choosen_rows):
        super().__init__()
        self.setupUi(self)
        self.edit_or_add = edit_or_add
        self.choosen_rows = choosen_rows
        self.add_func_to_btn()

    def add_func_to_btn(self):
        if self.edit_or_add == 'Добавить':
            self.commit_btn.clicked.connect(self.add_coffee_to_bd)
        else:
            self.commit_btn.clicked.connect(self.edit_coffee_in_bd)
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()

            result = cur.execute(f'''SELECT * FROM Info WHERE id = {int(self.choosen_rows[0])}''').fetchone()

            self.name_edit.setText(result[1])
            self.degree_edit.setText(result[2])
            self.ground_or_in_grains_box.setCurrentText(result[3])
            self.taste_edit.setText(result[4])
            self.cost_edit.setText(str(result[5]))
            self.packing_volume_edit.setText(str(result[6]))

            self.id = result[0]

            cur.close()

    def add_coffee_to_bd(self):
        self.error_lbl.setText('')
        title = self.name_edit.text()
        degree = self.degree_edit.text()
        type_of_coffee = self.ground_or_in_grains_box.currentText()
        taste = self.taste_edit.text()
        cost = self.cost_edit.text()
        packing_volume = self.packing_volume_edit.text()

        try:
            cost = int(cost)
            packing_volume = int(packing_volume)
        except ValueError:
            self.error_lbl.setText('Введены некорректные данные')
            return False

        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()

        cur.execute(f'''INSERT INTO Info(title, degree_of_roasting, 
        ground_or_in_grains, taste, cost, packing_volume)  
        VALUES ('{title}', '{degree}', '{type_of_coffee}', '{taste}', {cost}, {packing_volume})''')

        con.commit()
        cur.close()

        self.close()

    def edit_coffee_in_bd(self):
        self.error_lbl.setText('')
        title = self.name_edit.text()
        degree = self.degree_edit.text()
        type_of_coffee = self.ground_or_in_grains_box.currentText()
        taste = self.taste_edit.text()
        cost = self.cost_edit.text()
        packing_volume = self.packing_volume_edit.text()

        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()

        cur.execute(f'''UPDATE info 
        SET title = '{title}', 
        degree_of_roasting = '{degree}', 
        ground_or_in_grains = '{type_of_coffee}',
        taste = '{taste}',
        cost = {cost}, 
        packing_volume = {packing_volume} 
        WHERE id = {self.id}''')

        con.commit()
        cur.close()

        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cfm = Coffee_Mapp()
    cfm.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
