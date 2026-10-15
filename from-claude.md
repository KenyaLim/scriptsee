Berikut teks lengkap yang sudah direvisi, bisa langsung kamu copy-paste. Bagian sampul, halaman persetujuan, dan Daftar Pustaka tidak berubah, jadi pakai yang lama. Tabel ditulis dengan pemisah "|" supaya mudah kamu ubah jadi tabel di Word.

Hal yang perlu kamu isi atau cek sendiri ditandai dengan [ ... ].

======================================================

1. Latar Belakang

Jaringan nirkabel (Wireless Local Area Network/WLAN) kini menjadi cara utama perangkat seperti laptop dan ponsel pintar terhubung ke internet, baik di rumah, kampus, perkantoran, maupun tempat umum. Kemudahan ini datang bersama risiko. Sinyal nirkabel merambat di udara dan dapat diterima siapapun dalam jangkauannya, sehingga penyerang bisa mengamati bahkan menyusup ke komunikasi tanpa perlu akses fisik ke kabel jaringan. Karena itu, keamanan pada lapisan akses jaringan perlu mendapat perhatian khusus.

Salah satu ancaman yang paling sering dibahas adalah evil twin access point (AP), yaitu AP palsu yang meniru AP sah dengan menyamakan SSID dan, pada beberapa kasus, alamat MAC. Penyerang dapat memanfaatkan evil twin untuk memalsukan pesan dan menyadap komunikasi pengguna (Seo et al., 2020). Evil twin sulit dikenali karena tampilannya hampir sama dengan AP sah. Studi eksperimen pada jaringan Wi-Fi kampus menunjukkan ancaman ini nyata. Asiana et al. (2025) menguji 13 lokasi di kampus dengan perangkat NodeMCU ESP8266 dan menemukan 5 lokasi (38,46%) rentan, yaitu pengguna terarah ke SSID palsu dan memasukkan kredensial. Serangan juga terus berkembang. Louca et al. (2023) menunjukkan evil twin dapat diperkuat dengan memanfaatkan mekanisme protokol 802.11v, sehingga pertahanan yang hanya mengandalkan nama jaringan semakin tidak memadai.

Berbagai pendekatan deteksi evil twin sudah dikembangkan. Seo et al. (2020) memakai klasifikasi pembelajaran mesin dengan banyak fitur, Tian et al. (2021) memakai convolutional neural network, dan Banakh et al. (2024) memakai pendekatan data mining. Pendekatan tersebut menjanjikan, tetapi umumnya membutuhkan data latih, pengolahan yang kompleks, atau perangkat tertentu. Di sisi lain, deteksi berbasis skrip Python seperti Snappy menunjukkan bahwa pemindaian dan fingerprinting AP dapat dilakukan dengan alat yang ringan ("Rogue Wifi AP detection with Snappy", 2024).

Ancaman kedua berada pada layanan Dynamic Host Configuration Protocol (DHCP). DHCP memberikan alamat IP, gateway, dan DNS secara otomatis kepada klien. Karena klien dapat menerima pesan DHCPOFFER dari lebih dari satu server, penyerang mudah memasang rogue DHCP server di jaringan WLAN (Wachira, 2021). Server palsu ini dapat membagikan alamat IP, DNS, dan informasi routing yang salah, sehingga lalu lintas korban dapat dialihkan atau disadap (Makarova & Maksutov, 2021). Rogue DHCP juga dapat memicu serangan man-in-the-middle (MITM). Penelitian lain menunjukkan bahwa pengecekan alamat IP server saja dapat dikelabui lewat pemalsuan IP, sehingga perlu dikombinasikan dengan pemeriksaan alamat MAC ("An effective technique to automatically detect and neutralize rogue DHCP server", 2023). Pengamanan umum seperti DHCP snooping dan DHCP alert efektif, tetapi bergantung pada konfigurasi perangkat jaringan terkelola ("The DHCP snooping and DHCP alert method", 2021). Perangkat semacam itu tidak selalu ada di jaringan kecil atau kampus dengan anggaran terbatas.

Kedua serangan ini sering saling berkaitan. Penyerang yang memasang evil twin biasanya juga menjalankan layanan DHCP sendiri supaya korban mendapat IP, gateway, dan DNS yang dikendalikan penyerang. Namun, penelitian yang ada cenderung membahas keduanya secara terpisah, yaitu evil twin pada lapisan 802.11 dan rogue DHCP pada lapisan jaringan. Belum banyak alat sederhana yang menggabungkan kedua deteksi dalam satu aplikasi yang dapat dijalankan administrator jaringan tanpa bergantung pada fitur perangkat terkelola.

