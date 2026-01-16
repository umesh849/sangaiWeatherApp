# Sangai Weather – Kivy UI App

A modern **mobile-style weather application** built using **Kivy (Python)**.
The app connects to a **FastAPI backend** to fetch real-time forecasts and disaster warnings.

---

## Features

✔ Live weather forecast (Today, Tomorrow, Day After Tomorrow)
✔ Multi-hazard alerts (Heatwave, Coldwave, Hailstorm)
✔ FastAPI backend integration
✔ Multi-language support (English + Manipuri)
✔ Popup alerts for severe conditions
✔ Mobile UI layout (360x540)
✔ Auto fetch on app start

---

## UI Preview

_Phone-style interface with forecast cards and alerts_

---

## Tech Stack

- **Python**
- **Kivy**
- **FastAPI (Backend)**
- **OpenWeather API**
- **Machine Learning models**
- **REST API**

---

## 📂 Project Structure

```
project/
│
├── main.py           # Kivy UI App
├── src/
│   └── ui.kv         # UI Layout
├── fonts/
│   └── NotoSansMeeteiMayek.ttf
└── README.md
```

---

## ⚙ Setup & Run

### 1️⃣ Install dependencies

```bash
pip install kivy requests
```

### 2️⃣ Run backend server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3️⃣ Update server IP

```python
SERVER_IP = "YOUR_LOCAL_IP"
```

### 4️⃣ Run UI app

```bash
python main.py
```

---

## 🌐 API Used

```
POST /predict
```

Payload example:

```json
{
  "lat": 24.8039,
  "lon": 93.942,
  "district": "Imphal East"
}
```

---

## Important

✔ Backend must be running
✔ Same WiFi network
✔ Firewall should allow port 8000

---

## Languages Supported

- English
- Manipuri (Meitei Mayek)

---

## 📌 Author

**Adi Prakash**
GitHub: [https://github.com/adiorinder](https://github.com/adiorinder)

---

## ⭐ Future Enhancements

- GPS auto-location
- Push notifications
- Offline mode
- Dark mode
- Android APK build

---

## License

MIT License
