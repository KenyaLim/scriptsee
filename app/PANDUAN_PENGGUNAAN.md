# Panduan Menjalankan Scriptsee

Dokumen ini menjelaskan cara menjalankan aplikasi detector port scanning yang
berada di folder `app/`.

## 1. Struktur file

```text
scriptsee/
├── requirements.txt
└── app/
    ├── detect.py
    ├── portscan_detector.py
    ├── test_portscan_detector.py
    └── PANDUAN_PENGGUNAAN.md
```

Fungsi setiap file:

| File | Fungsi |
|---|---|
| `detect.py` | Command-line interface untuk menjalankan deteksi |
| `portscan_detector.py` | Logika detector, pembacaan PCAP, live capture, dan output CSV |
| `test_portscan_detector.py` | Unit test |
| `requirements.txt` | Daftar dependency Python, terutama Scapy |

## 2. Persiapan awal

Panduan ini menggunakan Linux atau Linux Mint. Jalankan perintah berikut dari
folder repository:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
```

Pastikan Python dan modul virtual environment sudah tersedia:

```bash
python3 --version
python3 -m venv --help
```

Jika perintah `venv` belum tersedia di Linux Mint atau Ubuntu, pasang paketnya:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

## 3. Membuat virtual environment

Virtual environment memisahkan dependency aplikasi dari Python sistem.

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
python3 -m venv .venv
source .venv/bin/activate
```

Jika berhasil, biasanya nama `(.venv)` muncul di awal prompt terminal.

Perbarui `pip`, lalu pasang dependency:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Setiap kali membuka terminal baru, aktifkan kembali environment:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
```

Untuk keluar dari environment:

```bash
deactivate
```

## 4. Menjalankan unit test

Sebelum menjalankan detector, pastikan folder kerja berada di `app/` karena
file `detect.py` mengimpor `portscan_detector.py` dari folder yang sama.

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python -m unittest -v test_portscan_detector.py
```

Hasil yang diharapkan:

```text
Ran 4 tests
OK
```

Test ini memeriksa:

- alert ketika jumlah port unik melewati threshold;
- penghapusan event lama dari sliding window;
- penghapusan state setelah TTL berakhir;
- penolakan konfigurasi TTL yang lebih kecil daripada sliding window.

## 5. Melihat bantuan command line

Dari folder `app/`, jalankan:

```bash
python detect.py --help
```

Parameter yang tersedia:

| Parameter | Keterangan | Nilai default |
|---|---|---:|
| `--pcap` | File PCAP yang akan dianalisis | - |
| `--interface` | Interface untuk live capture | - |
| `--output` | Lokasi file hasil alert | `alerts.csv` |
| `--window` | Durasi sliding window dalam detik | `10` |
| `--ttl` | Durasi state disimpan dalam detik | `30` |
| `--ports-threshold` | Minimum jumlah port unik | `10` |
| `--connections-threshold` | Minimum jumlah paket/koneksi | `20` |
| `--syn-ratio-threshold` | Minimum rasio paket SYN | `0.70` |
| `--count` | Jumlah paket live capture; `0` berarti terus berjalan | `0` |

`--pcap` dan `--interface` harus dipilih salah satu. Keduanya tidak boleh
digunakan bersamaan.

## 6. Mode PCAP: cara yang disarankan untuk penelitian

Mode PCAP adalah cara paling mudah untuk memulai karena input dapat disimpan,
diulang, dan dibandingkan dengan ground truth.

## 6A. Test drive lokal tanpa VM

Untuk mencoba aplikasi sekarang, kamu **tidak perlu menyiapkan VM terlebih
dahulu**. Kamu dapat menguji laptop sendiri dengan cara:

```text
laptop sendiri sebagai Scanner + Sensor + Target
```

Fungsi aplikasi ini adalah **menganalisis traffic port scanning**, bukan
melakukan scanning secara otomatis. Jadi diperlukan dua hal:

1. program perekam traffic, misalnya `tcpdump`;
2. traffic uji, misalnya Nmap yang diarahkan ke laptop sendiri.

Scanning ke `127.0.0.1` atau alamat IP milik laptop sendiri aman untuk test
drive karena targetnya adalah komputer sendiri. Jangan mengarahkan Nmap ke
komputer atau jaringan lain tanpa izin.

### 6A.1 Pasang tool test drive

Jika belum tersedia:

```bash
sudo apt update
sudo apt install tcpdump nmap
```

Pastikan virtual environment aktif untuk menjalankan aplikasi:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
```

### 6A.2 Terminal pertama: mulai merekam traffic

Buka terminal pertama dan jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo tcpdump -i lo -w ../capture.pcap 'ip and tcp'
```

Keterangan:

- `lo` adalah interface loopback untuk traffic ke `127.0.0.1`;
- `-w ../capture.pcap` menyimpan hasil rekaman di root repository;
- perintah ini memang akan terus berjalan sampai dihentikan.

