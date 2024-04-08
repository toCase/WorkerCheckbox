# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Qt, Signal, Slot
# from XLS_Maker import XLS_Maker
from Base import Base

class OrderModel(QAbstractListModel):

    map = []
    otype = 2
    odebug = 1

    col1 = Qt.UserRole + 1
    col2 = Qt.UserRole + 2
    col3 = Qt.UserRole + 3
    col4 = Qt.UserRole + 4

    def __init__(self, parent=None):
        super().__init__(parent)

    modelReset = Signal()

    def rowCount(self, parent=QModelIndex):
        return len(self.map)

    @Slot()
    def loadModel(self):
        self.beginResetModel()

        self.map.clear()
        self.map = Base.order_get(self, self.otype, self.odebug)

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

    def roleNames(self):
        return {
            self.col1: b"id",
            self.col2: b"phone",
            self.col3: b"ttn",
            self.col4: b"num"
            }

    @Slot()
    def makeOrders(self):
        if len(self.map) > 0:
            for card in self.map:
                card['debug'] = 2
                r = Base.order_save(self, card)
                print(r)

            self.loadModel()