Selain itu, jaringan WLAN di kampus dan perkantoran pada praktiknya tidak terdiri dari satu AP. Jaringan tersebut umumnya memakai topologi seamless wireless, yaitu banyak AP yang dikelola satu wireless controller dan memancarkan SSID serta pengaturan keamanan yang sama, sehingga klien dapat berpindah (roaming) antar-AP tanpa memutus koneksi. Pada topologi ini, SSID yang sama bukan lagi tanda AP palsu karena seluruh AP sah memang memakai SSID yang sama. Akibatnya deteksi evil twin menjadi lebih sulit dan risiko AP sah salah ditandai sebagai palsu (false positive) meningkat. Sebagian besar penelitian terdahulu menguji pada satu AP atau jaringan kabel, sehingga belum menggambarkan kondisi jaringan riil tersebut.

Berdasarkan hal tersebut, penelitian ini merancang dan membangun aplikasi berbasis Python untuk mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP berbasis wireless controller. Python dipilih karena memiliki pustaka manipulasi paket seperti Scapy, bersifat lintas platform, dan mudah dikembangkan. Pengujian dilakukan di Laboratorium D, yang mensimulasikan satu wireless controller dengan 10 AP secara seamless, sehingga hasilnya menggambarkan jaringan riil di lapangan. Perangkat penyerang dan klien dibuat bervariasi (lebih dari satu perangkat), tidak hanya satu laptop dan satu ponsel.

2. Rumusan Masalah

1. Bagaimana merancang dan membangun aplikasi berbasis Python yang dapat mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP berbasis wireless controller?
2. Bagaimana cara aplikasi mengidentifikasi rogue DHCP server berdasarkan analisis pesan DHCP (DISCOVER, OFFER, REQUEST, ACK) dibandingkan daftar server sah?
3. Bagaimana cara aplikasi mengidentifikasi evil twin AP pada jaringan ber-SSID sama berdasarkan perbandingan atribut AP seperti BSSID, kanal, jenis enkripsi, dan kekuatan sinyal (RSSI) terhadap daftar AP sah, tanpa menimbulkan false positive pada AP sah?
4. Seberapa baik kinerja aplikasi yang dikembangkan dalam mendeteksi kedua serangan tersebut berdasarkan parameter akurasi, precision, recall, F1-score, false positive rate, dan waktu deteksi?

3. Batasan Masalah

1. Pengujian dilakukan pada topologi seamless wireless di Laboratorium D, yaitu satu wireless controller yang mengelola 10 AP dengan SSID dan pengaturan keamanan yang sama. Laptop pendeteksi dapat ditempatkan di beberapa titik, sedangkan perangkat penyerang dan perangkat klien sah terdiri dari lebih dari satu perangkat dengan tipe yang bervariasi.
2. Aplikasi dikembangkan menggunakan bahasa pemrograman Python dan hanya berfokus pada deteksi dan peringatan (alert), bukan pencegahan aktif, pemblokiran, atau serangan balik.
3. Jenis serangan yang dideteksi hanya rogue DHCP server dan evil twin AP; serangan lain seperti DHCP starvation, deauthentication flood, ARP spoofing, dan captive portal phishing tidak dibahas.
4. Pengujian hanya dilakukan di Laboratorium D dengan izin pengelola laboratorium dan pada jaringan yang terisolasi dari jaringan produksi, serta tidak dilakukan pada jaringan publik atau milik pihak lain.
5. Aplikasi bekerja pada jaringan IPv4; DHCPv6 tidak dibahas.
6. Pengujian terbatas pada pita frekuensi dan standar WLAN yang didukung oleh adapter nirkabel yang digunakan serta oleh perangkat controller dan AP di Laboratorium D.
7. Hasil penelitian berlaku untuk konfigurasi Laboratorium D [sebutkan merek dan tipe controller dan AP setelah dikonfirmasi] dan belum diuji pada merek atau skala jaringan lain.
8. Penelitian ini tidak membahas keamanan sistem aplikasi itu sendiri, misalnya enkripsi log atau autentikasi pengguna aplikasi.

4. Tujuan Penelitian

1. Merancang dan membangun aplikasi berbasis Python yang mendeteksi rogue DHCP server dan evil twin AP pada jaringan WLAN seamless multi-AP berbasis wireless controller.
2. Mengimplementasikan mekanisme deteksi rogue DHCP server melalui pengiriman paket DHCPDISCOVER dan analisis seluruh DHCPOFFER yang diterima terhadap daftar server sah (whitelist).
3. Mengimplementasikan mekanisme deteksi evil twin AP melalui pemindaian AP di sekitar dan analisis ketidakkonsistenan atribut AP (terutama BSSID, kanal, dan enkripsi) terhadap whitelist AP sah.
4. Mengevaluasi kinerja aplikasi menggunakan parameter akurasi, precision, recall, F1-score, false positive rate, dan waktu deteksi pada skenario normal (termasuk roaming klien) dan skenario serangan simulasi.

5. Manfaat Penelitian

1. Memperkuat jaringan internal. Aplikasi memberi administrator gambaran kondisi jaringan: AP mana yang sah dan mana yang mencurigakan, serta server DHCP mana yang berwenang. Dengan deteksi dini terhadap AP palsu dan DHCP server palsu, celah pada lapisan akses dapat segera diketahui dan ditutup, sehingga konfigurasi jaringan (alamat IP, gateway, dan DNS) tetap berasal dari sumber yang sah. Dengan begitu jaringan internal menjadi lebih andal dan terkelola.
2. Mencegah adanya penyusup. Peringatan dini dari aplikasi memungkinkan tindakan sebelum penyerang sempat mengalihkan lalu lintas atau mencuri data. Administrator dapat menelusuri perangkat mencurigakan, mengganti kredensial, atau memutus perangkat tersebut dari jaringan. Dengan demikian risiko penyadapan, pencurian kredensial, dan serangan lanjutan seperti MITM dapat ditekan.
3. Bagi peneliti: menambah pemahaman tentang protokol DHCP, standar IEEE 802.11, arsitektur wireless controller, dan teknik analisis paket dengan Python.
4. Bagi pengguna jaringan: meningkatkan kewaspadaan terhadap risiko terhubung ke jaringan palsu dan penyadapan data pribadi.
5. Bagi penelitian selanjutnya: menjadi dasar pengembangan sistem yang lebih lengkap, misalnya pencegahan aktif, deteksi serangan lain, atau penerapan pembelajaran mesin.

6. Tinjauan Pustaka dan Landasan Teori

6.0. Tinjauan Pustaka

Makarova dan Maksutov (2021) mengembangkan metode untuk mendeteksi rogue DHCP server dan memberikan perlindungan aktif pada host berbasis GNU/Linux. Mereka menjelaskan bahwa server DHCP tidak sah dapat bersaing dengan server sah dan membagikan alamat IP, DNS, serta informasi routing yang salah kepada klien. Penelitian ini relevan sebagai dasar mekanisme deteksi DHCP, tetapi tidak berfokus pada lingkungan WLAN.

Wachira (2021) merancang intrusion detection system (IDS) khusus untuk mendeteksi rogue DHCP server pada komunikasi WLAN dengan memantau dan menganalisis pesan transaksi DHCP. Pengujian pada jaringan yang berisi server sah dan palsu menunjukkan semua alamat IP yang ditawarkan server palsu berhasil terdeteksi (tingkat deteksi 100%). Penelitian ini menjadi acuan utama untuk analisis pesan DHCP pada penelitian ini.

Penelitian di Indonesia pada jurnal IJID menerapkan DHCP Snooping dan DHCP Alert untuk mengamankan server DHCP dari serangan rogue DHCP. DHCP Alert memantau proses DORA sehingga hanya terjadi antara server sah dan klien ("The DHCP Snooping and DHCP Alert Method", 2021). Pendekatan ini bergantung pada perangkat jaringan terkelola, sehingga penelitian ini mengambil pendekatan berbasis aplikasi yang tidak memerlukan konfigurasi perangkat tersebut.

Pada sisi evil twin, Seo et al. (2020) mengusulkan metode deteksi evil twin AP berbasis klasifikasi pembelajaran mesin dengan banyak fitur, dan melaporkan akurasi 100% dengan algoritma random forest. Penelitian ini memperlihatkan bahwa evil twin dapat meniru SSID dan alamat MAC, sehingga pemeriksaan satu atribut saja tidak cukup.

