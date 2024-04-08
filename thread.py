# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QThread, Signal, Slot
import time
import datetime
from CHB_Connector import CHB_Connector
from Base import Base


class thread(QThread):

    finished = Signal()
    working = Signal(float, arguments=['val'])

    def __init__(self):
        QThread.__init__(self)

    @Slot()
    def run(self):
        for i in range(1, 50, 1):
            value = i/50
            self.working.emit(value)
            print("VALUE: ", value)
        self.finished.emit()

class GoodsGet(QThread):

    started = Signal()
    finished = Signal()
    fail = Signal(str, arguments=['message'])
    working = Signal(float, arguments=['val'])

    def __init__(self):
        QThread.__init__(self)

    @Slot()
    def run(self):
        Base.connectDB(self)
        response = CHB_Connector.get_goods(self)

        error = response.get('message')
        data:list = response.get('results')
        if error:
            self.fail.emit(error)
        else:
            self.started.emit()
            i = 0
            for item in data:
                d = {
                    "p_ids":item.get("id"),
                    "code":item.get("code"),
                    "name":item.get("name"),
                    "price":item.get("price")
                }
                Base.product_save(self, d)

                progress = (i + 1) / len(data)
                self.working.emit(progress)
                time.sleep(0.1)
                i = i + 1

            self.finished.emit()

class OrdersSet(QThread):

    type_load = 0

    started = Signal()
    finished = Signal()
    fail = Signal(str, arguments=['message'])
    working = Signal(float, arguments=['val'])

    def __init__(self):
        QThread.__init__(self)

    @Slot(int)
    def data_setter(self, l:int):
        self.type_load = l


    @Slot()
    def run(self):
        Base.connectDB(self)

        print("START SELL")
        self.started.emit()

        map = Base.order_get(self, 1, 1)

        print(len(map))
        if len(map) > 0:
            i = 0
            for card in map:
                order_id = card.get("id")
                response = CHB_Connector.make_sell(self, order_id)
                status_code = response.get("status")
                if status_code != 201:
                    error = response.get("response").get("message")
                    self.fail.emit(error)
                else:
                    card["debug"] = 1
                    card["statusCB"] = status_code
                    card["dateCB"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

                    Base.order_save(self, card)

                    progress = (i + 1) / len(map)
                    self.working.emit(progress)
                    i=i+1
                    time.sleep(1)

        Base.disconnectDB(self)
        self.finished.emit()

class NovaTracking(QThread):

    UP_STATUS = [9, 10, 11]

    started = Signal()
    finished = Signal()
    fail = Signal(str, arguments=['message'])
    working = Signal(float, arguments=['val'])

    def __init__(self):
        QThread.__init__(self)

    @Slot()
    def run(self):
        self.started.emit()

        Base.connectDB(self)
        map = Base.order_get(self, 2, 2)
        print(len(map))

        if len(map) > 0:
            doc = []
            for card in map:
                d = {"DocumentNumber":card.get("ttn"), "Phone":card.get("phone")}
                doc.append(d)

            resp = CHB_Connector.getTrackingNova(self, doc)
            i = 0
            for item in resp:
                ttn = item.get('NUMBER')
                status = item.get('STATUS')
                status_code = int(item.get('STATUS_CODE'))

                card = Base.order_getCardTTN(self, ttn)
                card['debug'] = 2
                card['statusNP'] = status

                if status_code in self.UP_STATUS:
                    if card.get('statusCB') != "201":
                        print("CARD NEED LOAD: ", card.get('id'))

                        order_id = card.get("id")
                        response = CHB_Connector.make_sell(self, order_id)
                        status_code = response.get("status")
                        if status_code != 201:
                            card["statusCB"] = status_code
                            card["dateCB"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                        else:
                            card["statusCB"] = status_code
                            card["dateCB"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

                            Base.order_save(self, card)

                            progress = (i + 1) / len(map)
                            self.working.emit(progress)
                            i=i+1
                            time.sleep(1)

                    else:
                        print("CARD NO NEED LOAD: ", card.get('id'))
                else:
                    print("CARD NO NEED LOAD: ", card.get('id'))


                res = Base.order_save(self, card)

                if res.get('r') == False:
                    self.fail.emit(res.get('error'))
                else:
                    progress = (i + 1) / len(resp)
                    self.working.emit(progress)
                    i = i + 1
                    time.sleep(0.5)

        Base.disconnectDB(self)
        self.finished.emit()

