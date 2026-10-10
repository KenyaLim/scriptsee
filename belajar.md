Kalau kamu sendiri masih merasa “SYN flood itu apa, port scanning itu buat apa, lalu penelitian saya sebenarnya berguna atau tidak?”, menurut saya jangan buru-buru mengunci judul. Kita harus mundur satu langkah dan memahami masalah jaringannya dulu.
Saya akan jelaskan seperti dosen jaringan yang sedang menguji apakah topik ini memang layak jadi skripsi.

1. Gambaran besarnya dulu
Ketiga judulmu sebenarnya berada di satu bidang:
Mendeteksi aktivitas mencurigakan dari traffic jaringan menggunakan program Python.
Bedanya adalah apa yang dideteksi.
Judul
Yang dideteksi
Pertanyaan sederhananya
1. SYN Flood
Serangan yang membanjiri server dengan paket SYN
“Apakah ada terlalu banyak permintaan koneksi TCP?”
2. Port Scanning
Aktivitas mencari port yang terbuka
“Apakah ada komputer yang sedang mencari-cari pintu masuk ke server?”
3. Port Scanning + SYN Flood
Dua aktivitas tersebut
“Bisakah satu IDS mendeteksi dua jenis perilaku jaringan?”

Jadi jangan melihatnya sebagai tiga penelitian yang sama sekali berbeda.
Judul 3 adalah gabungan judul 1 dan 2.

2. Sebelum masuk penelitian, pahami “port” dulu
Bayangkan komputer sebagai sebuah gedung.
Di gedung itu ada banyak pintu:
Komputer
│
├── Port 22  → SSH
├── Port 80  → HTTP
├── Port 443 → HTTPS
├── Port 21  → FTP
└── Port lainnya
Port adalah salah satu cara komputer menentukan layanan jaringan mana yang dituju.
Misalnya:
Laptop ────────> Server
          port 22
Artinya laptop mencoba berkomunikasi dengan layanan SSH pada server.

3. Apa itu port scanning?
Sekarang bayangkan seseorang tidak tahu pintu mana yang terbuka.
Dia mencoba:
Port 21  → terbuka?
Port 22  → terbuka?
Port 23  → terbuka?
Port 25  → terbuka?
Port 80  → terbuka?
Port 443 → terbuka?
...
Itulah konsep port scanning.
NIST mendefinisikan port scanning sebagai aktivitas untuk menentukan port mana pada sistem yang terbuka atau memungkinkan koneksi. (NIST Computer Security Resource Center)
Contohnya:
Attacker
   │
   ├──> Server:22
   ├──> Server:23
   ├──> Server:25
   ├──> Server:80
   ├──> Server:443
   └──> Server:8080
Dari hasilnya, orang tersebut bisa mengetahui:
22   OPEN
23   CLOSED
25   CLOSED
80   OPEN
443  OPEN
Berarti dia menemukan:
Server mempunyai SSH, HTTP, dan HTTPS yang dapat diakses.

4. Apakah port scanning berbahaya?
Ini bagian yang sangat penting.
Port scanning sendiri bukan berarti server sudah diretas.
Port scanning lebih tepat dianggap sebagai reconnaissance, yaitu tahap pengumpulan informasi.
Penelitian Ring dkk. menjelaskan bahwa port scan sering menjadi indikator awal sebelum serangan yang lebih serius. Mereka juga menekankan bahwa scanning itu sendiri tidak menyebabkan kerusakan langsung, tetapi dapat menjadi tahap awal serangan berikutnya. (PLOS)
Sederhananya:
Reconnaissance
      ↓
Port Scanning
      ↓
Menemukan layanan
      ↓
Mencari kelemahan
      ↓
Serangan berikutnya
Karena itu mendeteksi port scanning mempunyai nilai keamanan.

