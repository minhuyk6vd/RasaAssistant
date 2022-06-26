import string
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

list_ten_san_bong = ["Tuyên Sơn", "Ngũ Hành Sơn", "Hoà Vang", "Nam Phước",
                    "Hoà Hải", "FPT", "Tân Sơn Nhất", "Hoà Sơn"]

list_ten_dia_ban = ["Quang Vinh", "Quang Thị Lại", "Nam Kì Khởi Nghĩa", "Nguyễn Hữu Thọ", 
                    "nam ki khoi nghia", "Nam Ki Khoi Nghia" ]

list_san_pham = ["giày","áo","quần","áo thun"]

class ActionShowLinkSanBong(Action):

    def name(self) -> Text:
        return "action_show_link_san_bong"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ten_san_bong = tracker.get_slot("ten_san_bong")
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="12345678",
        database="project_football_pitch")

        cur = mydb.cursor()
        sql = 'select f.* from football_pitchs f where f.name like "%{0}%" and f.user_id is not null;'.format(ten_san_bong)
        cur.execute(sql)
        for table in cur:
            id = table[0]

        if  ten_san_bong not in list_ten_san_bong :
            dispatcher.utter_message(text="Chúng tôi không có sân bóng nào tên như vậy cả. Vui lòng nhập đúng tên sân bóng!")
        else:
            dispatcher.utter_message(text=f"Đây là link sân bóng {ten_san_bong}, bạn vui lòng click vào link để xem chi tiết giá và thời gian đặt sân: https://92f2-116-105-174-200.ap.ngrok.io/booking/pitch/{id}")
        return []

class ActionShowLinkSanBongTrenDiaBan(Action):

    def name(self) -> Text:
        return "action_show_link_san_bong_tren_dia_ban"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ten_dia_ban = tracker.get_slot("ten_dia_ban")

        mydb = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="12345678",
        database="project_football_pitch")

        cur = mydb.cursor()
        sql = 'select f.* from football_pitchs f where f.street_number like "%{0}%" and f.user_id is not null;'.format(ten_dia_ban)
        cur.execute(sql)

        if  ten_dia_ban not in list_ten_dia_ban :
            dispatcher.utter_message(text="Xin lỗi chúng tôi không có sân bóng nào gần khu vực cả bạn cả!")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sân gần khu vực {ten_dia_ban}, bạn vui lòng click vào link từng sân để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[7]}: https://92f2-116-105-174-200.ap.ngrok.io/booking/pitch/{table[0]}")

        return []

class ActionShowLinkSanPhamChiTiet(Action):

    def name(self) -> Text:
        return "action_show_link_san_pham_chi_tiet"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        san_pham = tracker.get_slot("san_pham")

        mydb = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="12345678",
        database="project_football_pitch")

        cur = mydb.cursor()
        sql = 'select p.* from products p where p.name like "%{0}%" and p.quantity > 0 ;'.format(san_pham)
        cur.execute(sql)

        if  san_pham not in list_san_pham :
            dispatcher.utter_message(text="Xin lỗi chúng tôi không có sân bóng nào gần khu vực cả bạn cả!")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm {san_pham} mà chúng tôi đang bán, click vào từng link để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: https://92f2-116-105-174-200.ap.ngrok.io/product-detail/value={table[0]}/category={table[13]}")

        return []