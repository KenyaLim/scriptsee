# Belajar Skripsi Scriptsee dari Nol

Dokumen ini adalah versi sederhana dari [rancangan.txt](/media/user/D/0-SKRIPSI/scriptsee/rancangan.txt).
Baca dari atas ke bawah. Kamu tidak harus langsung memahami semua istilah.
Tujuan awalnya adalah memahami **cerita besar skripsi**, lalu perlahan
memahami bagian teknisnya.

## 1. Skripsi ini sebenarnya membuat apa?

Skripsi ini membuat aplikasi Python untuk menjawab pertanyaan:

> Apakah sekumpulan traffic TCP terlihat seperti aktivitas port scanning?

Aplikasi tidak melakukan hacking dan tidak otomatis melakukan scanning.
Aplikasi hanya:

1. membaca traffic jaringan;
2. mengambil informasi penting dari paket;
3. menghitung pola traffic;
4. memberi alert jika pola tersebut memenuhi aturan tertentu.

Gambaran paling sederhananya:

```text
Nmap membuat traffic scanning
          |
          v
tcpdump/Wireshark merekam traffic menjadi PCAP
          |
          v
Scriptsee membaca PCAP
          |
          v
Scriptsee menghasilkan alert CSV
```

## 2. Apa itu jaringan, IP, port, dan paket?

### IP address

IP adalah alamat perangkat dalam jaringan. Contoh:

```text
192.168.1.10
127.0.0.1
```

`127.0.0.1` adalah alamat khusus yang berarti “laptop ini sendiri”.

### Port

Port adalah nomor pintu komunikasi pada perangkat. Nilainya 0 sampai 65535.
Contoh umum:

| Port | Contoh layanan |
|---:|---|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |

Port yang terbuka biasanya berarti ada program yang sedang menunggu koneksi.
Port yang tertutup akan menolak atau mengabaikan koneksi.

### Paket

Data jaringan tidak dikirim sekaligus sebagai satu benda besar. Data dipecah
menjadi paket-paket kecil. Setiap paket dapat memiliki:

- alamat sumber;
- alamat tujuan;
- port sumber;
- port tujuan;
- protocol;
- TCP flags;
- timestamp.

Scriptsee menganalisis metadata tersebut, bukan isi pesan atau password.

## 3. Apa itu port scanning?

Port scanning adalah aktivitas mencoba banyak port pada satu target untuk
mengetahui port mana yang terbuka.

Contoh sederhana:

```text
Scanner mencoba port 22, 23, 80, 443, 8080, dan seterusnya
```

Port scanning tidak selalu berarti serangan. Administrator juga dapat
memakainya untuk audit jaringan. Namun dari sudut pandang monitoring, pola ini
perlu diketahui karena dapat menjadi tahap awal serangan.

## 4. Apa itu TCP SYN scan dan TCP connect scan?

### TCP SYN scan (`-sS`)

Scanner mengirim paket SYN lalu mengamati respons. Koneksi tidak diselesaikan
seperti koneksi aplikasi biasa.

```text
Scanner -- SYN --> Target
Scanner <-- SYN-ACK/RST -- Target
```

Mode ini biasanya memerlukan hak administrator.

### TCP connect scan (`-sT`)

Scanner menggunakan koneksi TCP biasa sampai proses koneksi selesai atau
ditolak.

Mode ini lebih mudah digunakan untuk test drive sebagai pengguna biasa.

Penelitian ini hanya membahas dua jenis tersebut. UDP scan, FIN scan, NULL
scan, Xmas scan, dan fragmentasi berada di luar batasan.

## 5. Apa itu TCP flags?

TCP flags adalah penanda keadaan atau maksud sebuah paket TCP.

| Flag | Penjelasan sederhana |
|---|---|
| SYN | Memulai koneksi |
| SYN-ACK | Target menerima permintaan awal |
| ACK | Mengakui paket atau melanjutkan koneksi |
| RST | Menolak atau mereset koneksi |
| FIN | Menutup koneksi |

