# -*- coding: utf-8 -*-
"""MODUL 2 – Fitur-fitur karakteristik pemrograman fungsional (Effect-free programming)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n0zj-kXl2T5s_1tAg1uqC8JoD58mlR5-

MODUL 2 – Fitur-fitur karakteristik pemrograman fungsional (Effect-free programming)

SOAL A (INTERMEDIATE)
Modifikasi program yang telah kalian kerjakan sebelumnya pada modul 1 dengan menerapkan
materi yang sudah dipelajari pada modul 2 dengan ketentuan sebagai berikut:
1. Perbaiki/modifikasi fungsi-fungsi yang kalian buat sebelumnya agar menjadi pure
function untuk fungsi yang belum pure
2. Tambahkan fitur ‘find’ dan ‘edit’ data
3. Modifikasi fungsi-fungsi di dalam kode kalian dengan menerapkan lambda expression/list
comprehension/generator
Semakin banyak materi yang diimplementasikan, maka semakin baik nilai yang didapatkan
"""

# admin.py
import sqlite3

class Admin:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                judul TEXT,
                penulis TEXT,
                tahun_terbit TEXT
            )
        ''')
        self.connection.commit()

    def input_buku(self):
        judul = input("Masukkan judul buku: ")
        penulis = input("Masukkan nama penulis: ")
        tahun_terbit = input("Masukkan tahun terbit:")
        self.cursor.execute("INSERT INTO books (judul, penulis, tahun_terbit) VALUES (?, ?, ?)", (judul, penulis, tahun_terbit))
        self.connection.commit()
        print("Buku berhasil ditambahkan.")

    def find_buku(self, keyword):
        self.cursor.execute("SELECT * FROM books WHERE judul LIKE ?", ('%' + keyword + '%',))
        found_books = self.cursor.fetchall()
        return found_books

    def edit_buku(self, judul):
        penulis = input("Masukkan nama penulis baru: ")
        tahun_terbit = input("Masukkan tahun terbit baru:")
        self.cursor.execute("UPDATE books SET penulis = ?, tahun_terbit = ? WHERE judul = ?", (penulis, tahun_terbit, judul))
        self.connection.commit()
        print("Data buku berhasil diubah.")

    def lihat_buku(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if books:
            print("\nDaftar Buku:")
            for idx, buku in enumerate(books):
                print(f"{idx + 1}. Judul: {buku[1]}, Penulis: {buku[2]}, Tahun Terbit: {buku[3]}")
        else:
            print("Belum ada buku yang diinput.")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db_name = "book_database.db"
    admin = Admin(db_name)
    while True:
        print("\nMenu Admin:")
        print("1. Input Buku")
        print("2. Cari Buku")
        print("3. Edit Data Buku")
        print("4. Lihat Buku")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            admin.input_buku()
        elif pilihan == "2":
            keyword = input("Masukkan kata kunci pencarian: ")
            found_books = admin.find_buku(keyword)
            if found_books:
                print("Buku ditemukan:")
                for idx, buku in enumerate(found_books):
                    print(f"{idx + 1}. Judul: {buku[1]}")
            else:
                print("Buku tidak ditemukan.")
        elif pilihan == "3":
            judul = input("Masukkan judul buku yang akan diubah: ")
            admin.edit_buku(judul)
        elif pilihan == "4":
            admin.lihat_buku()
        elif pilihan == "5":
            admin.close()
            print("Terima kasih, admin!")
            break
        else:
            print("Pilihan tidak valid.")

# user.py
import sqlite3

class User:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def find_buku(self, keyword):
        self.cursor.execute("SELECT * FROM books WHERE judul LIKE ?", ('%' + keyword + '%',))
        found_books = self.cursor.fetchall()
        return found_books

    def pinjam_buku(self, judul):
        self.cursor.execute("SELECT * FROM books WHERE judul = ?", (judul,))
        book = self.cursor.fetchone()
        if book:
            self.cursor.execute("DELETE FROM books WHERE judul = ?", (judul,))
            self.connection.commit()
            return book
        return None

    def kembalikan_buku(self, buku):
        if buku:
            self.cursor.execute("INSERT INTO books (judul, penulis, tahun_terbit) VALUES (?, ?, ?)", (buku[1], buku[2], buku[3]))
            self.connection.commit()

    def lihat_buku_dipinjam(self, daftar_buku_dipinjam):
        if daftar_buku_dipinjam:
            print("\nDaftar Buku yang Anda Pinjam:")
            for idx, buku in enumerate(daftar_buku_dipinjam):
                print(f"{idx + 1}. Judul: {buku[1]}, Penulis: {buku[2]}, Tahun Terbit: {buku[3]}")
        else:
            print("Anda belum meminjam buku apapun.")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db_name = "book_database.db"
    user = User(db_name)
    daftar_buku_dipinjam = []
    while True:
        print("\nMenu User:")
        print("1. Cari Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. Lihat Buku yang Dipinjam")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            keyword = input("Masukkan kata kunci pencarian: ")
            found_books = user.find_buku(keyword)
            if found_books:
                print("Buku ditemukan:")
                for idx, buku in enumerate(found_books):
                    print(f"{idx + 1}. Judul: {buku[1]}")
            else:
                print("Buku tidak ditemukan.")
        elif pilihan == "2":
            judul = input("Masukkan judul buku yang ingin dipinjam: ")
            buku = user.pinjam_buku(judul)
            if buku:
                print(f"Anda berhasil meminjam buku '{buku[1]}'")
                daftar_buku_dipinjam.append(buku)
            else:
                print("Buku tidak tersedia atau judul tidak valid.")
        elif pilihan == "3":
            user.lihat_buku_dipinjam(daftar_buku_dipinjam)
            if daftar_buku_dipinjam:
                buku_kembali = int(input("Pilih buku yang ingin Anda kembalikan (nomor): ")) - 1
                if 0 <= buku_kembali < len(daftar_buku_dipinjam):
                    buku = daftar_buku_dipinjam.pop(buku_kembali)
                    user.kembalikan_buku(buku)
                    print(f"Anda telah mengembalikan buku '{buku[1]}'")
                else:
                    print("Nomor buku tidak valid.")
        elif pilihan == "4":
            user.lihat_buku_dipinjam(daftar_buku_dipinjam)
        elif pilihan == "5":
            user.close()
            print("Terima kasih, user!")
            break
        else:
            print("Pilihan tidak valid.")