# Gambaran Realisasi Skripsi Scriptsee

Dokumen ini menjelaskan **apa yang dibuat, siapa yang menggunakan, bagaimana
alur penggunaannya, dan urutan pengerjaannya**. Tujuannya supaya penelitian
tidak melebar menjadi proyek web, desktop, dan sistem keamanan jaringan
sekaligus.

## 1. Inti skripsi dalam satu kalimat

Penelitian ini mengembangkan aplikasi Python yang menerima traffic IPv4/TCP,
menghitung karakteristik traffic dalam jendela waktu tertentu, kemudian
memberikan alert apabila pola traffic memenuhi aturan port scanning.

Jadi, produk utama skripsi bukan tampilan web atau desktop. Produk utamanya
adalah **metode deteksi dan hasil evaluasinya**.

## 2. Masalah yang ingin diselesaikan

Administrator atau peneliti perlu mengetahui apakah traffic menuju suatu host
merupakan traffic normal atau aktivitas port scanning. Aplikasi ini membantu
dengan cara:

1. membaca paket jaringan;
2. mengambil source IP, destination IP, destination port, TCP flags, dan
   timestamp;
3. mengelompokkan paket berdasarkan pasangan source IP dan destination IP;
4. menghitung jumlah port unik, jumlah koneksi, dan rasio paket SYN;
5. membandingkan hasilnya dengan threshold;
6. menyimpan peringatan apabila aturan deteksi terpenuhi.

Penelitian ini tidak bertujuan memblokir penyerang, mengeksploitasi target,
atau menggantikan IDS/IPS produksi. Penelitian hanya mendeteksi dan
mengevaluasi pola traffic dalam jaringan uji yang terisolasi.

## 3. Siapa yang menggunakan aplikasi?

Pengguna utama adalah **peneliti atau administrator jaringan**. Pengguna
tersebut menjalankan aplikasi pada komputer sensor untuk:

- menganalisis file PCAP hasil rekaman traffic; atau
- memantau traffic secara langsung melalui network interface.

Pengguna tidak perlu mengoperasikan algoritma secara manual. Pengguna cukup
menentukan sumber traffic, threshold, dan lokasi output, kemudian membaca file
alert yang dihasilkan.

## 4. Bentuk aplikasi yang direkomendasikan

### Rekomendasi: Python core + CLI, kemudian web dashboard opsional

Untuk tahap skripsi, gunakan pembagian berikut:

```text
Core detector Python
        |
        +-- CLI untuk eksperimen dan pengujian
        |
        +-- Web dashboard sederhana (opsional, tahap presentasi)
```

**Jangan membangun web dan desktop sekaligus.** Keduanya hanya merupakan
antarmuka berbeda untuk algoritma yang sama, sedangkan skripsi berfokus pada
deteksi dan evaluasi.

### Mengapa tidak desktop?

Aplikasi desktop memang dapat menampilkan tabel dan grafik, tetapi:

- tidak memberikan nilai penelitian yang besar dibanding CLI;
- menambah pekerjaan UI, packaging, dan kompatibilitas sistem operasi;
- kurang sesuai untuk aplikasi yang dijalankan sebagai sensor jaringan.

Desktop baru layak dipilih jika dosen secara khusus meminta aplikasi GUI
lokal/offline.

### Mengapa web dashboard boleh ditambahkan?

Web dashboard berguna untuk demo karena hasil deteksi lebih mudah dibaca.
Namun dashboard sebaiknya hanya menjadi **lapisan presentasi**, bukan tempat
algoritma utama. Detector tetap berupa modul Python yang bisa diuji tanpa
browser.

Dashboard tahap akhir dapat menampilkan:

- status proses analisis;
- jumlah paket yang dibaca;
- jumlah alert;
- source IP dan destination IP;
- jumlah port unik, jumlah koneksi, dan rasio SYN;
- waktu alert;
- grafik sederhana traffic normal dan scanning.

## 5. Arsitektur sistem

```text
Traffic jaringan / file PCAP
              |
              v
      Packet collector (Scapy)
              |
              v
       Feature extraction
              |
              v
 Flow state: source IP + destination IP
        sliding window + TTL
              |
              v
       Rule-based detection
              |
              v
       Alert dan hasil evaluasi
              |
          CSV / dashboard
```