5. Lalu penelitianmu tentang port scanning sebenarnya melakukan apa?
Ini bagian yang harus benar-benar kamu pahami.
Kamu bukan membuat aplikasi untuk melakukan port scanning.
Kamu membuat aplikasi untuk:
mengamati traffic jaringan dan menentukan apakah pola traffic tersebut menunjukkan aktivitas port scanning.
Misalnya aplikasi melihat:
10.0.0.5 → Server:21
10.0.0.5 → Server:22
10.0.0.5 → Server:23
10.0.0.5 → Server:24
10.0.0.5 → Server:25
10.0.0.5 → Server:26
...
Aplikasi berpikir:
“Satu sumber mengakses banyak port tujuan dalam waktu tertentu.”
Kemudian rule kamu misalnya secara konseptual:
Jika:
1 sumber IP
mengakses ≥ X port berbeda
dalam Y detik

maka:
PORT SCANNING
Ini disebut rule-based detection.
IDS berbasis signature/rule memang bekerja dengan mencocokkan pola aktivitas dengan pola serangan yang sudah diketahui. (Springer)

6. Nah, apa itu SYN?
Sekarang masuk ke judul 1.
Sebelum memahami SYN flood, kamu harus memahami TCP handshake.
Misalnya laptop ingin membuat koneksi TCP dengan server.
Proses sederhananya:
Client                         Server

   SYN  ──────────────────────>

        <──────────────────── SYN + ACK

   ACK  ──────────────────────>
Ini disebut three-way handshake.
Sederhananya:
Client:  "Saya mau koneksi."
Server:  "Oke, saya siap."
Client:  "Oke."
Baru setelah itu komunikasi TCP berjalan.

7. Apa masalahnya dengan SYN Flood?
Sekarang bayangkan server menerima:
SYN
SYN
SYN
SYN
SYN
SYN
SYN
SYN
SYN
SYN
...
Sangat banyak permintaan koneksi.
Tetapi koneksinya tidak diselesaikan secara normal.
Secara konseptual:
Attacker                       Server

   SYN ───────────────────────>

   SYN ───────────────────────>

   SYN ───────────────────────>

   SYN ───────────────────────>

   SYN ───────────────────────>
Server menerima banyak permintaan awal.
Penelitian Bellaïche dan Grégoire menjelaskan bahwa SYN flood dapat dikenali dari anomali pada pola TCP handshake, karena pola handshake yang muncul selama serangan berbeda dari koneksi normal. (Wiley Online Library)

8. Kenapa SYN flood menjadi masalah?
Karena server harus menangani permintaan koneksi tersebut.
Secara sederhana:
Normal:

Client A ── SYN ──> Server
Client A <─ SYN/ACK
Client A ── ACK ──> Server

→ koneksi selesai
Sedangkan dalam kondisi serangan:
Banyak SYN
   ↓
Server mencoba menangani banyak koneksi
   ↓
Banyak handshake tidak selesai
   ↓
Resource server dapat terbebani
Jadi penelitianmu bukan sekadar:
“Saya menghitung paket SYN.”
Tetapi:
Saya ingin mengetahui apakah karakteristik traffic TCP dapat digunakan untuk membedakan traffic normal dengan SYN flood.
Itu jauh lebih masuk akal sebagai penelitian.

9. Jadi perbedaan SYN Flood dan Port Scanning apa?
Ini penting sekali.
Port scanning
Tujuannya mencari:
“Ada pintu apa saja yang terbuka?”
Contoh:
Attacker
   │
   ├── Server:21
   ├── Server:22
   ├── Server:23
   ├── Server:80
   └── Server:443
Ciri traffic:
Banyak port tujuan berbeda.

SYN Flood
Tujuannya bukan mencari banyak port.
Misalnya:
Attacker
   │
   ├── SYN → Server:80
   ├── SYN → Server:80
   ├── SYN → Server:80
   ├── SYN → Server:80
   ├── SYN → Server:80
   └── SYN → Server:80
Ciri yang diamati:
Banyak SYN dalam waktu tertentu dan pola handshake yang tidak normal.

10. Ini membuat ketiga judulmu lebih mudah dipahami
Judul 1
Pengembangan dan Evaluasi Aplikasi Deteksi SYN Flood Berbasis Analisis TCP Flags Menggunakan Python
Artinya:
Saya membuat program Python yang melihat paket TCP, terutama flag seperti SYN dan ACK, kemudian menentukan apakah traffic tersebut menunjukkan SYN flood.
Fokus:
TCP
 ↓
SYN / ACK
 ↓
Jumlah
 ↓
Interval waktu
 ↓
