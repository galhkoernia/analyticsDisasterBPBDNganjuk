# Tahap 1 — Data Understanding

Berdasarkan dataset yang Anda unggah, hasil identifikasi awal adalah sebagai berikut.

## Ringkasan Dataset

| Parameter           | Hasil                          |
| ------------------- | ------------------------------ |
| Jumlah data         | 73 kejadian                    |
| Jumlah atribut      | 36 kolom                       |
| Format              | Excel                          |
| Data duplikat penuh | Tidak ditemukan                |
| Tipe data           | 32 Object, 3 Datetime, 1 Float |

---

## Karakteristik Data

Saya mengelompokkan atribut menjadi beberapa domain.

### 1. Metadata Laporan

Contoh:

* Timestamp
* Kode klasifikasi
* Nomor laporan
* Nama petugas
* NIP

Fungsi:

Sebagai identitas administrasi.

Analisis:

Tidak perlu divisualisasikan.

---

### 2. Temporal

Contoh:

* Tanggal pelaporan
* Waktu pelaporan
* Tanggal kejadian
* Waktu kejadian

Potensi analisis:

* Tren bulanan
* Tren tahunan
* Distribusi jam
* Hari dengan kejadian terbanyak
* Selisih waktu kejadian–pelaporan (response delay)

---

### 3. Lokasi

Contoh:

* Koordinat
* RT/RW
* Desa
* Kecamatan

Potensi analisis:

* Persebaran spasial
* Hotspot
* Ranking wilayah
* Frekuensi per kecamatan
* Frekuensi per desa

---

### 4. Karakteristik Bencana

Contoh:

* Jenis bencana
* Penyebab
* Kronologi

Potensi analisis:

* Distribusi jenis
* Penyebab dominan
* Pola kejadian

---

### 5. Dampak

Contoh:

* Korban
* Rumah rusak
* Kerugian
* Dampak lain

Potensi analisis:

* Severity Index
* Dampak per wilayah
* Dampak per jenis

---

### 6. Operasional

Contoh:

* Personel
* Kebutuhan
* Upaya
* Dokumentasi

Potensi analisis:

* Distribusi personel
* Kebutuhan terbanyak
* Evaluasi operasional

---

## Kesimpulan Tahap 1

Dataset ini **bukan sekadar data statistik**, melainkan **data operasional kejadian**. Artinya, analisis kita nantinya harus menggabungkan:

* analisis waktu,
* analisis wilayah,
* analisis dampak,
* analisis operasional.

Dengan demikian, dashboard yang dibangun akan memiliki nilai analitis, bukan hanya menampilkan jumlah kejadian.

---

# Tahap 2 — Data Quality Assessment

Tahap ini bertujuan mengevaluasi apakah data sudah layak dianalisis.

## 1. Missing Value

Hasil pemeriksaan awal menunjukkan beberapa kolom memiliki nilai kosong.

| Kolom                     | Jumlah Kosong |
| ------------------------- | ------------: |
| Upload Foto/Video         |            19 |
| Nomor Surat Laporan       |            13 |
| Keterangan Dampak Lainnya |             7 |
| Personil Terlibat         |             1 |

### Interpretasi

**Upload Foto**

Bukan masalah kualitas data, karena dokumentasi tidak selalu tersedia.

Status:

**Dapat diterima.**

---

**Nomor Surat Laporan**

Perlu ditinjau lebih lanjut.

Kemungkinan:

* laporan belum diterbitkan,
* kejadian masih awal,
* kesalahan input.

Ini merupakan atribut administrasi sehingga perlu aturan validasi.

---

**Keterangan Dampak Lainnya**

Normal.

Tidak semua kejadian memiliki dampak tambahan.

---

**Personil**

Hanya satu data kosong.

Tidak signifikan.

---

## 2. Duplicate

Hasil awal:

* Tidak ada baris yang identik sepenuhnya.
* Namun terdapat **16 nilai nomor surat yang berulang**.

Hal ini **belum tentu merupakan kesalahan**. Kemungkinan penyebabnya antara lain:

* satu nomor surat digunakan untuk beberapa entri terkait,
* adanya pembaruan terhadap laporan yang sama,
* atau memang terjadi duplikasi administrasi.

Langkah berikutnya adalah mengidentifikasi pola pengulangan tersebut sebelum memutuskan apakah perlu dibersihkan.

---

## 3. Konsistensi

Tahap berikutnya yang belum dilakukan meliputi:

* konsistensi penulisan nama kecamatan,
* konsistensi nama desa,
* konsistensi jenis bencana,
* konsistensi format koordinat,
* konsistensi penulisan penyebab.

Contoh masalah yang sering muncul:

```
Nganjuk
Kec. Nganjuk
NGANJUK
```

Ketiganya harus distandarkan menjadi satu nilai.

---

## 4. Validitas Koordinat

Koordinat perlu diperiksa:

* format latitude/longitude,
* apakah dapat dipetakan,
* apakah berada di wilayah Kabupaten Nganjuk,
* apakah terdapat koordinat kosong atau tidak valid.

Tahap ini sangat penting sebelum membuat analisis spasial.

---

## 5. Validitas Waktu

Beberapa pemeriksaan yang perlu dilakukan:

* tanggal kejadian setelah tanggal pelaporan (indikasi kesalahan),
* format tanggal seragam,
* jam valid,
* tidak ada tanggal di masa depan.

---

## 6. Pemeriksaan Nilai Numerik

Seluruh atribut numerik perlu divalidasi, misalnya:

* korban tidak boleh negatif,
* kerugian tidak boleh negatif,
* jumlah rumah rusak tidak boleh negatif,
* nilai ekstrem perlu diverifikasi.

---

# Deliverable Tahap 2

Saya mengusulkan setiap dataset yang masuk akan menghasilkan **Data Quality Report** otomatis dengan komponen:

* Ringkasan dataset (jumlah data, kolom, tipe data).
* Persentase missing value per kolom.
* Deteksi duplikasi.
* Pemeriksaan konsistensi kategori.
* Validasi koordinat.
* Validasi tanggal dan waktu.
* Pemeriksaan nilai numerik.
* Daftar anomali yang memerlukan verifikasi.
* Skor kualitas data (Data Quality Score) berdasarkan aturan yang kita tetapkan.

Laporan ini menjadi prasyarat sebelum analisis lanjutan dilakukan.

---

# Konsep Teknologi

Saya menyarankan kita **tidak langsung membuat aplikasi web**, tetapi membangun **platform analisis** yang modular.

Arsitektur sederhananya:

```text
Excel / CSV
      │
      ▼
Data Loader
      │
      ▼
Data Validation
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Analysis Engine
      │
      ▼
Visualization Engine
      │
      ▼
Dashboard
```

Setiap tahap berdiri sendiri sehingga mudah diuji dan dikembangkan.

---

# Struktur Folder yang Direkomendasikan

```text
disaster-analytics/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
│
├── config/
│   ├── settings.py
│   └── constants.py
│
├── modules/
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── validator.py
│   │
│   ├── quality/
│   │   ├── missing.py
│   │   ├── duplicate.py
│   │   ├── consistency.py
│   │   ├── coordinate.py
│   │   └── report.py
│   │
│   ├── preprocessing/
│   │   ├── cleaner.py
│   │   ├── transformer.py
│   │   └── feature_engineering.py
│   │
│   ├── analysis/
│   │   ├── temporal.py
│   │   ├── spatial.py
│   │   ├── disaster.py
│   │   ├── impact.py
│   │   ├── operational.py
│   │   └── statistics.py
│   │
│   ├── visualization/
│   │   ├── charts.py
│   │   ├── maps.py
│   │   └── export.py
│   │
│   └── utils/
│       ├── logger.py
│       └── helper.py
│
├── outputs/
│   ├── reports/
│   ├── figures/
│   └── dashboard/
│
├── main.py
└── requirements.txt
```

## Mengapa struktur ini?

* **Setiap folder merepresentasikan satu tahap analisis**, sehingga mudah dipelihara.
* Penambahan analisis baru cukup membuat modul baru di `modules/analysis`.
* Perubahan aturan validasi tidak memengaruhi modul analisis.
* Nantinya dashboard hanya mengonsumsi hasil dari `outputs/` atau langsung memanggil modul analisis.

## Rekomendasi Teknologi

Saya menyarankan tetap sesederhana mungkin:

* **Bahasa**: Python 3.12+
* **Data Processing**: pandas, numpy
* **Validasi Data**: pandera (opsional pada tahap awal)
* **Visualisasi**: Plotly (interaktif) dan Folium/Leaflet untuk peta
* **Dashboard**: Streamlit (prototipe cepat) atau FastAPI + frontend jika kebutuhan berkembang
* **Konfigurasi**: `pyproject.toml` untuk manajemen proyek modern

