Hasil itu **sudah berhasil** untuk test drive pertama. Aku akan menambahkan penjelasan langsung ke tutorial tentang arti setiap kolom, maksud “port berbeda”, dan urutan percobaan berikutnya supaya kamu tidak hanya mengulang tanpa tahu apa yang sedang dibandingkan.

Edit 

Ran terminal command: git --no-pager diff --check -- TUTORIAL_TEST_DRIVE_LAPTOP.md

Read , lines 225 to 380
Completed with input: {
  "path": "/media/user/D/0-SKRIPSI/scriptsee/TUTORIAL_TEST_DRIVE_LAPTOP.md",
  "view_range": [
    225,
    380
  ]
}

Iya, **test drive pertama kamu berhasil**. Output ini:

```text
Deteksi selesai: 1 alert, state tersisa: 1
Alert tersimpan di: ../alerts.csv
```

berarti aplikasi berhasil:

```text
membaca PCAP
→ menemukan paket IPv4/TCP
→ menghitung karakteristik
→ rule terpenuhi
→ menyimpan alert ke CSV
```

## Arti hasil kamu

```text
unique_ports = 10
connections  = 12
syn_ratio    = 0.3333
reason       = unique_ports_threshold
```

Artinya:

- `127.0.0.1` sebagai source dan destination berarti laptop melakukan scan ke dirinya sendiri;
- detector melihat **10 port berbeda** dalam sliding window;
- ada 12 event/paket TCP yang dihitung;
- sekitar 33,33% event memiliki flag SYN;
- alert muncul karena jumlah port unik mencapai threshold default, yaitu `10`.

Jadi `reason`:

```text
unique_ports_threshold
```

menunjukkan alasan aplikasi mendeteksi pola tersebut sebagai scanning.

Timestamp yang muncul menggunakan format UTC. Itu sebabnya waktu di CSV bisa terlihat berbeda beberapa jam dari waktu lokal Linux Mint kamu.

## Apakah ini sudah hasil akhir skripsi?

Belum. Ini adalah:

> **hasil test drive pertama untuk membuktikan aplikasi berjalan.**

Untuk skripsi, kamu masih perlu mengumpulkan banyak skenario dan membandingkan hasilnya dengan kondisi sebenarnya.

## Maksud “port berbeda” apa?

Maksudnya adalah mengubah **rentang port yang diperiksa oleh Nmap**, bukan mengubah port aplikasi atau port Linux secara manual.

Contoh:

```bash
nmap -sT -p 1-10 127.0.0.1
```

Berarti Nmap memeriksa port 1 sampai 10.

```bash
nmap -sT -p 1-50 127.0.0.1
```

Berarti Nmap memeriksa port 1 sampai 50.

```bash
nmap -sT -p 1-100 127.0.0.1
```

Berarti Nmap memeriksa port 1 sampai 100.

Kamu juga bisa mencoba:

```bash
nmap -sT -p 100-200 127.0.0.1
```

Target tetap:

```text
127.0.0.1
```

karena itu adalah laptopmu sendiri.

## Percobaan berikutnya

Jangan menjalankan semua percobaan dengan nama file yang sama karena hasil lama bisa tertimpa. Simpan dengan nama berbeda.

Contoh percobaan:

| Percobaan | Perintah | Tujuan |
|---|---|---|
| 1 | `nmap -sT -p 1-5 127.0.0.1` | Sedikit port |
| 2 | `nmap -sT -p 1-10 127.0.0.1` | Tepat sekitar threshold |
| 3 | `nmap -sT -p 1-50 127.0.0.1` | Jumlah port sedang |
| 4 | `nmap -sT -p 1-100 127.0.0.1` | Jumlah port lebih banyak |
| 5 | `sudo nmap -sS -p 1-100 127.0.0.1` | Membandingkan SYN scan |

Untuk setiap percobaan:

1. Jalankan `tcpdump`.
2. Jalankan satu perintah Nmap.
3. Hentikan `tcpdump` dengan `Ctrl+C`.
4. Jalankan detector.
5. Simpan PCAP dan CSV dengan nama berbeda.
6. Catat hasilnya.

Contoh untuk scan port 1–50.

### Terminal A

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app

sudo tcpdump \
  -i lo \
  -w ../capture-port-50.pcap \
  'ip and tcp'
```

### Terminal B

```bash
nmap -sT -p 1-50 127.0.0.1
```

Setelah Nmap selesai, tekan `Ctrl+C` di Terminal A.

### Jalankan detector

```bash
cd /media/user/D/0-SKRIPSI/scriptsee/app

python detect.py \
  --pcap ../capture-port-50.pcap \
  --output ../alerts-port-50.csv
```

Lihat hasilnya:

```bash
cat ../alerts-port-50.csv
```

## Nama file yang disarankan

```text
capture-port-5.pcap
alerts-port-5.csv

capture-port-10.pcap
alerts-port-10.csv

capture-port-50.pcap
alerts-port-50.csv

capture-port-100.pcap
alerts-port-100.csv
```

## Yang perlu dicatat

Buat tabel sederhana:

| Percobaan | Rentang port | Alert | Unique ports | Connections | Reason |
|---|---:|---|---:|---:|---|
| 1 | 1–5 | Ya/Tidak | ... | ... | ... |
| 2 | 1–10 | Ya/Tidak | ... | ... | ... |
| 3 | 1–50 | Ya/Tidak | ... | ... | ... |
| 4 | 1–100 | Ya/Tidak | ... | ... | ... |

Perlu diperhatikan:

> Jumlah port yang diminta Nmap dan nilai `unique_ports` pada CSV bisa berbeda.

Misalnya kamu meminta Nmap memindai port 1–100, tetapi detector hanya melihat 10 port unik dalam sliding window tertentu. Itu bisa terjadi karena:

- paket yang terbaca tidak semuanya sama;
- filter hanya mengambil IPv4/TCP;
- event berada di luar window;
- pola traffic TCP connect scan berbeda dari perkiraan;
- detector menghitung paket yang masuk ke state, bukan sekadar jumlah port pada perintah Nmap.

Aku juga sudah menambahkan penjelasan ini ke `TUTORIAL_TEST_DRIVE_LAPTOP.md`.

Jadi langkahmu sekarang:

```text
test pertama berhasil
→ coba port 1–5
→ coba port 1–10
→ coba port 1–50
→ coba port 1–100
→ simpan semua hasil
→ bandingkan unique_ports, connections, dan alert
```

Setelah itu baru kita bisa membahas kenapa hasil tiap percobaan berbeda dan mulai membuat tabel eksperimen skripsi.