Rule
 ↓
Normal / SYN Flood

11. Judul 2
Pengembangan dan Evaluasi Aplikasi Deteksi Port Scanning Berdasarkan Karakteristik Traffic Jaringan Menggunakan Python
Artinya:
Saya membuat program Python yang mengamati traffic dan mencari pola ketika satu sumber mengakses banyak port.
Fokus:
Traffic
 ↓
Source IP
 ↓
Destination Port
 ↓
Jumlah port berbeda
 ↓
Interval waktu
 ↓
Rule
 ↓
Normal / Port Scan

12. Judul 3
Pengembangan dan Evaluasi IDS Berbasis Rule untuk Deteksi Port Scanning dan SYN Flood
Artinya:
Kamu membuat satu sistem IDS yang mempunyai dua kemampuan deteksi.
                Traffic
                    │
                    ▼
             Packet Capture
                    │
                    ▼
             Feature Extraction
                    │
            ┌───────┴───────┐
            ▼               ▼
       Rule Port        Rule SYN
       Scanning          Flood
            │               │
            └───────┬───────┘
                    ▼
                  Alert
Ini lebih terlihat sebagai sebuah aplikasi IDS, bukan sekadar program deteksi satu serangan.
Tetapi konsekuensinya:
lebih luas dan lebih sulit diuji.

13. Sekarang pertanyaan paling penting: “Apakah penelitian ini sudah pernah dilakukan?”
Ya.
Dan ini justru harus kamu terima dari awal.
Penelitian tentang:
port scanning,
SYN flood,
IDS,
rule-based detection,
TCP traffic analysis,
sudah sangat banyak.
Contohnya, penelitian SYN flood berdasarkan anomali TCP handshake sudah dilakukan Bellaïche & Grégoire. (Wiley Online Library)
Penelitian deteksi slow port scanning juga sudah dilakukan Ring dkk. dan mereka menguji metode deteksi menggunakan traffic jaringan. (PLOS)
Bahkan penelitian IDS secara umum sudah sangat luas. Survey Khraisat dkk. membahas berbagai pendekatan IDS, termasuk signature-based dan anomaly-based detection. (Springer)
Jadi kalau kamu mengatakan:
“Saya menemukan cara baru mendeteksi SYN flood.”
itu tidak benar.
Kalau kamu mengatakan:
“Saya membuat aplikasi Python untuk mendeteksi SYN flood.”
itu belum cukup kuat sebagai kontribusi penelitian.

14. Tapi penelitian yang sudah pernah dilakukan tetap bisa menjadi skripsi
Ini kesalahpahaman yang sering terjadi.
Skripsi S1 tidak harus menemukan sesuatu yang belum pernah ditemukan manusia.
Yang penting adalah kamu mempunyai:
masalah yang jelas,
metode yang jelas,
implementasi,
eksperimen,
data,
parameter,
evaluasi,
analisis hasil.
Misalnya kamu membuat detector:
Jika SYN > 100 paket/detik
→ SYN Flood
Kemudian kamu menguji:
50 SYN/s
100 SYN/s
200 SYN/s
500 SYN/s
1000 SYN/s
Lalu kamu mendapatkan:
Kondisi
Detection Rate
FPR
FNR
Normal
...
...
...
Low
...
...
...
Medium
...
...
...
High
...
...
...

Nah, di sinilah penelitianmu mulai memiliki isi.

15. Tapi saya akan mengkritik penelitianmu kalau hanya seperti itu
Kalau kamu datang sebagai mahasiswa dan berkata:
“Pak, saya membuat program Python. Kalau SYN lebih dari 100, program bilang SYN flood.”
Saya sebagai dosen akan bertanya:
“Kenapa 100?”
Kamu jawab:
“Karena saya menentukan 100.”
Saya akan bertanya lagi:
“Dasarnya apa?”
Nah.
Ini titik lemah terbesar penelitianmu saat ini.

16. Jangan sampai penelitianmu hanya menjadi IF-ELSE
Contohnya:
if syn_count > 100:
    attack = True
else:
    attack = False
Secara pemrograman memang bekerja.
Tetapi secara penelitian, saya akan bertanya:
Apa dasar threshold 100?
Kalau tidak ada dasar, penelitianmu menjadi terlalu sederhana.

