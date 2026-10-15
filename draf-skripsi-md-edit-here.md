Rancang Bangun Aplikasi Deteksi Rogue DHCP dan Evil Twin AP pada WLAN Berbasis Python


Proposal Tugas Akhir Skripsi





Diajukan oleh:
KENYA SYALWA ARIFIA
71231025




PROGRAM STUDI INFORMATIKA
FAKULTAS TEKNOLOGI INFORMASI
UNIVERSITAS KRISTEN DUTA WACANA
YOGYAKARTA
2026

Rancang Bangun Aplikasi Deteksi Rogue DHCP dan Evil Twin AP pada WLAN Berbasis Python

Mata kuliah pendukung
:
1. [Tuliskan mata kuliah pendukung yang sudah diambil]
[Nilai]




2. [Jika Ada]
[Nilai]








Mata kuliah wajib profil
:
1. [Tuliskan daftar mata kuliah wajib profil yang sudah diambil]
[Nilai]




2. [Jika Ada]
[Nilai]








Profesi Lulusan
:
[ PSD / AI / DMS / NI ] *) pilih



		


NIM
:
71231025
Nama Lengkap
:
Kenya Syalwa Arifia
IPK
:
3.18
No. HP
:
081239816129
Email
:
kenyasyalwa@ti.ukdw.ac.id




Proposal ini diajukan dalam seminar kolokium sebagai persyaratan untuk memulai penulisan skripsi.	

Proposal Desk Evaluation [I/II]
Semester Gasal 2026/2027
2026
HALAMAN PERSETUJUAN PROPOSAL





Pada tanggal ………..

Proposal dengan keterangan:
NIM			: 71231025
JUDUL PROPOSAL	: [JUDUL PROPOSAL]
Telah disetujui oleh:






Calon Dosen Pembimbing 1
Calon Dosen Pembimbing 2







Nama Lengkap Dosen
Nama Lengkap Dosen

