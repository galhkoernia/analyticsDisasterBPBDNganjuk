# Disaster Analytics Engine

Disaster Analytics Engine merupakan sistem analisis data kebencanaan yang dirancang untuk mengubah data operasional menjadi informasi, insight, dan visualisasi yang dapat mendukung proses pengambilan keputusan.

Sistem ini **bukan dashboard**, melainkan sebuah **Analytics Engine** yang menjadi fondasi berbagai aplikasi visualisasi maupun dashboard di masa mendatang.

Seluruh pengembangan dilakukan secara modular sehingga setiap komponen dapat dikembangkan tanpa mengubah struktur sistem yang telah ada.

---

# Tujuan Proyek

Membangun platform analisis data kebencanaan yang mampu:

- Memahami karakteristik dataset.
- Melakukan validasi kualitas data.
- Membersihkan data secara otomatis.
- Menghasilkan profil data.
- Melakukan Exploratory Data Analysis (EDA).
- Menyediakan analisis statistik.
- Menghasilkan insight secara otomatis.
- Menyediakan visualisasi interaktif.
- Menjadi fondasi dashboard operasional.

---

# Filosofi Sistem

Analytics Engine dikembangkan berdasarkan prinsip bahwa visualisasi bukan merupakan tujuan utama.

Alur kerja sistem adalah:

```
Raw Dataset
      │
      ▼
Data Validation
      │
      ▼
Data Cleaning
      │
      ▼
Data Profiling
      │
      ▼
Exploratory Data Analysis
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
Dashboard
```

Dashboard hanyalah salah satu media penyajian hasil analisis.

Seluruh logika analisis berada di dalam Analytics Engine.

---

# Arsitektur Pengembangan

Pengembangan dilakukan secara bertahap.

## Phase 1

Data Understanding

Tujuan

- Membaca dataset
- Membaca metadata
- Mengidentifikasi struktur data
- Mengidentifikasi tipe data
- Statistik dasar

Output

- Dataset Summary

---

## Phase 2

Data Quality Assessment

Tujuan

- Missing Value Detection
- Duplicate Detection
- Consistency Checking
- Coordinate Validation
- Datetime Validation
- Numeric Validation

Output

- Data Quality Report

---

## Phase 3

Data Preprocessing

Tujuan

- Cleaning
- Transformation
- Feature Engineering

Output

- Clean Dataset

---

## Phase 4

Exploratory Data Analysis

Analisis meliputi

- Temporal Analysis
- Spatial Analysis
- Disaster Analysis
- Impact Analysis
- Operational Analysis

Output

- Insight awal
- Grafik eksplorasi

---

## Phase 5

Statistical Analysis

Analisis statistik meliputi

- Distribusi Data
- Korelasi
- Cross Tabulation
- Trend Analysis
- Comparative Analysis

Output

- Statistical Report

---

## Phase 6

Insight Generator

Tujuan

Menghasilkan insight otomatis berdasarkan pola data.

Contoh

- Wilayah paling rawan.
- Jenis bencana dominan.
- Dampak terbesar.
- Pola kejadian.
- Perubahan tren.

---

## Phase 7

Visualization

Output

- Interactive Chart
- Interactive Map
- Dashboard Component
- Report Visualization

---

# Struktur Proyek

```
disaster-analytics/

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
│
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
├── requirements.txt
└── README.md
```

---

# Prinsip Modular

Setiap modul hanya memiliki satu tanggung jawab.

| Modul | Tanggung Jawab |
|---------|----------------|
| ingestion | Membaca dataset |
| quality | Pemeriksaan kualitas data |
| preprocessing | Pembersihan dan transformasi data |
| analysis | Analisis data |
| visualization | Visualisasi hasil analisis |
| utils | Fungsi pendukung |
| config | Konfigurasi sistem |

Seluruh modul bersifat reusable dan independen.

---

# Teknologi

Bahasa

- Python 3.12+

Library

- pandas
- numpy
- openpyxl
- scipy
- matplotlib
- plotly
- folium
- scikit-learn
- pathlib
- logging

Belum menggunakan

- Database
- REST API
- Framework Web

Seluruh proses dijalankan secara lokal.

---

# Data Pipeline

```
Dataset
    │
    ▼
Loader
    │
    ▼
Validation
    │
    ▼
Quality Assessment
    │
    ▼
Cleaning
    │
    ▼
Transformation
    │
    ▼
Feature Engineering
    │
    ▼
Analysis
    │
    ▼
Insight
    │
    ▼
Visualization
```

Pipeline dibuat modular sehingga setiap tahap dapat dijalankan secara mandiri.

---

# Standar Coding

Seluruh pengembangan mengikuti prinsip berikut.

- Clean Code
- Modular Architecture
- Single Responsibility Principle
- Reusable Function
- Maintainable Code
- Readable Code
- Type Hint
- Relative Path
- Logging
- Error Handling

Komentar dibuat singkat dan hanya menjelaskan tujuan kode.

---

# Output Sistem

Analytics Engine akan menghasilkan beberapa keluaran.

## Data Quality

- Dataset Summary
- Missing Value Report
- Duplicate Report
- Consistency Report
- Coordinate Report
- Datetime Report
- Numeric Report
- Data Quality Score

---

## Analysis

- Temporal Analysis
- Spatial Analysis
- Disaster Analysis
- Impact Analysis
- Operational Analysis

---

## Visualization

- Interactive Chart
- Interactive Map
- Statistical Graph
- Insight Visualization

---

## Report

- HTML Report
- Excel Report
- PDF Report

---


# Visi Proyek

Disaster Analytics Engine dikembangkan sebagai fondasi analisis data kebencanaan yang modular, dapat dikembangkan secara berkelanjutan, dan mampu menghasilkan informasi yang mendukung proses pengambilan keputusan berbasis data.

Dengan memisahkan proses analisis dari proses visualisasi, sistem ini dapat digunakan kembali pada berbagai platform seperti dashboard web, aplikasi desktop, maupun layanan API tanpa mengubah logika inti analisis.