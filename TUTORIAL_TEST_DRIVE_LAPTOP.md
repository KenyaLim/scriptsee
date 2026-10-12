# Tutorial Test Drive Scriptsee di Laptop Sendiri

Tutorial ini dibuat untuk kondisi awal: belum memakai VM, belum membuat
topologi jaringan, dan ingin mencoba aplikasi secara aman di laptop Linux
Mint sendiri.

## Hasil yang ingin dicapai

Di akhir tutorial, alurnya akan menjadi:

```text
Nmap scan 127.0.0.1
        |
        v
tcpdump merekam capture.pcap
        |
        v
Scriptsee membaca capture.pcap
        |
        v
Scriptsee membuat alerts.csv
```

Laptop sendiri digunakan sebagai:

```text
Scanner + Sensor + Target
```

Ini adalah test drive untuk memahami alur aplikasi, bukan eksperimen skripsi
final. Eksperimen final tetap sebaiknya menggunakan jaringan terisolasi dan
ground truth yang terdokumentasi.

## 1. Sebelum mulai: kenali tiga terminal

Akan lebih mudah jika menggunakan tiga terminal:

| Terminal | Fungsi |
|---|---|
| Terminal A | Merekam traffic dengan tcpdump |
| Terminal B | Menjalankan Nmap |
| Terminal C | Menjalankan Scriptsee |

Semua perintah di bawah menggunakan lokasi repository:

```text
/media/user/D/0-SKRIPSI/scriptsee
```

Jika lokasi repository berbeda, sesuaikan semua path.

## 2. Pasang software sistem

Jalankan satu kali:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip tcpdump nmap
```

Periksa:

```bash
python3 --version
tcpdump --version
nmap --version
```

## 3. Buat dan siapkan virtual environment

Virtual environment adalah ruang Python khusus untuk proyek ini. Scapy harus
dipasang di ruang tersebut, bukan hanya di Python sistem.

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Prompt terminal harus memiliki `(.venv)`:

```text
(.venv) kenya@mint ...
```

Periksa bahwa Python dan Scapy berasal dari environment proyek:

```bash
which python
python -c "import sys, scapy; print(sys.executable); print(scapy.__file__)"
```

Output Python harus mengarah ke:

```text
/media/user/D/0-SKRIPSI/scriptsee/.venv/bin/python
```

Jika tidak ingin mengaktifkan environment, gunakan path lengkap ini pada
langkah-langkah berikut:

```text
/media/user/D/0-SKRIPSI/scriptsee/.venv/bin/python
```

## 4. Jalankan unit test terlebih dahulu

Tujuannya memastikan bagian inti aplikasi dapat bekerja sebelum membaca PCAP.

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python -m unittest -v test_portscan_detector.py
```

Hasil yang diharapkan:

```text
Ran 4 tests
OK
```

Jika `python` tidak ditemukan, environment belum aktif. Jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
cd app
```

## 5. Terminal A: mulai merekam traffic

Buka Terminal A. Aktifkan environment tidak wajib untuk `tcpdump`, tetapi
gunakan path yang jelas:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo tcpdump -i lo -w ../capture.pcap 'ip and tcp'
```

Penjelasan:

- `sudo`: memberi izin membaca interface;
- `tcpdump`: program perekam paket;
- `-i lo`: merekam interface loopback;
- `-w ../capture.pcap`: menyimpan file di root repository;
- `'ip and tcp'`: hanya merekam traffic IPv4/TCP.

Setelah perintah dijalankan, terminal biasanya menunggu tanpa kembali ke
prompt. Itu normal. Jangan tekan `Ctrl+C` dulu.

## 6. Terminal B: buat traffic scan ke laptop sendiri

Buka Terminal B:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
nmap -sT -p 1-100 127.0.0.1
```

Penjelasan:

- `nmap`: pembuat traffic scanning;
- `-sT`: TCP connect scan;
- `-p 1-100`: mencoba port 1 sampai 100;
- `127.0.0.1`: laptop sendiri.

Target `127.0.0.1` dipakai karena aman untuk test drive pribadi. Jangan
mengganti target menjadi IP perangkat lain tanpa izin.

Setelah Nmap selesai, catat hasilnya. Pada tahap skripsi, perintah, target,
port, dan waktu pelaksanaan harus dicatat sebagai bagian dari ground truth.

## 7. Hentikan rekaman di Terminal A

Kembali ke Terminal A dan tekan:

```text
Ctrl+C
```

Kemudian periksa file:

```bash
ls -lh /media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

File harus ada dengan ukuran lebih besar dari 0 byte.

Jika file tidak ada, berarti rekaman belum dibuat pada lokasi yang diharapkan.
Ulangi langkah Terminal A, jalankan Nmap, lalu hentikan tcpdump setelah Nmap
selesai.

## 8. Terminal C: baca PCAP dengan Scriptsee

Buka Terminal C atau gunakan terminal yang sudah bebas:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
cd app
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts.csv
```

`../capture.pcap` berarti:

```text
/media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

Jika proses berhasil, terminal menampilkan jumlah alert dan lokasi output:

```text
Deteksi selesai: ... alert, state tersisa: ...
Alert tersimpan di: ../alerts.csv
```

Baca hasil:

```bash
cat ../alerts.csv
```

Atau dalam format tabel:

```bash
column -s, -t < ../alerts.csv
```

## 9. Memahami `alerts.csv`

Kolom hasil berarti:

| Kolom | Arti |
|---|---|
| `timestamp` | Waktu alert dibuat |
| `source_ip` | Pengirim paket |
| `destination_ip` | Tujuan paket |
| `unique_ports` | Jumlah port berbeda dalam window |
| `connections` | Jumlah paket/event dalam window |
| `syn_ratio` | Rasio paket dengan flag SYN |
| `reason` | Rule yang terpenuhi |

Contoh `reason`:

```text
unique_ports_threshold
```

berarti alert dibuat karena jumlah port unik mencapai threshold.

```text
connections_threshold,syn_ratio_threshold
```

berarti dua rule terpenuhi.

Jika CSV hanya berisi header, artinya tidak ada paket yang memenuhi rule.
Itu belum tentu error.

### Contoh hasil test drive kamu

Contoh hasil:

```text
timestamp,source_ip,destination_ip,unique_ports,connections,syn_ratio,reason
2026-10-12T07:29:30.398629+00:00,127.0.0.1,127.0.0.1,10,12,0.3333,unique_ports_threshold
```

Artinya:

- `source_ip` dan `destination_ip` sama-sama `127.0.0.1` karena laptop
  melakukan scan terhadap dirinya sendiri;
- `unique_ports=10` berarti detector melihat 10 destination port berbeda
  dalam window;
- `connections=12` berarti ada 12 event/paket TCP yang dihitung;
- `syn_ratio=0.3333` berarti sekitar 33,33% event yang dihitung memiliki flag
  SYN;
- `reason=unique_ports_threshold` berarti alert muncul karena rule jumlah port
  unik terpenuhi;
- satu alert berarti aplikasi berhasil menemukan setidaknya satu pola yang
  memenuhi rule, bukan berarti hanya ada satu paket.

Jadi hasil kamu menunjukkan pipeline sudah bekerja:

```text
Nmap membuat traffic
→ tcpdump merekam traffic
→ Scapy membaca PCAP
→ detector menghitung karakteristik
→ detector menghasilkan alert CSV
```

Hasil ini belum merupakan hasil akhir skripsi. Ini adalah bukti bahwa aplikasi
dan alur test drive dapat berjalan.

## 9A. Apa maksudnya mengulang dengan port berbeda?

“Port berbeda” berarti **mengubah rentang port yang diperiksa oleh Nmap**,
bukan harus mencari atau mengubah port aplikasi yang sedang digunakan laptop.

Contoh:

```bash
nmap -sT -p 1-10 127.0.0.1
nmap -sT -p 1-50 127.0.0.1
nmap -sT -p 1-100 127.0.0.1
nmap -sT -p 100-200 127.0.0.1
```

Keterangan:

- `-p 1-10`: Nmap mencoba port 1 sampai 10;
- `-p 1-50`: Nmap mencoba port 1 sampai 50;
- `-p 100-200`: Nmap mencoba port 100 sampai 200;
- target tetap `127.0.0.1`, yaitu laptop sendiri.

