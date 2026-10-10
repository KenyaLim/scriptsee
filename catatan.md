Saya akan cek isi repository dan rancangan metode terlebih dahulu, lalu membuat kerangka aplikasi Python yang bisa dijalankan di VM serta menjelaskan topologi IP dan cara pengujiannya secara aman.

Find files matching `**/*`

Read , lines 380 to 470
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/rancangan.txt",
  "view_range": [
    380,
    470
  ]
}

Read , line 1 to the end
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/README.md",
  "view_range": [
    1,
    -1
  ]
}

Saya akan membuat versi awal yang bisa diuji tanpa langsung melakukan scanning: mode utama membaca PCAP, mengekstrak paket IPv4/TCP, mengelola sliding window + TTL, menerapkan rule, dan menyimpan alert CSV. Mode live capture akan dibuat opsional karena membutuhkan izin administrator/root di VM.

"Apply Patch" failed
Completed with input: {"path":"/media/user/D/0-SKRIPSI/scriptsee/test_portscan_detector.py"}
Tool execution failed: Error: File already exists: /media/user/D/0-SKRIPSI/scriptsee/README.md

Kerangka aplikasi inti sudah dibuat; penambahan README tertahan karena file README lama sudah ada, jadi saya akan memperbaruinya secara langsung lalu menjalankan unit test dan pemeriksaan sintaks.

Edit 

Ran terminal command: python3 -m unittest -v test_portscan_detector.py

Ran terminal command: python3 -m py_compile portscan_detector.py detect.py test_portscan_detector.py

Ran terminal command: git --no-pager diff --check -- portscan_detector.py detect.py test_portscan_detector.py README.md requirements.txt && git --no-pager status --short

Bisa, bahkan VM sangat cocok untuk penelitian ini karena lingkungan pengujian bisa dibuat terisolasi dan tidak mengganggu jaringan kampus atau jaringan publik.

Saya sudah membuat aplikasi Python dalam beberapa file:

- `portscan_detector.py` — inti detector, sliding window, hash table, TTL, rule detection, PCAP, dan live capture.
- `detect.py` — aplikasi command line untuk menjalankan deteksi.
- `test_portscan_detector.py` — unit test.
- `requirements.txt` — dependensi Scapy.
- `README.md` — panduan instalasi, topologi, dan eksperimen.

Unit test sudah dijalankan dan hasilnya:

```text
Ran 4 tests
OK
```

## Konsep VM dan IP

Contoh topologi yang disarankan:

```text
VM Scanner                         VM Target
Nmap                                Layanan uji
192.168.56.10                       192.168.56.30
       \                              /
        \                            /
         Jaringan internal VM
              |
        VM Sensor/Detector
        192.168.56.20
```

Namun, ada hal penting:

> Memberikan IP pada semua VM dalam satu jaringan belum otomatis membuat VM Sensor bisa melihat traffic antara Scanner dan Target.

Kalau Scanner dan Target hanya berkomunikasi langsung melalui virtual switch, traffic unicast mereka biasanya tidak melewati Sensor. Akibatnya aplikasi tidak akan mendapatkan paket scanning tersebut.

Ada dua pilihan desain.

### Pilihan 1 — Sensor sebagai gateway/router

Ini pilihan yang paling mudah dijelaskan dalam skripsi.

Contoh:

```text
Scanner 192.168.56.10
Gateway 192.168.56.20
Target  192.168.57.30
```

Scanner diarahkan menggunakan Sensor sebagai gateway. Traffic dari Scanner ke Target akan melewati Sensor, sehingga aplikasi dapat menangkapnya.

Topologinya:

```text
VM Scanner
192.168.56.10
     |
     | jaringan scanner
     |
VM Sensor/Detector
192.168.56.20 dan 192.168.57.20
     |
     | jaringan target
     |
VM Target
192.168.57.30
```

Pada desain ini:

