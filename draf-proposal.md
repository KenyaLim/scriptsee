# PENGEMBANGAN DAN EVALUASI APLIKASI DETEKSI PORT SCANNING
# BERDASARKAN KARAKTERISTIK TRAFFIC JARINGAN MENGGUNAKAN PYTHON

## Proposal Tugas Akhir Skripsi

**Diajukan oleh:**

- Nama lengkap: `[NAMA LENGKAP]`
- NIM: `[NIM]`

**Program Studi Informatika**  
**Fakultas Teknologi Informasi**  
**Universitas Kristen Duta Wacana**  
**Yogyakarta**  
`[TAHUN]`

---

## Identitas Pengusul

**Judul usulan:**  
Pengembangan dan Evaluasi Aplikasi Deteksi Port Scanning Berdasarkan
Karakteristik Traffic Jaringan Menggunakan Python

**Mata kuliah pendukung:**

1. Pengantar Keamanan Jaringan — `[Nilai]`
2. `[Mata kuliah pendukung lainnya, jika ada]` — `[Nilai]`

**Mata kuliah wajib profil:**

1. Pengantar Keamanan Jaringan — `[Nilai]`
2. Keamanan Jaringan — `[Nilai]`

**Profesi lulusan:** `[PSD / AI / DMS / NI]`

| Informasi | Keterangan |
|---|---|
| NIM | `[Tuliskan NIM]` |
| Nama lengkap | `[Tuliskan Nama Lengkap]` |
| IPK | `[IPK Anda]` |
| No. HP/WhatsApp | `[Nomor HP]` |
| Email | `[Email @ti.ukdw.ac.id]` |

Proposal ini diajukan dalam seminar kolokium sebagai persyaratan untuk memulai
penulisan skripsi.

**Proposal Desk Evaluation:** `[I/II]`  
**Semester:** `[Gasal/Genap] [Tahun Akademik]`  
**Tahun:** `[TAHUN]`

## Halaman Persetujuan Proposal

Pada tanggal `[tanggal persetujuan]`, proposal dengan keterangan berikut:

| Keterangan | Isi |
|---|---|
| NIM | `[NIM MAHASISWA]` |
| Judul proposal | Pengembangan dan Evaluasi Aplikasi Deteksi Port Scanning Berdasarkan Karakteristik Traffic Jaringan Menggunakan Python |

telah disetujui oleh:

| Calon Dosen Pembimbing 1 | Calon Dosen Pembimbing 2 |
|---|---|
|  |  |
| **[Nama Lengkap Dosen]** | **[Nama Lengkap Dosen]** |

---

# 1. Latar Belakang

Jaringan komputer memungkinkan berbagai perangkat berkomunikasi melalui alamat
IP dan port tertentu. Port digunakan sebagai endpoint bagi layanan yang berjalan
pada suatu host. Informasi mengenai port yang terbuka dapat memberikan gambaran
tentang layanan yang tersedia dan menjadi informasi awal dalam proses pengenalan
terhadap target jaringan.

Port scanning merupakan aktivitas pengiriman probe atau koneksi ke sejumlah port
pada host atau jaringan untuk mengetahui port yang terbuka dan layanan yang
tersedia. Dalam konteks keamanan jaringan, port scanning dapat menjadi tahap awal
sebelum serangan lanjutan karena hasil pemindaian dapat memberikan informasi
mengenai host aktif, port yang tersedia, dan layanan yang dapat diakses
(Pittman, 2023a). Oleh sebab itu, kemampuan mengenali pola port scanning dari
traffic jaringan penting untuk mendukung pemantauan keamanan.

Aktivitas port scanning menghasilkan karakteristik traffic yang berbeda dari
sebagian traffic normal. Pada *vertical port scan*, satu source IP mengirimkan
probe menuju banyak destination port pada destination IP yang sama. Jumlah
destination port yang berbeda, jumlah koneksi, dan frekuensi koneksi dalam
interval waktu tertentu dapat digunakan sebagai indikator scanning
(Pittman, 2023b). TCP flags juga dapat membantu membedakan pola koneksi,
misalnya dominasi paket SYN tanpa penyelesaian koneksi atau rasio respons
SYN-ACK dan RST terhadap paket SYN yang dikirim.

