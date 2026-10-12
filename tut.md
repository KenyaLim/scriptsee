Error-nya bukan dari Scapy atau detector: aplikasi mencari file `../capture.pcap`, tetapi file itu belum ada. Aku akan menambahkan bagian “test drive lokal tanpa VM” ke panduan, termasuk cara menangkap traffic loopback laptop sendiri dan cara membaca hasilnya.

Edit 

Read , lines 105 to 260
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/app/PANDUAN_PENGGUNAAN.md",
  "view_range": [
    105,
    260
  ]
}

Read , lines 330 to 410
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/app/PANDUAN_PENGGUNAAN.md",
  "view_range": [
    330,
    410
  ]
}

Ran terminal command: git --no-pager diff --check -- app/PANDUAN_PENGGUNAAN.md

Read , lines 260 to 335
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/app/PANDUAN_PENGGUNAAN.md",
  "view_range": [
    260,
    335
  ]
}

Read , lines 410 to 470
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/app/PANDUAN_PENGGUNAAN.md",
  "view_range": [
    410,
    470
  ]
}

Selain memperjelas panduan, aku akan memperbaiki pesan error pada CLI supaya ketika file PCAP belum ada, pengguna mendapat instruksi yang jelas, bukan traceback Scapy yang panjang.

Edit 

Ran terminal command: cd app && python3 -m unittest -v test_portscan_detector.py

Ran terminal command: cd app && python3 detect.py --pcap ../capture.pcap --output ../alerts.csv
Tool execution failed with exit code 2

Ran terminal command: git --no-pager diff --check -- app/detect.py app/PANDUAN_PENGGUNAAN.md

Bisa, kamu **bisa test drive tanpa VM** terlebih dahulu. Untuk percobaan awal, laptopmu bisa berperan sebagai:

```text
Scanner + Sensor + Target
```

Namun perlu dipahami:

> Aplikasi ini bukan aplikasi untuk melakukan scanning. Aplikasi ini menganalisis traffic port scanning yang sudah direkam, lalu menghasilkan alert.

Jadi alurnya:

```text
Nmap membuat traffic scan
        ↓
tcpdump merekam traffic
        ↓
Scriptsee membaca file PCAP
        ↓
Scriptsee menghasilkan alerts.csv
```

## Penyebab error kamu

Error ini:

```text
FileNotFoundError: [Errno 2] No such file or directory: '../capture.pcap'
```

berarti file berikut belum ada:

```text
/media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

Perintah ini:

```bash
python detect.py --pcap ../capture.pcap --output ../alerts.csv
```

hanya membaca file PCAP. Perintah tersebut **tidak membuat `capture.pcap` secara otomatis**.

Kemungkinan sebelumnya kamu menghentikan `tcpdump` sebelum file berhasil dibuat, atau file dibuat di folder lain.

## Cara test drive laptop sendiri

### 1. Pasang Nmap dan tcpdump

Jalankan sekali:

```bash
sudo apt update
sudo apt install tcpdump nmap
```

Pastikan environment aktif:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
```

### 2. Terminal pertama: mulai merekam

Buka terminal pertama:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo tcpdump -i lo -w ../capture.pcap 'ip and tcp'
```

`lo` adalah interface loopback untuk traffic ke laptop sendiri melalui `127.0.0.1`.

Biarkan terminal ini tetap berjalan.

### 3. Terminal kedua: scan laptop sendiri

Buka terminal kedua:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
nmap -sT -p 1-100 127.0.0.1
```

Perintah ini melakukan TCP connect scan pada port 1 sampai 100 di laptopmu sendiri.

Ini aman untuk test drive karena targetnya adalah:

```text
127.0.0.1
```

Setelah Nmap selesai, kembali ke terminal pertama dan tekan:

```text
Ctrl+C
```

### 4. Pastikan file PCAP ada

Jalankan:

```bash
ls -lh /media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

File tersebut harus ada dan ukurannya lebih besar dari 0 byte.

### 5. Jalankan detector

Dari folder `app/`:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app

python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts.csv
```

Lihat hasilnya:

```bash
cat ../alerts.csv
```

Kalau berhasil, kamu akan mendapatkan file:

```text
/media/user/D/0-SKRIPSI/scriptsee/alerts.csv
```

## Jika belum muncul alert

Coba gunakan threshold yang lebih rendah untuk test drive:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app

python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts-test.csv \
  --ports-threshold 3 \
  --connections-threshold 5 \
  --syn-ratio-threshold 0.50
```

Threshold rendah ini hanya untuk memastikan alur aplikasi bekerja. Untuk skripsi, threshold harus diuji menggunakan beberapa skenario dan tidak boleh langsung dianggap sebagai hasil final.

## Apakah bisa scan port laptop sendiri?

Bisa. Contoh paling aman:

```bash
nmap -sT -p 1-100 127.0.0.1
```

Kamu juga bisa melihat service yang sedang terbuka:

```bash
nmap -sT -p 1-1000 127.0.0.1
```

Tetapi perlu dibedakan:

- `127.0.0.1` berarti laptop itu sendiri;
- alamat IP laptop di jaringan berarti interface jaringan laptop;
- perangkat lain yang terhubung ke Wi-Fi bukan otomatis boleh dipindai;
- scan perangkat lain hanya boleh dilakukan jika perangkat tersebut milikmu atau sudah mendapat izin.

## Peran aplikasi dalam skripsimu

Secara sederhana, aplikasi ini menjawab pertanyaan:

> “Apakah pola traffic TCP tertentu terlihat seperti port scanning?”

Aplikasi melihat beberapa karakteristik:

- siapa sumber traffic;
- siapa tujuan traffic;
- port tujuan yang diakses;
- jumlah port berbeda;
- jumlah koneksi;
- rasio paket SYN;
- waktu antar-paket.

Kemudian aplikasi menggunakan aturan seperti:

```text
Jika satu source IP mengakses banyak port tujuan
dalam waktu tertentu,
maka buat alert port scanning.
```

Jadi pada test drive lokal:

```text
Nmap          = pembuat traffic scanning
tcpdump       = perekam traffic
portscan app  = penganalisis traffic
alerts.csv    = hasil deteksi
```

Aku juga sudah:

- menambahkan panduan test drive lokal ke `PANDUAN_PENGGUNAAN.md`;
- memperbaiki `detect.py` agar menampilkan pesan yang lebih jelas ketika file PCAP belum ada;
- menjalankan unit test, dan hasilnya:

```text
Ran 4 tests
OK
```

Untuk sekarang, kamu tidak perlu memikirkan VM dulu. Jalankan test drive dengan `127.0.0.1` sampai kamu memahami alur:

```text
rekam → scan → hentikan rekaman → analisis PCAP → baca alerts.csv
```