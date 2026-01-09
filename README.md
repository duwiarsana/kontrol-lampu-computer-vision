# 🖐️ Kontrol Lampu dengan Gesture Tangan (Computer Vision & MQTT)

**Ubah webcam komputer Anda menjadi saklar lampu pintar yang futuristik!** 🚀

Project ini adalah aplikasi **Smart Home IoT** sederhana yang menggunakan kecerdasan buatan (AI) untuk mendeteksi gerakan tangan dan mengirimkan perintah ke perangkat elektronik (seperti lampu) melalui internet menggunakan protokol MQTT.

Sangat cocok untuk:
- Belajar **Computer Vision** (OpenCV + MediaPipe).
- Belajar **IoT** (Internet of Things & MQTT).
- Project hobi untuk otomatisasi kamar.

![Demo Status](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Fitur Unggulan

- **✋ Kontrol Tanpa Sentuh (Touchless)**:
  - **Buka Tangan (✋)** → Kirim sinyal `1` (ON).
  - **Kepal Tangan (✊)** → Kirim sinyal `0` (OFF).
  
- **🔒 Mode Pengaman (Safety Lock)**:
  - Mencegah "salah pencet" saat Anda hanya lewat di depan kamera.
  - Sistem default **TERKUNCI** (Merah).
  - **Buka Kunci**: Tunjukkan gesture **"Peace/Victory" (✌️)** selama sesaat.
  - **Auto-Lock**: Otomatis terkunci kembali setelah 5 detik diam.
  
- **⚡ Stabil & Cerdas**:
  - **Anti-Flicker**: Algoritma "Debouncing" mencegah lampu kedip-kedip saat transisi tangan.
  - **Cooldown**: Jeda 2 detik setelah perintah terkirim agar tidak spamming data.

---

## 🛠️ Persyaratan (Requirements)

### Hardware
1. **Laptop/PC** dengan Webcam.
2. **Koneksi Internet** (Wajib, untuk MQTT).
3. *(Opsional)* **Perangkat IoT**: ESP8266 + Relay + Lampu (untuk tes fisik).

### Software & Library
Project ini dibangun dengan **Python 3**. Library yang digunakan:
- `opencv-python`: Untuk mengambil gambar dari webcam.
- `mediapipe`: Google AI untuk mendeteksi titik koordinat tangan.
- `paho-mqtt`: Untuk mengirim data ke broker MQTT.

---

## 🚀 Cara Instalasi (Langkah demi Langkah)

### 1. Download Project
Buka terminal dan jalankan:
```bash
git clone https://github.com/duwiarsana/kontrol-lampu-computer-vision.git
cd kontrol-lampu-computer-vision
```

### 2. Install Library
Install semua kebutuhan otomatis:
```bash
pip install -r requirements.txt
```

### 3. (PENTING) Download Model AI
Aplikasi memerlukan file model AI agar bisa "melihat" tangan.
👉 **[Download File `hand_landmarker.task` Disini](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)**

**Wajib:** Pindahkan file yang sudah didownload ke dalam folder project ini (satu folder dengan `main.py`).

---

## 🎮 Cara Menggunakan

1. **Jalankan Aplikasi**
   ```bash
   python main.py
   ```

2. **Lihat Status di Layar**
   - **STATUS: LOCKED (Merah)**: Aplikasi standby. Gerakan tangan tidak akan direspon.
   
3. **Mulai Kontrol**
   - Tunjukkan **Dua Jari (✌️)** ke kamera.
   - Status berubah jadi **ACTIVE (Hijau)**.
   - Sekarang, **Buka Tangan** untuk ON, **Kepal Tangan** untuk OFF.
   - Jika sudah selesai, biarkan saja. Setelah 5 detik akan terkunci otomatis.

---

## ⚙️ Konfigurasi MQTT (Untuk Integrasi IoT)

Secara default, aplikasi menggunakan Public Broker:
- **Host**: `202.74.74.42`
- **Port**: `1883`
- **Topic**: `gesture/control`

Jika Anda ingin mengubahnya, edit bagian atas file `main.py`:
```python
MQTT_BROKER = "192.168.1.xxx"  # Ganti IP Broker lokal anda jika ada
MQTT_TOPIC = "rumah/ruangtamu/lampu"
```

---

## 📡 Firmware untuk ESP8266 (Opsional)

Jika Anda ingin membuat alat IoT sungguhan untuk menerima perintah ini:
1. Buka folder `iot_firmware`.
2. Upload `iot_relay.ino` ke **ESP8266 (NodeMCU/Wemos)**.
3. Rangkaian: Hubungkan **Relay Module** ke pin **D2 (GPIO 4)**.
4. Setting WiFi & MQTT akan muncul di Captive Portal saat pertama kali dinyalakan.

---

## ❓ Troubleshooting

- **Error `Could not open camera`**: 
  Izinkan akses kamera untuk Terminal/Code Editor Anda di pengaturan Privacy OS (terutama macOS).
  
- **Layar Hitam / Error MediaPipe**:
  Pastikan file `hand_landmarker.task` sudah ada di folder project.
  
- **MQTT Gagal Konek**:
  Pastikan internet lancar. Coba ping IP broker `202.74.74.42`.

---

**Selamat Berkreasi!** 🚀
Project ini dibuat untuk edukasi dan hobi.
Dikembangkan oleh **Duwi Arsana**.