Komponen yang sudah ada di repository:

- `app/portscan_detector.py`: feature, state manager, sliding window, TTL,
  aturan deteksi, pembacaan PCAP, live capture, dan penulisan CSV;
- `app/detect.py`: command-line interface;
- `app/test_portscan_detector.py`: unit test untuk threshold, window, dan TTL;
- `requirements.txt`: dependensi Scapy.

## 6. Bagaimana penggunaannya?

### Mode A — Analisis PCAP (mode utama untuk penelitian)

Mode ini paling disarankan pada tahap awal karena hasilnya dapat diulang dan
lebih mudah dibandingkan dengan ground truth.

Alurnya:

1. Jalankan traffic normal atau skenario port scanning pada jaringan uji.
2. Rekam traffic menggunakan `tcpdump` atau Wireshark.
3. Salin file `.pcap` ke komputer sensor.
4. Jalankan detector terhadap file tersebut.
5. Buka file `alerts.csv`.
6. Bandingkan alert dengan label skenario yang sebenarnya.

Contoh:

```bash
python detect.py --pcap capture.pcap --output alerts.csv
```

Threshold dapat diubah untuk eksperimen:

```bash
python detect.py \
  --pcap capture.pcap \
  --output alerts.csv \
  --window 10 \
  --ttl 30 \
  --ports-threshold 10 \
  --connections-threshold 20 \
  --syn-ratio-threshold 0.70
```

### Mode B — Live capture (tahap lanjutan)

Setelah mode PCAP stabil, detector dapat membaca interface secara langsung:

```bash
sudo .venv/bin/python detect.py \
  --interface eth1 \
  --output alerts.csv
```

Mode ini biasanya membutuhkan hak administrator atau capability jaringan.
Gunakan hanya pada interface dan jaringan yang memang dimiliki atau sudah
mendapat izin.

## 7. Topologi pengujian

Gunakan jaringan virtual yang terisolasi, misalnya tiga VM:

```text
VM Scanner                  VM Sensor                  VM Target
Menjalankan Nmap            Menjalankan Python         Host yang diuji
192.168.56.10               192.168.56.20              192.168.57.30
                                  |
                         gateway / titik capture
```

Desain yang paling mudah dijelaskan adalah Sensor sebagai gateway di antara
Scanner dan Target. Dengan demikian traffic dari Scanner ke Target melewati
Sensor dan dapat diamati oleh detector. Sekadar menempatkan tiga VM pada satu
virtual switch belum tentu membuat Sensor melihat traffic unicast antara dua
VM lain.

Pembagian tugas:

| Komponen | Peran | Software |
|---|---|---|
| Scanner | Menghasilkan skenario scanning | Linux dan Nmap |
| Sensor | Menangkap dan menganalisis traffic | Linux, Python, Scapy, tcpdump |
| Target | Menjadi host yang diuji | Linux dan service uji seperlunya |
| Host | Menjalankan VM dan mengembangkan kode | Linux Mint dan VirtualBox |

Nmap hanya boleh diarahkan ke VM Target milik sendiri dalam jaringan
penelitian. Semua alamat IP, versi OS, konfigurasi VM, waktu pengujian, dan
perintah pengujian perlu dicatat.

## 8. Skenario penelitian

Minimal buat dua kelompok data:

### Traffic normal

Contohnya komunikasi biasa antara VM, seperti ping, SSH, atau akses HTTP yang
memang disiapkan pada jaringan uji. Traffic normal harus diberi label sebagai
`normal`.

### Traffic port scanning

Gunakan beberapa variasi yang terdokumentasi:

- jumlah port sedikit dan banyak;
- scanning cepat dan lambat;
- TCP SYN scan dan TCP connect scan;
- durasi scanning yang berbeda.

Contoh perintah hanya untuk jaringan uji milik sendiri:

```bash
nmap -sS -p 20-40 192.168.57.30
nmap -sT -p 20-40 192.168.57.30
```

Setiap file PCAP harus memiliki catatan ground truth: jenis traffic, alamat
scanner, alamat target, daftar port, waktu mulai, waktu selesai, dan label.

## 9. Apa yang diukur dalam skripsi?