17. Supaya menjadi penelitian, threshold harus menjadi bagian dari eksperimen
Misalnya kamu tidak langsung mengatakan:
threshold = 100
Tetapi kamu melakukan eksperimen.
Misalnya:
Traffic normal
       ↓
ambil baseline
       ↓
uji beberapa threshold
       ↓
50
100
150
200
250
       ↓
ukur:
Detection Rate
False Positive Rate
False Negative Rate
Detection Time
Barulah kamu dapat mengatakan:
“Pada lingkungan pengujian ini, perubahan threshold memengaruhi kemampuan deteksi dan false alarm.”
Itu lebih ilmiah.

18. Hal yang sama berlaku untuk port scanning
Jangan hanya:
if unique_ports > 10:
    scan = True
Dosen akan bertanya:
“Kenapa 10?”
Lebih baik:
5 port
10 port
20 port
30 port
50 port
100 port
Kemudian lihat bagaimana detector bekerja.
Bahkan kamu bisa menguji:
Fast scan
↓
banyak port dalam waktu singkat

Slow scan
↓
sedikit port
tetapi dilakukan perlahan
Ini justru menarik karena penelitian tentang slow port scanning menunjukkan bahwa scanning yang dilakukan perlahan memang lebih sulit dideteksi dibanding pola yang lebih jelas. (PLOS)

19. Nah, apakah port scanning berguna?
Ya, secara keamanan jaringan memang berguna untuk dideteksi.
Karena port scanning dapat menjadi tahap awal sebelum aktivitas serangan berikutnya. (PLOS)
Bayangkan IDS kamu memberikan:
[ALERT]

Source:
192.168.1.20

Destination:
192.168.1.10

Ports accessed:
22
23
25
53
80
110
139
443
...

Classification:
PORT SCANNING
Administrator jaringan mendapatkan informasi:
“Ada host yang sedang melakukan reconnaissance terhadap server saya.”
Jadi nilai praktisnya bukan:
“Port scanning merusak server.”
Tetapi:
“Port scanning dapat memberikan indikasi awal adanya aktivitas reconnaissance.”

20. Apakah SYN Flood berguna untuk diteliti?
Juga ya.
Karena kamu dapat mengamati hubungan:
Jumlah SYN
      ↓
Interval waktu
      ↓
Pola handshake
      ↓
Kemampuan detector
Penelitian terdahulu memang sudah menggunakan karakteristik handshake TCP untuk mendeteksi SYN flooding. (Wiley Online Library)
Jadi masalahnya bukan:
“Apakah SYN flood penting?”
Jawabannya jelas penting.
Masalah penelitianmu adalah:
“Apa yang sebenarnya ingin saya evaluasi?”

21. Kalau saya menjadi dosen pembimbingmu, saya akan meminta kamu menentukan kontribusi
Ada perbedaan antara:
Implementasi
Saya membuat aplikasi Python untuk mendeteksi SYN flood.
dengan:
Penelitian
Saya mengevaluasi kemampuan deteksi aplikasi rule-based terhadap variasi karakteristik traffic SYN flood berdasarkan perubahan intensitas traffic dan threshold.
Yang kedua jauh lebih layak menjadi skripsi.

22. Jadi sebenarnya “produk” dan “penelitian” kamu berbeda
Ini konsep yang harus kamu pegang.
Produk
Python IDS
Penelitian
Bagaimana performa IDS tersebut
ketika menghadapi kondisi traffic yang berbeda?
Produk adalah alat.
Penelitian adalah eksperimen terhadap alat tersebut.

23. Contoh penelitian yang lebih konkret
Misalnya kamu mengambil judul 1.
Aplikasi
Python + Scapy
Aplikasi melakukan:
Capture packet
      ↓
Filter TCP
      ↓
Ambil TCP flags
      ↓
Hitung SYN
      ↓
Hitung ACK
      ↓
Analisis interval
      ↓
Rule
      ↓
Normal / SYN Flood
Scapy memang menyediakan kemampuan untuk menangkap dan menganalisis paket serta mengakses informasi protokol jaringan dari Python.

24. Kemudian kamu membuat skenario
Skenario A: normal
Client
  ↓
