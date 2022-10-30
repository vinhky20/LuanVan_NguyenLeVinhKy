import mysql.connector as con
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction
import numpy as np
import requests
from datetime import datetime


class booking_form(Action):
    def name(self) -> Text:
        return "booking_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["service", "clinic", "customer",
                          "phone", "email", "date", "time", "note"]


class submit_form_booking(Action):
    def name(self) -> Text:
        return "action_submit_form"
    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            template="utter_slots_values", gender=tracker.get_slot("gender"), service_book=tracker.get_slot("service"),
            clinic_book=tracker.get_slot("clinic"), customer_book=tracker.get_slot("customer"),
            phone_book=tracker.get_slot("phone"), email_book=tracker.get_slot("email"),
            date_book=tracker.get_slot("date"), time_book=tracker.get_slot("time"), note_book=tracker.get_slot("note")
        )
        select = ["Đồng ý đặt lịch", "Bỏ đặt lịch"]
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/book_intent{\"book_check\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class insert_form_booking(Action):
    def name(self) -> Text:
        return "action_insert_val_form"
    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:
        book_check = tracker.get_slot("book_check")
        print('book check: ', book_check)
        service = tracker.get_slot("service")
        clinic = tracker.get_slot("clinic")
        customer = tracker.get_slot("customer")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        note = tracker.get_slot("note")
        gender = tracker.get_slot("gender")
        genderChanged = 'Nam'
        if (gender == 'Chị'):
            genderChanged = 'Nữ'
        print(genderChanged)
        #################################################
        # lay id dich vu
        response = requests.get("http://localhost:5000/services")
        data = response.json()
        for x in data:
            if (x['SERVICE_NAME'] == service):
                idService = x['SERVICE_ID']
        print(idService)
        # convert ngay
        date = tracker.get_slot("date")
        dateChanged = datetime.strptime(date, "%Y-%m-%d")
        # date_object = datetime.strptime(date, "%Y-%m-%d")
        # print("date_object =", date_object)
        # timestamp = datetime.timestamp(date_object)
        # dateChanged = str(timestamp).replace(".0", "") + '000'
        # print(dateChanged)

        # layIDphòngkhám
        response = requests.get("http://localhost:5000/clinics")
        data = response.json()
        for x in data:
            if (x['CLINIC_NAME'] == clinic):
                idClinic = x['CLINIC_ID']
        print(idClinic)

        # timeChanged
        time = tracker.get_slot("time")
        timeChanged = 'T1'

        if (time == '8h30-9h00'):
            timeChanged = 'T2'
        elif (time == '9h00-9h30'):
            timeChanged = 'T3'
        elif (time == '9h30-10h00'):
            timeChanged = 'T4'
        elif (time == '10h00-10h30'):
            timeChanged = 'T5'
        elif (time == '10h30-11h00'):
            timeChanged = 'T6'
        elif (time == '11h00-11h30'):
            timeChanged = 'T7'
        elif (time == '13h00-13h30'):
            timeChanged = 'T8'
        elif (time == '13h30-14h00'):
            timeChanged = 'T9'
        elif (time == '14h00-14h30'):
            timeChanged = 'T10'
        elif (time == '14h30-15h00'):
            timeChanged = 'T11'
        elif (time == '15h00-15h30'):
            timeChanged = 'T12'
        elif (time == '15h30-16h00'):
            timeChanged = 'T13'
        elif (time == '16h00-16h30'):
            timeChanged = 'T14'
        elif (time == '16h30-17h00'):
            timeChanged = 'T15'
        elif (time == '17h00-17h30'):
            timeChanged = 'T16'

        print(timeChanged)
        # apipost
        booking = {"BOOKING_CLINIC": idClinic, "BOOKING_TIMESLOT": timeChanged, "BOOKING_DATE": dateChanged, "BOOKING_EMAIL": email, "BOOKING_STATUS": 0,
                   "BOOKING_CUSTOMER": customer, "BOOKING_GENDER": genderChanged, "BOOKING_SERVICE": idService, "BOOKING_CONTACT_PHONE": phone, "BOOKING_NOTE": note}
        response = requests.post(
            "http://localhost:5000/bookings", data=booking)
        # print (str(response.content)) == response.text
        booking2 = {"BOOKING_CLINIC": idClinic,
                    "BOOKING_DATE": dateChanged, "BOOKING_TIMESLOT": timeChanged}
        res = response.json()
        if (res['errCode'] == 0):
            dispatcher.utter_message("Đặt lịch thành công")
            response2 = requests.post(
                "http://localhost:5000/update-slot-schedule", data=booking2)
        elif (res['errCode'] == 1):
            dispatcher.utter_message(
                "Đặt lịch không thành công, vui lòng đặt lại !")
        if (book_check == "Bỏ đặt lịch"):
            dispatcher.utter_message("Đã huỷ đặt lịch")


class AskSlotServiceAction(Action):
    def name(self) -> Text:
        return "action_ask_service"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        services = []
        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        for x in data['data']:
            services.append(x['ServiceData']['valueVi'])
        print(services)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(
            gender + ' vui lòng chọn dịch vụ mình muốn ạ:')
        for x in services:
            button.append(
                {"title": x, "payload": '/give_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskSlotClinicAction(Action):
    def name(self) -> Text:
        return "action_ask_clinic"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        clinics = []
        response = requests.get("http://localhost:5000/get-all-doctors")
        data = response.json()
        for x in data['data']:
            clinics.append(x['firstName'])
        print(clinics)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(gender + ' vui lòng chọn nha sĩ muốn khám')
        for x in clinics:
            button.append(
                {"title": "" + x, "payload": '/give_clinic{\"clinic\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskSlotTimeAction(Action):
    def name(self) -> Text:
        return "action_ask_time"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        service = tracker.get_slot("service")
        clinic = tracker.get_slot("clinic")
        # layIDnhasi
        response = requests.get("http://localhost:5000/get-all-doctors")
        data = response.json()
        for x in data['data']:
            if (x['firstName'] == clinic):
                idClinic = x['id']
        print(idClinic)
        # convert ngay
        date = tracker.get_slot("date")
        date_object = datetime.strptime(date, "%d/%m/%Y")
        print("date_object =", date_object)
        timestamp = datetime.timestamp(date_object)
        dateChanged = str(timestamp).replace(".0", "") + '000'
        print(dateChanged)
        # lay khung gio
        api = 'http://localhost:5000/get-schedule-doctor-by-date?doctorId=' + str(
            idClinic) + '&date=' + dateChanged
        response2 = requests.get(api)
        data2 = response2.json()
        arr = []  # listtime
        for x in data2['data']:
            if (x['currentNumber'] != 1):
                arr.append(x['timeTypeData']['valueVi'])
        print(arr)
        if not arr:
            dispatcher.utter_message('Ngày vừa chọn không có khung giờ trống')
            dispatcher.utter_message('Vui lòng chọn ngày khác!')
        else:
            dispatcher.utter_message('Hãy chọn thời gian đến khám bệnh:')
        button = []
        for x in arr:
            button.append(
                {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskSlotNoteAction(Action):
    def name(self) -> Text:
        return "action_ask_note"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(gender + ' có lưu ý gì không ạ')
        dispatcher.utter_message("Nếu có lưu ý, vui lòng nhập phía dưới")
        select2 = ["Không"]
        button = []
        for x in select2:
            button.append(
                {"title": x, "payload": '/book_note{\"note\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class Greet(Action):
    def name(self) -> Text:
        return "rep_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Dạ để tiện xưng hô, anh/chị vui lòng chọn giúp em danh xưng mình muốn được gọi nhé:')
        select = ['Anh', 'Chị']
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/get_gender{\"gender\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class Gender(Action):
    def name(self) -> Text:
        return "rep_get_gender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Xin chào ' + service.lower() + ' đã đến với Thế Giới Nha Khoa')
        return []


class Goodbye(Action):
    def name(self) -> Text:
        return "rep_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Dạ xin chào tạm biệt ' + service.lower() + '. Hẹn gặp lại ' + service.lower() + ' ạ!')
        return []


class Ask(Action):
    def name(self) -> Text:
        return "rep_ask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Dạ ' + gender.lower() + ' vui lòng chọn dịch vụ mình muốn được tư vấn ạ:')

        services = []
        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        for x in data['data']:
            services.append(x['ServiceData']['valueVi'])
        button = []
        for x in services:
            button.append(
                {"title": x, "payload": '/ask_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskService(Action):
    def name(self) -> Text:
        return "rep_ask_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        service = tracker.get_slot("service")
        serviceChange = service.lower()
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['description']
        dispatcher.utter_message(arr[serviceChange])

        return []


class AskPrice(Action):

    def name(self) -> Text:
        return "rep_ask_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        service = tracker.get_slot('price')
        serviceChange = service.lower()
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['PriceData']['valueVi']
        print(arr)
        print(arr[tracker.get_slot('price')])
        dispatcher.utter_message(arr[serviceChange])
        return []

# class AskPrice(Action):
#
#     def name(self) -> Text:
#         return "rep_ask_price"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         response = requests.get("http://localhost:5000/service-chatbot")
#         data = response.json()
#         price = tracker.get_slot('price')
#         arr = []
#         for x in data['data']:
#             if (x['ServiceData']['valueVi']) == price:
#                 arr[0].append(x['PriceData']['valueVi'])
#         print(arr[0])
#         dispatcher.utter_message('Dạ giá của dich vụ ' + price + ' là: ' + str(arr[0]) + ' VNĐ')
#         return []


class AskTimeToDo(Action):

    def name(self) -> Text:
        return "rep_ask_timetodo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        timetodo = tracker.get_slot('timetodo')
        timetodoChange = timetodo.lower()
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['timetodo']
        dispatcher.utter_message(arr[timetodoChange])

        return []


class AskAddress(Action):

    def name(self) -> Text:
        return "rep_ask_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("http://localhost:5000/service-chatbot")
        data = response.json()
        address = tracker.get_slot('address')
        addressChange = address.lower()
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['address']
        dispatcher.utter_message(arr[addressChange])

        return []


class AskDental(Action):
    def name(self) -> Text:
        return "rep_ask_dental"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dental = tracker.get_slot("dental")
        response = requests.get("http://localhost:5000/get-all-doctors")
        data = response.json()
        id = ''
        for x in data['data']:
            if (x['firstName'] == dental):
                id += str(x['id'])
        api = 'http://localhost:5000/get-detail-doctor-by-id?id=' + id
        response2 = requests.get(api)
        data2 = response2.json()
        # if(data2['data']['Markdown']['description'] == null):
        dispatcher.utter_message(data2['data']['Markdown']['description'])
        return []


class AskListDental(Action):
    def name(self) -> Text:
        return "rep_ask_list_dental"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Dạ đây là danh sách nha sĩ của phòng khám ạ:')
        clinics = []
        response = requests.get("http://localhost:5000/get-all-doctors")
        data = response.json()
        for x in data['data']:
            clinics.append(x['firstName'])
        button = []
        for x in clinics:
            button.append(
                {"title": x, "payload": '/ask_dental{\"dental\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []
