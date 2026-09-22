# Posttest 1 PBO - Manajemen Pegawai Kebab Cendana

## Deskripsi Program

Program ini merupakan program sederhana untuk mengelola data pegawai pada **Kebab Cendana** menggunakan konsep **Object Oriented Programming (OOP)** dengan Python.

Program dibuat berdasarkan materi:

1. **Class & Object**
2. **Atribut & Method**
3. **Encapsulation & Property**

Program memiliki tiga class utama, yaitu:

- `Pegawai`
- `ShiftKerja`
- `GajiPegawai`

Ketiga class tersebut saling berhubungan. `Pegawai` menyimpan data pegawai, `ShiftKerja` digunakan untuk mengatur jadwal kerja, sedangkan `GajiPegawai` digunakan untuk menghitung gaji pegawai.

---

## Tujuan Program

Program ini dibuat untuk menerapkan konsep dasar OOP dalam sebuah kasus yang sederhana dan mudah dipahami, khususnya:

- Pembuatan class dan object.
- Penggunaan atribut kelas dan atribut instance.
- Penggunaan instance method, class method, dan static method.
- Penerapan atribut private.
- Penggunaan `@property` dan setter.
- Validasi data menggunakan setter.
- Interaksi antar-object dari class yang berbeda.

---

# Struktur Class

## 1. Class `Pegawai`

Class `Pegawai` digunakan untuk menyimpan informasi dasar pegawai.

### Atribut Kelas

```python
nama_instansi = "Kebab Cendana"
total_pegawai = 0
batas_pegawai = 50
```

Keterangan:

- `nama_instansi` menyimpan nama instansi.
- `total_pegawai` menghitung jumlah pegawai yang dibuat.
- `batas_pegawai` menyimpan batas jumlah pegawai.

### Atribut Instance

```python
self.nama
self.jabatan
self.__pin_absen
```

`nama` dan `jabatan` merupakan atribut public.

`__pin_absen` merupakan atribut private karena menggunakan dua garis bawah. PIN diakses melalui property agar perubahan data dapat divalidasi.

### Method

**Instance method**

```python
profil_pegawai()
```

Digunakan untuk menampilkan nama dan jabatan pegawai.

**Class method**

```python
ubah_nama_instansi()
```

Digunakan untuk mengubah nama instansi yang merupakan atribut kelas.

**Static method**

```python
cek_format_pin()
```

Digunakan untuk memeriksa format PIN. PIN harus berupa angka dan minimal empat digit.

---

## 2. Class `ShiftKerja`

Class `ShiftKerja` digunakan untuk menyimpan jadwal kerja pegawai.

### Atribut Kelas

```python
total_shift_dibuat = 0
pilihan_shift = ["Pagi", "Sore", "Malam"]
jam_operasional = "08:00 - 24:00"
```

### Atribut Instance

```python
self.pegawai
self.tanggal
self.__jenis_shift
```

`pegawai` dan `tanggal` merupakan atribut public.

`__jenis_shift` merupakan atribut private dan perubahan nilainya dilakukan melalui property.

Class ini juga menerima object dari class `Pegawai`, sehingga terdapat hubungan antar-class.

### Method

**Instance method**

```python
info_jadwal()
```

Digunakan untuk menampilkan jadwal kerja pegawai.

**Class method**

```python
tambah_pilihan_shift()
```

Digunakan untuk menambahkan jenis shift baru ke daftar `pilihan_shift`.

**Static method**

```python
cek_ketersediaan_shift()
```

Digunakan untuk memeriksa apakah jenis shift tersedia di dalam daftar.

---

## 3. Class `GajiPegawai`

Class `GajiPegawai` digunakan untuk menghitung dan menampilkan gaji pegawai.

### Atribut Kelas

```python
total_pengeluaran = 0
potongan_pajak = 0.05
mata_uang = "IDR"
```

### Atribut Instance

```python
self.pegawai
self.hari_hadir
self.__gaji_harian
```

`pegawai` dan `hari_hadir` merupakan atribut public.

`__gaji_harian` merupakan atribut private sehingga perubahan nominal harus melalui setter.

