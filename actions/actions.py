import string
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from datetime import date, datetime, timedelta
import mysql.connector


mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="12345678",
    database="project_football_pitch")

list_ten_san_bong = ["Tuyên Sơn", "Ngũ Hành Sơn", "Hoà Vang", "Nam Phước",
                    "Hoà Hải", "FPT", "Tân Sơn Nhất", "Hoà Sơn"]

list_ten_dia_ban = ["Quang Vinh", "Quang Thị Lại", "Nam Kì Khởi Nghĩa", "Nguyễn Hữu Thọ"]

list_san_pham = ["giày","áo","quần","áo thun"]


list_thoi_gian_ngay = ["ngày mai", "mai", "chiều mai", "sáng mai",
                    "ngày mốt", "mốt", "chiều mốt", "sáng mốt",
                    "hôm nay", "bữa nay", "chiều nay", "sáng nay"]

list_thoi_gian_gio = ["3 giờ", "4 giờ", "5 giờ", "6 giờ",
                    "7 giờ", "8 giờ", "9 giờ", "3 giờ chiều",
                    "4 giờ chiều", "5 giờ chiều", "6 giờ chiều", "7 giờ",]

hom_nay = ["hôm nay", "bữa nay", "chiều nay", "sáng nay"]
ngay_mai = ["ngày mai", "mai", "chiều mai", "sáng mai"]
ngay_mot = ["ngày mốt", "mốt", "chiều mốt", "sáng mốt"]

thoi_gian_5_gio = ["5 giờ chiều","5 giờ"]
thoi_gian_6_gio = ["6 giờ chiều","6 giờ"]
thoi_gian_7_gio = ["7 giờ chiều","7 giờ"]

link_web = "http://localhost:8080"


class ActionShowLinkSanBong(Action):

    def name(self) -> Text:
        return "action_show_link_san_bong"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ten_san_bong = tracker.get_slot("ten_san_bong")


        cur = mydb.cursor()
        sql = 'select f.* from football_pitchs f where f.name like "%{0}%" and f.user_id is not null;'.format(ten_san_bong)
        cur.execute(sql)
        for table in cur:
            id = table[0]

        if  ten_san_bong not in list_ten_san_bong :
            dispatcher.utter_message(text="Chúng tôi không có sân bóng nào tên như vậy cả. Vui lòng nhập đúng tên sân bóng!")
        else:
            dispatcher.utter_message(text=f"Đây là link sân bóng {ten_san_bong}, bạn vui lòng click vào link để xem chi tiết giá và thời gian đặt sân: "+link_web+f"/booking/pitch/{id}")
        return []

class ActionShowLinkSanBongTrenDiaBan(Action):

    def name(self) -> Text:
        return "action_show_link_san_bong_tren_dia_ban"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ten_dia_ban = tracker.get_slot("ten_dia_ban")

        cur = mydb.cursor()
        # sql = 'select f.* from football_pitchs f where f.street_number like "%{0}%" and f.user_id is not null;'.format(ten_dia_ban)

        sql = 'SELECT f.* FROM football_pitchs f \
                inner join wards w on f.ward_id = w.id \
                inner join districts d on w.district_id=d.id \
                where (d.district_name like "%{0}%" or w.ward_name like "%{0}%" or f.street_number like "%{0}%") and f.user_id is not null;'.format(ten_dia_ban)

        # sql = 'SELECT f.*, FROM football_pitchs f \
        #         inner join wards w on f.ward_id = w.id \
        #         inner join districts d on w.district_id=d.id \
        #         where d.district_name like "%{0}%" or w.ward_name like "%{0}%" \
        #         or f.street_number like "%{0}%" and user_id is not null;'.format(ten_dia_ban)
        cur.execute(sql)

        if  ten_dia_ban not in list_ten_dia_ban :
            dispatcher.utter_message(text="Xin lỗi chúng tôi không có sân bóng nào gần khu vực của bạn cả!")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sân gần khu vực {ten_dia_ban}, bạn vui lòng click vào link từng sân để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[7]}: "+link_web+f"/booking/pitch/{table[0]}")

        return []

class ActionShowLinkSanPhamChiTiet(Action):

    def name(self) -> Text:
        return "action_show_link_san_pham_chi_tiet"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        san_pham = tracker.get_slot("san_pham")

        cur = mydb.cursor()
        sql = 'select p.* from products p where p.name like "%{0}%" and p.quantity > 0 ;'.format(san_pham)
        cur.execute(sql)

        if  san_pham not in list_san_pham :
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không bán loại sản phẩm {san_pham}! Đây là danh sách sản phẩm đang được bày bán https://92f2-116-105-174-200.ap.ngrok.io/products")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm {san_pham} mà chúng tôi đang bán, click vào từng link để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: "+link_web+f"/product-detail/value={table[0]}/category={table[13]}")

        return []

class ActionShowLinkTatCaSanPhamBanChay(Action):

    def name(self) -> Text:
        return "action_show_link_tat_ca_san_pham_ban_chay"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = mydb.cursor()
        sql = 'select p.*,sum(o.quantity) as tongSoLuongBan from products p inner join order_detail \
            as o on o.product_id = p.id group by p.id order by tongSoLuongBan desc limit 8;'
        cur.execute(sql)

        dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm bán chạy của cửa hàng, click vào từng link để xem chi tiết:")
        for table in cur:
            dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: "+link_web+f"/product-detail/value={table[0]}/category={table[13]}")

        return []

