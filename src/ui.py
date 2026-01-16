from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '540')

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.core.text import LabelBase
from kivy.network.urlrequest import UrlRequest
from src.location import get_loc
import json
#Change the ip address
SERVER_IP = "192.168.1.3"
API_URL = f"http://{SERVER_IP}:8000/predict"

LabelBase.register(
    name="Meitei",
    fn_regular="fonts/NotoSansMeeteiMayek-Medium.ttf"
)

Builder.load_file("src/ui.kv")

weather_data = {
    "today": {"temp_max": 0, "temp_min": 0, "rainfall_mm": 0, "humidity": 0, "wind_speed": 0},
    "tomorrow": {"temp_max": 0, "temp_min": 0, "rainfall_mm": 0, "humidity": 0, "wind_speed": 0},
    "day_after": {"temp_max": 0, "temp_min": 0, "rainfall_mm": 0, "humidity": 0, "wind_speed": 0},
    "warnings": {},
    "overall_alert": "NORMAL"
}


class WeatherUI(BoxLayout):

    today_temp_max = NumericProperty(0)
    today_temp_min = NumericProperty(0)
    tomorrow_temp_max = NumericProperty(0)
    tomorrow_temp_min = NumericProperty(0)
    day_after_temp_max = NumericProperty(0)
    day_after_temp_min = NumericProperty(0)

    today_rainfall_mm = NumericProperty(0)
    tomorrow_rainfall_mm = NumericProperty(0)
    day_after_rainfall_mm = NumericProperty(0)

    lang = StringProperty("en")

    translations = {
        "en": {
            "title": "Sangai Weather",
            "forecast": "Weather Forecast",
            "today": "TODAY",
            "tomorrow": "Tomorrow",
            "day_after": "Day After Tomorrow",
            "temp": "Temperature",
            "rainfall_mm": "Rainfall",
            "more": "More Info"
        },
        "mni": {
            "title": "ꯁꯥꯡꯒꯥꯏ ꯋꯦꯗꯔ",
            "forecast": "ꯋꯦꯗꯔ ꯐꯣꯔꯀꯥꯁ꯭ꯇ",
            "today": "ꯅꯨꯡꯁꯤ",
            "tomorrow": "ꯅꯤꯡꯊꯥꯡ",
            "day_after": "ꯂꯩꯡꯊꯥꯡ",
            "temp": "ꯍꯤꯟꯅꯩ",
            "rainfall_mm": "ꯂꯩꯔꯥꯟ",
            "more": "ꯍꯣꯠꯅ ꯑꯃꯇ"
        }
    }

    def t(self, key):
        return self.translations[self.lang][key]

    def switch_lang(self):
        self.lang = "mni" if self.lang == "en" else "en"

    

    def send_location(self):
        print("SENDING POST REQUEST")  

        payload = {
            "lat": get_loc()[0],
            "lon": get_loc()[1],
            "district": "Imphal East",
            "rainfall_3d": None,
            "soil_moisture": 0.4,
            "slope": 10,
            "elevation": 500
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        UrlRequest(
            API_URL,
            req_body=json.dumps(payload).encode("utf-8"),
            req_headers=headers,
            on_success=self.on_success,
            on_error=self.on_error,
            on_failure=self.on_failure,
            method="POST",
            timeout=10
        )



    def on_success(self, req, result):
        global weather_data
        weather_data = result
        self.set_data()
        self.check_warnings()

    def on_error(self, req, error):
        self.show_popup(f"Server Error:\n{error}")

    def on_failure(self, req, result):
        self.show_popup("Cannot connect to FastAPI server\nCheck WiFi / Firewall / IP")

    def get_data(self):
        return weather_data

    def set_data(self):
        data = self.get_data()

        self.today_temp_max = data["today"]["temp_max"]
        self.today_temp_min = data["today"]["temp_min"]
        self.today_rainfall_mm = 0

        self.tomorrow_temp_max = data["tomorrow"]["temp_max"]
        self.tomorrow_temp_min = data["tomorrow"]["temp_min"]
        self.tomorrow_rainfall_mm = 0

        self.day_after_temp_max = data["day_after"]["temp_max"]
        self.day_after_temp_min = data["day_after"]["temp_min"]
        self.day_after_rainfall_mm =0


    def check_warnings(self):
        warnings = self.get_data().get("warnings", {})

        for event, info in warnings.items():
            if info.get("active"):# add not to check
                msg = (
                    f"{event.upper()}\n\n"
                    f"Severity: {info['severity']}\n"
                    f"Reason: {info['reason']}"
                )
                self.show_popup(msg)

    def show_popup(self, text):
        lbl = Label(
            text=text,
            halign="center",
            valign="middle",
            text_size=(300, None),
            size_hint=(None, None),
            size=(340, 200)
        )

        layout = BoxLayout(padding=[15, 15, 15, 20])
        layout.add_widget(lbl)
        popup = Popup(
            title="Weather Alert",
            content=layout,
            size_hint=(None, None),
            size=(420, 400),
            auto_dismiss=True
         )
        popup.open()

    def show_details(self, day):
        d = self.get_data()[day]
        text = (
            f"Humidity: {d['humidity']}%\n"
            f"Wind Speed: {d['wind_speed']} km/h\n"
        )

        Popup(
            title="Weather Details",
            content=Label(text=text),
            size_hint=(.8, .4)
        ).open()


class WeatherApp(App):
    def build(self):
        return WeatherUI()

    def on_start(self):
        print("APP STARTED")
        Clock.schedule_once(self.debug_start, 1)

    def debug_start(self, dt):
        print("CALLING send_location()")
        self.root.send_location() 


if __name__ == "__main__":
    WeatherApp().run()