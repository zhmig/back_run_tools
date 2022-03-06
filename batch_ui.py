#!/usr/bin/env python
# coding=utf-8
'''
Author        : zhenghaoming
Date          : 2022-02-24 00:30:04
FilePath      : \BooBoo\batch_ui.py
version       : 
LastEditors   : zhenghaoming
LastEditTime  : 2022-02-28 18:25:09
'''
import sys,os

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import widgets,exp_app
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class save_DirLine(QLineEdit):

    def mouseDoubleClickEvent(self, event):
        QLineEdit.mousePressEvent(self, event)
        path = QFileDialog.getExistingDirectory(self)
        if path:
            self.setText(path.replace("\\", "/"))
            
class file_DirLine(QLineEdit,widgets.Ui_MainWindow):

    def mouseDoubleClickEvent(self, event):
        QLineEdit.mousePressEvent(self, event)
        path = QFileDialog.getExistingDirectory(self)
        
        if path:
            self.setText(path.replace("\\", "/"))
            self.get_maya_file(path)

    def get_maya_file(self,path):
        list_files = []
        for root, dirs, files in os.walk(path):
            for f in files:
                list_files.append(os.path.join(root, f))

        list_files = list(filter(self.file_filter, list_files))

        for items in range(len(list_files)) :
            fiename = os.path.splitext(os.path.split(list_files[items])[1])[0]
            self.model.appendRow([QStandardItem(fiename),QStandardItem(list_files[items])])

        self.table.setModel(self.model)

    def file_filter(self,file_name):
        mayaFilters = ['.ma','.mb','.MA','.MB']
        if file_name[-3:] in mayaFilters :
            return True
        else:
            return False

class scriptLine(QLineEdit):

    def mouseDoubleClickEvent(self, event):
        QLineEdit.mousePressEvent(self, event)
        path, _ = QFileDialog.getOpenFileName(self, None, None, "Script (*.mel *.py)")
        if path:
            self.setText(path.replace("\\", "/"))

class BatchUI(QMainWindow, widgets.Ui_MainWindow):
    '''
    '''
    def __init__(self, parent=None):
        '''
        '''
        super(BatchUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(u'批处理工具')

        self.tableHead()
        self.save_lineedit()
        self.file_lineedit()
        self.script_lineedit()

        self.table.customContextMenuRequested.connect(self.create_context_menu)
        self.setAcceptDrops(True)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)

    def tableHead(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([u'文件名字',u'文件路径'])

        # self.table = QTableView()
        self.table.setModel(self.model)
        self.header = self.table.horizontalHeader()
        self.header.resizeSection(0, 200)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pass

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                # self.listWidget.addItem(url.toLocalFile())
                if os.path.isfile(url.toLocalFile()):
                    self.model.appendRow([QStandardItem(os.path.basename(url.toLocalFile())),
                                    QStandardItem(url.toLocalFile())])

            self.table.setModel(self.model)
        else:
            event.ignore()

    @Slot(QPoint)
    def create_context_menu(self, point):
        '''
        添加右键菜单信号,并且关联到tableview上
        '''
        menu = QMenu(self.table)
        menu.addAction(u'删除', self.remove_select_items)
        menu.addSeparator()
        # menu.addAction(u'清除',self.clear_all_items)
        menu.exec_(QCursor.pos())

    def remove_select_items(self):
        '''
        可删除选中的多行或者单行
        '''
        index_list = []                                                          
        for model_index in self.table.selectionModel().selectedRows():       
            index = QPersistentModelIndex(model_index)         
            index_list.append(index)                                             

        for index in index_list:                                      
            self.model.removeRow(index.row())                                                               


    def clear_all_items(self):
        pass

    def save_lineedit(self):
        self.savepath = save_DirLine()
        self.savepath.setMinimumSize(QSize(0, 25))
        self.savepath.setPlaceholderText(u'设置保存路径,双击即可')

        font = QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(8)
        self.savepath.setFont(font)
        self.savepath.setStyleSheet("QLineEdit{\n"
            "    border:2px solid rgb(37,39,48);\n"
            "    padding -left: 20px;\n"
            "    padding -right: 20px;\n"
            "    font: 9pt \"Microsoft JhengHei UI\";\n"
            "    \n"
            "}\n"
            "QlineEdit:hover{\n"
            "    border:2px solid rgb(48,50,62);\n"
            "}\n"
            "QlineEdit:focus{\n"
            "    border:2px solid rgb(85,170,255);\n"
            "}")

        self.save_lay.addWidget(self.savepath)
        
    def file_lineedit(self):
        self.filepath = file_DirLine()
        self.filepath.setMinimumSize(QSize(0, 25))
        self.filepath.setPlaceholderText(u'设置maya文件目录,双击即可')

        font = QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(8)
        self.filepath.setFont(font)
        self.filepath.setStyleSheet("QLineEdit{\n"
            "    border:2px solid rgb(37,39,48);\n"
            "    padding -left: 20px;\n"
            "    padding -right: 20px;\n"
            "    font: 9pt \"Microsoft JhengHei UI\";\n"
            "    \n"
            "}\n"
            "QlineEdit:hover{\n"
            "    border:2px solid rgb(48,50,62);\n"
            "}\n"
            "QlineEdit:focus{\n"
            "    border:2px solid rgb(85,170,255);\n"
            "}")

        self.file_lay.addWidget(self.filepath)   
        self.filepath.model = self.model
        self.filepath.table = self.table

    def script_lineedit(self):
        self.scriptpath = scriptLine()
        self.scriptpath.setMinimumSize(QSize(0, 25))
        self.scriptpath.setPlaceholderText(u'获取脚本文件,双击即可')

        font = QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(8)
        self.scriptpath.setFont(font)
        self.scriptpath.setStyleSheet("QLineEdit{\n"
            "    border:2px solid rgb(37,39,48);\n"
            "    padding -left: 20px;\n"
            "    padding -right: 20px;\n"
            "    font: 9pt \"Microsoft JhengHei UI\";\n"
            "    \n"
            "}\n"
            "QlineEdit:hover{\n"
            "    border:2px solid rgb(48,50,62);\n"
            "}\n"
            "QlineEdit:focus{\n"
            "    border:2px solid rgb(85,170,255);\n"
            "}")

        self.script_lay.addWidget(self.scriptpath)  

    @Slot(bool)
    def on_run_btn_clicked(self, args):
        model = self.table.model()
        data = []

        self.time = QBasicTimer()

        savefilepath = self.savepath.text()
        scriptfile = self.scriptpath.text()

        result = QMessageBox.question(self, u'确认', u'确认开始 ? ? ?')
        if result == QMessageBox.StandardButton.No:
            return

        for row in range(model.rowCount()):
            data.append([])
            for colum in range(model.columnCount()):
                item = model.index(row,colum)
                data[row].append(model.data(item))

        exp_app.main(self,data,savefilepath,scriptfile)
        self.progressBar.setValue(100)

        QMessageBox.about(None, u'结果', u'已完成 ! !')



def main():
    '''
    '''
    app = QApplication(sys.argv)
    wnd = BatchUI()
    wnd.show()
    app.exec_()



if __name__ == '__main__':
    main()