Server

Traffic TCP normal
Skenario B: SYN flood rendah
Traffic attack rendah
Skenario C: SYN flood sedang
Traffic attack sedang
Skenario D: SYN flood tinggi
Traffic attack tinggi
Kemudian aplikasi mencatat:
timestamp
source IP
destination IP
source port
destination port
TCP flags
jumlah SYN
jumlah ACK
status deteksi

25. Setelah itu baru kamu bicara Detection Rate
Misalnya ground truth kamu sudah diketahui karena setiap eksperimen kamu sendiri yang menentukan:
Scenario 1 = NORMAL
Scenario 2 = SYN FLOOD
Scenario 3 = SYN FLOOD
Kemudian aplikasi menghasilkan:
Actual             Detection

Normal             Normal
Normal             Attack
Attack             Attack
Attack             Normal
Dari sini muncul:
TP
TN
FP
FN
Kemudian:
Detection Rate / TPR
DR=TPTP+FN×100%DR = \frac{TP}{TP+FN}\times100\%
False Positive Rate
FPR=FPFP+TN×100%FPR = \frac{FP}{FP+TN}\times100\%
False Negative Rate
FNR=FNFN+TP×100%FNR = \frac{FN}{FN+TP}\times100\%
Ini jauh lebih kuat daripada hanya menunjukkan:
“Program saya berhasil mendeteksi serangan.”

26. Sekarang saya kritik ketiga judulmu
Judul 1: SYN Flood
Kelebihan:
Fokus jelas.
Materi jaringan jelas.
Kamu bisa belajar TCP secara mendalam.
Variabel traffic cukup banyak.
Eksperimen relatif mudah dikontrol.
Tidak perlu ML.
Cocok untuk aplikasi Python.
Kekurangan:
Sudah banyak penelitian.
Kalau hanya menghitung SYN, terlalu sederhana.
Threshold harus memiliki dasar.
Harus hati-hati membedakan SYN flood dengan traffic TCP normal yang tinggi.
Penilaian saya sebagai dosen:
Layak, tetapi metodologinya harus dibuat serius.

27. Judul 2: Port Scanning
Kelebihan:
Sangat jelas hubungannya dengan network security.
Konsepnya mudah dipahami.
Mudah divisualisasikan.
Bisa menguji fast scan dan slow scan.
Bisa menggunakan karakteristik traffic.
Ada masalah penelitian yang menarik karena slow scan lebih sulit dideteksi. (PLOS)
Kekurangan:
Kalau hanya menghitung jumlah port, terlalu sederhana.
Threshold kembali menjadi masalah.
Port scanning sudah sangat banyak diteliti.
Harus menentukan jenis scanning yang benar-benar diuji.
Penilaian saya:
Layak, bahkan cukup menarik untuk mahasiswa jaringan jika eksperimennya dirancang dengan baik.

28. Judul 3: Port Scanning + SYN Flood
Ini paling terlihat seperti:
“Saya membuat IDS.”
Tetapi saya akan lebih banyak bertanya.
Misalnya:
Bagaimana menentukan rule port scan?
Bagaimana menentukan rule SYN flood?
Apakah performanya berbeda?
Bagaimana jika dua traffic terjadi bersamaan?
Bagaimana sistem membedakan keduanya?
Bagaimana kalau traffic normal meningkat?
Apakah false positive meningkat?
Artinya:
Judul 1
1 masalah utama

Judul 2
1 masalah utama

Judul 3
2 masalah utama
Untuk skripsi S1, lebih luas bukan otomatis lebih baik.

29. Kalau saya menjadi dosenmu, saya justru tidak akan menyuruhmu langsung mengambil judul 3
Saya akan bilang:
Pilih satu dulu dan lakukan dengan benar.
Karena kamu mengatakan sendiri bahwa kamu masih memahami konsep dasarnya.
Kalau langsung:
IDS
+
Port Scanning
+
SYN Flood
+
Python
+
Rule
+
Detection Rate
+
FPR
+
FNR
kamu berisiko membuat penelitian yang terlihat besar tetapi sebenarnya dangkal.

