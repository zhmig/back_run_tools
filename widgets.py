# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets.ui'
#
# Created: Sat Mar  5 13:28:50 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.save_lay = QtWidgets.QHBoxLayout()
        self.save_lay.setObjectName("save_lay")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"color: rgb(188, 188, 188);")
        self.label.setObjectName("label")
        self.save_lay.addWidget(self.label)
        self.verticalLayout.addLayout(self.save_lay)
        self.file_lay = QtWidgets.QHBoxLayout()
        self.file_lay.setObjectName("file_lay")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"color: rgb(188, 188, 188);")
        self.label_2.setObjectName("label_2")
        self.file_lay.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.file_lay)
        self.script_lay = QtWidgets.QHBoxLayout()
        self.script_lay.setObjectName("script_lay")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"color: rgb(188, 188, 188);")
        self.label_3.setObjectName("label_3")
        self.script_lay.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.script_lay)
        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.setDragEnabled(True)
        self.table.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.table.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.table.setObjectName("table")
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.render_chbox = QtWidgets.QCheckBox(self.centralwidget)
        self.render_chbox.setChecked(False)
        self.render_chbox.setObjectName("render_chbox")
        self.horizontalLayout_4.addWidget(self.render_chbox)
        self.singeFrame_radioBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.singeFrame_radioBtn.setEnabled(False)
        self.singeFrame_radioBtn.setChecked(True)
        self.singeFrame_radioBtn.setObjectName("singeFrame_radioBtn")
        self.horizontalLayout_4.addWidget(self.singeFrame_radioBtn)
        self.sequence_radioBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.sequence_radioBtn.setEnabled(False)
        self.sequence_radioBtn.setObjectName("sequence_radioBtn")
        self.horizontalLayout_4.addWidget(self.sequence_radioBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.run_btn = QtWidgets.QPushButton(self.centralwidget)
        self.run_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setWeight(9)
        font.setItalic(False)
        font.setBold(False)
        self.run_btn.setFont(font)
        self.run_btn.setStyleSheet("QPushButton{\n"
"    font: 75 14pt \"Microsoft YaHei UI\";\n"
"    background-color: rgb(48, 51, 62);\n"
"    color: rgb(188, 188, 188);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(75, 80, 97);\n"
"}\n"
"QPushButton:focus{\n"
"    \n"
"    background-color: rgb(38, 41, 50);\n"
"}")
        self.run_btn.setObjectName("run_btn")
        self.verticalLayout.addWidget(self.run_btn)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid #2196F3;/*边框以及边框颜色*/\n"
"    border-radius: 5px;\n"
"    background-color: #E0E0E0;\n"
"}")
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.render_chbox, QtCore.SIGNAL("clicked(bool)"), self.sequence_radioBtn.setEnabled)
        QtCore.QObject.connect(self.render_chbox, QtCore.SIGNAL("clicked(bool)"), self.singeFrame_radioBtn.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Save File Path: ", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "File Path:          ", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Script Path:      ", None, -1))
        self.render_chbox.setText(QtWidgets.QApplication.translate("MainWindow", "Render", None, -1))
        self.singeFrame_radioBtn.setText(QtWidgets.QApplication.translate("MainWindow", "SingleFrame", None, -1))
        self.sequence_radioBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Sequence", None, -1))
        self.run_btn.setText(QtWidgets.QApplication.translate("MainWindow", "Run", None, -1))

        