Port scanning dapat dilakukan secara cepat maupun perlahan. Pemindaian cepat
dapat menghasilkan banyak probe dalam interval singkat sehingga lebih mudah
terlihat. Sebaliknya, *slow port scan* memberikan jeda yang lebih panjang antar
probe agar menyerupai traffic normal. Pittman (2023a) menjelaskan bahwa
efektivitas dan karakteristik traffic dapat berbeda berdasarkan tool dan jenis
scan yang digunakan. Hal ini menunjukkan bahwa pengujian perlu mencatat tool,
parameter, dan waktu pelaksanaan secara terukur, termasuk ketika menguji traffic
dengan interval probe yang panjang.

Tantangan utama pendekatan *rule-based* adalah merumuskan threshold yang tidak
terlalu sensitif sehingga traffic normal yang padat tidak menghasilkan banyak
*false positive*, tetapi tetap cukup peka untuk mendeteksi *slow port scan*
yang menyerupai traffic normal. Oleh karena itu, penelitian ini tidak hanya
menggunakan jumlah port, tetapi menggabungkan jumlah port unik, frekuensi
koneksi, interval antar-koneksi, serta rasio TCP flags sebagai dasar aturan
deteksi. Nilai threshold akan diuji pada beberapa skenario dan dievaluasi
menggunakan *ground truth*.

Penelitian ini mengembangkan aplikasi deteksi port scanning berbasis Python.
Aplikasi mengambil source IP, destination IP, destination port, protocol, TCP
flags, dan timestamp dari paket IPv4 TCP menggunakan Scapy. Paket dapat
ditangkap secara langsung atau dibaca dari file PCAP. Data paket kemudian
dikelompokkan berdasarkan pasangan source IP dan destination IP dalam *sliding
time window*.

Untuk mencegah pertumbuhan penggunaan memori ketika aplikasi berjalan lama,
state setiap pasangan source IP dan destination IP disimpan dalam *hash table*
yang memiliki waktu kedaluwarsa atau TTL (*Time-To-Live*). Setiap entri
menyimpan timestamp paket terakhir, himpunan destination port unik, jumlah
koneksi, jumlah flag TCP, dan timestamp koneksi sebelumnya. Pada setiap paket
baru, entri yang melewati TTL dikeluarkan sebelum evaluasi berikutnya. Dengan
demikian, data di luar *sliding window* tidak terus tersimpan dan risiko
*memory leak* akibat state traffic lama dapat dikurangi.

Traffic port scanning dibangkitkan di jaringan terisolasi menggunakan Nmap,
yaitu tool yang umum digunakan untuk *network discovery* dan *security
auditing* (Nmap Project, 2026). Jenis scan TCP yang diuji adalah TCP SYN scan
(`nmap -sS`) dan TCP connect scan (`nmap -sT`). TCP SYN scan mengirim SYN dan
mengamati respons tanpa menyelesaikan koneksi secara penuh, sedangkan TCP
connect scan menyelesaikan koneksi TCP melalui system call. Setiap perintah,
target, rentang port, interval, dan waktu pelaksanaan dicatat agar label
*ground truth* dapat diverifikasi. Variasi *fast*, *medium*, dan *slow* dibuat
dengan mengatur jumlah port serta jeda antar-probe. Penggunaan Nmap dibatasi
pada host yang dimiliki atau telah memperoleh izin pengujian.

Pengujian juga menggunakan traffic normal yang dibangkitkan secara terkendali.
Hasil deteksi aplikasi dibandingkan dengan *ground truth* untuk memperoleh
*true positive* (TP), *true negative* (TN), *false positive* (FP), dan *false
negative* (FN). Selanjutnya dihitung *Detection Rate*, *False Positive Rate*,
*False Negative Rate*, dan *Detection Time*. Hasil tersebut digunakan untuk
menganalisis pengaruh jenis scan, jumlah port, interval probe, durasi scan, dan
threshold terhadap kinerja aplikasi.

# 2. Rumusan Masalah

1. Bagaimana mengembangkan aplikasi berbasis Python untuk menangkap dan
   mengekstraksi karakteristik traffic IPv4 TCP yang berkaitan dengan port
   scanning?
2. Bagaimana merumuskan aturan deteksi berbasis karakteristik traffic, yaitu
   jumlah destination port unik dalam *sliding time window*, frekuensi koneksi,
   interval antar-koneksi, dan rasio TCP flags, untuk membedakan traffic normal
   dan port scanning?
3. Bagaimana menerapkan struktur data berbasis *hash table* dengan TTL untuk
   mengelola state *sliding time window* agar penggunaan memori tetap
   terkendali selama aplikasi berjalan?
4. Bagaimana kemampuan aplikasi mendeteksi TCP SYN scan dan TCP connect scan
   menggunakan variasi jumlah port, interval probe, dan durasi scanning?
5. Berapa nilai *Detection Rate*, *False Positive Rate*, *False Negative Rate*,
   dan *Detection Time* yang dihasilkan aplikasi pada setiap skenario
   pengujian?

# 3. Batasan Masalah

1. Penelitian berfokus pada deteksi port scanning berdasarkan traffic jaringan,
   bukan eksploitasi vulnerability setelah port ditemukan.
2. Penelitian menggunakan pendekatan *rule-based detection* dan tidak
   menggunakan *Machine Learning* atau *Deep Learning*.
3. Traffic yang dianalisis adalah IPv4 dengan transport protocol TCP.
4. Parameter yang dianalisis meliputi source IP, destination IP, destination
   port, timestamp, TCP flags, jumlah destination port unik, jumlah koneksi,
   frekuensi koneksi, dan interval antar-koneksi.
5. Pengelompokan state dilakukan berdasarkan pasangan source IP dan destination
   IP dalam *sliding time window*. State dikelola menggunakan *hash table*
   dengan TTL yang nilainya ditentukan dan diuji dalam eksperimen.
6. Paket yang berada di luar *sliding time window* atau telah melewati TTL
   dikeluarkan dari state aplikasi.
7. Penelitian tidak menganalisis payload aplikasi dan tidak melakukan *deep
   packet inspection*.
8. Pengujian dilakukan pada lingkungan jaringan virtual atau fisik yang
   terisolasi dan dikendalikan.
9. Traffic uji terdiri atas traffic normal dan traffic port scanning yang
   dibangkitkan menggunakan Nmap dengan parameter yang terdokumentasi.
10. Jenis scan yang diuji adalah TCP SYN scan (`-sS`) dan TCP connect scan
    (`-sT`). UDP scan, FIN scan, NULL scan, Xmas scan, dan teknik fragmentasi
    tidak termasuk dalam penelitian ini.
11. Variasi pengujian meliputi *fast scan*, *medium scan*, *slow scan*, jumlah
    port, interval antar-probe, durasi scanning, dan nilai threshold.
12. Setiap traffic yang dibangkitkan sebagai scanning diberi label scanning
    berdasarkan perintah Nmap dan waktu pelaksanaan. Traffic normal diberi label
    normal.
13. Evaluasi menggunakan TP, TN, FP, FN, *Detection Rate*, *False Positive
    Rate*, *False Negative Rate*, dan *Detection Time*.

# 4. Tujuan Penelitian

1. Mengembangkan aplikasi berbasis Python untuk menangkap dan mengekstraksi
   karakteristik traffic IPv4 TCP.
2. Mengidentifikasi karakteristik traffic yang relevan untuk mendeteksi port
   scanning, meliputi port unik, frekuensi koneksi, interval koneksi, dan TCP
   flags.
3. Merancang dan mengimplementasikan *rule-based detection* dengan threshold
   yang dapat diuji pada beberapa skenario.
4. Menerapkan *hash table* dengan TTL untuk mengelola data *sliding time window*
   dan membatasi penyimpanan state traffic lama.
5. Menguji aplikasi pada TCP SYN scan dan TCP connect scan yang dibangkitkan
   menggunakan Nmap serta pada traffic normal.
6. Mengukur *Detection Rate*, *False Positive Rate*, *False Negative Rate*, dan
   *Detection Time*.
7. Menganalisis pengaruh jenis scan, jumlah port, interval probe, durasi
   scanning, dan threshold terhadap kemampuan deteksi.

# 5. Manfaat Penelitian

1. Menghasilkan aplikasi sederhana untuk mendeteksi aktivitas TCP port scanning
   berdasarkan traffic jaringan.
2. Memberikan evaluasi kuantitatif terhadap pendekatan *rule-based detection*.
3. Memberikan gambaran karakteristik traffic yang dapat digunakan untuk
   membedakan traffic normal dan port scanning.
4. Memberikan contoh penerapan *sliding time window* dan TTL untuk mengelola
   state analisis traffic tanpa menyimpan data lama secara tidak terbatas.
5. Menjadi referensi untuk penelitian *network security* dan *traffic analysis*.
6. Menerapkan konsep jaringan komputer, TCP, *packet analysis*, keamanan
   jaringan, dan pemrograman Python.

# 6. Tinjauan Pustaka dan Landasan Teori

## 6.1 Penelitian Terkait

Pittman (2023a) membandingkan efektivitas Nmap, ZMap, dan Masscan dengan
prosedur eksperimen yang mengukur akurasi, *false positive*, *false negative*,
dan efisiensi. Penelitian tersebut menunjukkan bahwa tool scanning dapat
menghasilkan karakteristik output yang berbeda sehingga tool dan parameter
harus didokumentasikan dalam data uji.

Pittman (2023b) menyajikan tinjauan sistematis terhadap penelitian deteksi port
scan berbasis *machine learning*. Walaupun penelitian ini tidak menggunakan
*machine learning*, tinjauan tersebut mendukung penggunaan karakteristik
traffic dan evaluasi terukur dalam penelitian deteksi port scan.

Wu et al. (2023) membahas pendeteksian *covert port scan* pada jaringan
berkecepatan tinggi. Penelitian tersebut menunjukkan bahwa port scanning dapat
memiliki pola cepat maupun lambat sehingga sistem perlu diuji pada beberapa
interval.

Scapy Project (2026) mendokumentasikan pemrosesan paket dan PCAP yang
digunakan sebagai dasar implementasi ekstraksi feature pada penelitian ini.
Nmap Project (2026) mendokumentasikan tipe dan parameter pemindaian Nmap yang
digunakan untuk membangkitkan data uji dengan *ground truth*.

Penelitian ini mengambil pendekatan *rule-based* yang lebih sederhana.
Perbedaan utamanya adalah penggabungan jumlah port unik, frekuensi koneksi,
interval koneksi, dan rasio TCP flags dalam *sliding time window*, serta
pengelolaan state menggunakan *hash table* dengan TTL.

## 6.2 Port Scanning

Port scanning adalah aktivitas pengiriman probe atau koneksi menuju sejumlah
port pada host untuk mengetahui port yang terbuka atau layanan yang tersedia.
Pada TCP SYN scan, scanner mengirim paket SYN dan mengamati respons target.
Pada TCP connect scan, scanner menyelesaikan proses koneksi TCP. Perbedaan
respons dan TCP flags dari kedua jenis scan tersebut menghasilkan variasi
traffic yang digunakan sebagai data uji.

## 6.3 Karakteristik Traffic

Karakteristik yang digunakan dalam penelitian ini adalah:

1. Source IP dan destination IP sebagai identitas sumber serta tujuan traffic.
2. Destination port unik sebagai jumlah port berbeda yang diakses dalam window.
3. Jumlah koneksi dan frekuensi koneksi sebagai ukuran intensitas traffic.
4. Interval koneksi sebagai selisih timestamp antar-koneksi dari sumber yang
   sama.
5. TCP flags, terutama SYN, SYN-ACK, ACK, dan RST.
6. Rasio flag, misalnya jumlah SYN terhadap total paket dan jumlah RST
   terhadap jumlah SYN.

## 6.4 Sliding Time Window dan Hash Table TTL

*Sliding time window* membatasi paket yang digunakan dalam evaluasi pada rentang
waktu tertentu. State dapat direpresentasikan sebagai berikut:

```text
state[(source_ip, destination_ip)] = record
```

Record menyimpan `last_seen`, `expires_at`, `unique_ports`,
`connection_count`, `last_timestamp`, serta penghitung TCP flags. *Hash table*
memberikan akses berdasarkan pasangan IP secara efisien. TTL digunakan untuk
menetapkan waktu kedaluwarsa setiap record.

Pada saat paket diproses, aplikasi melakukan langkah berikut:

1. Menghapus record yang `expires_at`-nya telah terlampaui.
2. Mengambil atau membuat record berdasarkan pasangan IP.
3. Menghapus port atau event yang timestamp-nya berada di luar window.
4. Memasukkan data paket terbaru dan memperbarui `last_seen`.
5. Mengevaluasi rule deteksi.
6. Memperbarui TTL record.

Pembersihan dilakukan secara berkala dan sebelum evaluasi paket baru. Dengan
mekanisme ini, jumlah record dibatasi oleh traffic yang masih aktif dalam
window, bukan oleh seluruh traffic sejak aplikasi dijalankan.

## 6.5 Rule-Based Detection

Suatu record diberi indikasi port scanning apabila karakteristiknya memenuhi
kombinasi aturan yang telah ditentukan. Contoh rancangan aturan:

1. Jumlah destination port unik dalam window mencapai atau melampaui threshold
   port.
2. Jumlah koneksi atau frekuensi koneksi melampaui threshold koneksi.
3. Interval antar-koneksi berada pada rentang karakteristik skenario scanning.
4. Rasio TCP flags menunjukkan pola probe, misalnya rasio SYN terhadap total
   paket atau rasio RST terhadap SYN melampaui threshold tertentu.

Nilai akhir rule dan bobot setiap indikator ditentukan melalui pengujian awal
dan dibandingkan pada beberapa nilai threshold. Hasil rule hanya dikategorikan
sebagai normal atau scanning; penelitian tidak mengklaim atribusi identitas
penyerang.

## 6.6 Packet Capture dengan Scapy

Scapy digunakan untuk menangkap paket, membaca field IP dan TCP, memfilter
paket, serta membaca atau menulis file PCAP (Scapy Project, 2026). Informasi
yang diekstraksi dari setiap paket meliputi timestamp, source IP, destination
IP, destination port, dan TCP flags.

## 6.7 Pembangkitan Data Uji dengan Nmap

Nmap digunakan untuk membangkitkan data scanning pada target uji yang
terisolasi (Nmap Project, 2026). Contoh parameter yang didokumentasikan dalam
eksperimen:

1. TCP SYN scan: `nmap -sS -p <daftar-port> <target>`.
2. TCP connect scan: `nmap -sT -p <daftar-port> <target>`.
3. Jumlah port: kelompok kecil, sedang, dan besar sesuai kapasitas lingkungan
   uji.
4. Interval dan durasi: *fast*, *medium*, dan *slow* sesuai rancangan
   skenario.

Perintah aktual, waktu mulai, waktu selesai, target, dan daftar port dicatat
bersama file PCAP. Catatan tersebut menjadi dasar validasi *ground truth*.

## 6.8 Confusion Matrix dan Metrik Evaluasi

TP adalah traffic scanning yang berhasil dideteksi sebagai scanning. TN adalah
traffic normal yang berhasil dikategorikan sebagai normal. FP adalah traffic
normal yang salah dikategorikan sebagai scanning. FN adalah traffic scanning
yang tidak terdeteksi.

Metrik yang digunakan adalah:

```text
Detection Rate      = TP / (TP + FN) × 100%
False Positive Rate = FP / (FP + TN) × 100%
False Negative Rate = FN / (FN + TP) × 100%
```

*Detection Time* adalah selisih waktu antara timestamp *ground truth* mulai
scanning dan timestamp ketika aplikasi pertama kali menghasilkan alert untuk
scanning tersebut.

# 7. Blok Diagram Sistem