### Method

**Instance method**

```python
cetak_slip_gaji()
```

Digunakan untuk menghitung gaji kotor, pajak, gaji bersih, dan menampilkan hasilnya.

**Class method**

```python
akumulasi_pengeluaran()
```

Digunakan untuk menambahkan gaji bersih ke total pengeluaran.

**Static method**

```python
validasi_nominal()
```

Digunakan untuk memastikan nominal gaji berupa angka dan lebih besar dari nol.

---

# Encapsulation dan Property

Program menggunakan atribut private pada ketiga class.

Contohnya:

```python
self.__pin_absen
self.__jenis_shift
self.__gaji_harian
```

Untuk mengakses atribut tersebut digunakan `@property` sebagai getter dan `@nama_property.setter` sebagai setter.

Contoh pada class `Pegawai`:

```python
@property
def pin_absen(self):
    return self.__pin_absen

@pin_absen.setter
def pin_absen(self, pin_baru):
    if Pegawai.cek_format_pin(pin_baru):
        self.__pin_absen = pin_baru
    else:
        raise ValueError("PIN harus berupa angka dan minimal 4 digit")
```

Setter melakukan validasi sebelum data disimpan. Dengan begitu, data yang tidak sesuai tidak langsung masuk ke atribut private.

Pola yang sama digunakan untuk:

- `pin_absen`
- `jenis_shift`
- `gaji_harian`

---

# Alur Program

Program dijalankan dari bagian:

```python
if __name__ == "__main__":
```

Alur program adalah sebagai berikut:

### 1. Membuat object pegawai

Program membuat dua object:

```python
pegawai1 = Pegawai("Antung", "Kasir", "1024")
pegawai2 = Pegawai("Dimas", "Dapur", "2048")
```

Pada saat object dibuat, data nama, jabatan, dan PIN dimasukkan. PIN diproses melalui setter sehingga validasi tetap dilakukan.

### 2. Mengubah nama instansi

Nama instansi diubah menggunakan class method:

```python
Pegawai.ubah_nama_instansi("Kebab Cendana Pusat")
```

### 3. Menampilkan data pegawai

Program memanggil instance method:

```python
pegawai1.profil_pegawai()
pegawai2.profil_pegawai()
```

### 4. Membuat jadwal kerja

Program membuat dua object `ShiftKerja`:

```python
shift1 = ShiftKerja(pegawai1, "23-10-2026", "Pagi")
shift2 = ShiftKerja(pegawai2, "23-10-2026", "Sore")
```

Object `Pegawai` digunakan sebagai data pada object `ShiftKerja`.

### 5. Menambah pilihan shift

Program menambahkan shift baru menggunakan class method:

```python
ShiftKerja.tambah_pilihan_shift("Tengah Malam")
```

### 6. Menampilkan jadwal

Jadwal masing-masing pegawai ditampilkan dengan:

```python
shift1.info_jadwal()
shift2.info_jadwal()
```

### 7. Membuat data gaji

Program membuat dua object `GajiPegawai`:

```python
gaji1 = GajiPegawai(pegawai1, 20, 100000)
gaji2 = GajiPegawai(pegawai2, 15, 120000)
```

### 8. Menghitung gaji

Method `cetak_slip_gaji()` menghitung gaji kotor, pajak 5%, kemudian menghasilkan gaji bersih.

Hasil yang diperoleh:

- Antung = `IDR 1.900.000`
- Dimas = `IDR 1.710.000`
- Total pengeluaran = `IDR 3.610.000`

### 9. Menguji data tidak valid

Program mencoba memasukkan:

- PIN `"12"`
- Shift `"Subuh"`
- Gaji `-50000`

Ketiganya ditolak karena tidak memenuhi aturan validasi.

### 10. Menguji data valid

Program kemudian mengubah data menjadi:

```python
pegawai1.pin_absen = "9999"
shift2.jenis_shift = "Tengah Malam"
gaji1.gaji_harian = 150000
```

Ketiga perubahan berhasil karena datanya memenuhi validasi.

---

# Cara Menjalankan Program

