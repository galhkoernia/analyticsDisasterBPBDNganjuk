# Tujuan Utama Analisis

Tujuan kita bukan sekadar menjawab:

> "Berapa jumlah bencana?"

Tetapi menjawab pertanyaan-pertanyaan operasional seperti:

* Apa pola kejadian bencana?
* Wilayah mana yang paling rentan?
* Apakah ada tren kenaikan atau penurunan?
* Faktor apa yang sering muncul?
* Dampak apa yang paling dominan?
* Bagaimana karakteristik setiap jenis bencana?
* Apa rekomendasi yang dapat diambil berdasarkan data?

Dengan kata lain, kita ingin mengubah **data operasional menjadi informasi**, kemudian menjadi **insight**, dan akhirnya menjadi **dasar pengambilan keputusan**.

---

# Framework Analisis

Saya mengusulkan alur analisis sebagai berikut.

```text
Raw Data
     │
     ▼
Data Understanding
     │
     ▼
Data Cleaning
     │
     ▼
Data Profiling
     │
     ▼
Exploratory Data Analysis (EDA)
     │
     ▼
Statistical Analysis
     │
     ▼
Insight Extraction
     │
     ▼
Visualization
     │
     ▼
Interactive Dashboard
```

Artinya, dashboard hanyalah **media penyajian hasil analisis**, bukan inti pekerjaan kita.

---

# Tahap 1 — Data Understanding

Tahap pertama adalah memahami isi dataset secara menyeluruh.

Yang akan kita identifikasi antara lain:

## Struktur Data

* Jumlah atribut
* Tipe data
* Hubungan antarvariabel
* Variabel numerik
* Variabel kategorikal
* Variabel spasial
* Variabel temporal

Contoh pertanyaan:

* Kolom mana yang menjadi identitas?
* Mana yang menunjukkan lokasi?
* Mana yang menunjukkan waktu?
* Mana yang menggambarkan dampak?
* Mana yang menggambarkan proses penanganan?

Output tahap ini adalah **peta struktur data**.

---

# Tahap 2 — Data Quality Assessment

Sebelum dianalisis, kualitas data harus diperiksa.

Beberapa aspek yang akan dievaluasi:

## Completeness

* Missing value
* Data kosong
* Kolom tidak terisi

## Consistency

* Penulisan kecamatan berbeda
* Penulisan desa berbeda
* Format tanggal berbeda

## Accuracy

* Koordinat valid atau tidak
* Nilai korban masuk akal atau tidak
* Kerugian bernilai negatif atau tidak

## Duplicate

* Kejadian ganda
* Nomor laporan ganda

Outputnya adalah **laporan kualitas data**.

---

# Tahap 3 — Data Profiling

Tahap ini bertujuan memahami karakteristik setiap variabel.

Contohnya:

Untuk variabel *Jenis Bencana*:

* Berapa kategori?
* Persentase masing-masing?
* Apakah ada kategori yang mendominasi?

Untuk variabel *Kecamatan*:

* Kecamatan dengan kejadian tertinggi
* Kecamatan dengan kejadian terendah
* Sebaran data

Untuk variabel *Tanggal*:

* Rentang waktu
* Distribusi bulanan
* Distribusi tahunan

Outputnya berupa **profil statistik setiap atribut**.

---

# Tahap 4 — Exploratory Data Analysis (EDA)

Ini adalah inti pekerjaan data analyst.

Bukan hanya membuat grafik, tetapi mencari pola yang sebelumnya belum diketahui.

EDA saya bagi menjadi lima kelompok.

## A. Analisis Temporal

Menjawab:

* Kapan bencana paling sering terjadi?
* Bulan paling rawan?
* Hari tertentu?
* Jam tertentu?

Output:

* Tren waktu
* Moving average
* Musiman
* Perubahan tahunan

---

## B. Analisis Spasial

Menjawab:

* Di mana lokasi paling rawan?
* Kecamatan dominan?
* Desa dominan?
* Persebaran koordinat?

Output:

* Distribusi wilayah
* Peta titik
* Heatmap
* Klaster wilayah

---

## C. Analisis Karakteristik Bencana

Menjawab:

* Jenis bencana dominan?
* Penyebab dominan?
* Hubungan penyebab dengan jenis bencana?
* Apakah jenis tertentu hanya muncul di wilayah tertentu?

