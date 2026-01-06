# Kontrol Lampu dengan Computer Vision & MQTT

Aplikasi Python ini memungkinkan Anda mengontrol lampu (atau perangkat IoT lainnya) menggunakan **gesture tangan** yang dideteksi melalui webcam. Aplikasi dibuat menggunakan **OpenCV**, **MediaPipe**, dan **Paho-MQTT**.

## Fitur Utama

- **Deteksi Tangan Presisi**: Menggunakan Google MediaPipe Hand Landmarker.
- **Gesture Buka/Tutup**:
  - **Tangan Mengepal (Fist)**: Mengirim sinyal `0` (OFF).
  - **Tangan Terbuka (Open)**: Mengirim sinyal `1` (ON).
- **Safety Lock / Mode Pengaman** 🔒:
  - Mencegah "kepencet" saat Anda hanya lewat di depan kamera.
  - **Default**: Terkunci (LOCKED).
  - **Unlock**: Tunjukkan gesture **Peace/Victory (✌️)**.
  - **Auto-Lock**: Otomatis terkunci kembali setelah 5 detik.
- **Stabilisasi & Cooldown**:
  - Mencegah *flickering* (lampu kedip-kedip) saat transisi tangan.
  - Ada jeda (cooldown) 2 detik setelah setiap pengiriman perintah.
- **Visual Feedback**: Tampilan status Lock, Timer, dan Light ON/OFF langsung di layar.

## Persyaratan Sistem

- Python 3.8 - 3.13
- Webcam yang aktif
- Koneksi Internet (untuk akses ke MQTT Broker publik)

## Instalasi

1. **Clone Repository ini**:
   ```bash
   git clone https://github.com/duwiarsana/kontrol-lampu-computer-vision.git
   cd kontrol-lampu-computer-vision
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Dependency utama: `opencv-python`, `mediapipe`, `paho-mqtt`.*

3. **Pastikan Model MediaPipe Ada**:
   File `hand_landmarker.task` harus ada di folder yang sama dengan `main.py`. Jika tidak ada, download dari [Google MediaPipe Models](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task).

## Cara Penggunaan

1. **Jalankan Aplikasi**:
   ```bash
   python main.py
   ```
   *Catatan untuk pengguna macOS: Jika kamera tidak terbuka, pastikan Terminal Anda sudah diberikan izin akses Kamera di System Settings -> Privacy & Security.*

2. **Kontrol Gestur**:
   - **Buka Kunci**: Tunjukkan dua jari (✌️) ke kamera hingga status berubah menjadi **ACTIVE (Hijau)**.
   - **Nyalakan Lampu**: Buka telapak tangan Anda.
   - **Matikan Lampu**: Kepalkan tangan Anda.
   - **Tungu Cooldown**: Setelah perintah terkirim, akan muncul tulisan `COOLDOWN...` selama 2 detik.

## Konfigurasi MQTT

Secara default, aplikasi dikonfigurasi ke:
- **Broker**: `202.74.74.42`
- **Port**: `1883`
- **Topic**: `gesture/control`

Anda dapat mengubah konfigurasi ini dengan mengedit bagian atas file `main.py`:
```python
MQTT_BROKER = "202.74.74.42"
MQTT_TOPIC = "custom/topic"
```

## Troubleshooting

- **Error `ImportError: ... solutions`**: Pastikan anda menggunakan versi MediaPipe yang sesuai atau script `main.py` yang sudah dimigrasi ke Tasks API (versi di repo ini sudah menggunakan Tasks API yang baru).
- **MQTT Gagal Connect**: Cek koneksi internet Anda atau pastikan broker MQTT sedang online.

---
Dikembangkan oleh Duwi Arsana.