Alur utama aplikasi adalah sebagai berikut:

```text
Packet Capture atau PCAP
        |
        v
Packet Filtering (IPv4 dan TCP)
        |
        v
Feature Extraction (IP, port, flags, timestamp)
        |
        v
State Manager (hash table, sliding window, TTL cleanup)
        |
        v
Rule-Based Detection Engine
        |
        +--> Alert dan Logging
        |
        v
Evaluation (ground truth, confusion matrix, metrik)
```

# 8. Metode Penelitian

Metode penelitian yang digunakan adalah eksperimen kuantitatif pada lingkungan
jaringan terisolasi. Tahapan penelitian adalah sebagai berikut:

1. Studi literatur mengenai port scanning, traffic analysis, *sliding time
   window*, *rule-based detection*, TCP flags, Scapy, dan Nmap.
2. Identifikasi karakteristik traffic port scanning dan traffic normal.
3. Perancangan struktur record, *hash table*, *sliding time window*, TTL
   cleanup, serta rule dan threshold.
4. Perancangan arsitektur aplikasi dan format logging.
5. Implementasi *packet capture* dan pembacaan PCAP menggunakan Python dan
   Scapy.
6. Implementasi filtering serta ekstraksi feature traffic.
7. Implementasi state manager dengan *hash table* dan TTL.
8. Implementasi *rule-based detection* dan pencatatan alert.
9. Pembangkitan traffic normal serta TCP SYN scan dan TCP connect scan
   menggunakan Nmap pada lingkungan yang terisolasi.
10. Pelabelan *ground truth* berdasarkan skenario, perintah, dan timestamp
    pembangkitan traffic.
11. Pengujian variasi jumlah port, interval probe, durasi scanning, jenis scan,
    dan threshold.
12. Perhitungan TP, TN, FP, FN, *Detection Rate*, *False Positive Rate*,
    *False Negative Rate*, dan *Detection Time*.
13. Analisis hasil dan penyusunan kesimpulan.

## 8.1 Rancangan Metode Penelitian

| Metode/Langkah | Input | Proses |
|---|---|---|
| Studi literatur | Jurnal, dokumentasi | Mengidentifikasi teori dan penelitian terkait |
| Perancangan rule | Karakteristik traffic | Menentukan feature, window, TTL, dan threshold |
| Perancangan sistem | Kebutuhan aplikasi | Menentukan modul dan alur |
| Packet capture | Paket jaringan/PCAP | Menangkap dan membaca paket |
| Filtering | Packet stream | Memilih IPv4 dan TCP |
| Feature extraction | Paket TCP | Mengambil IP, port, flag, dan timestamp |
| State management | Feature packet | Mengelola hash table, window, dan TTL cleanup |
| Rule detection | Traffic window | Membandingkan feature dengan threshold |
| Pembangkitan scanning | Target uji | Menjalankan Nmap `-sS`/`-sT` |
| Ground truth | Log skenario | Memberi label normal/scanning |
| Evaluation | Label dan hasil deteksi | Menghitung confusion matrix |
| Analisis | Metrik tiap skenario | Membandingkan hasil dan menarik kesimpulan |

## 8.2 Perangkat dan Tools

1. **Python** untuk implementasi aplikasi dan perhitungan evaluasi.
2. **Scapy** untuk *packet capture*, ekstraksi field, dan pengolahan PCAP.
3. **Nmap** untuk membangkitkan TCP SYN scan dan TCP connect scan.
4. **Wireshark atau tcpdump** untuk verifikasi isi PCAP dan timestamp.
5. **CSV atau SQLite** untuk menyimpan log hasil eksperimen.
6. **Draw.io** untuk menggambarkan blok diagram dan topologi pengujian.

## 8.3 Lingkungan Perangkat Lunak

1. Sistem operasi host adalah Linux Mint yang digunakan untuk menjalankan
   hypervisor, mengelola file penelitian, dan melakukan dokumentasi.
2. Hypervisor yang digunakan adalah VirtualBox atau hypervisor sejenis untuk
   membuat jaringan virtual yang terisolasi.
