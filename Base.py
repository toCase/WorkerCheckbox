# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, QDateTime
from PySide6.QtSql import QSqlDatabase, QSqlQuery


class Base(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.connectDB

    @Slot()
    def connectDB(self):
        db = QSqlDatabase.database("base")
        if db.isOpen() == False:
            db = QSqlDatabase.addDatabase("QSQLITE", "base")
            db.setDatabaseName("base.db3")
            db.open()

            if db.isOpen():
                qstr = [
                '''CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                o_date INTEGER, o_type INTEGER, o_phone TEXT, o_ttn TEXT, o_debug INTEGER,
                statusNP TEXT, statusCB TEXT, dateCB TEXT)''',
                '''CREATE TABLE IF NOT EXISTS Config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                c_login TEXT, c_pass TEXT, c_token TEXT, c_token_np TEXT)''',
                '''CREATE TABLE IF NOT EXISTS Detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                p_order INTEGER, p_name TEXT, p_code TEXT, p_quan TEXT, p_ids TEXT)''',

                '''CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                p_ids TEXT, p_name TEXT, p_code TEXT, p_price TEXT)''',
                ]

                for q in qstr:
                    query = QSqlQuery(q, db)
                    query.exec()

    @Slot()
    def disconnectDB(self):
        db = QSqlDatabase.database("base")
        if db.isOpen():
            db.close()


    @Slot(int, int, result=list)
    def order_get(self, otype:int, odebug:int):
        r = []
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = '''SELECT O.id, O.o_phone, O.o_ttn, O.statusNP, O.statusCB, O.dateCB FROM Orders AS O
            WHERE (O.o_type = \'{}\' AND O.o_debug = \'{}\')
            '''.format(otype, odebug)
            query = QSqlQuery(qstr, db)

            while query.next():
                d = {
                    'id':query.value(0),
                    'phone':query.value(1),
                    'ttn':query.value(2),
                    'statusNP':query.value(3),
                    'statusCB':query.value(4),
                    'dateCB':query.value(5),
                }
                r.append(d)
            else:
                return r
        return r

    @Slot(int, result=dict)
    def order_getCard(self, id:int):
        r = {}
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = '''SELECT O.id, O.o_phone, O.o_ttn, O.statusNP, O.statusCB, O.dateCB FROM Orders AS O
            WHERE (O.id = \'{}\')
            '''.format(id)
            query = QSqlQuery(qstr, db)
            query.next()
            r = {
            'id':query.value(0),
            'phone':query.value(1),
            'ttn':query.value(2),
            'statusNP':query.value(3),
            'statusCB':query.value(4),
            'dateCB':query.value(5),
            }
        return r


    @Slot(str, result=dict)
    def order_getCardTTN(self, ttn:str):
        r = {}
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = '''SELECT O.id, O.o_phone, O.o_ttn, O.statusNP, O.statusCB, O.dateCB FROM Orders AS O
            WHERE (O.o_ttn = \'{}\')
            '''.format(ttn)
            query = QSqlQuery(qstr, db)
            query.next()
            r = {
            'id':query.value(0),
            'phone':query.value(1),
            'ttn':query.value(2),
            'statusNP':query.value(3),
            'statusCB':query.value(4),
            'dateCB':query.value(5),
            }
        return r


    @Slot(dict, result=dict)
    def order_save(self, l:dict):
        result:dict
        id = l.get("id")
        db = QSqlDatabase.database("base")
        if db.isOpen():
            if id == 0:
                q_str = '''INSERT INTO Orders (o_date, o_type, o_phone, o_ttn, o_debug, statusNP, statusCB, dateCB)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
                query = QSqlQuery(q_str, db)
                query.bindValue(0, QDateTime.currentSecsSinceEpoch())
                query.bindValue(1, l.get("type"))
                query.bindValue(2, l.get("phone"))
                query.bindValue(3, l.get("ttn"))
                query.bindValue(4, l.get("debug"))
                query.bindValue(5, "")
                query.bindValue(6, "")
                query.bindValue(7, "")
                r = query.exec()
                result = {
                'r':r,
                'error':query.lastError().text()
                }
                if r:
                    result['id'] = int(query.lastInsertId())
            elif id > 0:
                q_str = '''UPDATE Orders SET o_debug = \'{}\', statusNP = \'{}\', statusCB = \'{}\',
                dateCB = \'{}\' WHERE (Orders.id = \'{}\') '''.format(
                l.get("debug"), l.get("statusNP"), l.get("statusCB"), l.get("dateCB"), id)
                query = QSqlQuery(q_str, db)
                r = query.exec()
                result = {
                'r':r,
                'error':query.lastError().text()
                }
        else:
            result = {
                'r': False,
                'error': "No connect to db"
            }
        return result;

    @Slot()
    def order_del_debug(self):
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = "SELECT Orders.id FROM Orders WHERE (Orders.o_debug = \'1\')"
            query = QSqlQuery(qstr, db)
            while query.next():
                qstr = "DELETE FROM Detail WHERE (Detail.p_order = \'{}\')".format(int(query.value(0)))
                queryA = QSqlQuery(qstr, db)
                queryA.exec()
            qstr = "DELETE FROM Orders WHERE (Orders.o_debug = \'1\')"
            query = QSqlQuery(qstr, db)
            query.exec()

    @Slot(int)
    def order_del(self, order:int):
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = "DELETE FROM Detail WHERE (Detail.p_order = \'{}\')".format(order)
            queryA = QSqlQuery(qstr, db)
            queryA.exec()

            qstr = "DELETE FROM Orders WHERE (Orders.id = \'{}\')".format(order)
            query = QSqlQuery(qstr, db)
            query.exec()

    @Slot()
    def order_delDone(self):
        print("ORDER DELETE DONE")
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = "SELECT Orders.id FROM Orders WHERE (Orders.statusCB = \'201\')"
            query = QSqlQuery(qstr, db)
            while query.next():
                qstr = "DELETE FROM Detail WHERE (Detail.p_order = \'{}\')".format(int(query.value(0)))
                queryA = QSqlQuery(qstr, db)
                queryA.exec()
            qstr = "DELETE FROM Orders WHERE (Orders.statusCB = \'201\')"
            query = QSqlQuery(qstr, db)
            query.exec()




    @Slot(int, result=list)
    def detail_getX(self, order:int):
        l = []
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = "SELECT Detail.p_name, Detail.p_quan, Detail.p_ids FROM Detail WHERE Detail.p_order = \'{}\'".format(order)
            query = QSqlQuery(qstr, db)
            while query.next():
                s = str(query.value(0)) + "  кіл-ть: " + str(query.value(1))
                if query.value(2) == "None":
                    s = s + " -- <b>Немає в CHECKBOX</b>"
                l.append(s)
        return l

    @Slot(int, result=list)
    def detail_getCard(self, order:int):
        l = []
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = '''SELECT Detail.p_name, Detail.p_code, Detail.p_quan, Products.p_price
            FROM Detail
            INNER JOIN Products ON Products.p_ids = Detail.p_ids
            WHERE Detail.p_order = \'{}\' '''.format(order)
            query = QSqlQuery(qstr, db)
            while query.next():
                d = {
                # "good":{"code": "", "name": query.value(0), "price": int(query.value(3))},
                "good":{"code": query.value(1), "name": query.value(0), "price": int(query.value(3))},                
                "quantity": int(query.value(2)) * 1000,
                "is_return": False,
                "is_winnings_payout": False,
                }
                l.append(d)
        return l

    @Slot(int, result=int)
    def detail_getCardSum(self, order:int):
        r = 0
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = '''SELECT SUM(Detail.p_quan * Products.p_price)
            FROM Detail
            INNER JOIN Products ON Products.p_ids = Detail.p_ids
            WHERE Detail.p_order = \'{}\' '''.format(order)
            query = QSqlQuery(qstr, db)
            query.next()
            r = int(query.value(0))
        return r



    @Slot(dict)
    def detail_save(l:dict):
        result = {}
        db = QSqlDatabase.database("base")
        if db.isOpen():
            id = l.get("id")
            if id == 0:
                qstr = '''INSERT INTO Detail (p_order, p_name, p_code, p_quan, p_ids)
                VALUES (?, ?, ?, ?, ?)'''
                query = QSqlQuery(qstr, db)
                query.bindValue(0, l.get('p_order'))
                query.bindValue(1, l.get('p_name'))
                query.bindValue(2, l.get('p_code'))
                query.bindValue(3, l.get('p_quan'))
                query.bindValue(4, l.get('p_ids'))
                r = query.exec()
                result = {
                'r':r,
                'error':query.lastError().text()
                }
                if r:
                    result['id'] = int(query.lastInsertId())
            elif id > 0:
                qstr = '''UPDATE Detail SET p_order = \'{}\', p_name = \'{}\', p_code = \'{}\',
                p_quan = \'{}\', p_ids = \'{}\' WHERE (Detail.id = \'{}\') '''.format(
                    l.get('p_order'), l.get('p_name'), l.get('p_code'), l.get('p_quan'), l.get('p_ids'), id
                )
                query = QSqlQuery(qstr, db)
                r = query.exec()
                result = {
                'r':r,
                'error':query.lastError().text()
                }
        else:
            result = {
                'r': False,
                'error': "No connect to db"
            }
        return result;




    @Slot(result=list)
    def get_config(self):
        r = []
        db = QSqlDatabase.database("base")
        if db.isOpen():
            q_str = "SELECT c_login, c_pass, c_token, c_token_np FROM Config WHERE Config.id = \'1\' "
            query = QSqlQuery(q_str, db)
            query.next()
            r = [str(query.value(0)), str(query.value(1)), str(query.value(2)), str(query.value(3))]
        return r


    @Slot(list, result=list)
    def set_config(self, l:list):
        db = QSqlDatabase.database("base")
        if db.isOpen():
            qstr = "SELECT Config.id FROM Config WHERE Config.id = \'1\'"
            query = QSqlQuery(qstr, db)
            query.next()
            id = query.value(0)
            if id == None:
                qstr = "INSERT INTO Config (c_login, c_pass, c_token, c_token_np) VALUES (?, ?, ?, ?)"
                query = QSqlQuery(qstr, db)
                query.bindValue(0, l[0])
                query.bindValue(1, l[1])
                query.bindValue(2, l[2])
                query.bindValue(3, l[3])
                r = query.exec()
            else:
                q_str = '''UPDATE Config SET c_login = \'{}\', c_pass = \'{}\',
                c_token = \'{}\', c_token_np = \'{}\' WHERE Config.id = \'1\' '''.format(
                l[0], l[1], l[2], l[3]
                )
                query = QSqlQuery(q_str, db)
                r = query.exec()
            if r:
                d = [0, ""]
            else:
                d = [1, query.lastError().text()]
        else:
            d = [1, "No connect to db"]
        return d

    @Slot(result=str)
    def config_getToken(self):
        print("GET TOKEN")
        db = QSqlDatabase.database("base")
        r = ""
        if db.isOpen():
            q_str = "SELECT Config.c_token FROM Config WHERE Config.id = \'1\' "
            query = QSqlQuery(q_str, db)
            query.next()
            if query.isValid():
                r = str(query.value(0))
        return r

    @Slot(dict)
    def product_save(self, l:dict):
        db = QSqlDatabase.database("base")
        # r = ""
        p_ids = l.get("p_ids")
        if db.isOpen():
            qstr = "SELECT Products.id FROM Products WHERE Products.p_ids = \'{}\'".format(p_ids)
            query = QSqlQuery(qstr, db)
            query.next()
            id = query.value(0)
            if id != None:
                qstr = '''UPDATE Products SET p_ids = \'{}\', p_code = \'{}\', p_name = \'{}\', p_price = \'{}\'
                WHERE Products.id = \'{}\' '''.format(l.get("p_ids"), l.get("code"), l.get("name"), l.get("price"), id)
                query = QSqlQuery(qstr, db)
                query.exec()
            else:
                qstr = '''INSERT INTO Products (p_ids, p_code, p_name, p_price)
                VALUES (?, ?, ?, ?)'''
                query = QSqlQuery(qstr, db)
                query.bindValue(0, l.get("p_ids"))
                query.bindValue(1, l.get("code"))
                query.bindValue(2, l.get("name"))
                query.bindValue(3, l.get("price"))
                query.exec()

    @Slot(result=list)
    def product_get(self):
        db = QSqlDatabase.database("base")
        r = []
        if db.isOpen():
            qstr = "SELECT P.id, P.p_ids, P.p_name, P.p_code, P.p_price FROM Products AS P "
            query = QSqlQuery(qstr, db)
            while query.next():
                d = {
                    "id":str(query.value(0)),
                    "p_ids":str(query.value(1)),
                    "p_name":str(query.value(2)),
                    "p_code":str(query.value(3)),
                    "p_price":str(query.value(4))
                }
                r.append(d)
        return r

    @Slot(str, result=str)
    def product_getIDS(self, code:str):
        db = QSqlDatabase.database("base")
        r = ""
        if db.isOpen():
            qstr = "SELECT P.p_ids FROM Products AS P WHERE (P.p_code = \'{}\')".format(code)
            query = QSqlQuery(qstr, db)
            query.next()
            r = str(query.value(0))
        return r