Jangan berhenti pada pernyataan “aplikasi berhasil berjalan”. Hasil utama
penelitian adalah pengukuran:

- **TP**: scanning terdeteksi sebagai scanning;
- **TN**: traffic normal tidak menghasilkan alert;
- **FP**: traffic normal salah dianggap scanning;
- **FN**: scanning tidak terdeteksi;
- **Detection Rate** atau recall: `TP / (TP + FN)`;
- **False Positive Rate**: `FP / (FP + TN)`;
- **False Negative Rate**: `FN / (TP + FN)`;
- **Detection Time**: waktu sejak scanning dimulai sampai alert muncul.

Hasil tersebut dibandingkan untuk setiap variasi jumlah port, interval probe,
dan durasi scanning. Threshold awal di dalam aplikasi bukan hasil final;
threshold harus diuji dan dijelaskan berdasarkan data eksperimen.

## 10. Urutan pengerjaan yang realistis

### Tahap 1 — Pastikan core detector

1. Pahami `PacketFeature`, `DetectionConfig`, dan `PortScanDetector`.
2. Jalankan unit test.
3. Uji input paket buatan untuk memastikan alert muncul pada kondisi yang
   diharapkan.
4. Pastikan output CSV dapat dibaca.

### Tahap 2 — Siapkan eksperimen PCAP

1. Buat jaringan internal tiga VM.
2. Pastikan Scanner dapat mencapai Target.
3. Pastikan Sensor benar-benar melihat traffic.
4. Rekam traffic normal dan beberapa skenario scanning.
5. Jalankan detector pada setiap PCAP.

### Tahap 3 — Evaluasi

1. Buat tabel ground truth.
2. Cocokkan alert dengan skenario.
3. Hitung TP, TN, FP, FN, dan metrik lainnya.
4. Ulangi pengujian jika hasil dipengaruhi konfigurasi jaringan atau threshold.

### Tahap 4 — Dokumentasi skripsi

Dokumentasikan arsitektur, algoritma, konfigurasi threshold, topologi VM,
skenario, hasil, keterbatasan, dan analisis. Jelaskan bahwa fokus penelitian
adalah rule-based detection, bukan machine learning.

### Tahap 5 — Dashboard opsional

Jika core dan evaluasi sudah selesai, buat web dashboard kecil yang membaca
hasil CSV atau database. Dashboard tidak boleh mengubah hasil algoritma dan
tidak boleh menjadi alasan untuk menunda eksperimen utama.

## 11. Keputusan yang sebaiknya dibawa ke dosen

Rancangan yang dapat disampaikan:

> Penelitian ini menghasilkan aplikasi detector berbasis Python. Aplikasi
> menerima traffic IPv4/TCP dari PCAP dan, sebagai tahap lanjutan, dari live
> capture. Detector mengelompokkan traffic berdasarkan source IP dan
> destination IP, menerapkan sliding time window serta TTL, lalu menggunakan
> rule berdasarkan jumlah port unik, jumlah koneksi, dan rasio SYN. Pengujian
> dilakukan pada tiga VM terisolasi yang terdiri dari Scanner, Sensor, dan
> Target. Hasil deteksi disimpan ke CSV dan dievaluasi menggunakan TP, TN, FP,
> FN, Detection Rate, False Positive Rate, False Negative Rate, dan Detection
> Time. Web dashboard hanya merupakan antarmuka tambahan untuk menampilkan
> hasil, bukan fokus utama penelitian.

## 12. Kesimpulan praktis

Untuk sekarang, pilihan yang paling tepat adalah:

1. **Buat dan selesaikan detector Python terlebih dahulu.**
2. **Gunakan CLI + PCAP sebagai jalur eksperimen utama.**
3. **Gunakan tiga VM terisolasi untuk menghasilkan data dan ground truth.**
4. **Ukur performa deteksi, bukan hanya membuat aplikasi berjalan.**
5. **Tambahkan web dashboard hanya jika eksperimen utama sudah stabil.**
6. **Tidak perlu membuat aplikasi desktop.**

Dengan pembagian ini, skripsi tetap terarah: Python menjadi inti metode,
PCAP/VM menjadi sarana eksperimen, CSV menjadi output yang dapat dievaluasi,
dan web dashboard menjadi fitur presentasi opsional.