1. Latar Belakang
Jaringan nirkabel (Wireless Local Area Network/WLAN) kini menjadi cara utama perangkat seperti laptop dan ponsel pintar terhubung ke internet, baik di rumah, kampus, perkantoran, maupun tempat umum. Kemudahan ini datang bersama risiko. Sinyal nirkabel merambat di udara dan dapat diterima siapapun dalam jangkauannya, sehingga penyerang bisa mengamati bahkan menyusup ke komunikasi tanpa perlu akses fisik ke kabel jaringan. Karena itu, keamanan pada lapisan akses jaringan perlu mendapat perhatian khusus.
Salah satu ancaman yang paling sering dibahas adalah evil twin access point (AP), yaitu AP palsu yang meniru AP sah dengan menyamakan SSID dan, pada beberapa kasus, alamat MAC. Penyerang dapat memanfaatkan evil twin untuk memalsukan pesan dan menyadap komunikasi pengguna (Seo et al., 2020). Evil twin sulit dikenali karena tampilannya hampir sama dengan AP sah. Studi eksperimen pada jaringan Wi-Fi kampus menunjukkan ancaman ini nyata. Asiana et al. (2025) menguji 13 lokasi di kampus dengan perangkat NodeMCU ESP8266 dan menemukan 5 lokasi (38,46%) rentan, yaitu pengguna terarah ke SSID palsu dan memasukkan kredensial. Serangan juga terus berkembang. Louca et al. (2023) menunjukkan evil twin dapat diperkuat dengan memanfaatkan mekanisme protokol 802.11v, sehingga pertahanan yang hanya mengandalkan nama jaringan semakin tidak memadai.
Berbagai pendekatan deteksi evil twin sudah dikembangkan. Seo et al. (2020) memakai klasifikasi pembelajaran mesin dengan banyak fitur, Tian et al. (2021) memakai convolutional neural network, dan Banakh et al. (2024) memakai pendekatan data mining. Pendekatan tersebut menjanjikan, tetapi umumnya membutuhkan data latih, pengolahan yang kompleks, atau perangkat tertentu. Di sisi lain, deteksi berbasis skrip Python seperti Snappy menunjukkan bahwa pemindaian dan fingerprinting AP dapat dilakukan dengan alat yang ringan (“Rogue Wifi AP detection with Snappy”, 2024).
Ancaman kedua berada pada layanan Dynamic Host Configuration Protocol (DHCP). DHCP memberikan alamat IP, gateway, dan DNS secara otomatis kepada klien. Karena klien dapat menerima pesan DHCPOFFER dari lebih dari satu server, penyerang mudah memasang rogue DHCP server di jaringan WLAN (Wachira, 2021). Server palsu ini dapat membagikan alamat IP, DNS, dan informasi routing yang salah, sehingga lalu lintas korban dapat dialihkan atau disadap (Makarova & Maksutov, 2021). Rogue DHCP juga dapat memicu serangan man-in-the-middle (MITM). Penelitian lain menunjukkan bahwa pengecekan alamat IP server saja dapat dikelabui lewat pemalsuan IP, sehingga perlu dikombinasikan dengan pemeriksaan alamat MAC (“An effective technique to automatically detect and neutralize rogue DHCP server”, 2023). Pengamanan umum seperti DHCP snooping dan DHCP alert efektif, tetapi bergantung pada konfigurasi perangkat jaringan terkelola (“The DHCP snooping and DHCP alert method”, 2021). Perangkat semacam itu tidak selalu ada di jaringan kecil, rumah, atau kampus dengan anggaran terbatas.
Kedua serangan ini sering saling berkaitan. Penyerang yang memasang evil twin biasanya juga menjalankan layanan DHCP sendiri supaya korban mendapat IP, gateway, dan DNS yang dikendalikan penyerang. Namun, penelitian yang ada cenderung membahas keduanya secara terpisah, yaitu evil twin pada lapisan 802.11 dan rogue DHCP pada lapisan jaringan. Belum banyak alat sederhana yang menggabungkan kedua deteksi dalam satu aplikasi yang dapat dijalankan administrator jaringan tanpa bergantung pada fitur perangkat jaringan terkelola.
Selain itu, jaringan WLAN di kampus dan perkantoran pada praktiknya tidak hanya terdiri dari satu AP. Jaringan tersebut umumnya memakai topologi seamless wireless, yaitu banyak AP yang dikelola oleh satu wireless controller dan memancarkan SSID serta pengaturan keamanan yang sama, sehingga klien dapat berpindah (roaming) antar-AP tanpa memutus koneksi. Pada topologi ini, SSID yang sama bukan tanda AP palsu karena seluruh AP sah memang menggunakan SSID tersebut. Deteksi evil twin menjadi lebih sulit dan risiko AP sah salah ditandai sebagai palsu (false positive) meningkat.
Berdasarkan hal tersebut, penelitian ini merancang dan membangun aplikasi berbasis Python untuk mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP berbasis wireless controller. Python dipilih karena memiliki pustaka manipulasi paket seperti Scapy, bersifat lintas platform, dan mudah dikembangkan. Pengujian dilakukan di Laboratorium D yang mensimulasikan satu wireless controller dengan 10 AP secara seamless. Perangkat penyerang dan klien sah dibuat bervariasi, tidak hanya satu laptop dan satu ponsel.
2. Rumusan Masalah
1. Bagaimana merancang dan membangun aplikasi berbasis Python yang dapat mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP?
2. Bagaimana cara aplikasi mengidentifikasi rogue DHCP server berdasarkan analisis pesan DHCP (DISCOVER, OFFER, REQUEST, ACK) dibandingkan daftar server sah?
3. Bagaimana cara aplikasi mengidentifikasi evil twin AP pada jaringan ber-SSID sama berdasarkan perbandingan atribut AP seperti BSSID, kanal, jenis enkripsi, dan kekuatan sinyal (RSSI) terhadap daftar AP sah tanpa menandai AP sah sebagai palsu?
4. Seberapa baik kinerja aplikasi yang dikembangkan dalam mendeteksi kedua serangan tersebut berdasarkan parameter akurasi, precision, recall, false positive rate, dan waktu deteksi?
3. Batasan Masalah
1. Pengujian dilakukan pada topologi seamless wireless di Laboratorium D, yaitu satu wireless controller yang mengelola 10 AP dengan SSID dan pengaturan keamanan yang sama. Laptop pendeteksi dapat ditempatkan di beberapa titik, sedangkan perangkat penyerang dan perangkat klien sah terdiri dari lebih dari satu perangkat dengan tipe yang bervariasi.
2. Aplikasi dikembangkan menggunakan bahasa pemrograman Python dan hanya berfokus pada deteksi dan peringatan (alert), bukan pencegahan aktif, pemblokiran, atau serangan balik.
3. Jenis serangan yang dideteksi hanya rogue DHCP server dan evil twin AP; serangan lain seperti DHCP starvation, deauthentication flood, ARP spoofing, dan captive portal phishing tidak dibahas.
4. Pengujian dilakukan di Laboratorium D dengan izin pengelola laboratorium dan pada jaringan yang terisolasi dari jaringan produksi. Pengujian tidak dilakukan pada jaringan publik atau milik pihak lain.
5. Aplikasi bekerja pada jaringan IPv4; DHCPv6 tidak dibahas.
6. Pengujian terbatas pada pita frekuensi dan standar WLAN yang didukung oleh adapter nirkabel yang digunakan serta oleh perangkat controller dan AP di Laboratorium D.
7. Hasil penelitian berlaku untuk konfigurasi Laboratorium D [sebutkan merek dan tipe controller dan AP setelah dikonfirmasi] dan belum diuji pada merek atau skala jaringan lain.
8. Penelitian ini tidak membahas keamanan sistem aplikasi itu sendiri, misalnya enkripsi log atau autentikasi pengguna aplikasi.
4. Tujuan Penelitian
1. Merancang dan membangun aplikasi berbasis Python yang mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP.
2. Mengimplementasikan mekanisme deteksi rogue DHCP server melalui pengiriman paket DHCPDISCOVER dan analisis seluruh DHCPOFFER yang diterima terhadap daftar server sah (whitelist).
3. Mengimplementasikan mekanisme deteksi evil twin AP melalui pemindaian AP di sekitar dan analisis ketidakkonsistenan atribut AP, terutama BSSID, kanal, dan enkripsi, terhadap whitelist seluruh AP sah.
4. Mengevaluasi kinerja aplikasi menggunakan parameter akurasi, precision, recall, false positive rate, dan waktu deteksi pada skenario serangan simulasi.

5. Manfaat Penelitian
1. Memperkuat jaringan internal. Aplikasi memberi administrator gambaran kondisi jaringan: AP mana yang sah dan mana yang mencurigakan, serta server DHCP mana yang berwenang. Dengan deteksi dini terhadap AP palsu dan DHCP server palsu, celah pada lapisan akses dapat segera diketahui dan ditutup, sehingga konfigurasi jaringan (alamat IP, gateway, dan DNS) tetap berasal dari sumber yang sah. Dengan begitu jaringan internal menjadi lebih andal dan terkelola.
2. Mencegah adanya penyusup. Peringatan dini dari aplikasi memungkinkan tindakan sebelum penyerang sempat mengalihkan lalu lintas atau mencuri data. Administrator dapat menelusuri perangkat mencurigakan, mengganti kredensial, atau memutus perangkat tersebut dari jaringan. Dengan demikian risiko penyadapan, pencurian kredensial, dan serangan lanjutan seperti MITM dapat ditekan.
3. Bagi peneliti: menambah pemahaman tentang protokol DHCP, standar IEEE 802.11, dan teknik analisis paket dengan Python.
4. Bagi pengguna jaringan: meningkatkan kewaspadaan terhadap risiko terhubung ke jaringan palsu dan penyadapan data pribadi.
5. Bagi penelitian selanjutnya: menjadi dasar pengembangan sistem yang lebih lengkap, misalnya pencegahan aktif, deteksi serangan lain, atau penerapan pembelajaran mesin.
6. Tinjauan Pustaka dan Landasan Teori
6.1. Tinjauan Pustaka
Makarova dan Maksutov (2021) mengembangkan metode untuk mendeteksi rogue DHCP server dan memberikan perlindungan aktif pada host berbasis GNU/Linux. Mereka menjelaskan bahwa server DHCP tidak sah dapat bersaing dengan server sah dan membagikan alamat IP, DNS, serta informasi routing yang salah kepada klien. Penelitian ini relevan sebagai dasar mekanisme deteksi DHCP, tetapi tidak berfokus pada lingkungan WLAN.
Wachira (2021) merancang intrusion detection system (IDS) khusus untuk mendeteksi rogue DHCP server pada komunikasi WLAN dengan memantau dan menganalisis pesan transaksi DHCP. Pengujian pada jaringan yang berisi server sah dan palsu menunjukkan semua alamat IP yang ditawarkan server palsu berhasil terdeteksi (tingkat deteksi 100%). Penelitian ini menjadi acuan utama untuk analisis pesan DHCP pada penelitian ini.
Penelitian di Indonesia pada jurnal IJID menerapkan DHCP Snooping dan DHCP Alert untuk mengamankan server DHCP dari serangan rogue DHCP. DHCP Alert memantau proses DORA sehingga hanya terjadi antara server sah dan klien ("The DHCP Snooping and DHCP Alert Method", 2021). Pendekatan ini bergantung pada perangkat jaringan terkelola, sehingga penelitian ini mengambil pendekatan berbasis aplikasi yang tidak memerlukan konfigurasi perangkat tersebut.
Pada sisi evil twin, Seo et al. (2020) mengusulkan metode deteksi evil twin AP berbasis klasifikasi pembelajaran mesin dengan banyak fitur, dan melaporkan akurasi 100% dengan algoritma random forest. Penelitian ini memperlihatkan bahwa evil twin dapat meniru SSID dan alamat MAC, sehingga pemeriksaan satu atribut saja tidak cukup.
Penelitian terbaru berjudul Rogue Wi-Fi AP detection with Snappy (2024) membahas skrip Python bernama Snappy yang dirancang untuk melakukan sidik jari dan mendeteksi AP Wi-Fi palsu, serta menjelaskan konsep mode monitor dan penggunaan Scapy. Penelitian ini mendukung pemilihan Python dan Scapy sebagai dasar pengembangan aplikasi.
Berdasarkan penelusuran tersebut, penelitian terdahulu umumnya membahas rogue DHCP dan evil twin secara terpisah. Kontribusi penelitian ini adalah menggabungkan kedua deteksi dalam satu aplikasi Python yang dapat dijalankan dengan perangkat sederhana (laptop dan ponsel).

Tabel 1. Perbandingan Penelitian Terkait
No.
Peneliti (Tahun)
Fokus
Metode
Perbedaan dengan Penelitian Ini
1
Makarova & Maksutov (2021)
Rogue DHCP server
Deteksi dan perlindungan host pada GNU/Linux
Tidak fokus WLAN; tidak mencakup evil twin
2
Wachira (2021)
Rogue DHCP pada WLAN
IDS berbasis analisis pesan DHCP
Hanya DHCP; tidak mencakup evil twin
3
IJID (2021)
Rogue DHCP
DHCP Snooping dan DHCP Alert
Bergantung pada perangkat jaringan terkelola
4
Seo et al. (2020)
Evil twin AP
Pembelajaran mesin dengan fitur clock skew
Hanya evil twin; tidak mencakup DHCP
5
Snappy (2024)
Rogue Wi-Fi AP
Skrip Python untuk fingerprinting AP
Hanya sisi AP; tidak mencakup DHCP
6
Penelitian ini
Rogue DHCP dan evil twin
Aplikasi Python (Scapy) berbasis laptop dan ponsel
Menggabungkan kedua deteksi dalam satu aplikasi

Sebagaimana terlihat pada Tabel 1, belum ada penelitian pada daftar tersebut yang menggabungkan kedua deteksi dalam satu aplikasi.
6.2. Landasan Teori
a. Wireless Local Area Network (WLAN). WLAN adalah jaringan lokal nirkabel berbasis standar IEEE 802.11. Komunikasi antara klien dan AP dilakukan melalui frame manajemen (misalnya beacon, probe request/response, authentication, association), frame kontrol, dan frame data. Beacon frame dikirim AP secara berkala dan memuat informasi seperti SSID, BSSID, kanal, dan jenis enkripsi.
b. Evil Twin AP. Evil twin adalah AP palsu yang menyamar sebagai AP sah dengan meniru SSID dan kadang MAC address (Seo et al., 2020). Ciri yang dapat dibandingkan dengan AP sah meliputi: (1) satu SSID dengan BSSID yang tidak terdaftar, (2) kanal yang berbeda, (3) jenis enkripsi yang lebih lemah atau terbuka, (4) RSSI yang berbeda dari profil normal, dan (5) vendor OUI pada BSSID yang tidak sesuai.
c. DHCP dan Rogue DHCP Server. DHCP menyediakan konfigurasi jaringan otomatis melalui proses DORA: Discover, Offer, Request, Acknowledge. Karena klien dapat menerima OFFER dari lebih dari satu server, penyerang dapat memasang server palsu yang membagikan konfigurasi berbahaya (Wachira, 2021; Makarova & Maksutov, 2021). Rogue DHCP dikenali dari Server Identifier, alamat IP/MAC pengirim, serta isi gateway dan DNS pada OFFER yang tidak sesuai dengan data server sah.
d. Python dan Scapy. Scapy adalah pustaka Python untuk membuat, mengirim, dan menganalisis paket jaringan, termasuk layer 802.11 (Dot11Beacon, Dot11ProbeReq) dan DHCP. Pustaka ini juga dipakai pada penelitian deteksi AP palsu ('Rogue Wi-Fi AP detection with Snappy', 2024).
e. Mode Monitor. Mode monitor memungkinkan adapter nirkabel menangkap seluruh frame 802.11 di udara tanpa harus terhubung ke jaringan ('Rogue Wi-Fi AP detection with Snappy', 2024). Tidak semua adapter bawaan laptop mendukung mode ini, sehingga penelitian ini menyiapkan dua mode: (1) mode monitor jika didukung, dan (2) pemindaian jaringan biasa (managed mode) melalui perintah sistem operasi jika tidak didukung.
f. Metrik Evaluasi. Kinerja deteksi dihitung menggunakan confusion matrix (TP, TN, FP, FN), false positive rate, dan waktu deteksi:
Akurasi = (TP + TN) / (TP + TN + FP + FN) [1]
Precision = TP / (TP + FP) [2]
Recall = TP / (TP + FN) [3]
False positive rate = FP / (FP + TN) [4]
TP adalah serangan yang terdeteksi dengan benar, TN adalah kondisi normal yang tidak diberi peringatan, FP adalah peringatan palsu, dan FN adalah serangan yang tidak terdeteksi. Persamaan 1 digunakan untuk menilai ketepatan keseluruhan, Persamaan 2 untuk menilai ketepatan peringatan, Persamaan 3 untuk menilai kemampuan menangkap serangan, dan Persamaan 4 untuk menilai proporsi kondisi normal yang salah diberi peringatan.