Jangan menekan `Ctrl+C` sebelum traffic uji selesai dibuat.

### 6A.3 Terminal kedua: lakukan scanning ke laptop sendiri

Buka terminal kedua, aktifkan environment, lalu jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
nmap -sT -p 1-100 127.0.0.1
```

Perintah tersebut melakukan TCP connect scan ke port 1 sampai 100 pada
loopback laptop sendiri. Port yang tertutup tetap menghasilkan traffic TCP
yang dapat dianalisis.

Setelah Nmap selesai, kembali ke terminal pertama dan tekan:

```text
Ctrl+C
```

Pastikan file berhasil dibuat:

```bash
ls -lh /media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

Ukuran file harus lebih besar dari nol.

### 6A.4 Analisis file PCAP

Masih dari terminal kedua atau terminal lain:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts.csv
```

Kemudian baca hasilnya:

```bash
cat ../alerts.csv
```

Dengan default `--ports-threshold 10`, scanning 100 port biasanya diharapkan
menghasilkan alert jika paket dari Nmap terbaca pada interface `lo`.

Jika belum menghasilkan alert, coba threshold yang lebih rendah untuk
test-drive:

```bash
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts-test.csv \
  --ports-threshold 3 \
  --connections-threshold 5 \
  --syn-ratio-threshold 0.50
```

Threshold rendah ini hanya untuk memastikan alur aplikasi bekerja. Jangan
langsung menjadikannya threshold final skripsi.

### 6A.5 Alternatif menggunakan alamat IP laptop

Jika ingin menguji traffic melalui interface jaringan, cari alamat IP laptop:

```bash
ip -4 addr
```

Kemudian rekam pada interface yang sesuai, misalnya `wlan0` atau `enp3s0`:

```bash
sudo tcpdump -i wlan0 -w ../capture-lan.pcap 'host ALAMAT_IP_LAPTOP and tcp'
```

Untuk test drive pertama, loopback `lo` dan `127.0.0.1` lebih mudah karena
tidak bergantung pada Wi-Fi atau kabel jaringan.

### 6A.6 Apa arti hasil test drive ini?

Test drive lokal membuktikan bahwa:

1. traffic TCP dapat direkam;
2. Scapy dapat membaca file PCAP;
3. detector dapat mengambil fitur paket;
4. rule dapat menghasilkan alert;
5. hasil dapat ditulis ke CSV.

Test drive ini **belum menjadi eksperimen skripsi final** karena Scanner,
Sensor, dan Target masih berada di satu laptop. Untuk eksperimen final,
gunakan jaringan VM terisolasi agar skenarionya lebih terkontrol.

### 6.1 Menyiapkan file PCAP

File PCAP dapat dibuat menggunakan `tcpdump` pada Sensor:

```bash
sudo tcpdump -i eth1 -w capture.pcap 'ip and tcp'
```

Biarkan proses tersebut berjalan ketika traffic normal atau skenario port
scanning dibuat. Hentikan dengan menekan `Ctrl+C`.

Nama interface tidak selalu `eth1`. Periksa interface yang tersedia dengan:

```bash
ip link
```

Alternatifnya, traffic dapat direkam menggunakan Wireshark lalu disimpan
sebagai file `.pcap` atau `.pcapng`. Untuk penggunaan awal, gunakan format
PCAP yang dapat dibaca Scapy.

### 6.2 Menjalankan analisis PCAP

Salin file PCAP ke folder yang mudah diakses, kemudian jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts.csv
```

Jika proses berhasil, terminal menampilkan jumlah alert dan lokasi file
output. Contoh:

```text
Deteksi selesai: 1 alert, state tersisa: 1
Alert tersimpan di: ../alerts.csv
```

### 6.3 Membaca hasil

File `alerts.csv` memiliki kolom:

| Kolom | Arti |
|---|---|
| `timestamp` | Waktu ketika alert dibuat |
| `source_ip` | Alamat IP sumber traffic |
| `destination_ip` | Alamat IP tujuan |
| `unique_ports` | Jumlah destination port berbeda dalam window |
| `connections` | Jumlah paket yang dihitung dalam window |
| `syn_ratio` | Rasio paket yang memiliki TCP flag SYN |
| `reason` | Aturan yang terpenuhi |

Contoh melihat hasil dari terminal:

```bash
column -s, -t < ../alerts.csv
```

Jika tidak ada alert, file tetap dibuat dan hanya berisi header. Kondisi ini
tidak otomatis berarti aplikasi rusak; traffic bisa saja memang tidak
memenuhi threshold.

## 7. Mengubah threshold

Contoh berikut menggunakan window 10 detik, minimum 5 port unik, minimum 10
paket, dan rasio SYN minimal 70 persen:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts-threshold-5.csv \
  --window 10 \
  --ttl 30 \
  --ports-threshold 5 \
  --connections-threshold 10 \
  --syn-ratio-threshold 0.70