3. VM Scanner, VM Sensor, dan VM Target menggunakan sistem operasi Linux yang
   ditentukan sebelum eksperimen. Distribusi Linux pada VM dapat menggunakan
   Linux Mint, Ubuntu, atau distribusi lain yang kompatibel dengan Python,
   Nmap, Scapy, dan tcpdump. Distribusi serta versinya harus dicatat dalam
   laporan hasil eksperimen.
4. Python 3 dan modul `venv` digunakan untuk membuat environment aplikasi yang
   terpisah. Dependensi Python dipasang menggunakan `pip` dari berkas
   `requirements.txt`.
5. Scapy dipasang pada VM Sensor untuk membaca PCAP dan melakukan *packet
   capture*. Mode *live capture* dapat memerlukan hak administrator atau
   *capability* jaringan.
6. Nmap dipasang pada VM Scanner untuk membangkitkan TCP SYN scan dan TCP
   connect scan hanya terhadap VM Target.
7. tcpdump atau Wireshark digunakan untuk merekam dan memverifikasi paket. Tool
   yang dipilih dan versinya dicatat sebagai bagian dari konfigurasi eksperimen.
8. Git dan Visual Studio Code bersifat opsional, digunakan untuk pengelolaan
   kode sumber dan dokumentasi, bukan sebagai komponen utama sistem deteksi.

## 8.4 Skenario Pengujian

| Skenario | Kondisi |
|---|---|
| Traffic normal | Aktivitas koneksi normal tanpa pemindaian |
| Fast SYN scan | Nmap `-sS`, banyak port, interval pendek |
| Medium SYN scan | Nmap `-sS`, jumlah port dan interval sedang |
| Slow SYN scan | Nmap `-sS`, interval probe diperbesar |
| Fast connect scan | Nmap `-sT`, banyak port, interval pendek |
| Medium connect scan | Nmap `-sT`, jumlah port dan interval sedang |
| Slow connect scan | Nmap `-sT`, interval probe diperbesar |
| Threshold rendah | Menguji sensitivitas dan potensi false positive |
| Threshold sedang | Nilai threshold acuan |
| Threshold tinggi | Menguji kemungkinan false negative |

Setiap skenario dijalankan dalam beberapa pengulangan. Jumlah pengulangan,
rentang port, ukuran *sliding window*, TTL, dan nilai threshold final ditetapkan
sebelum eksperimen utama dan dicatat pada konfigurasi penelitian. Traffic normal
dan traffic scanning tidak dijalankan bersamaan pada satu eksperimen *ground
truth* agar pelabelan hasil dapat diverifikasi.

# 9. Daftar Pustaka

Nmap Project. (2026). *Nmap reference guide*.  
https://nmap.org/book/man.html

Pittman, J. M. (2023a). *A comparative analysis of port scanning tool
efficacy*. arXiv.  
https://doi.org/10.48550/arXiv.2303.11282

Pittman, J. M. (2023b). *Machine learning and port scans: A systematic review*.
arXiv.  
https://doi.org/10.48550/arXiv.2301.13581

Scapy Project. (2026). *Scapy documentation*.  
https://scapy.readthedocs.io/

Wu, H., Shao, Z., Yang, F., Cheng, G., Hu, X., Ren, J., & Wang, W. (2023).
PD-CPS: A practical scheme for detecting covert port scans in high-speed
networks. *Computer Networks, 231*, 109825.  
https://doi.org/10.1016/j.comnet.2023.109825

---

## Checklist Sebelum Dikumpulkan

1. Ganti seluruh placeholder identitas, mata kuliah, nilai, IPK, dan dosen.
2. Sesuaikan jumlah port, ukuran *sliding window*, TTL, dan jumlah pengulangan
   dengan kapasitas komputer serta topologi pengujian yang benar-benar
   digunakan.
3. Verifikasi metadata seluruh artikel melalui sumber asli dan kelola sitasi
   dengan format APA menggunakan Mendeley, Zotero, atau Word.
4. Buat gambar blok diagram dan topologi jaringan sesuai alur pada Bagian 7.