Untuk setiap percobaan, ulangi seluruh alur:

1. hapus atau ganti nama PCAP lama;
2. mulai `tcpdump`;
3. jalankan satu perintah Nmap;
4. hentikan `tcpdump`;
5. jalankan detector;
6. simpan CSV dengan nama berbeda.

Contoh nama hasil:

```text
capture-port-10.pcap
alerts-port-10.csv
capture-port-50.pcap
alerts-port-50.csv
capture-port-100.pcap
alerts-port-100.csv
```

Contoh perintah untuk percobaan port 1 sampai 50:

Terminal A:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo tcpdump -i lo -w ../capture-port-50.pcap 'ip and tcp'
```

Terminal B:

```bash
nmap -sT -p 1-50 127.0.0.1
```

Setelah Nmap selesai, tekan `Ctrl+C` di Terminal A. Kemudian jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py \
  --pcap ../capture-port-50.pcap \
  --output ../alerts-port-50.csv
```

## 9B. Percobaan berikutnya yang lebih bermakna

Jangan hanya mengulang perintah yang sama. Buat beberapa kondisi agar hasil
memiliki pembanding:

| Percobaan | Traffic | Tujuan |
|---|---|---|
| A | Tidak menjalankan Nmap, hanya membuat PCAP kosong/minimal | Melihat kondisi tanpa scanning |
| B | Scan port 1-10 | Jumlah port sedikit |
| C | Scan port 1-50 | Jumlah port sedang |
| D | Scan port 1-100 | Jumlah port lebih banyak |
| E | TCP connect scan `-sT` | Menguji jenis scan yang dipakai sekarang |
| F | TCP SYN scan `-sS` | Membandingkan jenis scan kedua |

Untuk sekarang, fokuskan dulu pada B, C, dan D. Setelah itu baru mencoba
`-sS`, karena SYN scan biasanya memerlukan `sudo`:

```bash
sudo nmap -sS -p 1-100 127.0.0.1
```

Setiap percobaan harus memiliki file PCAP dan CSV sendiri. Jangan menimpa
hasil lama karena hasil lama diperlukan untuk perbandingan.

## 9C. Apa yang perlu dicatat?

Buat catatan sederhana seperti berikut:

| ID | Perintah | Port | Alert? | Unique ports | Connections | Reason |
|---|---|---:|---|---:|---:|---|
| B | `nmap -sT -p 1-10 127.0.0.1` | 10 | Ya/Tidak | ... | ... | ... |
| C | `nmap -sT -p 1-50 127.0.0.1` | 50 | Ya/Tidak | ... | ... | ... |
| D | `nmap -sT -p 1-100 127.0.0.1` | 100 | Ya/Tidak | ... | ... | ... |

Kolom `port` pada tabel berarti jumlah port yang diminta Nmap untuk diperiksa.
Kolom `unique_ports` pada CSV adalah jumlah port yang benar-benar terlihat
oleh detector dalam sliding window. Kedua angka tersebut bisa berbeda.

## 9D. Mengapa perlu traffic normal?

Scanning saja belum cukup untuk menilai detector. Kamu juga perlu kondisi
normal sebagai pembanding, misalnya membuka website atau menggunakan koneksi
SSH ke laptop sendiri jika service tersebut tersedia.

Tujuannya:

- scanning yang terdeteksi = kandidat TP;
- traffic normal yang tidak menghasilkan alert = kandidat TN;
- traffic normal yang menghasilkan alert = kandidat FP;
- scanning yang tidak menghasilkan alert = kandidat FN.

Pada test drive laptop, jangan langsung mengklaim nilai Detection Rate.
Kumpulkan beberapa percobaan dengan label yang jelas terlebih dahulu.

## 10. Jika belum ada alert

Coba ulangi analisis dengan threshold test drive yang lebih rendah:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py \
  --pcap ../capture.pcap \
  --output ../alerts-test.csv \
  --ports-threshold 3 \
  --connections-threshold 5 \
  --syn-ratio-threshold 0.50