Penelitian terbaru berjudul Rogue Wi-Fi AP detection with Snappy (2024) membahas skrip Python bernama Snappy yang dirancang untuk melakukan sidik jari dan mendeteksi AP Wi-Fi palsu, serta menjelaskan konsep mode monitor dan penggunaan Scapy. Penelitian ini mendukung pemilihan Python dan Scapy sebagai dasar pengembangan aplikasi.

Berdasarkan penelusuran tersebut, penelitian terdahulu umumnya membahas rogue DHCP dan evil twin secara terpisah dan tidak secara khusus menguji pada topologi WLAN multi-AP ber-SSID sama yang dikelola wireless controller. Kontribusi penelitian ini adalah menggabungkan kedua deteksi dalam satu aplikasi Python dan mengujinya pada topologi seamless wireless yang menggambarkan jaringan riil, dengan perhatian khusus pada false positive akibat banyaknya AP sah ber-SSID sama.

Tabel 1. Perbandingan Penelitian Terkait

No | Peneliti (Tahun) | Fokus | Metode | Perbedaan dengan Penelitian Ini
1 | Makarova & Maksutov (2021) | Rogue DHCP server | Deteksi dan perlindungan host pada GNU/Linux | Tidak fokus WLAN; tidak mencakup evil twin
2 | Wachira (2021) | Rogue DHCP pada WLAN | IDS berbasis analisis pesan DHCP | Hanya DHCP; tidak mencakup evil twin
3 | IJID (2021) | Rogue DHCP | DHCP Snooping dan DHCP Alert | Bergantung pada perangkat jaringan terkelola
4 | Seo et al. (2020) | Evil twin AP | Pembelajaran mesin dengan fitur clock skew | Hanya evil twin; tidak mencakup DHCP
5 | Snappy (2024) | Rogue Wi-Fi AP | Skrip Python untuk fingerprinting AP | Hanya sisi AP; tidak mencakup DHCP
6 | Penelitian ini | Rogue DHCP dan evil twin | Aplikasi Python (Scapy) pada WLAN seamless multi-AP (10 AP, 1 controller) di Lab D | Menggabungkan kedua deteksi dalam satu aplikasi dan menguji pada topologi multi-AP ber-SSID sama

Sebagaimana terlihat pada Tabel 1, belum ada penelitian pada daftar tersebut yang menggabungkan kedua deteksi dalam satu aplikasi.

6.1. Landasan Teori

a. Wireless Local Area Network (WLAN). WLAN adalah jaringan lokal nirkabel berbasis standar IEEE 802.11. Komunikasi antara klien dan AP dilakukan melalui frame manajemen (misalnya beacon, probe request/response, authentication, association), frame kontrol, dan frame data. Beacon frame dikirim AP secara berkala dan memuat informasi seperti SSID, BSSID, kanal, dan jenis enkripsi.

b. Wireless Controller dan Topologi Seamless. Wireless controller adalah perangkat atau layanan yang mengelola banyak AP secara terpusat, termasuk konfigurasi SSID, keamanan, dan kanal. Pada topologi seamless wireless, seluruh AP memancarkan SSID dan pengaturan keamanan yang sama sehingga klien dapat berpindah (roaming) antar-AP tanpa memutus koneksi. Setiap AP, bahkan setiap radio (2,4 GHz dan 5 GHz) dan SSID pada AP tersebut, memiliki BSSID sendiri. Akibatnya, pada topologi ini satu SSID akan dipancarkan oleh banyak BSSID sah, sehingga daftar BSSID sah menjadi penanda utama dalam membedakan AP sah dan AP palsu.

c. Evil Twin AP. Evil twin adalah AP palsu yang menyamar sebagai AP sah dengan meniru SSID dan kadang MAC address (Seo et al., 2020). Ciri yang dapat dibandingkan dengan AP sah meliputi: (1) BSSID yang tidak terdaftar pada whitelist, (2) kanal yang berbeda dari profil, (3) jenis enkripsi yang lebih lemah atau terbuka, (4) RSSI yang tidak wajar sebagai indikator pendukung, dan (5) vendor OUI pada BSSID yang tidak sesuai. Pada kasus SSID dan BSSID dikloning, whitelist BSSID saja tidak cukup, sehingga diperlukan atribut tambahan seperti anomali kanal, enkripsi, interval beacon, atau BSSID yang sama terdeteksi pada kanal berbeda.