class ActionShowLinkSanPhamBanChayTheoLoaiSanPham(Action):

    def name(self) -> Text:
        return "action_show_link_ban_chay_theo_loai_san_pham"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        san_pham = tracker.get_slot("san_pham")

        cur = mydb.cursor()
        sql = 'select p.*,sum(o.quantity) as tongSoLuongBan from products p inner join order_detail as o on o.product_id = p.id \
            where p.name like "%{0}%" group by p.id order by tongSoLuongBan desc limit 5;'.format(san_pham)
        cur.execute(sql)

        if  san_pham not in list_san_pham :
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không bán loại sản phẩm {san_pham}! Đây là danh sách sản phẩm đang được bày bán https://"+link_web+"/products")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm {san_pham} bán chạy của cửa hàng, click vào từng link để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: "+link_web+f"/product-detail/value={table[0]}/category={table[13]}")

        return []

class ActionShowLinkTatCaSanPhamMoiNhat(Action):

    def name(self) -> Text:
        return "action_show_link_tat_ca_san_pham_moi"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = mydb.cursor()
        sql = 'SELECT * FROM project_football_pitch.products where (status = 1 and quantity > 0) order by createddate DESC limit 8;'
        cur.execute(sql)

        dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm mới nhất của cửa hàng, click vào từng link để xem chi tiết:")
        for table in cur:
            dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: "+link_web+f"/product-detail/value={table[0]}/category={table[13]}")

        return []

class ActionShowLinkSanPhamMoiNhatTheoLoaiSanPham(Action):

    def name(self) -> Text:
        return "action_show_link_san_pham_moi_theo_loai"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        san_pham = tracker.get_slot("san_pham")

        cur = mydb.cursor()
        sql = 'SELECT * FROM project_football_pitch.products p where (status = 1 and quantity > 0 and p.name like "%{0} %") order by createddate DESC limit 5;'.format(san_pham)
        cur.execute(sql)

        if  san_pham not in list_san_pham :
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không bán loại sản phẩm {san_pham}! Đây là danh sách sản phẩm đang được bày bán https://"+link_web+"/products")
        else:
            dispatcher.utter_message(text=f"Đây là danh sách các sản phẩm {san_pham} mới nhất của của cửa hàng, click vào từng link để xem chi tiết:")
            for table in cur:
                dispatcher.utter_message(text=f"{table[8]}, giá:{table[9]}VND. Chi tiết: "+link_web+f"/product-detail/value={table[0]}/category={table[13]}")

        return []


class ValidateSanBongChuaDuocThueForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_san_bong_chua_duoc_thue_form"

    def validate_ten_san_bong(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
            if slot_value.lower() not in list_ten_san_bong:
                dispatcher.utter_message(text=f"Chúng tôi không có sân bóng nào tên như vậy cả. Vui lòng nhập đúng tên sân bóng!")
                return {"ten_san_bong":None}
            return {"ten_san_bong":slot_value}


    
    def validate_thoi_gian_ngay(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
            if slot_value.lower() not in list_thoi_gian_ngay:
                dispatcher.utter_message(text=f"Chúng tôi chỉ hỗ trợ xem các sân chưa được thuê vào hôm nay, ngày mai hoặc ngày mốt.")
                return{"thoi_gian_ngay":None}
            return{"thoi_gian_ngay":slot_value}

    
    
    def validate_thoi_gian_gio(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
            if slot_value.lower() not in list_thoi_gian_ngay:
                dispatcher.utter_message(text=f"Xin lỗi chúng tôi không hiểu thời gian bạn đã nhập")
                return{"thoi_gian_gio":None}
            return{"thoi_gian_gio":slot_value}


class ActionClearSlots(Action):

    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: "CollectingDispatcher", 
             tracker: Tracker, 
            domain: "DomainDict") -> List[Dict[Text, Any]]:


        return [SlotSet('ten_san_bong', None),
                 SlotSet('thoi_gian_ngay', None),
                SlotSet('thoi_gian_gio', None)]

class ActionShowLinkSanChuaDuocThue(Action):

    def name(self) -> Text:
         return "action_show_link_san_chua_duoc_thue"

    def run(self, dispatcher: "CollectingDispatcher", 
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:

        ten_san_bong = tracker.get_slot("ten_san_bong")
        thoi_gian_ngay = tracker.get_slot("thoi_gian_ngay")
        thoi_gian_gio = tracker.get_slot("thoi_gian_gio")

        if thoi_gian_ngay in hom_nay:
            thoi_gian_ngay = datetime.now().strftime('%Y-%m-%d')
        elif  thoi_gian_ngay in ngay_mai:
            thoi_gian_ngay = (datetime.now()+timedelta(1)).strftime('%Y-%m-%d')
        elif thoi_gian_ngay in ngay_mot:
            thoi_gian_ngay = (datetime.now()+timedelta(2)).strftime('%Y-%m-%d')

        if thoi_gian_gio in thoi_gian_5_gio:
            thoi_gian_gio = "17:00:00"
        elif thoi_gian_gio in thoi_gian_6_gio:
            thoi_gian_gio = "18:00:00"
        elif thoi_gian_gio in thoi_gian_7_gio:
            thoi_gian_gio = "19:00:00"

        cur = mydb.cursor()

        sql = "select distinct sp.id from football_pitchs_schedule fps \
                inner join sub_pitch sp on fps.sub_pitch_id = sp.id \
                inner join football_pitchs fp on sp.pitch_pitch_id = fp.id \
                where sp.name like '%"+ten_san_bong+"%' and fps.date_booking != '"+thoi_gian_ngay+"' \
                and '"+thoi_gian_gio+"' not between fps.time_start and fps.time_end  ;"

        cur.execute(sql)
        dispatcher.utter_message(text=f"Đây là danh sách các sân nhỏ còn trống, bạn vui lòng click vào link từng sân nhỏ để xem chi tiết:")
        for table in cur:
                dispatcher.utter_message(text=f"{table[0]}: "+link_web+f"/booking/pitch/{table[0]}")
                dispatcher.utter_image_url("")
        
        return []




