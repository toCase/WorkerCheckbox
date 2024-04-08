# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Qt, Signal, Slot
from Base import Base

class ProductModel(QAbstractListModel):

    map = []

    col1 = Qt.UserRole + 1
    col2 = Qt.UserRole + 2
    col3 = Qt.UserRole + 3
    col4 = Qt.UserRole + 4
    col5 = Qt.UserRole + 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadModel()

    modelReset = Signal()

    def rowCount(self, parent=QModelIndex):
        return len(self.map)

    @Slot()
    def loadModel(self):
        self.beginResetModel()

        self.map.clear()
        Base.connectDB(self)
        self.map = Base.product_get(self)

        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if index.isValid():
            if role == self.col1:
                return self.map[row].get("id")
            if role == self.col2:
                return self.map[row].get("p_ids")
            if role == self.col3:
                return self.map[row].get("p_name")
            if role == self.col4:
                return self.map[row].get("p_code")
            if role == self.col5:
                return self.map[row].get("p_price")

    def roleNames(self):
        return {
            self.col1: b"id",
            self.col2: b"p_ids",
            self.col3: b"p_name",
            self.col4: b"p_code",
            self.col5: b"p_price",
            }