d. DHCP dan Rogue DHCP Server. DHCP menyediakan konfigurasi jaringan otomatis melalui proses DORA: Discover, Offer, Request, Acknowledge. Karena klien dapat menerima OFFER dari lebih dari satu server, penyerang dapat memasang server palsu yang membagikan konfigurasi berbahaya (Wachira, 2021; Makarova & Maksutov, 2021). Rogue DHCP dikenali dari Server Identifier, alamat IP/MAC pengirim, serta isi gateway dan DNS pada OFFER yang tidak sesuai dengan data server sah.

e. Python dan Scapy. Scapy adalah pustaka Python untuk membuat, mengirim, dan menganalisis paket jaringan, termasuk layer 802.11 (Dot11Beacon, Dot11ProbeReq) dan DHCP. Pustaka ini juga dipakai pada penelitian deteksi AP palsu ("Rogue Wi-Fi AP detection with Snappy", 2024).

f. Mode Monitor. Mode monitor memungkinkan adapter nirkabel menangkap seluruh frame 802.11 di udara tanpa harus terhubung ke jaringan ("Rogue Wi-Fi AP detection with Snappy", 2024). Tidak semua adapter bawaan laptop mendukung mode ini, sehingga penelitian ini menyiapkan dua mode: (1) mode monitor jika didukung (misalnya dengan adapter USB eksternal), dan (2) pemindaian jaringan biasa (managed mode) melalui perintah sistem operasi jika tidak didukung.

g. Pilot Testing. Pilot testing adalah pengujian awal berskala kecil sebelum pengujian utama untuk memeriksa kelayakan alat, skenario, dan prosedur, serta menentukan parameter yang akan dipakai. Data pilot dipisahkan dari data pengujian utama.

h. Metrik Evaluasi. Kinerja deteksi dihitung menggunakan confusion matrix (TP, TN, FP, FN):

Akurasi = (TP + TN) / (TP + TN + FP + FN) [1]
Precision = TP / (TP + FP) [2]
Recall = TP / (TP + FN) [3]
F1-score = 2 x (Precision x Recall) / (Precision + Recall) [4]
False Positive Rate (FPR) = FP / (FP + TN) [5]

TP adalah serangan yang terdeteksi dengan benar, TN adalah kondisi normal yang tidak diberi peringatan, FP adalah peringatan palsu, dan FN adalah serangan yang tidak terdeteksi. Persamaan 1 digunakan untuk menilai ketepatan keseluruhan, Persamaan 2 untuk menilai ketepatan peringatan, Persamaan 3 untuk menilai kemampuan menangkap serangan, Persamaan 4 untuk menyeimbangkan precision dan recall, dan Persamaan 5 untuk menilai seberapa sering kondisi normal (termasuk AP sah dan klien yang roaming) salah ditandai sebagai serangan. Selain itu, waktu deteksi diukur sebagai selang waktu sejak serangan aktif sampai peringatan pertama muncul.

7. Blok Diagram Sistem

Gambaran besar sistem terdiri dari tiga bagian: lingkungan pengujian, modul aplikasi, dan keluaran.

Lingkungan pengujian: satu wireless controller mengelola 10 AP sah di Laboratorium D dengan SSID dan keamanan yang sama. Server DHCP sah terhubung ke jaringan tersebut. Laptop pendeteksi menjalankan aplikasi dan dapat ditempatkan di beberapa titik. Penyerang simulasi berupa lebih dari satu perangkat (misalnya ponsel hotspot dan laptop dengan hostapd/dnsmasq) yang mengaktifkan AP dengan SSID yang sama (evil twin) dan/atau menjalankan layanan DHCP sebagai rogue server. Beberapa klien sah (laptop dan ponsel) terhubung dan melakukan roaming.

[Gambar 1. Diagram Umum — gambar ulang: controller, 10 AP, server DHCP, laptop pendeteksi, perangkat penyerang, klien sah]

Alur umum sistem:
1. Pengguna menjalankan aplikasi dan memuat whitelist, yaitu seluruh BSSID sah dari 10 AP (beserta kanal, enkripsi, dan vendor OUI), serta IP/MAC server DHCP sah dan IP gateway sah.
2. Modul Pemindai WLAN memindai AP di sekitar dan mengumpulkan atribut SSID, BSSID, kanal, enkripsi, dan RSSI.
3. Modul Deteksi Evil Twin membandingkan hasil pindaian dengan whitelist dan menandai AP yang mencurigakan.
4. Modul Deteksi Rogue DHCP mengirim DHCPDISCOVER (Scapy), mengumpulkan semua DHCPOFFER selama jangka waktu tertentu, lalu membandingkan Server Identifier, IP, dan MAC pengirim dengan whitelist.
5. Modul Pelaporan menampilkan peringatan (alert) pada antarmuka dan menyimpan log (waktu, jenis serangan, bukti).
6. Pengguna meninjau hasil dan log.

