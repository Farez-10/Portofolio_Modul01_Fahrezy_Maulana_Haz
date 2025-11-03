-- 1. Buat database dan gunakan
CREATE DATABASE IF NOT EXISTS portal_pelamar;
USE portal_pelamar;

-- 2. Tabel data pelamar
CREATE TABLE IF NOT EXISTS pelamar (
    ID VARCHAR(10) PRIMARY KEY,
    Nama VARCHAR(100) NOT NULL,
    Posisi VARCHAR(50) NOT NULL,
    Pengalaman VARCHAR(50),
    Pendidikan VARCHAR(100),
    Kontak VARCHAR(20),
    Email VARCHAR(100),
    Status ENUM('Menunggu', 'Lolos Administrasi', 'Lolos Interview', 'Tidak Lolos') DEFAULT 'Menunggu'
);

-- 3. Tabel riwayat perubahan
CREATE TABLE IF NOT EXISTS riwayat_perubahan (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Waktu DATETIME NOT NULL,
    Admin VARCHAR(50) NOT NULL,
    ID_Pelamar VARCHAR(10),
    Kolom VARCHAR(50),
    Dari TEXT,
    Ke TEXT,
    FOREIGN KEY (ID_Pelamar) REFERENCES pelamar(ID) ON DELETE SET NULL
);

-- 4. Tabel admin (login)
CREATE TABLE IF NOT EXISTS admin_hrd (
    Username VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(100) NOT NULL
);

-- 5. Isi akun admin (opsional)
INSERT INTO admin_hrd (Username, Password) VALUES
('farez', '12345'),
('matteo', '67890')
ON DUPLICATE KEY UPDATE Password=VALUES(Password);

USE portal_pelamar;
SELECT * FROM pelamar;
SELECT * FROM admin_hrd;
