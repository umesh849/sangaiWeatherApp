from kivy.config import Config
Config.set('graphics', 'width', '360')   
Config.set('graphics', 'height', '540')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.core.text import LabelBase

LabelBase.register(
    name="Meitei",
    fn_regular="fonts/NotoSansMeeteiMayek-Medium.ttf"
)
Builder.load_file("src/ui.kv")

weather_data = {
  "location": {
    "lat": 24.8039,
    "lon": 93.9420,
    "district": "Imphal East"
  },

  "timestamp": "2026-01-15T22:30:45+05:30",

  "observed_weather": {
    "temperature_c": 32.4,
    "pressure_hpa": 1006,
    "humidity_percent": 71,
    "wind_speed_mps": 3.2
  },
    "today": {
        "temp_max": 32,
        "temp_min": 28,
        "rainfall_mm": 150,
        "humidity": 65,
        "wind_speed": 14
    },
    "tomorrow": {
        "temp_max": 30,
        "temp_min": 25,
        "rainfall_mm": 120,
        "humidity": 58,
        "wind_speed": 10
    },
    "day_after": {
        "temp_max": 29,
        "temp_min": 24,
        "rainfall_mm": 134,
        "humidity": 70,
        "wind_speed": 18
    },
    
  
  "weather_prediction": {
    "rainfall_mm": 78.4
  },

  "warnings": {
    "heatwave": {
      "severity": "NONE",
      "reason": "Conditions not met"
    },
    "coldwave": {
      "severity": "NONE",
      "reason": "Conditions not met"
    },
    "thunderstorm": {
      "severity": "MODERATE",
      "reason": "High moisture, cloud buildup and pressure drop"
    },
    "hailstorm": {
      "severity": "NONE",
      "reason": "No hail-favorable dynamics"
    }
  },

  "risk_assessment": {
    "flood": {
      "probability": 0.82,
      "risk_level": "HIGH"
    },
    "landslide": {
      "probability": 0.61,
      "risk_level": "MODERATE"
    },
    "earthquake": {
      "zone": "HIGH"
    }
  },

  "overall_alert": "SEVERE"
}

class WeatherUI(BoxLayout):
    today_temp_max = NumericProperty(0)
    today_temp_min = NumericProperty(0)
    tomorrow_temp_max = NumericProperty(0)
    tomorrow_temp_min = NumericProperty(0)
    day_after_temp_max = NumericProperty(0)
    day_after_temp_min = NumericProperty(0)
    # change this for integer
    today_rain = NumericProperty(0)
    tomorrow_rain = NumericProperty(0)
    day_after_rain = NumericProperty(0)

    lang = StringProperty("en")

    translations = {
        "en": {
            "title": "Sangai Weather",
            "forecast": "Weather Forecast",
            "today": "TODAY",
            "tomorrow": "Tomorrow",
            "day_after":"Day After Tomorrow",
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

    def get_data(self):
        return weather_data
    
    def set_data(self):
        self.today_temp_max = self.get_data()["today"]["temp_max"]
        self.today_temp_min = self.get_data()["today"]["temp_min"]
        self.today_rainfall_mm = self.get_data()["today"]["rainfall_mm"]
        self.tomorrow_temp_max = self.get_data()["tomorrow"]["temp_max"]
        self.tomorrow_temp_min = self.get_data()["tomorrow"]["temp_min"]
        self.tomorrow_rainfall_mm = self.get_data()["tomorrow"]["rainfall_mm"]    
        self.day_after_temp_max = self.get_data()["day_after"]["temp_max"]
        self.day_after_temp_min = self.get_data()["day_after"]["temp_min"]
        self.day_after_rainfall_mm = self.get_data()["day_after"]["rainfall_mm"]
    
    
    def send_location(self):
        pass

    def check_warnings(self):
        warnings = self.get_data()["warnings"]

        for event, info in warnings.items():
            if info["severity"] != "NONE":

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
            text_size=(280, None), 
            size_hint=(None, None),
            size=(340, 200)
        )
        layout = BoxLayout(
            padding=[15, 15, 15, 20]  
        )
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
        text = (
            f"Humidity: {self.get_data()[day]['humidity']}%\n"
            f"Wind Speed: {self.get_data()[day]['wind_speed']} km/h\n"
        )

        Popup(
            title="Weather Details",
            content=Label(text=text),
            size_hint=(.8,.4)
        ).open()


class WeatherApp(App):
    def build(self):
        return WeatherUI()
    def on_start(self):
        self.root.check_warnings()
        self.root.set_data()


if __name__ == "__main__":
    WeatherApp().run()
