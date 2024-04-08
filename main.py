# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import XLS_Maker
import DataModel
import ProductModel
import OrderModel
import OrderModelN
import TTN_Model
import Base
import CHB_Connector
import thread

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    base = Base.Base()
    engine.rootContext().setContextProperty("base", base)

    api_cb = CHB_Connector.CHB_Connector()
    # api_cb.getTrackingNova()
    engine.rootContext().setContextProperty("api_checkbox", api_cb)

    xls_maker = XLS_Maker.XLS_Maker()
    engine.rootContext().setContextProperty("xls", xls_maker)

    data_model = DataModel.DataModel()
    engine.rootContext().setContextProperty("modelData", data_model)

    product_model = ProductModel.ProductModel()
    engine.rootContext().setContextProperty("modelProduct", product_model)

    order_modelN = OrderModelN.OrderModelN()
    engine.rootContext().setContextProperty("modelOrderN", order_modelN)
    order_modelT = OrderModel.OrderModel()
    engine.rootContext().setContextProperty("modelOrderT", order_modelT)

    ttn_model = TTN_Model.TTN_Model()
    engine.rootContext().setContextProperty("model_ttn", ttn_model)

    trd = thread.thread()
    engine.rootContext().setContextProperty("thread", trd)
    tGoods = thread.GoodsGet()
    engine.rootContext().setContextProperty("tGoods", tGoods)
    tOrders = thread.OrdersSet()
    engine.rootContext().setContextProperty("tOrders", tOrders)
    tNova = thread.NovaTracking()
    engine.rootContext().setContextProperty("tNova", tNova)





    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