```

Nilai threshold di atas adalah contoh eksperimen, bukan nilai final skripsi.
Saat penelitian, simpan threshold yang dipakai untuk setiap percobaan dan
bandingkan pengaruhnya terhadap TP, TN, FP, dan FN.

`--ttl` tidak boleh lebih kecil daripada `--window`. Contoh berikut akan
ditolak:

```bash
python detect.py --pcap ../capture.pcap --window 10 --ttl 5
```

## 8. Mode live capture

Mode live capture membaca paket langsung dari network interface. Gunakan mode
ini setelah mode PCAP berhasil.

Pertama, cari nama interface:

```bash
ip link
```

Kemudian jalankan detector, misalnya pada `eth1`:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo ../.venv/bin/python detect.py \
  --interface eth1 \
  --output ../live-alerts.csv
```

Aplikasi berjalan sampai dihentikan dengan `Ctrl+C`. Untuk membatasi jumlah
paket, gunakan `--count`:

```bash
sudo ../.venv/bin/python detect.py \
  --interface eth1 \
  --count 1000 \
  --output ../live-alerts.csv
```

Live capture biasanya membutuhkan hak administrator. Jangan menggunakan
interface jaringan publik untuk eksperimen tanpa izin.

## 9. Alur penggunaan untuk eksperimen skripsi

Gunakan alur berikut untuk setiap skenario:

1. Siapkan Scanner, Sensor, dan Target pada jaringan VM terisolasi.
2. Catat alamat IP, interface, waktu mulai, dan konfigurasi threshold.
3. Rekam traffic pada Sensor ke file PCAP.
4. Jalankan traffic normal atau port scanning hanya ke Target milik sendiri.
5. Hentikan rekaman setelah skenario selesai.
6. Jalankan `detect.py` pada file PCAP.
7. Simpan file alert dengan nama yang menggambarkan skenarionya.
8. Catat apakah skenario sebenarnya normal atau scanning.
9. Bandingkan label tersebut dengan isi `alerts.csv`.
10. Masukkan hasilnya ke tabel TP, TN, FP, dan FN.

Contoh penamaan output:

```text
normal-01-alerts.csv
syn-scan-fast-01-alerts.csv
syn-scan-slow-01-alerts.csv
connect-scan-01-alerts.csv
```

## 10. Contoh skenario port scanning

Jalankan perintah berikut hanya dari Scanner ke VM Target milik sendiri:

```bash
nmap -sS -p 20-40 192.168.57.30
nmap -sT -p 20-40 192.168.57.30
```

Keterangan:

- `-sS`: TCP SYN scan;
- `-sT`: TCP connect scan;
- `-p 20-40`: memindai port 20 sampai 40;
- `192.168.57.30`: alamat VM Target dalam contoh.

Sesuaikan alamat IP dengan topologi yang benar-benar digunakan. Jangan
mengarahkan Nmap ke alamat publik, jaringan kampus, atau perangkat yang tidak
mendapat izin.

## 11. Masalah umum

### `ModuleNotFoundError: No module named 'scapy'`

Pastikan virtual environment aktif, lalu pasang dependency:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### `can't open file 'detect.py'`

Pindah ke folder `app` terlebih dahulu:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
```

### `No such file or directory` untuk file PCAP

Pesan seperti:

```text
FileNotFoundError: ... '../capture.pcap'
```

berarti file PCAP belum ada pada lokasi tersebut. Dari folder `app`, path
`../capture.pcap` berarti:

```text
/media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

Periksa dengan:

```bash
ls -lh ../capture.pcap
```

Jika belum ada, buat rekaman terlebih dahulu menggunakan langkah test drive
lokal di bagian sebelumnya. Menekan `Ctrl+C` sebelum `tcpdump` menerima paket
juga dapat menyebabkan file tidak terbentuk atau berukuran nol.

### Live capture tidak menerima paket

Periksa hal berikut:

1. nama interface dengan `ip link`;
2. Sensor benar-benar berada pada jalur traffic atau menggunakan port
   mirroring;
3. filter hanya membaca IPv4/TCP;
4. proses dijalankan dengan permission yang sesuai;
5. Scanner dan Target dapat saling berkomunikasi.

### Tidak ada alert

Periksa apakah:

- file PCAP benar-benar berisi paket IPv4/TCP;
- source IP dan destination IP sesuai yang diharapkan;
- jumlah port dalam window memenuhi threshold;
- interval scanning tidak terlalu panjang dibandingkan `--window`;
- skenario memang memiliki paket TCP SYN jika mengandalkan rasio SYN.

Tidak adanya alert perlu dicatat sebagai hasil eksperimen, bukan langsung
dianggap sebagai error.

## 12. Perintah singkat dari awal sampai akhir

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd app
python -m unittest -v test_portscan_detector.py
python detect.py --pcap ../capture.pcap --output ../alerts.csv
```

Setelah selesai:

```bash
deactivate
```