7. Blok Diagram Sistem
Gambaran besar sistem terdiri dari tiga bagian: lingkungan pengujian, modul aplikasi, dan keluaran.
Lingkungan pengujian: satu wireless controller mengelola 10 AP sah dengan SSID dan pengaturan keamanan yang sama. Laptop menjalankan aplikasi deteksi dan dapat ditempatkan di beberapa titik. Beberapa perangkat klien sah digunakan untuk menguji roaming, sedangkan ponsel atau laptop berperan sebagai penyerang simulasi dengan mengaktifkan AP ber-SSID sama dan/atau menjalankan layanan DHCP sebagai rogue server.

Gambar 1. Diagram Umum
Alur umum sistem:
Pengguna menjalankan aplikasi dan menetapkan profil seluruh AP sah (SSID, BSSID, kanal, enkripsi, IP server DHCP, dan IP gateway) sebagai whitelist.
Modul Pemindai WLAN memindai AP di sekitar dan mengumpulkan atribut SSID, BSSID, kanal, enkripsi, dan RSSI.
Modul Deteksi Evil Twin membandingkan hasil pindaian dengan profil sah dan menandai AP yang mencurigakan.
Modul Deteksi Rogue DHCP mengirim DHCPDISCOVER (Scapy), mengumpulkan semua DHCPOFFER selama jangka waktu tertentu, lalu membandingkan Server Identifier, IP, dan MAC pengirim dengan whitelist.
Modul Pelaporan menampilkan peringatan (alert) pada antarmuka dan menyimpan log (waktu, jenis serangan, bukti).
Pengguna meninjau hasil dan log.
Diagram khusus per modul:
Evil twin: Mulai → pindai AP → kelompokkan berdasarkan SSID → periksa setiap BSSID pada whitelist → jika tidak terdaftar, bandingkan kanal, enkripsi, dan RSSI sebagai indikator pendukung → jika mencurigakan maka peringatan evil twin, jika sesuai maka normal → catat log.
Rogue DHCP: Mulai → kirim DHCPDISCOVER → tunggu semua DHCPOFFER → bandingkan Server Identifier, IP, dan MAC dengan whitelist → jika tidak terdaftar atau memberikan konfigurasi berbeda maka peringatan rogue DHCP, jika terdaftar maka normal → catat log.

