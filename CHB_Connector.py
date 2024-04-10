# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot

import requests
import uuid

from Base import Base

class CHB_Connector(QObject):

    def __init__(self):
        QObject.__init__(self)
        Base.connectDB(self)



    @Slot(list, result=str)
    def get_token(self, l:list):
        url = "https://api.checkbox.in.ua/api/v1/cashier/signin"
        headers = {
            "accept": "application/json",
            "X-Client-Name": "PPO Test",
            "X-Client-Version": "v1",
            "Content-Type": "application/json"
        }

        payload = {
            "login": l[0],
            "password": l[1]
        }

        response = requests.post(url, headers=headers, json=payload)

        print(response.json())

        if response.status_code == 200:
            data = dict(response.json())
            r = data['access_token']
        else:
            r = str(response.status_code)
        return r

    @Slot(result=str)
    def get_cassir(self):
        token = Base.config_getToken(self)
        print("Token:", token)
        url = "https://api.checkbox.in.ua/api/v1/cashier/me"
        headers = {
            "accept": "application/json",
            "X-Client-Name": "PPO Test",
            "X-Client-Version": "v1",
            "Authorization": "Bearer " + token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = dict(response.json())
            r = data['full_name']
        else:
            r = str(response.status_code)
        return r

    @Slot(result=dict)
    def get_goods(self):
        token = Base.config_getToken(self)

        url = "https://api.checkbox.in.ua/api/v1/goods?without_group_only=false&load_children=false&limit=1000&offset=0"
        headers = {
            "accept": "application/json",
            "X-Client-Name": "PPO Test",
            "X-Client-Version": "v1",
            "Authorization": "Bearer " + token
        }
        response = requests.get(url, headers=headers)
        return dict(response.json())


    # @Slot()
    # def get_goods(self):
    #     token = Base.config_getToken(self)

    #     url = "https://api.checkbox.in.ua/api/v1/goods?without_group_only=false&load_children=false&limit=1000&offset=0"
    #     headers = {
    #         "accept": "application/json",
    #         "X-Client-Name": "PPO Test",
    #         "X-Client-Version": "v1",
    #         "Authorization": "Bearer " + token
    #     }
    #     response = requests.get(url, headers=headers)

    #     if response.status_code == 200:
    #         data = dict(response.json()).get('results')
    #         for item in data:
    #             d = {
    #                 "p_ids":item.get("id"),
    #                 "code":item.get("code"),
    #                 "name":item.get("name"),
    #                 "price":item.get("price")
    #             }
    #             Base.product_save(self, d)

    #     else:
    #         print(response.status_code)
    #         print(response.json())



    @Slot(int, int, result=dict)
    def make_sell(self, order_id:int, t:int):
        token = Base.config_getToken(self)

        card = Base.order_getCard(self, order_id)
        detail = Base.detail_getCard(self, order_id)
        pay = Base.detail_getCardSum(self, order_id)
        cassir = CHB_Connector.get_cassir(self)

        print("CARD: ", card)
        print("DETAIL: ", detail)

        url = "https://api.checkbox.in.ua/api/v1/receipts/sell"
        headers = {
            "accept": "application/json",
            "X-Client-Name": "PPO Test",
            "X-Client-Version": "v1",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }

        if t == 1:
            payment_label = "Передплата"
        elif t == 2:
            payment_label = "Безготівкова"

        payload = {
            "id": str(uuid.uuid4()),
            "cashier_name": cassir,
            "departament": "",
            # "goods":[
            #     {
            #     "good":{ "code": "31531", "name": "Toy BIg", "price": 18500 },
            #     "quantity": 1000,
            #     "is_return": False,
            #     "is_winnings_payout": False,
            #     }
            # ],
            "goods":detail,
            "delivery":{
                "phone": card.get("phone")
            },
            "discounts": [],
            "bonuses": [],            
            "payments":[{"type":"CASHLESS", "label":payment_label, "value":pay}],
            "rounding": False,
            "header": "",
            "footer": "",
            "barcode": ""
        }

        print("PAYLOAD: ", payload)

        response = requests.post(url, headers=headers, json=payload)

        r = {
            "status":response.status_code,
            "response":dict(response.json())
        }
        if response.status_code != 201:
            print(response.json())
        return r


    @Slot(list, result=list)
    def getTrackingNova(self, doc:list):
        url = "https://api.novaposhta.ua/v2.0/json/"

        payload = {
            "apiKey": "",
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {
                "Documents": doc
                # "Documents": [
                #     {"DocumentNumber": "59001129284111","Phone": "3800660048186"}
                # ]
            }
        }
        response = requests.get(url, json=payload)
        r = dict(response.json())
        l = []
        if r.get('success'):
            data = r.get('data')
            for item in data:
                d = {"NUMBER":item.get('Number'), "STATUS":item.get('Status'), "STATUS_CODE":item.get('StatusCode')}
                l.append(d)

        return l

        # print(response.json())
