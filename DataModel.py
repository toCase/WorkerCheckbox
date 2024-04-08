# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Qt, Signal, Slot
from XLS_Maker import XLS_Maker

class DataModel(QAbstractListModel):

    map = []

    col1 = Qt.UserRole + 1
    col2 = Qt.UserRole + 2
    col3 = Qt.UserRole + 3
    col4 = Qt.UserRole + 4
    col5 = Qt.UserRole + 5
    col6 = Qt.UserRole + 6
    col7 = Qt.UserRole + 7
    col8 = Qt.UserRole + 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadModel("")

    modelReset = Signal()

    def rowCount(self, parent=QModelIndex):
        return len(self.map)

    @Slot(str)
    def loadModel(self, fname:str):
        self.beginResetModel()

        self.map.clear()
        result = XLS_Maker.get_data(self, fname)
        print(result)

        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if index.isValid():
            if role == self.col1:
                return self.map[row].get("phone")
            if role == self.col2:
                return self.map[row].get("product")
            if role == self.col3:
                return self.map[row].get("p_id")
            if role == self.col4:
                return self.map[row].get("ttn")
            if role == self.col5:
                return self.map[row].get("p_check")
            if role == self.col6:
                return self.map[row].get("l_result")
            if role == self.col7:
                return self.map[row].get("l_messa")
            if role == self.col8:
                return self.map[row].get("num")

    def roleNames(self):
        return {
            self.col1: b"phone",
            self.col2: b"product",
            self.col3: b"p_id",
            self.col4: b"ttn",
            self.col5: b"p_check",
            self.col6: b"l_result",
            self.col7: b"l_messa",
            self.col8: b"num",
            }