Diagram khusus per modul:
- Evil twin: Mulai → pindai AP → kelompokkan per SSID → untuk setiap BSSID, cek apakah ada di whitelist → jika tidak ada maka peringatan evil twin; jika ada, bandingkan kanal, enkripsi, dan indikator pendukung (RSSI, interval beacon) dengan profil → jika tidak cocok maka peringatan (BSSID dikloning), jika cocok maka normal → catat log.
- Rogue DHCP: Mulai → kirim DHCPDISCOVER → tunggu semua DHCPOFFER → bandingkan Server Identifier, IP, dan MAC dengan whitelist → jika tidak terdaftar atau lebih dari satu server menjawab dengan konfigurasi berbeda maka peringatan rogue DHCP, jika terdaftar maka normal → catat log.

[Gambar 2. Diagram Deteksi Evil Twin — tambahkan langkah "BSSID ada di whitelist?"]
[Gambar 3. Diagram Deteksi Rogue DHCP]

8. Metode Penelitian

Penelitian ini menggunakan pendekatan eksperimental dengan pengembangan aplikasi secara bertahap, dengan tahapan sebagai berikut.

1. Studi literatur: mempelajari WLAN 802.11, arsitektur wireless controller dan roaming, DHCP, evil twin, rogue DHCP, serta penggunaan Python dan Scapy.
2. Analisis kebutuhan: menentukan kebutuhan fungsional (pemindaian, deteksi, pelaporan, log) dan kebutuhan perangkat (laptop pendeteksi, adapter nirkabel, perangkat penyerang, dan perangkat klien).
3. Observasi lingkungan Laboratorium D: mencatat merek dan tipe controller dan AP, penempatan 10 AP, kanal, jenis enkripsi, serta pengaturan VLAN dan DHCP. Seluruh BSSID sah dikumpulkan saat jaringan dalam kondisi bersih sebagai baseline (whitelist).
4. Perancangan sistem: merancang arsitektur aplikasi, alur deteksi berbasis whitelist multi-BSSID, dan antarmuka (CLI atau GUI sederhana).
5. Implementasi: membangun aplikasi dengan Python dan Scapy.
6. Pilot testing: pengujian awal berskala kecil sebelum pengujian utama (dijelaskan di bawah).
7. Pembangunan skenario pengujian utama: menyiapkan skenario normal dan serangan pada seluruh 10 AP.
8. Pengujian utama: menjalankan seluruh skenario dengan pengulangan.
9. Evaluasi: menghitung metrik evaluasi dan menganalisis hasil.
10. Penyusunan laporan: menarik kesimpulan dan saran.

8.1 Pilot Testing

Pilot testing dilakukan sebelum pengujian utama pada skala kecil, yaitu menggunakan 2 sampai 3 AP dari Laboratorium D yang berada di bawah controller yang sama. Tujuannya:

1. Validasi alat: memastikan adapter nirkabel yang dipakai mendukung mode monitor atau hanya managed mode, serta memastikan hak akses dan eksekusi Python/Scapy berjalan. Adapter USB eksternal disiapkan sebagai cadangan.
2. Validasi serangan: memastikan evil twin dan rogue DHCP benar-benar berhasil terbentuk dan perangkat korban benar-benar terhubung ke AP palsu atau menerima OFFER dari server palsu, sebelum kinerja deteksi diukur.
3. Penentuan parameter: menentukan interval pemindaian, batas waktu tunggu DHCPOFFER, dan bobot atau ambang RSSI, dengan tujuan menekan false positive.
4. Uji prosedur: memeriksa urutan langkah pengujian, format pencatatan data, dan jumlah pengulangan yang realistis.

Hasil pilot dipakai untuk memperbaiki aplikasi dan menetapkan parameter final. Data pilot tidak dimasukkan ke dalam hasil pengujian utama.

8.2 Skenario Pengujian Utama

