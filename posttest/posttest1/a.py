class Pegawai:
    nama_instansi = "Kebab Cendana"
    total_pegawai = 0
    batas_pegawai = 50

    def __init__(self, nama, jabatan, pin):
        self.nama = nama
        self.jabatan = jabatan
        self.__pin_absen = None
        self.pin_absen = pin
        Pegawai.total_pegawai += 1

    @property
    def pin_absen(self):
        return self.__pin_absen

    @pin_absen.setter
    def pin_absen(self, pin_baru):
        if Pegawai.cek_format_pin(pin_baru):
            self.__pin_absen = pin_baru
        else:
            raise ValueError("PIN harus berupa angka dan minimal 4 digit")

    def profil_pegawai(self):
        print(f"Pegawai: {self.nama} | Jabatan: {self.jabatan}")

    @classmethod
    def ubah_nama_instansi(cls, nama_baru):
        cls.nama_instansi = nama_baru

    @staticmethod
    def cek_format_pin(pin):
        return str(pin).isdigit() and len(str(pin)) >= 4


class ShiftKerja:
    total_shift_dibuat = 0
    pilihan_shift = ["Pagi", "Sore", "Malam"]
    jam_operasional = "08:00 - 24:00"

    def __init__(self, pegawai, tanggal, jenis_shift):
        self.pegawai = pegawai
        self.tanggal = tanggal
        self.__jenis_shift = None
        self.jenis_shift = jenis_shift
        ShiftKerja.total_shift_dibuat += 1

    @property
    def jenis_shift(self):
        return self.__jenis_shift

    @jenis_shift.setter
    def jenis_shift(self, shift_baru):
        if ShiftKerja.cek_ketersediaan_shift(shift_baru, self.pilihan_shift):
            self.__jenis_shift = shift_baru
        else:
            raise ValueError("Jenis shift tidak terdaftar di sistem")

    def info_jadwal(self):
        print(f"Jadwal {self.pegawai.nama} pada {self.tanggal}: Shift {self.__jenis_shift}")

    @classmethod
    def tambah_pilihan_shift(cls, shift_baru):
        if shift_baru not in cls.pilihan_shift:
            cls.pilihan_shift.append(shift_baru)

    @staticmethod
    def cek_ketersediaan_shift(shift, daftar_shift):
        return shift in daftar_shift


class GajiPegawai:
    total_pengeluaran = 0
    potongan_pajak = 0.05
    mata_uang = "IDR"

    def __init__(self, pegawai, hari_hadir, gaji_harian):
        self.pegawai = pegawai
        self.hari_hadir = hari_hadir
        self.__gaji_harian = None
        self.gaji_harian = gaji_harian

    @property
    def gaji_harian(self):
        return self.__gaji_harian

    @gaji_harian.setter
    def gaji_harian(self, nominal):
        if self.validasi_nominal(nominal):
            self.__gaji_harian = nominal
        else:
            raise ValueError("Nominal gaji tidak boleh nol atau minus")

    def cetak_slip_gaji(self):
        kotor = self.hari_hadir * self.__gaji_harian
        pajak = kotor * self.potongan_pajak
        bersih = kotor - pajak
        GajiPegawai.akumulasi_pengeluaran(bersih)
        print(f"Gaji {self.pegawai.nama} ({self.hari_hadir} hari): {self.mata_uang} {bersih}")

    @classmethod
    def akumulasi_pengeluaran(cls, nominal):
        cls.total_pengeluaran += nominal

    @staticmethod
    def validasi_nominal(nominal):
        return isinstance(nominal, (int, float)) and nominal > 0


if __name__ == "__main__":
    pegawai1 = Pegawai("Antung", "Kasir", "1024")
    pegawai2 = Pegawai("Dimas", "Dapur", "2048")

    Pegawai.ubah_nama_instansi("Kebab Cendana Pusat")
    print(Pegawai.nama_instansi)
    pegawai1.profil_pegawai()
    pegawai2.profil_pegawai()
    print(f"Total pegawai terdaftar: {Pegawai.total_pegawai}\n")

    shift1 = ShiftKerja(pegawai1, "23-10-2026", "Pagi")
    shift2 = ShiftKerja(pegawai2, "23-10-2026", "Sore")

    ShiftKerja.tambah_pilihan_shift("Tengah Malam")
    shift1.info_jadwal()
    shift2.info_jadwal()
    print(f"Total jadwal dibuat: {ShiftKerja.total_shift_dibuat}\n")

    gaji1 = GajiPegawai(pegawai1, 20, 100000)
    gaji2 = GajiPegawai(pegawai2, 15, 120000)

    gaji1.cetak_slip_gaji()
    gaji2.cetak_slip_gaji()
    print(f"Total pengeluaran gaji: {GajiPegawai.mata_uang} {GajiPegawai.total_pengeluaran}\n")

    print("Uji validasi data salah:")
    try:
        pegawai1.pin_absen = "12"
    except ValueError as e:
        print(f"Gagal ubah PIN Antung: {e}")

    try:
        shift2.jenis_shift = "Subuh"
    except ValueError as e:
        print(f"Gagal ubah shift Dimas: {e}")

    try:
        gaji1.gaji_harian = -50000
    except ValueError as e:
        print(f"Gagal ubah gaji Antung: {e}")

    print("\nUji validasi data benar:")
    pegawai1.pin_absen = "9999"
    shift2.jenis_shift = "Tengah Malam"
    gaji1.gaji_harian = 150000
    print("Data Antung dan Dimas berhasil diubah.")