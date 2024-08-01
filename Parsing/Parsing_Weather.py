from table import table
from parsing_weather_desktop import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableView
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
import sys
from pandasModel import pandasModel

def msg_error_website():
    msg_error = QMessageBox()
    msg_error.setWindowTitle("ERROR!")
    msg_error.setText("Выберите сайт!")
    msg_error.setIcon(QMessageBox.Critical)
    msg_error.exec_()

def msg_error_dataset():
    msg_error = QMessageBox()
    msg_error.setWindowTitle("ERROR!")
    msg_error.setText("Не удалось обновить данные! Попробуйте позже!")
    msg_error.setIcon(QMessageBox.Critical)
    msg_error.exec_()

def msg_error_view():
    msg_error = QMessageBox()
    msg_error.setWindowTitle("ERROR!")
    msg_error.setText("Не удалось вывести данные!")
    msg_error.setIcon(QMessageBox.Critical)
    msg_error.exec_()

def msg_error_backup():
    msg_error = QMessageBox()
    msg_error.setWindowTitle("ERROR!")
    msg_error.setText("Не удалось сделать backup!")
    msg_error.setIcon(QMessageBox.Critical)
    msg_error.exec_()

def on_click_Moscow():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            table.update("Moscow", "GisMeteo")
            ui.pushButton.setEnabled(False)
        except:
            msg_error_dataset()
    elif ui.radioButton_2.isChecked():
        try:
            table.update("Moscow", "Yandex")
            ui.pushButton.setEnabled(False)
        except:
            msg_error_dataset()

def on_click_Krasnodar():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            table.update("Krasnodar", "GisMeteo")
            ui.pushButton_2.setEnabled(False)
        except:
            msg_error_dataset()
    elif ui.radioButton_2.isChecked():
        try:
            table.update("Krasnodar", "Yandex")
            ui.pushButton_2.setEnabled(False)
        except:
            msg_error_dataset()

def on_click_Ekaterinburg():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            table.update("Ekaterinburg", "GisMeteo")
            ui.pushButton_3.setEnabled(False)
        except:
            msg_error_dataset()
    elif ui.radioButton_2.isChecked():
        try:
            table.update("Ekaterinburg", "Yandex")
            ui.pushButton_3.setEnabled(False)
        except:
            msg_error_dataset()

def on_click_backup():
    try:
        table.backup()
    except:
        msg_error_backup()

def on_click_rd_Moscow():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            model = pandasModel(table.view("Moscow", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_2.isChecked():
        try:
            model = pandasModel(table.view("Moscow", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()

def on_click_rd_Krasnodar():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            model = pandasModel(table.view("Krasnodar", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_2.isChecked():
        try:
            model = pandasModel(table.view("Krasnodar", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()

def on_click_rd_Ekaterinburg():
    if not ui.radioButton.isChecked() and not ui.radioButton_2.isChecked():
        msg_error_website()
    elif ui.radioButton.isChecked():
        try:
            model = pandasModel(table.view("Ekaterinburg", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_2.isChecked():
        try:
            model = pandasModel(table.view("Ekaterinburg", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()

def on_click_rd_Yandex():
    ui.pushButton.setEnabled(True)
    ui.pushButton_2.setEnabled(True)
    ui.pushButton_3.setEnabled(True)

    if ui.radioButton_3.isChecked():
        try:
            model = pandasModel(table.view("Moscow", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_4.isChecked():
        try:
            model = pandasModel(table.view("Krasnodar", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_5.isChecked():
        try:
            model = pandasModel(table.view("Ekaterinburg", "Yandex", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()


def on_click_rd_GisMeteo():
    ui.pushButton.setEnabled(True)
    ui.pushButton_2.setEnabled(True)
    ui.pushButton_3.setEnabled(True)

    if ui.radioButton_3.isChecked():
        try:
            model = pandasModel(table.view("Moscow", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_4.isChecked():
        try:
            model = pandasModel(table.view("Krasnodar", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()
    elif ui.radioButton_5.isChecked():
        try:
            model = pandasModel(table.view("Ekaterinburg", "GisMeteo", "all"))
            ui.tableView.setModel(model)
        except:
            msg_error_view()


if __name__ == "__main__":
    table = table()
    app = QtWidgets.QApplication(sys.argv)
    Parsing_Weather = QtWidgets.QMainWindow()
    ui = Ui_Parsing_Weather()
    ui.setupUi(Parsing_Weather)
    Parsing_Weather.show()

    ui.pushButton.clicked.connect(on_click_Moscow)
    ui.pushButton_2.clicked.connect(on_click_Krasnodar)
    ui.pushButton_3.clicked.connect(on_click_Ekaterinburg)
    ui.pushButton_4.clicked.connect(on_click_backup)

    ui.radioButton.clicked.connect(on_click_rd_GisMeteo)
    ui.radioButton_2.clicked.connect(on_click_rd_Yandex)

    ui.radioButton_3.clicked.connect(on_click_rd_Moscow)
    ui.radioButton_4.clicked.connect(on_click_rd_Krasnodar)
    ui.radioButton_5.clicked.connect(on_click_rd_Ekaterinburg)

    sys.exit(app.exec_())