- Scanner menjalankan Nmap.
- Target menjalankan layanan atau port uji.
- Sensor menjalankan aplikasi Python.
- Sensor memiliki dua network interface.
- Sensor meneruskan traffic dari jaringan Scanner ke jaringan Target.
- Aplikasi menangkap traffic pada interface Sensor.

Ini paling sesuai untuk demonstrasi bahwa aplikasi mendeteksi traffic yang melewati sensor.

### Pilihan 2 — Port mirroring/promiscuous mode

Scanner dan Target tetap berada dalam satu jaringan, kemudian traffic disalin ke interface Sensor.

Pilihan ini bergantung pada dukungan hypervisor, misalnya:

- VirtualBox;
- VMware;
- Proxmox;
- GNS3;
- EVE-NG.

Konfigurasinya lebih rumit karena membutuhkan port mirroring atau network tap. Untuk tahap awal, desain Sensor sebagai gateway lebih sederhana.

## Apakah IP harus dipasangkan secara manual?

Ya, setiap VM perlu memiliki alamat IP yang berbeda tetapi masih sesuai subnet jaringan pengujiannya.

Contoh sederhana:

```text
Scanner : 192.168.56.10
Sensor  : 192.168.56.20
Target  : 192.168.56.30
Netmask : 255.255.255.0
```

Jangan menggunakan IP yang sama pada dua VM karena akan menyebabkan konflik alamat.

Untuk pengecekan di setiap VM:

```bash
ip addr
ip route
ping 192.168.56.30
```

Konfigurasi IP bisa dilakukan secara sementara dengan `ip addr`, atau secara permanen melalui konfigurasi jaringan Linux. Cara permanennya berbeda tergantung sistem operasi, misalnya Ubuntu menggunakan Netplan pada beberapa versi.

## Pembagian fungsi VM

| VM | Fungsi | Tool |
|---|---|---|
| Scanner | Menghasilkan port scanning | Nmap |
| Sensor | Menangkap dan menganalisis traffic | Python, Scapy |
| Target | Host yang dipindai | SSH, HTTP, atau service uji lain |

Nmap hanya perlu dipasang di VM Scanner. Aplikasi Python dan Scapy dipasang di VM Sensor. VM Target tidak perlu menjalankan aplikasi detector.

## Cara menjalankan aplikasi

Di VM Sensor:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v test_portscan_detector.py
```

Untuk membaca file PCAP:

```bash
python detect.py \
  --pcap capture.pcap \
  --output alerts.csv
```

Untuk live capture:

```bash
sudo .venv/bin/python detect.py \
  --interface eth1 \
  --output alerts.csv
```

Live capture biasanya memerlukan `sudo` karena membaca interface jaringan secara langsung.

Di VM Scanner, pengujian dapat dilakukan hanya ke VM Target:

```bash
nmap -sS -p 20-40 192.168.57.30
```

atau:

```bash
nmap -sT -p 20-40 192.168.57.30
```

Pengujian tersebut hanya dilakukan pada VM milik sendiri atau jaringan yang sudah mendapat izin.

## Saran untuk dibawa saat konsultasi dosen

Sampaikan rancangan berikut:

> Pengujian akan menggunakan tiga VM yang terdiri dari VM Scanner, VM Sensor/Detector, dan VM Target. Ketiga VM ditempatkan pada jaringan virtual terisolasi. VM Scanner menjalankan Nmap, VM Target menyediakan port atau layanan uji, sedangkan VM Sensor menjalankan aplikasi Python dan ditempatkan sebagai gateway atau titik capture agar traffic antara Scanner dan Target dapat diamati.

Untuk tahap awal, saya menyarankan menggunakan **PCAP terlebih dahulu**, bukan langsung live capture. Alurnya:

1. Buat traffic scanning dari Scanner.
2. Simpan traffic menggunakan `tcpdump` atau Wireshark.
3. Salin file PCAP ke VM Sensor.
4. Jalankan aplikasi Python terhadap PCAP.
5. Periksa hasil pada `alerts.csv`.

Cara ini lebih mudah untuk debugging, pengulangan eksperimen, dan pembuktian ground truth sebelum aplikasi digunakan secara live.