Kode | Kondisi | Tujuan
S0 | Normal, tanpa serangan, klien roaming antar-AP | Mengukur false positive pada AP sah ber-SSID sama
S1 | Rogue DHCP pada jaringan yang sama | Menguji deteksi rogue DHCP
S2 | Evil twin: SSID sama, BSSID berbeda, enkripsi terbuka | Kasus dasar evil twin
S3 | Evil twin: SSID sama, BSSID berbeda, enkripsi sama (WPA2) | Evil twin yang lebih sulit dibedakan
S4 | Evil twin: SSID dan BSSID dikloning | Menguji batas kemampuan deteksi
S5 | Evil twin dan rogue DHCP bersamaan | Menguji serangan gabungan

Variabel tambahan yang divariasikan: lokasi penyerang (dekat AP, di antara AP, dan area tepi jangkauan), lokasi laptop pendeteksi, jumlah klien (lebih dari satu), dan tipe perangkat klien. Perangkat penyerang berupa ponsel hotspot dan laptop (hostapd/dnsmasq). Setiap skenario diulang minimal [20–30] kali agar hasilnya memiliki dasar statistik.

8.3 Metrik Evaluasi

Kinerja aplikasi dinilai menggunakan akurasi, precision, recall, F1-score, false positive rate, dan waktu deteksi sejak serangan aktif. Selain itu diukur overhead aplikasi (penggunaan CPU dan RAM) serta konsistensi hasil antar-lokasi dan antar-pengulangan. Jika wireless controller di Laboratorium D memiliki fitur rogue AP detection bawaan, fitur tersebut dapat dijadikan pembanding.

8.4 Etika dan Batasan Pengujian

Seluruh serangan simulasi dilakukan di Laboratorium D dengan izin pengelola laboratorium, pada jaringan yang terisolasi dari jaringan produksi, dan tidak mengganggu pengguna lain. Hasil penelitian berlaku untuk topologi dan perangkat Laboratorium D, dan kemampuan deteksi dari sisi klien bergantung pada kemampuan adapter nirkabel yang digunakan.

Tabel 2. Tabel Metode Penelitian

Metode/Langkah | Input | Proses | Output | Tool (Opsional)
Observasi Lab D dan penentuan whitelist | Konfigurasi controller dan 10 AP | Mengumpulkan semua BSSID, kanal, enkripsi, IP/MAC server DHCP, dan IP gateway sah | File whitelist (JSON) | Python, JSON
Pilot testing | 2–3 AP, skenario serangan awal | Validasi alat dan serangan, penentuan parameter | Parameter final dan catatan prosedur | Python, Scapy
Pemindaian WLAN | Sinyal beacon/probe response AP sekitar | Mengumpulkan atribut AP | Daftar AP (SSID, BSSID, kanal, enkripsi, RSSI) | Scapy / perintah OS
Deteksi evil twin | Daftar AP dan whitelist | Membandingkan per SSID: BSSID, kanal, enkripsi, RSSI | Status AP: sah atau mencurigakan | Python
Deteksi rogue DHCP | Paket DHCPDISCOVER dan semua DHCPOFFER | Membandingkan Server Identifier, IP, MAC dengan whitelist | Status server DHCP: sah atau rogue | Scapy
Pelaporan dan log | Hasil deteksi | Menampilkan peringatan dan menyimpan log | Alert dan file log | Python (logging)
Pengujian utama (S0–S5) | Skenario normal dan serangan pada 10 AP | Eksekusi berulang [20–30] kali dengan variasi lokasi dan perangkat | Data mentah hasil pengujian | Lab D
Evaluasi | Hasil deteksi dan kondisi sebenarnya | Menghitung confusion matrix, akurasi, precision, recall, F1-score, FPR, waktu deteksi | Tabel hasil evaluasi | Python, Excel

9. Daftar Pustaka

(Tidak berubah, pakai daftar pustaka yang lama.)

======================================================

Catatan:
- Ganti bagian [ ... ] setelah kamu konfirmasi ke laboran/dosen: merek dan tipe controller dan AP, serta jumlah pengulangan.
- Gambar 1 sampai 3 perlu digambar ulang sesuai keterangan di Bab 7.
- Pada Bab 1 aku menambahkan satu paragraf baru tentang topologi seamless sebagai dasar kenapa penelitian ini perlu dilakukan di multi-AP. Itu argumen yang kamu butuhkan di kolokium.
- Kalau dosen bertanya soal S4 (SSID dan BSSID dikloning), jawabannya: itu sengaja dimasukkan sebagai batas kemampuan deteksi dan akan dilaporkan apa adanya.