Port scan dapat menghasilkan banyak SYN, lalu respons SYN-ACK atau RST.
Karena itu flags dapat menjadi petunjuk, tetapi satu flag saja tidak cukup
untuk membuktikan bahwa traffic adalah scanning.

## 6. Karakteristik apa yang dihitung aplikasi?

Berdasarkan rancangan, aplikasi dapat menggunakan:

1. `source_ip`: siapa yang mengirim;
2. `destination_ip`: siapa yang dituju;
3. `destination_port`: port yang dituju;
4. timestamp: kapan paket terjadi;
5. jumlah port unik;
6. jumlah koneksi;
7. frekuensi koneksi;
8. interval antar-koneksi;
9. TCP flags dan rasionya.

Contoh:

```text
source IP      = 10.0.0.2
destination IP = 10.0.0.3
port yang dicoba = 20, 21, 22, 23, 24, 25, 80
jumlah port unik = 7
```

Jika satu sumber mencoba banyak port pada tujuan yang sama dalam waktu
singkat, pola tersebut lebih mirip port scanning daripada koneksi normal.

## 7. Apa itu sliding time window?

Sliding time window berarti aplikasi hanya melihat traffic dalam rentang waktu
terakhir, misalnya 10 detik.

```text
Waktu sekarang: 12:00:20
Window 10 detik: 12:00:10 sampai 12:00:20
```

Paket pada 12:00:05 tidak lagi dihitung. Ketika waktu bergerak, window ikut
bergeser. Inilah alasan namanya “sliding”.

Mengapa diperlukan?

- scanning cepat terlihat dalam window;
- traffic lama tidak terus memengaruhi keputusan;
- memory tidak menyimpan seluruh sejarah traffic selamanya.

## 8. Apa itu hash table dan TTL?

Hash table dapat dibayangkan sebagai kamus Python:

```python
state[(source_ip, destination_ip)] = data_traffic
```

Contoh:

```python
state[("10.0.0.2", "10.0.0.3")] = {
    "ports": {20, 21, 22},
    "connections": 3,
    "last_seen": 100.5,
    "expires_at": 130.5,
}
```

TTL atau Time-To-Live adalah batas waktu hidup sebuah record. Jika tidak ada
traffic baru sampai TTL berakhir, record dihapus.

Alur setiap paket:

1. hapus state yang sudah kedaluwarsa;
2. cari state berdasarkan pasangan source dan destination IP;
3. buang event di luar window;
4. tambahkan paket baru;
5. hitung ulang karakteristik;
6. evaluasi rule;
7. perbarui TTL.

## 9. Apa itu rule-based detection?

Rule-based berarti keputusan dibuat menggunakan aturan dan threshold yang
ditentukan, bukan Machine Learning.

Contoh rule:

```text
Jika port unik >= 10
atau jumlah koneksi >= 20
atau rasio SYN >= 70 persen,
maka buat alert.
```

Threshold bukan angka sakral. Threshold harus diuji dengan traffic normal dan
traffic scanning. Threshold terlalu rendah dapat menghasilkan banyak false
positive. Threshold terlalu tinggi dapat melewatkan scanning.

## 10. Apa fungsi setiap file aplikasi sekarang?

| File | Fungsi |
|---|---|
| [portscan_detector.py](/media/user/D/0-SKRIPSI/scriptsee/app/portscan_detector.py) | Logika utama detector |
| [detect.py](/media/user/D/0-SKRIPSI/scriptsee/app/detect.py) | Perintah untuk menjalankan detector |
| [test_portscan_detector.py](/media/user/D/0-SKRIPSI/scriptsee/app/test_portscan_detector.py) | Test otomatis |
| [requirements.txt](/media/user/D/0-SKRIPSI/scriptsee/requirements.txt) | Dependency, termasuk Scapy |

### `PacketFeature`

Mewakili informasi penting dari satu paket:

```text
timestamp
source_ip
destination_ip
destination_port
flags
```

### `DetectionConfig`

Menyimpan pengaturan:

```text
window_seconds
ttl_seconds
unique_ports_threshold
connections_threshold
syn_ratio_threshold
```

### `PortScanDetector`

Mengelola state, sliding window, TTL, dan evaluasi rule.

### `read_pcap`

Membaca file PCAP menggunakan Scapy dan mengambil paket IPv4/TCP.

### `capture_live`

Membaca traffic langsung dari interface jaringan.

### `write_alerts`

Menyimpan alert ke CSV.

## 11. Perbedaan rancangan dengan implementasi saat ini

Ini bagian penting agar ekspektasimu benar.

`rancangan.txt` adalah desain target penelitian. Implementasi sekarang sudah
memiliki:

- pembacaan PCAP;
- live capture;
- filtering IPv4/TCP;
- ekstraksi IP, port, flags, timestamp;
- state berdasarkan source IP dan destination IP;
- sliding window;
- TTL cleanup;
- rule port unik;
- rule jumlah koneksi;
- rule rasio SYN;
- output alert CSV;
- unit test.

Namun rancangan juga menyebut interval antar-koneksi, rasio RST terhadap SYN,
evaluasi otomatis TP/TN/FP/FN, Detection Time, dan beberapa variasi eksperimen.
Bagian tersebut masih merupakan pekerjaan pengembangan/evaluasi berikutnya,
bukan berarti sudah seluruhnya tersedia di aplikasi saat ini.

## 12. Bagaimana membuktikan aplikasi bagus?

Tidak cukup hanya menunjukkan bahwa program dapat dijalankan. Penelitian perlu
menyediakan ground truth.

### Ground truth

Ground truth adalah label kondisi sebenarnya:

```text
File A = traffic normal
File B = TCP SYN scan
File C = TCP connect scan
```

Label dibuat dari perintah Nmap dan waktu pelaksanaan yang dicatat.

### Confusion matrix

| Kondisi sebenarnya | Detector memberi scanning | Detector memberi normal |
|---|---:|---:|
| Scanning | TP | FN |
| Normal | FP | TN |

- TP: scanning terdeteksi;
- FN: scanning tidak terdeteksi;
- FP: normal dianggap scanning;
- TN: normal tetap dianggap normal.

### Rumus

```text
Detection Rate      = TP / (TP + FN) x 100%
False Positive Rate = FP / (FP + TN) x 100%
False Negative Rate = FN / (FN + TP) x 100%
```

Detection Time adalah waktu dari awal scanning sampai alert pertama muncul.

## 13. Urutan belajar yang disarankan

Jangan mencoba mempelajari semua bagian sekaligus.

1. Pahami IP, port, paket, dan TCP.
2. Jalankan test drive lokal.
3. Baca hasil `alerts.csv`.
4. Baca kode `PacketFeature` dan `DetectionConfig`.
5. Pahami sliding window dan TTL.
6. Ubah threshold dan amati perubahan alert.
7. Pelajari Nmap dan variasi scan.
8. Siapkan data normal dan scanning.
9. Hitung TP, TN, FP, FN.
10. Baru siapkan VM untuk eksperimen yang lebih terkontrol.

## 14. Ringkasan yang perlu diingat

```text
Port scanning = mencoba banyak port
Scapy         = membaca/menangkap paket
Nmap          = pembuat traffic scanning
PCAP          = file rekaman traffic
Feature       = informasi yang diambil dari paket
Window        = rentang waktu pengamatan
TTL           = waktu hidup state
Rule          = aturan keputusan
Alert         = indikasi scanning
Ground truth  = label kondisi sebenarnya
```

Kalimat paling penting:

> Skripsi ini bukan sekadar membuat program yang mengeluarkan alert. Skripsi
> ini menguji apakah aturan berdasarkan karakteristik traffic dapat membedakan
> traffic normal dan port scanning secara terukur.
