# Portal Pelamar PT. Rimbo Peraduan

Sebuah aplikasi **manajemen data pelamar berbasis Python dan MySQL**, yang dibuat untuk membantu admin HRD dalam mengelola proses rekrutmen — mulai dari input data, menampilkan data, mengedit status, hingga menghapus pelamar.

Program ini dapat dijalankan dalam dua mode:
- **In-Memory Mode** → data hanya tersimpan sementara di RAM.
- **Database Mode** → data disimpan dan dimuat langsung dari MySQL.

---

## Fitur Utama

 Login Admin (verifikasi username & password)  
 Tambah data pelamar  
 Lihat semua data pelamar  
 Ubah status pelamar (misalnya: *Menunggu → Lolos Interview*)  
 Hapus data pelamar  
 Pencarian data berdasarkan ID  
 Sinkronisasi otomatis ke database (jika kosong, data awal akan dimasukkan otomatis)  
 Tampilan terminal bergaya HR Portal  

---

##  Struktur Database (MySQL)

```sql
CREATE DATABASE portal_pelamar;
USE portal_pelamar;

CREATE TABLE pelamar (
    ID VARCHAR(10) PRIMARY KEY,
    Nama VARCHAR(100),
    Posisi VARCHAR(100),
    Pengalaman VARCHAR(50),
    Pendidikan VARCHAR(50),
    Kontak VARCHAR(20),
    Email VARCHAR(100),
    Status VARCHAR(50)
);
```

---

##  Cara Menjalankan Program

### 1 Instal library yang diperlukan
```bash
pip install mysql-connector-python
```

### 2 Konfigurasi Koneksi Database
Edit di `portal_pelamar.py`:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "2003",
    "database": "portal_pelamar",
    "port": 3306
}
```

### 3 Jalankan Program
```bash
python portal_pelamar.py
```

Jika tabel kosong, sistem otomatis akan menyinkronkan 3 data default dari `self.data_pelamar`.

---

## Data Awal

| ID | Nama | Posisi | Pengalaman | Pendidikan | Kontak | Email | Status |
|----|-------|---------|-------------|-------------|---------|--------|--------|
| P001 | Fahrezy Maulana Haz | Surveyor | 2 tahun | S1 Teknik Geodesi | 089509125473 | farez@gmail.com | Lolos Interview |
| P002 | Jimmy Neutron | IT Support | 1 tahun | D3 Teknik Informatika | 089876543210 | jimmy@gmail.com | Menunggu |
| P003 | Sandy Cheeks | Safety Officer | 3 tahun | S1 Teknik K3 | 081234567891 | sandy@gmail.com | Menunggu |

---

## Login Admin

```
Username: farez
Password: 12345
```