```

Lihat:

```bash
cat ../alerts-test.csv
```

Angka rendah dipakai hanya untuk membuktikan pipeline bekerja. Jangan
menjadikannya threshold final skripsi sebelum melakukan pengujian traffic
normal dan beberapa skenario scanning.

## 11. Periksa isi PCAP jika hasil kosong

Gunakan tcpdump untuk melihat ringkasan paket:

```bash
tcpdump -r /media/user/D/0-SKRIPSI/scriptsee/capture.pcap \
  -nn 'ip and tcp'
```

Jika tidak ada output, file tidak berisi traffic IPv4/TCP yang sesuai filter.
Pastikan:

1. tcpdump memakai `-i lo`;
2. Nmap diarahkan ke `127.0.0.1`;
3. tcpdump belum dihentikan sebelum Nmap berjalan;
4. file PCAP yang dibaca adalah file yang baru dibuat.

## 12. Alternatif test dengan live capture

Setelah mode PCAP berhasil, kamu dapat mencoba detector langsung. Cari nama
interface:

```bash
ip link
```

Untuk loopback, gunakan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo ../.venv/bin/python detect.py \
  --interface lo \
  --count 100 \
  --output ../live-alerts.csv
```

Saat proses menunggu paket, jalankan Nmap di terminal lain:

```bash
nmap -sT -p 1-100 127.0.0.1
```

Setelah 100 paket tertangkap, proses berhenti dan hasil berada di
`live-alerts.csv`. Mode live lebih sulit diulang daripada PCAP, sehingga
gunakan PCAP sebagai mode utama belajar dan eksperimen.

## 13. Error yang paling umum

### `No module named 'scapy'`

Python yang dipakai bukan Python `.venv`. Jalankan:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import scapy; print(scapy.__file__)"
```

### `python: command not found`

Environment belum aktif. Gunakan:

```bash
source /media/user/D/0-SKRIPSI/scriptsee/.venv/bin/activate
```

Atau jalankan dengan path penuh:

```bash
/media/user/D/0-SKRIPSI/scriptsee/.venv/bin/python \
  /media/user/D/0-SKRIPSI/scriptsee/app/detect.py \
  --pcap /media/user/D/0-SKRIPSI/scriptsee/capture.pcap \
  --output /media/user/D/0-SKRIPSI/scriptsee/alerts.csv
```

### `PCAP file tidak ditemukan`

Periksa:

```bash
ls -lh /media/user/D/0-SKRIPSI/scriptsee/capture.pcap
```

Jika belum ada, ulangi proses tcpdump dan Nmap.

### Tidak ada permission saat menjalankan tcpdump

Gunakan `sudo` pada perintah tcpdump:

```bash
sudo tcpdump -i lo -w ../capture.pcap 'ip and tcp'
```

### Tidak ada alert

Pastikan PCAP berisi traffic, lalu coba threshold lebih rendah. Ingat bahwa
detector saat ini memproses IPv4/TCP dan rule akan membuat alert hanya jika
threshold terpenuhi.

## 14. Perintah singkat yang bisa disalin

Siapkan aplikasi:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Terminal A:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
sudo tcpdump -i lo -w ../capture.pcap 'ip and tcp'
```

Terminal B:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee
source .venv/bin/activate
nmap -sT -p 1-100 127.0.0.1
```

Hentikan Terminal A dengan `Ctrl+C`, lalu Terminal C:

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app
python detect.py --pcap ../capture.pcap --output ../alerts.csv
cat ../alerts.csv
```

## 15. Setelah test drive berhasil

Langkah berikutnya bukan langsung membuat web. Lakukan secara berurutan:

1. ulangi test dengan jumlah port berbeda;
2. ubah threshold dan catat hasilnya;
3. buat satu PCAP traffic normal;
4. buat satu PCAP scanning;
5. beri label setiap PCAP;
6. catat apakah alert sesuai label;
7. mulai membuat tabel TP, TN, FP, dan FN;
8. setelah memahami alur, baru siapkan VM.

Dengan urutan ini, kamu memahami fungsi setiap bagian sebelum masuk ke
eksperimen jaringan yang lebih kompleks.
