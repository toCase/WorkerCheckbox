# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Qt, Signal, Slot
# from XLS_Maker import XLS_Maker
from Base import Base

class TTN_Model(QAbstractListModel):

    map = []
    otype = 2
    odebug = 2

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
        self.loadModel()

    modelReset = Signal()

    def rowCount(self, parent=QModelIndex):
        return len(self.map)

    @Slot()
    def loadModel(self):
        self.beginResetModel()
        Base.connectDB(self)

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
            if role == self.col5:
                return self.map[row].get("statusNP")            
            if role == self.col6:
                return self.map[row].get("dateCB")
            if role == self.col7:
                if self.map[row].get("statusCB") == '':
                    return ""
                elif self.map[row].get("statusCB") == '201':
                    return "Успіх"
                else:
                    return "Fail"
            if role == self.col8:
                if self.map[row].get("statusCB") == '201':
                    return "#008000"
                else:
                    return "#990000"

    def roleNames(self):
        return {
            self.col1: b"id",
            self.col2: b"phone",
            self.col3: b"num_ttn",
            self.col4: b"num",
            self.col5: b"statusNP",            
            self.col6: b"dateCB",
            self.col7: b"statusCB",
            self.col8: b"clr",

            }

    @Slot(int, str, result=str)
    def getData(self, row:int, item:str):
        return str(self.map[row].get(item))

    @Slot(str)
    def deleteTTN(self, id:str):
        order = int(id)
        Base.order_del(self, order)
        self.loadModel()

    @Slot()
    def deleteDone(self):
        Base.order_delDone(self)
        self.loadModel()


