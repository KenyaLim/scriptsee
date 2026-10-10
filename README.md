# Scriptsee Port-Scan Detector

Aplikasi ini adalah prototipe nyata dari rancangan skripsi: deteksi port
scanning berbasis rule pada traffic IPv4/TCP menggunakan Python, sliding time
window, dan hash table dengan TTL.

## Struktur

- `portscan_detector.py`: feature, state manager, rule deteksi, PCAP/live
  capture, dan output CSV.
- `detect.py`: antarmuka command line.
- `test_portscan_detector.py`: unit test threshold, window, dan TTL.
- `requirements.txt`: dependensi Scapy.

## Instalasi di VM

Host penelitian yang digunakan adalah Linux Mint. VM dapat menggunakan Linux
Mint, Ubuntu, atau distribusi Linux lain yang kompatibel; distribusi dan
versinya harus dicatat pada laporan eksperimen.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v test_portscan_detector.py
```

Mode PCAP tidak membutuhkan hak administrator:

```bash
python detect.py --pcap capture.pcap --output alerts.csv
```

Mode live capture biasanya memerlukan root atau capability jaringan:

```bash
sudo .venv/bin/python detect.py --interface eth1 --output alerts.csv
```

Parameter utama:

```text
--window                 sliding window dalam detik (default 10)
--ttl                    TTL state dalam detik (default 30)
--ports-threshold        jumlah port unik (default 10)
--connections-threshold jumlah paket/koneksi (default 20)
--syn-ratio-threshold    rasio paket SYN (default 0.70)
```

Threshold tersebut adalah nilai awal eksperimen, bukan hasil final skripsi.
Nilainya harus diuji menggunakan traffic normal dan skenario Nmap yang
terdokumentasi.

## Topologi VM yang disarankan

Gunakan minimal tiga VM pada jaringan virtual **host-only/internal**, bukan
bridged ke jaringan publik:

```text
VM Scanner (Nmap)  192.168.56.10
        |
  internal network 192.168.56.0/24
        |
VM Sensor (aplikasi) 192.168.56.20
        |
VM Target            192.168.56.30
```

Sensor harus dapat melihat traffic antara Scanner dan Target. Cara paling
sederhana adalah menempatkan sensor sebagai gateway/router di antara keduanya
atau menggunakan port mirroring/promiscuous capture sesuai fitur hypervisor.
Jika Scanner dan Target hanya berada pada switch virtual yang sama, sensor
tidak otomatis melihat unicast traffic mereka.

Sebelum uji, pastikan:

```bash
ping 192.168.56.30
ip addr
ip route
```

Jalankan aplikasi pada interface yang benar (`ip link`) dan lakukan pengujian
hanya pada VM milik sendiri atau jaringan yang telah mendapat izin.

## Contoh alur eksperimen

1. Di Sensor, mulai capture atau simpan traffic ke PCAP dengan tcpdump.
2. Di Scanner, jalankan Nmap hanya ke Target:

   ```bash
   nmap -sS -p 20-40 192.168.56.30
   nmap -sT -p 20-40 192.168.56.30
   ```

3. Hentikan capture, lalu jalankan aplikasi pada PCAP.
4. Simpan perintah Nmap, waktu mulai/selesai, target, daftar port, dan label
   ground truth untuk setiap skenario.
5. Ulangi untuk traffic normal, fast, medium, dan slow scan.

Untuk slow scan, gunakan konfigurasi timing Nmap yang terdokumentasi dan
catat hasil aktualnya. Jangan melakukan pemindaian ke alamat di luar jaringan
uji.

## Software yang perlu disiapkan

### Wajib

- **VirtualBox** atau hypervisor sejenis untuk menjalankan VM.
- **Sistem operasi Linux** untuk VM Scanner, Sensor, dan Target.
- **Python 3**, `venv`, dan `pip` pada VM Sensor.
- **Scapy** pada VM Sensor, dipasang dari `requirements.txt`.
- **Nmap** pada VM Scanner.
- **tcpdump** atau **Wireshark** untuk merekam dan memverifikasi PCAP.

### Opsional tetapi membantu

- **Visual Studio Code** untuk mengedit kode.
- **Git** untuk menyimpan versi kode dan hasil perubahan.
- **Draw.io** untuk membuat diagram topologi dan blok diagram.
- **SQLite** apabila log eksperimen ingin disimpan dalam database; aplikasi
  saat ini menggunakan CSV untuk output alert.

Linux Mint adalah sistem operasi host, sedangkan sistem operasi guest di VM
boleh sama atau berbeda. Yang penting semua versi dan konfigurasi dicatat,
jaringan VM diisolasi, dan seluruh pemindaian hanya diarahkan ke VM Target
yang dimiliki sendiri.
