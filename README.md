# 🖐️ Kontrol Lampu dengan Gesture Tangan (Computer Vision & MQTT)

Selamat datang! Project ini memungkinkan Anda untuk menyalakan dan mematikan lampu (atau perangkat elektronik lainnya) hanya dengan gerakan tangan di depan webcam komputer Anda.

Project ini dibuat khusus agar **mudah digunakan**, bahkan untuk pemula. Sistem ini menggunakan kecerdasan buatan (AI) untuk mendeteksi tangan Anda dan mengirim perintah kemuduan ke saklar lampu pintar melalui internet (MQTT).

![Demo](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## 🌟 Fitur Unggulan

- **✋ Kontrol Tanpa Sentuh**:
  - **Buka Tangan (✋)** = Nyalakan Lampu (ON).
  - **Kepal Tangan (✊)** = Matikan Lampu (OFF).
  
- **🔒 Mode Pengaman (Safety Lock)**:
  - Tidak perlu khawatir lampu nyala/mati sendiri saat Anda "hanya lewat" di depan kamera.
  - Sistem akan terkunci otomatis. Anda harus membuka kunci dulu dengan gaya "Peace/Victory" (✌️).
  
- **⚡ Stabil & Cerdas**:
  - **Anti-Kedip**: Lampu tidak akan nyala-mati cepat (flickering) jika tangan Anda gemetar.
  - **Cooldown**: Ada jeda istirahat 2 detik setelah mengirim perintah, supaya tidak spamming.

---

## 🛠️ Persiapan (Apa yang Anda Butuhkan)

Sebelum memulai, pastikan Anda memiliki:
1. **Laptop/PC** dengan webcam.
2. **Python** terinstall (Download di [python.org](https://www.python.org/downloads/)).
3. **Koneksi Internet** (untuk mengirim data ke lampu).

---

## 🚀 Cara Instalasi (Langkah demi Langkah)

### 1. Download Project Ini
Buka terminal (Command Prompt/PowerShell/Terminal) dan jalankan perintah:

```bash
git clone https://github.com/duwiarsana/kontrol-lampu-computer-vision.git
cd kontrol-lampu-computer-vision
```
*Atau: Klik tombol hijau "Code" di atas kanan halaman GitHub -> "Download ZIP", lalu ekstrak foldernya.*

### 2. Install Library Pendukung
Aplikasi ini butuh beberapa "alat" tambahan (library) agar bisa berjalan. Jalankan perintah ini di terminal (di dalam folder project tadi):

```bash
pip install -r requirements.txt
```
*Tunggu sampai proses selesai. Pastikan internet lancar.*

### 3. (PENTING) Download Model AI
Aplikasi butuh file otak AI (`hand_landmarker.task`) agar bisa melihat tangan. 
**[Klik Disini untuk Download](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)**.

Setelah didownload, **pindahkan/copy file `hand_landmarker.task` tersebut ke dalam folder project ini** (folder yang sama dengan file `main.py`).

---

## 🎮 Cara Menggunakan

1. **Jalankan Aplikasi**
   Ketik perintah ini di terminal:
   ```bash
   python main.py
   ```
   *(Jika muncul error "camera permission", pastikan Terminal Anda sudah diizinkan akses kamera di pengaturan Laptop)*.

2. **Lihat Layar Kamera**
   Akan muncul jendela baru yang menampilkan wajah Anda. Perhatikan tulisan status di pojok kiri atas.

3. **Langkah-Langkah Kontrol**:
   
   **Langkah 1: Buka Kunci (Unlock)**
   - Saat baru mulai, statusnya **MERAH (LOCKED)**.
   - Angkat tangan dan buat simbul **PEACE / VICTORY (✌️)**.
   - Status akan berubah jadi **HIJAU (ACTIVE)**. Anda punya waktu 5 detik!

   **Langkah 2: Kendalikan Lampu**
   - Saat status **HIJAU (ACTIVE)**:
   - **Buka Telapak Tangan (✋)** -> Lampu NYALA (Data '1' terkirim).
   - **Kepalkan Tangan (✊)** -> Lampu MATI (Data '0' terkirim).
   
   *Setelah 5 detik tidak ada aktivitas, sistem akan terkunci lagi otomatis demi keamanan.*

---

## ⚙️ Pengaturan Lanjutan (MQTT)

Bagi Anda yang mengerti teknis IoT, aplikasi ini mengirim data ke MQTT Broker dengan detail berikut:

- **Broker**: `202.74.74.42` (Public)
- **Port**: `1883`
- **Topic**: `gesture/control`
- **Payload**:
  - `1`: Untuk menyalakan.
  - `0`: Untuk mematikan.

Anda bisa mengganti konfigurasi ini dengan membuka file `main.py` menggunakan Notepad/Text Editor dan ubah bagian paling atas:

```python
MQTT_BROKER = "alamat.broker.anda"
MQTT_TOPIC = "rumah/kamar/lampu"
```

---

## ❓ Masalah yang Sering Muncul (Troubleshooting)

1. **"Error: Could not open camera"**
   - Pastikan webcam tidak sedang dipakai aplikasi lain (Zoom, Meet, dll).
   - Jika di MacOS: Buka `System Settings` -> `Privacy & Security` -> `Camera`, lalu centang/izinkan Terminal/Code Editor Anda. Lalu restart terminal.

2. **Jendela Kamera tidak muncul / Error `ImportError`**
   - Pastikan Anda sudah menjalankan langkah `pip install -r requirements.txt`.
   - Pastikan file `hand_landmarker.task` SUDAH ADA di folder project.

3. **Lampu tidak berubah padahal status di layar berubah- **MQTT Gagal Connect**: Cek koneksi internet Anda atau pastikan broker MQTT sedang online.

---

## 📡 Firmware ESP8266 (Smart Lamp)

Untuk mengontrol lampu sungguhan, gunakan folder `iot_firmware`.

### Hardware
- ESP8266 (NodeMCU / Wemos D1 Mini)
- Modul Relay (koneksikan ke **D2 / GPIO 4**)
- Lampu + Power Supply

### Libraries (Arduino IDE)
Install library berikut lewat Library Manager:
1. `WiFiManager` by tzapu
2. `PubSubClient` by Nick O'Leary
3. `ArduinoJson` by Benoit Blanchon (versi 6.x)

### Cara Upload
1. Buka `iot_firmware/iot_relay.ino` di Arduino IDE.
2. Upload ke board ESP8266 Anda.

### Cara Setting (Pertama Kali)
1. Nyalakan ESP8266.
2. Cari WiFi bernama `Gesture_Lamp_AP` di HP/Laptop.
3. Connect, lalu akan muncul halaman konfigurasi (atau buka `192.168.4.1`).
4. Pilih WiFi rumah Anda.
5. Masukkan konfigurasi MQTT:
   - Server: `202.74.74.42`
   - Port: `1883`
   - Topic: `gesture/control`
6. Save & Reboot. Alat siap digunakan!

---
Dikembangkan oleh Duwi Arsana.

---

**Selamat Mencoba!** 🚀
Dibuat dengan ❤️ oleh Duwi Arsana.
