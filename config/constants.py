#
# Created on Thu Jul 02 2026
#
# Copyright (c) 2026 Your Company
#

"""Konstanta domain sistem. """

from typing import Final

# Dataset / Schema

RAW_COLUMN_MAP: Final[dict[str, str]] = {

    # Metadata
    "timestamp": "Timestamp",
    "kode_klasifikasi": "KODE KLASIFIKASI KEJADIAN ",
    "nomor_surat_laporan": "NOMOR SURAT LAPORAN KEJADIAN",
    "nama_petugas": "NAMA PETUGAS BPBD",
    "nip": "NIP/NOMOR IDENTITAS ",

    # Temporal
    "tanggal_pelaporan": "TANGGAL PELAPORAN",
    "waktu_pelaporan": "WAKTU PELAPORAN KEJADIAN",
    "tanggal_kejadian": "TANGGAL KEJADIAN",
    "waktu_kejadian": "WAKTU KEJADIAN",

    # Lokasi
    "koordinat": "KOORDINAT LOKASI KEJADIAN",
    "rt_rw": "RT/RW/DUSUN",
    "desa": "DESA/KELURAHAN ",
    "kecamatan": "KECAMATAN",

    # Karakteristik
    "jenis_bencana": "JENIS BENCANA / KEJADIAN ",
    "penyebab": "PENYEBAB KEJADIAN",
    "kronologi": "KRONOLOGI KEJADIAN ",

    # Dampak
    "korban_meninggal": "KORBAN MENINGGAL \nket. Jumlah_Rincinan Nama \nJika tidak ada disi ( - ) / Nihil ",
    "korban_luka": "LUKA BERAT / RINGAN / SEDANG \nKet. Luka Berat_Angka dst. \nJika tidak ada disi ( - ) / Nihil ",
    "korban_hilang": "KORBAN DALAM PENCARIAN  \nket. Jumlah_Rincian Nama \n( Jika tidak ada disi ( - ) / Nihil ) ",
    "pengungsi": "Jumlah Pengungsi / Terdampak \n(orang/kk)  Jika tidak ada disi ( - ) / Nihil ",

    "rumah_rusak_berat": "RUMAH RUSAK BERAT",
    "rumah_rusak_sedang": "RUMAH RUSAK SEDANG",
    "rumah_rusak_ringan": "RUMAH RUSAK RINGAN",

    "fasilitas_umum": "FASILITAS UMUM TERDAMPAK ",
    "kerusakan_fasilitas": "KETERANGAN KERUSAKAN FASUM \n( diisi dengan jumlah unit yang rusak, nama infrastruktur yang rusak dan Rincinan kerusakan ) \nContoh : 2 unit bangunan Pasar Pringgondani P : 3 m L : 3 m dst.",
    "kerugian": "KERUSAKAN MATERIAL",
    "dampak_lainnya": "KETERANGAN DAMPAK LAINNYA",

    # Operasional
    "status_penanganan": "Status Penanganan Saat Ini ",
    "upaya_penanganan": "UPAYA YANG TELAH DILAKSANAKAN",
    "rencana_tindak_lanjut": "RENCANA TINDAK LANJUT",
    "kebutuhan": "Kebutuhan Mendesak",
    "personil_terlibat": "PERSONIL TERLIBAT",

    "kendala": "Kendala / Hambatan  di Lapangan ",
    "kondisi_terkini": "KONDISI TERKINI ",

    "upload_foto_video": "Upload Foto / Video Kejadian ",
    "sumber_informasi": "SUMBER INFORMASI",

}

# Validation / Quality Contracts

# Missing Value
# Kolom yang secara business-rule boleh memiliki missing values tanpa menurunkan skor
ACCEPTABLE_MISSING_COLUMNS: Final[set[str]] = {
    "nomor_surat_laporan",
}

# Consistency Checking (categorical)
CATEGORICAL_CONSISTENCY_COLUMNS: Final[list[str]] = [
    "kecamatan",
    "desa",
    "jenis_bencana",
    "status_penanganan",
]

# Duplicate Detection
DUPLICATE_KEY_COLUMNS: Final[list[str]] = [
    "kode_klasifikasi",
    "nomor_surat_laporan",
]

# Coordinate Validation
NGANJUK_BBOX: Final[dict[str, float]] = {
    "lat_min": -7.80,
    "lat_max": -7.20,
    "lon_min": 111.70,
    "lon_max": 112.10,
}

# Numeric Validation
NON_NEGATIVE_NUMERIC_COLUMNS: Final[list[str]] = [
    "kerugian",
]

# Data Quality Score
QUALITY_SCORE_WEIGHTS: Final[dict[str, float]] = {
    "completeness": 30,
    "consistency": 20,
    "coordinate_validity": 20,
    "temporal_validity": 15,
    "numeric_validity": 15,
}