30. Saya lebih menyarankan kamu memahami pilihan ini
Kalau kamu ingin belajar TCP lebih dalam:
Judul 1: SYN Flood
Kamu akan banyak belajar:
TCP
SYN
ACK
RST
Three-way handshake
Connection state
Packet rate
Time window

Kalau kamu ingin lebih fokus pada traffic analysis:
Judul 2: Port Scanning
Kamu akan banyak belajar:
Source IP
Destination IP
Destination Port
Connection
TCP flags
Distinct ports
Time window
Fast scan
Slow scan

Kalau kamu ingin membangun IDS yang lebih lengkap:
Judul 3
Tetapi saya menyarankan ini setelah kamu benar-benar memahami dua konsep sebelumnya.

31. Apakah penelitianmu “sudah ada”?
Topiknya sudah ada.
Tapi itu bukan masalah utama.
Yang harus kamu cari adalah:
“Apa yang belum saya evaluasi atau bagaimana saya membuat eksperimen yang berbeda dan terukur?”
Misalnya penelitian terdahulu sudah membahas:
SYN flood detection
Kamu tidak perlu mengklaim:
“Saya menemukan metode baru.”
Kamu dapat mengambil posisi:
“Saya mengembangkan implementasi rule-based berbasis Python dan mengevaluasi performanya pada beberapa variasi traffic dan threshold dalam lingkungan pengujian terkontrol.”
Itu klaim yang jauh lebih aman.

32. Dan ini menurut saya justru cocok dengan kondisi kamu
Kamu sebelumnya mengatakan tidak ingin:
Machine Learning
Deep Learning
penelitian terlalu berat
terlalu banyak infrastructure
terlalu jauh dari jaringan
Maka:
Python
   ↓
Packet Capture
   ↓
Traffic Analysis
   ↓
Rule
   ↓
Detection
   ↓
Experiment
   ↓
Detection Rate
memang cukup masuk akal.
Kamu tetap mengerjakan networking, tetapi produknya berupa aplikasi Python.

33. Tapi ada satu perubahan cara berpikir yang saya minta
Jangan berpikir:
“Saya harus membuat aplikasi yang hebat.”
Berpikir:
“Saya harus membuat eksperimen yang bisa membuktikan sesuatu tentang aplikasi saya.”
Misalnya:
Pertanyaan penelitian
Bagaimana pengaruh threshold terhadap kemampuan deteksi SYN flood?
Kemudian:
Threshold
50
100
150
200
250
diuji.
Hasil:
Threshold → Detection Rate
Threshold → FPR
Threshold → FNR
Itulah penelitian.

34. Kalau saya harus menyaring sekarang
Dengan mempertimbangkan kamu masih belajar konsep jaringan, saya akan membuat urutan seperti ini:
Pilihan A
SYN Flood
Cocok kalau kamu ingin memahami TCP secara mendalam.
Pilihan B
Port Scanning
Cocok kalau kamu lebih tertarik menganalisis pola traffic.
Pilihan C
Keduanya sebagai IDS
Cocok kalau kamu sudah memahami A dan B dan ingin membuat sistem lebih lengkap.
Saya tidak menyarankan langsung mengunci C hanya karena judulnya terlihat lebih besar.

35. Yang paling penting sebelum kita lanjut proposal
Sebelum menulis ulang proposal, menurut saya kamu perlu benar-benar menguasai dua cerita sederhana ini:
Cerita SYN Flood
TCP ingin membuat koneksi
        ↓
SYN
        ↓
SYN/ACK
        ↓
ACK
        ↓
Koneksi

SYN Flood:
banyak SYN
        ↓
handshake tidak normal
        ↓
server menerima banyak permintaan
        ↓
detector mencari pola tersebut
Cerita Port Scanning
Attacker ingin mengetahui layanan
        ↓
mencoba banyak port
        ↓
22
23
25
53
80
443
...
        ↓
muncul pola traffic
        ↓
detector mengidentifikasi pola
        ↓
PORT SCANNING
Kalau dua alur itu sudah kamu bisa jelaskan dengan kata-katamu sendiri tanpa menghafal, baru kita bisa menentukan judul yang paling masuk akal dan menyusun variabel, skenario eksperimen, threshold, data yang dikumpulkan, TP/TN/FP/FN, serta kontribusi penelitiannya.

