# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Qt, Signal, Slot
# from XLS_Maker import XLS_Maker
from Base import Base
from CHB_Connector import CHB_Connector

import time


class OrderModelN(QAbstractListModel):

    map = []
    otype = 1
    odebug = 1

    col1 = Qt.UserRole + 1
    col2 = Qt.UserRole + 2
    col3 = Qt.UserRole + 3
    col4 = Qt.UserRole + 4
    col5 = Qt.UserRole + 5
    col6 = Qt.UserRole + 6

    def __init__(self, parent=None):
        super().__init__(parent)

    modelReset = Signal()
    progSignal = Signal(float, arguments=['val'])

    def rowCount(self, parent=QModelIndex):
        return len(self.map)

    @Slot()
    def loadModel(self):
        self.beginResetModel()
        Base.connectDB(self)
        self.map.clear()
        self.map = Base.order_get(self, self.otype, self.odebug)
        print(self.map)
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if index.isValid():
            if role == self.col1:
                return self.map[row].get("id")
            if role == self.col2:
                return self.map[row].get("phone")
            if role == self.col3:
                return self.map[row].get("ttn")
            if role == self.col4:
                return row + 1
            if role == self.col5:
                if self.map[row].get("statusCB") == '':
                    return ""
                elif self.map[row].get("statusCB") == '201':
                    return "Успіх"
                else:
                    return "Fail"
            if role == self.col6:
                if self.map[row].get("statusCB") == '201':
                    return "#008000"
                else:
                    return "#990000"


    def roleNames(self):
        return {
            self.col1: b"id",
            self.col2: b"phone",
            self.col3: b"ttn",
            self.col4: b"num",
            self.col5: b"statusCB",
            self.col6: b"clr"
            }
