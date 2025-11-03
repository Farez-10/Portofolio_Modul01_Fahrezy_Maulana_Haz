# ==============================================================
# PORTAL PELAMAR KARYAWAN PT. RIMBO PERADUAN
# Versi: Class-based + Export CSV + in-memory/MySQL Hybrid (Auto Sync)
# ==============================================================

import datetime
import csv
import mysql.connector

use_db = True  # ubah ke False jika tidak ingin pakai MySQL

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "2003",
    "database": "portal_pelamar",
    "port": 3306
}

# ==============================================================
# CLASS PORTAL PELAMAR
# ==============================================================

class PortalPelamar:
    def __init__(self):
        self.data_pelamar = [
            {
                "ID": "P001",
                "Nama": "Fahrezy Maulana Haz",
                "Posisi": "Surveyor",
                "Pengalaman": "2 tahun",
                "Pendidikan": "S1 Teknik Geodesi",
                "Kontak": "089509125473",
                "Email": "farez@gmail.com",
                "Status": "Lolos Interview"
            },
            {
                "ID": "P002",
                "Nama": "Jimmy Neutron",
                "Posisi": "IT Support",
                "Pengalaman": "1 tahun",
                "Pendidikan": "D3 Teknik Informatika",
                "Kontak": "089876543210",
                "Email": "jimmy@gmail.com",
                "Status": "Menunggu"
            },
            {
                "ID": "P003",
                "Nama": "Sandy Cheeks",
                "Posisi": "Safety Officer",
                "Pengalaman": "3 tahun",
                "Pendidikan": "S1 Teknik K3",
                "Kontak": "081234567891",
                "Email": "sandy@gmail.com",
                "Status": "Menunggu"
            }
        ]
        self.riwayat_perubahan = []
        self.akun_login = {"farez": "12345", "matteo": "67890"}
        self.user_login = None

        # koneksi ke database jika diaktifkan
        if use_db:
            self.koneksi_mysql()

    # ----------------------------------------------------------
    # Koneksi dan Sinkronisasi Database
    # ----------------------------------------------------------
    def koneksi_mysql(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("Koneksi ke MySQL berhasil.")
            self.buat_tabel_jika_belum_ada()
            self.sinkronisasi_awal()
            self.muatan_awal_db()
        except mysql.connector.Error as err:
            print(f"Gagal koneksi ke database: {err}")
            self.conn = None
            self.cursor = None

    def buat_tabel_jika_belum_ada(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pelamar (
                ID VARCHAR(10) PRIMARY KEY,
                Nama VARCHAR(100),
                Posisi VARCHAR(50),
                Pengalaman VARCHAR(50),
                Pendidikan VARCHAR(100),
                Kontak VARCHAR(20),
                Email VARCHAR(100),
                Status VARCHAR(50)
            )
        """)
        self.conn.commit()

    def sinkronisasi_awal(self):
        self.cursor.execute("SELECT COUNT(*) FROM pelamar")
        count = self.cursor.fetchone()[0]
        if count == 0:
            for p in self.data_pelamar:
                self.cursor.execute("""
                    INSERT INTO pelamar (ID, Nama, Posisi, Pengalaman, Pendidikan, Kontak, Email, Status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (p["ID"], p["Nama"], p["Posisi"], p["Pengalaman"],
                      p["Pendidikan"], p["Kontak"], p["Email"], p["Status"]))
            self.conn.commit()
            print(f"{len(self.data_pelamar)} data pelamar awal berhasil dimasukkan ke database.")
        else:
            print(f"Tabel sudah berisi {count} data. Tidak perlu sinkronisasi awal.")

    def muatan_awal_db(self):
        self.cursor.execute("SELECT * FROM pelamar")
        hasil = self.cursor.fetchall()
        self.data_pelamar = [
            {
                "ID": row[0],
                "Nama": row[1],
                "Posisi": row[2],
                "Pengalaman": row[3],
                "Pendidikan": row[4],
                "Kontak": row[5],
                "Email": row[6],
                "Status": row[7]
            }
            for row in hasil
        ]
        print(f"\n{len(self.data_pelamar)} data pelamar berhasil dimuat dari database.\n")

    # ----------------------------------------------------------
    # Validasi Input
    # ----------------------------------------------------------
    def input_tidak_kosong(self, pesan):
        while True:
            data = input(pesan).strip()
            if data == "":
                print("Input tidak boleh kosong!")
            else:
                return data

    def validasi_email(self):
        while True:
            email = input("Email: ").strip().lower()
            if not email.endswith("@gmail.com"):
                print("Email harus menggunakan domain @gmail.com!")
            elif " " in email or len(email) < 12:
                print("Email tidak valid!")
            else:
                return email

    def validasi_nomor(self):
        while True:
            kontak = input("Nomor HP: ").strip()
            if not kontak.isdigit():
                print("Nomor HP hanya boleh angka!")
            elif len(kontak) < 10:
                print("Nomor HP terlalu pendek!")
            else:
                return kontak

    # ----------------------------------------------------------
    # Login
    # ----------------------------------------------------------
    def login(self):
        percobaan = 3
        while percobaan > 0:
            print("=== LOGIN ADMIN HRD ===")
            user = input("Masukkan Username : ").strip()
            pwd = input("Masukkan Password : ").strip()

            if user in self.akun_login and self.akun_login[user] == pwd:
                self.user_login = user
                print(f"\nLogin berhasil! Selamat datang, {user.title()}.\n")
                return True
            else:
                percobaan -= 1
                print(f"Username atau password salah! Sisa percobaan: {percobaan}\n")

        print("Anda telah 3 kali gagal login. Kembali ke menu utama.\n")
        return False

    # ----------------------------------------------------------
    # Generate ID Otomatis
    # ----------------------------------------------------------
    def generate_id_otomatis(self):
        if not self.data_pelamar:
            return "P001"
        last_id = max(int(p["ID"][1:]) for p in self.data_pelamar)
        return f"P{last_id + 1:03d}"

    # ----------------------------------------------------------
    # CRUD - Read
    # ----------------------------------------------------------
    def tampilkan_semua_data(self):
        if not self.data_pelamar:
            print("\nBelum ada data pelamar.\n")
            return
        print("\nDAFTAR DATA PELAMAR\n")
        print("=" * 120)
        print(f"{'ID':<6} {'Nama':<25} {'Posisi':<20} {'Pendidikan':<25} {'Pengalaman':<12} {'Status':<15}")
        print("-" * 120)
        for p in self.data_pelamar:
            print(f"{p['ID']:<6} {p['Nama']:<25} {p['Posisi']:<20} {p['Pendidikan']:<25} {p['Pengalaman']:<12} {p['Status']:<15}")
        print("=" * 120)

    def cari_data(self):
        cari_id = self.input_tidak_kosong("Masukkan ID Pelamar: ").upper()
        for p in self.data_pelamar:
            if p["ID"] == cari_id:
                print("\nDATA DITEMUKAN:\n")
                for k, v in p.items():
                    print(f"{k:<15}: {v}")
                return
        print("\nData tidak ditemukan.\n")

    # ----------------------------------------------------------
    # CRUD - Create
    # ----------------------------------------------------------
    def tambah_data(self):
        print("\n=== TAMBAH DATA PELAMAR ===")
        id_baru = self.generate_id_otomatis()
        print(f"ID Pelamar otomatis: {id_baru}")

        nama = self.input_tidak_kosong("Nama: ")
        posisi = self.input_tidak_kosong("Posisi dilamar: ")
        pengalaman = self.input_tidak_kosong("Pengalaman: ")
        pendidikan = self.input_tidak_kosong("Pendidikan: ")
        kontak = self.validasi_nomor()
        email = self.validasi_email()
        status = self.input_tidak_kosong("Status: ")

        simpan = input("Simpan data ini? (Y/N): ").upper()
        if simpan != "Y":
            print("Data batal disimpan.")
            return

        data_baru = {
            "ID": id_baru,
            "Nama": nama,
            "Posisi": posisi,
            "Pengalaman": pengalaman,
            "Pendidikan": pendidikan,
            "Kontak": kontak,
            "Email": email,
            "Status": status
        }

        self.data_pelamar.append(data_baru)
        if use_db:
            self.cursor.execute("""
                INSERT INTO pelamar (ID, Nama, Posisi, Pengalaman, Pendidikan, Kontak, Email, Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(data_baru.values()))
            self.conn.commit()

        print(f"\nData {nama} berhasil ditambahkan.\n")

    # ----------------------------------------------------------
    # CRUD - Update
    # ----------------------------------------------------------
    def ubah_data(self):
        print("\n=== UBAH DATA PELAMAR ===")
        self.tampilkan_semua_data()
        id_edit = self.input_tidak_kosong("Masukkan ID Pelamar yang ingin diubah: ").upper()
        for p in self.data_pelamar:
            if p["ID"] == id_edit:
                print(f"\nData ditemukan untuk {p['Nama']}.")
                kolom_opsi = ["Nama", "Posisi", "Pengalaman", "Pendidikan", "Kontak", "Email", "Status"]
                for i, kolom in enumerate(kolom_opsi, start=1):
                    print(f"{i}. {kolom}")
                pilihan = input("Pilih kolom (1-7): ")
                if not (pilihan.isdigit() and 1 <= int(pilihan) <= 7):
                    print("Pilihan tidak valid!")
                    return
                kolom = kolom_opsi[int(pilihan) - 1]
                nilai_lama = p[kolom]
                if kolom == "Email":
                    nilai_baru = self.validasi_email()
                elif kolom == "Kontak":
                    nilai_baru = self.validasi_nomor()
                else:
                    nilai_baru = self.input_tidak_kosong(f"Nilai baru untuk {kolom}: ")
                p[kolom] = nilai_baru

                if use_db:
                    self.cursor.execute(f"UPDATE pelamar SET {kolom}=%s WHERE ID=%s", (nilai_baru, id_edit))
                    self.conn.commit()

                self.riwayat_perubahan.append({
                    "Waktu": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Admin": self.user_login,
                    "ID": id_edit,
                    "Kolom": kolom,
                    "Dari": nilai_lama,
                    "Ke": nilai_baru
                })
                print(f"Data '{kolom}' berhasil diubah dari '{nilai_lama}' menjadi '{nilai_baru}'.")
                return
        print("Data tidak ditemukan.")

    # ----------------------------------------------------------
    # CRUD - Delete
    # ----------------------------------------------------------
    def hapus_data(self):
        print("\n=== HAPUS DATA PELAMAR ===")
        self.tampilkan_semua_data()
        id_hapus = self.input_tidak_kosong("Masukkan ID Pelamar yang ingin dihapus: ").upper()
        for p in self.data_pelamar[:]:
            if p["ID"] == id_hapus:
                konfirmasi = input(f"Yakin ingin menghapus {p['Nama']}? (Y/N): ").upper()
                if konfirmasi == "Y":
                    self.data_pelamar.remove(p)
                    if use_db:
                        self.cursor.execute("DELETE FROM pelamar WHERE ID=%s", (id_hapus,))
                        self.conn.commit()
                    self.riwayat_perubahan.append({
                        "Waktu": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        "Admin": self.user_login,
                        "ID": id_hapus,
                        "Kolom": "DELETE",
                        "Dari": p["Nama"],
                        "Ke": "Deleted"
                    })
                    print("Data berhasil dihapus.")
                return
        print("Data tidak ditemukan.")

    # ----------------------------------------------------------
    # HISTORY
    # ----------------------------------------------------------
    def tampilkan_riwayat(self):
        print("\n=== RIWAYAT PERUBAHAN DATA ===")
        if not self.riwayat_perubahan:
            print("Belum ada riwayat perubahan data.")
            return
        print("=" * 110)
        print(f"{'Waktu':<20} {'Admin':<10} {'ID':<10} {'Kolom':<15} {'Dari':<20} {'Ke':<20}")
        print("-" * 110)
        for r in self.riwayat_perubahan:
            print(f"{r['Waktu']:<20} {r['Admin']:<10} {r['ID']:<10} {r['Kolom']:<15} {r['Dari']:<20} {r['Ke']:<20}")
        print("=" * 110)

    # ----------------------------------------------------------
    # EXPORT CSV
    # ----------------------------------------------------------
    def export_csv(self):
        if not self.data_pelamar:
            print("\nTidak ada data untuk diexport.\n")
            return
        with open("data_pelamar.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.data_pelamar[0].keys())
            writer.writeheader()
            writer.writerows(self.data_pelamar)
        print("\nData pelamar berhasil diexport ke file 'data_pelamar.csv'.\n")

    # ----------------------------------------------------------
    # MENU UTAMA
    # ----------------------------------------------------------
    def menu_utama(self):
        while True:
            print("=" * 70)
            print("=== MENU UTAMA PORTAL PELAMAR ===")
            print("1. Tampilkan Data Pelamar")
            print("2. Tambah Data Pelamar")
            print("3. Ubah Data Pelamar")
            print("4. Hapus Data Pelamar")
            print("5. Tampilkan Riwayat")
            print("6. Export Data ke CSV")
            print("7. Logout")
            pilihan = input("Pilih menu (1-7): ").strip()

            if pilihan == "1":
                self.tampilkan_semua_data()
            elif pilihan == "2":
                self.tambah_data()
            elif pilihan == "3":
                self.ubah_data()
            elif pilihan == "4":
                self.hapus_data()
            elif pilihan == "5":
                self.tampilkan_riwayat()
            elif pilihan == "6":
                self.export_csv()
            elif pilihan == "7":
                print("\nLogout berhasil. Kembali ke menu login.\n")
                break
            else:
                print("Pilihan tidak valid!\n")


# ==============================================================
# PROGRAM UTAMA
# ==============================================================
if __name__ == "__main__":
    portal = PortalPelamar()
    while True:
        print("=" * 70)
        print("=== SELAMAT DATANG DI PORTAL PELAMAR PT. RIMBO PERADUAN ===")
        print("1. Login")
        print("2. Exit")
        pilihan = input("Pilih menu (1/2): ").strip()
        if pilihan == "1":
            if portal.login():
                portal.menu_utama()
        elif pilihan == "2":
            print("\nTerima kasih telah menggunakan Portal Pelamar. Sampai jumpa!\n")
            break
        else:
            print("\nPilihan tidak valid!\n")