Gambar 2. Diagram Deteksi Evil Twin

Gambar 3. Diagram Deteksi Rogue DHCP
8. Metode Penelitian
Penelitian ini menggunakan pendekatan eksperimental dengan pengembangan aplikasi secara bertahap.
1. Studi literatur: mempelajari WLAN 802.11, arsitektur wireless controller dan roaming, DHCP, evil twin, rogue DHCP, serta penggunaan Python dan Scapy.
2. Analisis kebutuhan: menentukan kebutuhan fungsional (pemindaian, deteksi, pelaporan, log) dan kebutuhan perangkat (laptop pendeteksi, adapter nirkabel, perangkat penyerang, dan beberapa perangkat klien).
3. Observasi lingkungan Laboratorium D: mencatat merek dan tipe controller dan AP, penempatan 10 AP, kanal, jenis enkripsi, serta pengaturan VLAN dan DHCP. Seluruh BSSID sah dikumpulkan saat jaringan dalam kondisi bersih sebagai baseline (whitelist).
4. Perancangan sistem: merancang arsitektur aplikasi, alur deteksi berbasis whitelist multi-BSSID, dan antarmuka (CLI atau GUI sederhana).
5. Implementasi: membangun aplikasi dengan Python dan Scapy.
6. Pilot testing: melakukan pengujian awal pada 2 sampai 3 AP untuk memvalidasi adapter, skenario serangan, parameter pemindaian, dan prosedur pencatatan.
7. Pembangunan skenario pengujian utama: menyiapkan skenario normal dan serangan pada seluruh 10 AP dengan variasi lokasi dan perangkat.
8. Pengujian utama: menjalankan seluruh skenario dengan pengulangan.
9. Evaluasi: menghitung akurasi, precision, recall, false positive rate, dan waktu deteksi.
10. Penyusunan laporan: menarik kesimpulan dan saran.

8.1. Pilot Testing
Pilot testing dilakukan sebelum pengujian utama pada 2 sampai 3 AP di bawah wireless controller yang sama. Tahap ini bertujuan memastikan adapter nirkabel yang digunakan mendukung mode monitor atau managed mode, memastikan eksekusi Python dan Scapy berjalan, memvalidasi pembentukan evil twin dan rogue DHCP, serta menentukan interval pemindaian dan batas waktu tunggu DHCPOFFER. Data pilot digunakan untuk memperbaiki aplikasi dan menetapkan prosedur, tetapi tidak dimasukkan ke hasil pengujian utama.

8.2. Skenario Pengujian Utama
Pengujian utama dilakukan pada seluruh 10 AP dengan variasi lokasi laptop pendeteksi, lokasi penyerang, jumlah klien, dan tipe perangkat klien. Skenario yang digunakan adalah:

S0: kondisi normal tanpa serangan, dengan klien berpindah (roaming) antar-AP, untuk mengukur false positive pada AP sah ber-SSID sama.

S1: rogue DHCP pada jaringan yang sama untuk menguji deteksi server DHCP tidak sah.

S2: evil twin dengan SSID sama, BSSID berbeda, dan enkripsi terbuka.

S3: evil twin dengan SSID sama, BSSID berbeda, dan enkripsi sama dengan jaringan sah.

S4: evil twin dengan SSID dan BSSID dikloning untuk menguji batas kemampuan deteksi berdasarkan atribut yang dapat diamati.

S5: evil twin dan rogue DHCP dijalankan secara bersamaan untuk menguji deteksi serangan gabungan.

Setiap skenario diulang minimal [20–30] kali setelah jumlah pengulangan dikonfirmasi dengan dosen pembimbing. Seluruh pengujian dilakukan pada jaringan terisolasi dengan izin pengelola Laboratorium D.