Pastikan Python sudah terpasang.

Buka terminal pada folder project, kemudian jalankan:

```bash
py a.py
```

atau:

```bash
python a.py
```

---

# Hasil Pengujian

Berikut hasil program saat dijalankan:

```text
Kebab Cendana Pusat
Pegawai: Antung | Jabatan: Kasir
Pegawai: Dimas | Jabatan: Dapur
Total pegawai terdaftar: 2

Jadwal Antung pada 23-10-2026: Shift Pagi
Jadwal Dimas pada 23-10-2026: Shift Sore
Total jadwal dibuat: 2

Gaji Antung (20 hari): IDR 1900000.0
Gaji Dimas (15 hari): IDR 1710000.0
Total pengeluaran gaji: IDR 3610000.0

Uji validasi data salah:
Gagal ubah PIN Antung: PIN harus berupa angka dan minimal 4 digit
Gagal ubah shift Dimas: Jenis shift tidak terdaftar di sistem
Gagal ubah gaji Antung: Nominal gaji tidak boleh nol atau minus

Uji validasi data benar:
Data Antung dan Dimas berhasil diubah.
```

---

# Kesesuaian dengan Ketentuan Tugas

| Ketentuan | Status | Implementasi |
|---|---|---|
| Minimal 3 class utama | ✅ | `Pegawai`, `ShiftKerja`, `GajiPegawai` |
| Minimal 3 atribut kelas | ✅ | Setiap class memiliki 3 atribut kelas |
| Atribut instance menggunakan `__init__()` | ✅ | Semua object menggunakan `self` |
| Atribut public | ✅ | Contoh: `nama`, `jabatan`, `tanggal` |
| Atribut private | ✅ | `__pin_absen`, `__jenis_shift`, `__gaji_harian` |
| Instance method | ✅ | `profil_pegawai()`, `info_jadwal()`, `cetak_slip_gaji()` |
| Class method | ✅ | `ubah_nama_instansi()`, `tambah_pilihan_shift()`, `akumulasi_pengeluaran()` |
| Static method | ✅ | `cek_format_pin()`, `cek_ketersediaan_shift()`, `validasi_nominal()` |
| Getter dengan `@property` | ✅ | Semua atribut private memiliki getter |
| Setter | ✅ | Semua property memiliki setter |
| Validasi setter | ✅ | Menggunakan pengecekan dan `ValueError` |
| Minimal 2 object tiap class | ✅ | 2 `Pegawai`, 2 `ShiftKerja`, 2 `GajiPegawai` |
| Data valid diuji | ✅ | PIN, shift, dan gaji berhasil diubah |
| Data tidak valid diuji | ✅ | Semua data yang salah ditolak |

---

# Catatan Pengujian Method

Instance method sudah dipanggil secara langsung pada bagian `main`.

Class method juga dipanggil secara langsung, contohnya:

```python
Pegawai.ubah_nama_instansi("Kebab Cendana Pusat")
ShiftKerja.tambah_pilihan_shift("Tengah Malam")
```

Static method digunakan oleh proses validasi pada setter dan perhitungan data.

Untuk memperjelas demonstrasi sesuai ketentuan tugas, static method dapat dipanggil langsung pada bagian `main`, misalnya:

```python
print(Pegawai.cek_format_pin("1234"))
print(ShiftKerja.cek_ketersediaan_shift("Pagi", ShiftKerja.pilihan_shift))
print(GajiPegawai.validasi_nominal(100000))
```

Penambahan ini tidak mengubah konsep program, tetapi membuat pengujian static method terlihat secara langsung pada output.

---

# Kesimpulan

Program `Posttest 1 PBO` telah menerapkan konsep OOP menggunakan tiga class utama, atribut kelas, atribut instance, atribut private, instance method, class method, static method, getter, setter, dan validasi data.

Program juga dapat menjalankan hubungan antar-object, melakukan perhitungan gaji, mengatur jadwal kerja, serta menolak data yang tidak sesuai aturan.

Hasil pengujian menunjukkan program dapat berjalan dan menghasilkan output sesuai proses yang dirancang.