Output:

* Frekuensi
* Cross-tabulation
* Distribusi kategori

---

## D. Analisis Dampak

Menjawab:

* Korban terbanyak?
* Kerusakan terbesar?
* Kerugian terbesar?
* Jenis bencana paling merusak?

Output:

* Ranking dampak
* Distribusi kerusakan
* Perbandingan jenis bencana

---

## E. Analisis Operasional

Jika tersedia data penanganan.

Menjawab:

* Status penanganan
* Waktu respon
* Kendala lapangan
* Kebutuhan logistik
* Distribusi personel

Analisis ini memberikan nilai tambah bagi evaluasi operasional BPBD.

---

# Tahap 5 — Analisis Hubungan Antarvariabel

Setelah memahami masing-masing variabel, kita mulai mencari hubungan.

Contohnya:

* Jenis bencana × Kecamatan
* Jenis bencana × Bulan
* Kecamatan × Dampak
* Penyebab × Jenis bencana
* Curah kejadian × Waktu

Di tahap ini kita mulai menggunakan teknik statistik, seperti:

* Tabel kontingensi
* Korelasi (untuk variabel numerik)
* Uji chi-square (untuk hubungan antarvariabel kategorikal, jika relevan)
* Analisis distribusi

Tujuannya bukan sekadar menghitung, tetapi menjelaskan hubungan yang bermakna.

---

# Tahap 6 — Insight Extraction

Ini adalah tahap yang sering terlewat.

Grafik belum tentu menghasilkan insight.

Insight adalah interpretasi yang menjawab "mengapa" atau "apa implikasinya".

Contoh:

* Kecamatan A memiliki jumlah kejadian tertinggi, tetapi dampaknya relatif rendah. Hal ini dapat mengindikasikan kejadian berskala kecil namun berulang.
* Longsor hanya menyumbang sebagian kecil jumlah kejadian, tetapi memberikan kontribusi terbesar terhadap kerusakan rumah.
* Angin kencang tersebar di banyak wilayah sehingga memerlukan strategi mitigasi yang berbeda dibanding longsor yang cenderung terlokalisasi.

Insight inilah yang nantinya menjadi dasar rekomendasi.

---

# Tahap 7 — Storytelling Data

Sebelum membuat dashboard, kita menyusun alur cerita analisis.

Sebagai contoh:

1. Gambaran umum kejadian bencana.
2. Perubahan jumlah kejadian dari waktu ke waktu.
3. Wilayah dengan intensitas tertinggi.
4. Jenis bencana yang mendominasi.
5. Dampak terhadap masyarakat dan infrastruktur.
6. Hubungan antara lokasi, waktu, dan jenis bencana.
7. Kesimpulan serta rekomendasi.

Dengan alur ini, dashboard tidak hanya menjadi kumpulan grafik, tetapi menyampaikan narasi yang logis.

---

# Tahap 8 — Visualisasi Dinamis

Barulah setelah seluruh analisis selesai, kita menentukan visualisasi yang paling tepat untuk setiap insight.

Prinsipnya adalah:

| Tujuan Analisis       | Visualisasi yang Tepat                  |
| --------------------- | --------------------------------------- |
| Tren waktu            | Line chart, area chart                  |
| Perbandingan kategori | Bar chart                               |
| Proporsi              | Donut chart (digunakan secara terbatas) |
| Distribusi spasial    | Peta interaktif, heatmap                |
| Ranking wilayah       | Horizontal bar chart                    |
| Korelasi numerik      | Scatter plot                            |
| Ringkasan operasional | KPI cards dan tabel interaktif          |

Visualisasi dipilih berdasarkan kebutuhan analisis, bukan sebaliknya.

---

## Pendekatan Kerja yang Saya Usulkan

Agar proyek ini terstruktur dan dapat berkembang, saya menyarankan kita membaginya menjadi empat fase utama:

1. **Audit Data**: memahami struktur, kualitas, dan karakteristik dataset.
2. **Analisis Mendalam**: melakukan EDA, analisis statistik, serta menyusun insight yang relevan bagi BPBD.
3. **Perancangan Visualisasi**: memilih bentuk visual yang paling tepat untuk menyampaikan setiap insight.
4. **Implementasi**: membangun visualisasi web dinamis yang membaca data terbaru tanpa mengubah konsep analisis yang telah disepakati.