Tabel 2. Tabel Metode Penelitian
Metode/Langkah
Input
Proses
Output
Tool (Opsional)
Observasi Lab D dan penentuan whitelist
Konfigurasi controller dan 10 AP
Mengumpulkan seluruh BSSID, kanal, enkripsi, IP/MAC server DHCP, dan IP gateway sah
File whitelist (JSON)
Python, JSON
Pilot testing
2–3 AP dan skenario serangan awal
Memvalidasi alat dan serangan serta menentukan parameter pemindaian
Parameter final dan catatan prosedur
Python, Scapy
Pemindaian WLAN
Sinyal beacon/probe response AP sekitar
Mengumpulkan atribut AP
Daftar AP (SSID, BSSID, kanal, enkripsi, RSSI)
Scapy / perintah OS
Deteksi evil twin
Daftar AP dan whitelist seluruh AP sah
Memeriksa BSSID per SSID, lalu membandingkan kanal, enkripsi, dan RSSI sebagai indikator pendukung
Status AP: sah atau mencurigakan
Python
Deteksi rogue DHCP
Paket DHCPDISCOVER dan semua DHCPOFFER
Membandingkan Server Identifier, IP, MAC dengan whitelist
Status server DHCP: sah atau rogue
Scapy
Pelaporan dan log
Hasil deteksi
Menampilkan peringatan dan menyimpan log
Alert dan file log
Python (logging)
Pengujian utama
Skenario normal dan serangan pada 10 AP
Melakukan pengujian berulang dengan variasi lokasi dan perangkat
Data mentah hasil pengujian
Laboratorium D
Evaluasi
Hasil deteksi dan kondisi sebenarnya
Menghitung confusion matrix, akurasi, precision, recall, false positive rate, dan waktu deteksi
Tabel hasil evaluasi
Python, Excel




9. Daftar Pustaka
Asiana, K. P., Huwae, R. B., & Jatmika, A. H. (2025). Studi eksperimen keamanan jaringan Wi-Fi kampus: Analisis kerentanan terhadap serangan Evil Twin dan Deauthentication. Edumatic: Jurnal Pendidikan Informatika, 9(2), 629–638. https://doi.org/10.29408/edumatic.v9i2.31822
Banakh, R., Nyemkova, E., Justice, C., Piskozub, A., & Lakh, Y. (2024). Data mining approach for evil twin attack identification in Wi-Fi networks. Data, 9(10), 119. https://doi.org/10.3390/data9100119
The DHCP snooping and DHCP alert method in securing DHCP server from DHCP rogue attack. (2021). IJID (International Journal on Informatics for Development), 10(1), 38–46. https://doi.org/10.14421/ijid.2021.2287
An effective technique to automatically detect and neutralize rogue DHCP server. (2023). [Prosiding konferensi IEEE, 21–23 September 2023]. https://ieeexplore.ieee.org/document/10303033
Louca, C., Peratikou, A., & Stavrou, S. (2023). A novel Evil Twin MiTM attack through 802.11v protocol exploitation. Computers & Security, 130, 103261. https://doi.org/10.1016/j.cose.2023.103261
Makarova, M. S., & Maksutov, A. A. (2021). Methods of detecting and neutralizing potential DHCP rogue servers. 2021 IEEE Conference of Russian Young Researchers in Electrical and Electronic Engineering (ElConRus), 522–525. https://doi.org/10.1109/ElConRus51938.2021.9396106
Rogue Wi-Fi AP detection with Snappy. (2024). CyLab. https://cylab.be/publications/75/download/2024-rogue-wi-fi-ap-detection-with-snappy.pdf
Seo, J., Cho, C., & Won, Y. (2020). Enhancing the reliability of Wi-Fi network using evil twin AP detection method based on machine learning. Journal of Information Processing Systems, 16(3), 541–556. https://doi.org/10.3745/JIPS.03.0137
Tian, Y., Wang, S., & Zhang, L. (2021). Convolutional neural network based Evil Twin attack detection in Wi-Fi networks. MATEC Web of Conferences, 336, 08006. https://doi.org/10.1051/matecconf/202133608006
Wachira, F. N. (2021). A model to detect and prevent rogue DHCP attacks on wireless LAN communication [Thesis, Strathmore University]. https://su-plus.strathmore.edu/items/37fa485a-7053-42dc-bf8e-5697ae78cfe9
