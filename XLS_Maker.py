# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot
from openpyxl import load_workbook
import requests
import json
import uuid

from Base import Base

class XLS_Maker(QObject):



    def __init__(self):
        QObject.__init__(self)
        Base.connectDB(self)

    @Slot(str, result=str)
    def url_name(self, file :str):
        file = file.replace("file:///", "")
        file = file.replace("/", "\\")
        # self.fname = file
        return file

    @Slot(str, result=list)
    def get_data(self, fname:str):
        print("DEL DEBUG DATA")
        Base.order_del_debug(self)

        print("GET DATA")


        if fname != "":

            wb = load_workbook(fname)
            sheets = wb.sheetnames
            sheet = wb[sheets[0]]

            row_start = 2
            row_count = 1
            for row in sheet.iter_rows(values_only=True):
                row_count = row_count + 1

            for r in range(row_start, row_count, 1):
                phone = "38" + str(sheet["A" + str(r)].value).replace("-", "").replace(" ", "")
                product = sheet["B" + str(r)].value
                code = product.split(" ")[-1]
                quan = str(sheet["C" + str(r)].value)
                ttn = sheet["D" + str(r)].value

                product_count = len(product.split("\n"))

                #make order
                otype = 1 if ttn == None else 2

                l = {
                    "id":0,
                    "type":otype,
                    "phone":phone,
                    "ttn":ttn,
                    "debug":1
                }

                order = Base.order_save(self, l)
                order_id = order.get('id')

                if order.get('r') == True:
                    if product_count == 0:

                        d = {
                            "id":0,
                            "p_order":order_id,
                            "p_name":product,
                            "p_code":code,
                            "p_quan":quan.split(" ")[0],
                            "p_ids":Base.product_getIDS(self, code),
                        }

                        detail = Base.detail_save(d)

                        if detail.get('r') == False:
                            return [0, detail.get("error")]

                    elif product_count > 0:
                        for p in range(0, product_count, 1):
                            d = {
                                "id":0,
                                "p_order":order_id,
                                "p_name":product.split("\n")[p],
                                "p_code":code,
                                "p_quan":quan.split("\n")[p].split(" ")[0],
                                "p_ids":Base.product_getIDS(self, code),
                            }

                            detail = Base.detail_save(d)
                            if detail.get('r') == False:
                                return [0, detail.get("error")]
                else:
                    return [0, order.get("error")]
            return [1, ""]
        else:
            return [0, "No file"]

