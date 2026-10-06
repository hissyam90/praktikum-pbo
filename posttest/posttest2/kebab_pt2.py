class Pegawai:
    nama_instansi = "Kebab Cendana"
    total_pegawai = 0
    batas_pegawai = 50

    def __init__(self, nama, jabatan, pin):
        self._nama = nama
        self._jabatan = jabatan
        self.__pin_absen = None
        self.pin_absen = pin
        Pegawai.total_pegawai += 1

    @property
    def nama(self):
        return self._nama

    @property
    def jabatan(self):
        return self._jabatan

    @property
    def pin_absen(self):
        return self.__pin_absen

    @pin_absen.setter
    def pin_absen(self, pin_baru):
        if Pegawai.cek_format_pin(pin_baru):
            self.__pin_absen = str(pin_baru)
        else:
            raise ValueError("PIN harus berupa angka dan minimal 4 digit")

    def profil_pegawai(self):
        print(f"Pegawai: {self._nama} | Jabatan: {self._jabatan}")

    @classmethod
    def ubah_nama_instansi(cls, nama_baru):
        cls.nama_instansi = nama_baru

    @staticmethod
    def cek_format_pin(pin):
        return str(pin).isdigit() and len(str(pin)) >= 4


class Kasir(Pegawai):
    def __init__(self, nama, pin, metode_pembayaran):
        super().__init__(nama, "Kasir", pin)
        self.metode_pembayaran = metode_pembayaran

    def profil_pegawai(self):
        print(f"Pegawai: {self._nama} | Jabatan: {self._jabatan} | Metode: {self.metode_pembayaran}")

    def layani_pembayaran(self, nominal):
        print(f"Kasir {self._nama} menerima pembayaran Rp{nominal:,}")


class PegawaiDapur(Pegawai):
    def __init__(self, nama, pin, spesialisasi_menu):
        super().__init__(nama, "Dapur", pin)
        self.spesialisasi_menu = spesialisasi_menu

    def siapkan_pesanan(self, menu):
        print(f"Dapur {self._nama} menyiapkan {menu} ({self.spesialisasi_menu})")


class KebabCendana:
    def __init__(self, nama_cabang):
        self.nama_cabang = nama_cabang
        self._daftar_pegawai = []

    def tambah_pegawai(self, pegawai):
        if isinstance(pegawai, Pegawai):
            self._daftar_pegawai.append(pegawai)
            print(f"{pegawai.nama} ditambahkan ke {self.nama_cabang}")

    def keluarkan_pegawai(self, nama):
        self._daftar_pegawai = [pegawai for pegawai in self._daftar_pegawai if pegawai.nama != nama]

    @property
    def total_pegawai(self):
        return len(self._daftar_pegawai)

    def tampilkan_daftar_pegawai(self):
        print(f"Daftar pegawai {self.nama_cabang}")
        for pegawai in self._daftar_pegawai:
            print(f"- {pegawai.nama} | {pegawai.jabatan}")
        print(f"Total: {self.total_pegawai}")


class MesinAbsensi:
    def __init__(self, id_mesin, lokasi):
        self.id_mesin = id_mesin
        self.lokasi = lokasi

    def proses_absensi(self, pegawai, pin):
        print(f"Absensi {pegawai.nama} melalui {self.id_mesin}")
        if pin == pegawai.pin_absen:
            print("Absensi berhasil")
        else:
            print("PIN salah")


class RincianGaji:
    def __init__(self, hari_hadir, gaji_harian, pajak):
        self.hari_hadir = hari_hadir
        self.gaji_harian = gaji_harian
        self.pajak = pajak
        self.gaji_kotor = hari_hadir * gaji_harian
        self.potongan_pajak = self.gaji_kotor * pajak
        self.gaji_bersih = self.gaji_kotor - self.potongan_pajak


class GajiPegawai:
    mata_uang = "IDR"
    total_pengeluaran = 0

    def __init__(self, pegawai, hari_hadir, gaji_harian, pajak=0.05):
        self.pegawai = pegawai
        if not self.validasi_nominal(gaji_harian):
            raise ValueError("Nominal gaji tidak boleh nol atau minus")
        self._rincian = RincianGaji(hari_hadir, gaji_harian, pajak)
        GajiPegawai.total_pengeluaran += self._rincian.gaji_bersih

    @property
    def gaji_bersih(self):
        return self._rincian.gaji_bersih

    def cetak_slip_gaji(self):
        print(f"Gaji {self.pegawai.nama} ({self._rincian.hari_hadir} hari): {self.mata_uang} {self.gaji_bersih:.0f}")

    @staticmethod
    def validasi_nominal(nominal):
        return isinstance(nominal, (int, float)) and nominal > 0


if __name__ == "__main__":
    pegawai1 = Kasir("Antung", "1024", "Cash / QRIS")
    pegawai2 = PegawaiDapur("Dita", "2048", "Kebab Original")

    print(Pegawai.nama_instansi)
    pegawai1.profil_pegawai()
    pegawai2.profil_pegawai()
    print(f"Total pegawai: {Pegawai.total_pegawai}")

    cabang = KebabCendana("Kebab Cendana Pusat")
    cabang.tambah_pegawai(pegawai1)
    cabang.tambah_pegawai(pegawai2)
    cabang.tampilkan_daftar_pegawai()

    mesin = MesinAbsensi("ABS-01", "Kebab Cendana Pusat")
    mesin.proses_absensi(pegawai1, "1024")
    mesin.proses_absensi(pegawai2, "1111")

    gaji1 = GajiPegawai(pegawai1, 20, 100000)
    gaji2 = GajiPegawai(pegawai2, 15, 120000)
    gaji1.cetak_slip_gaji()
    gaji2.cetak_slip_gaji()
    print(f"Total pengeluaran gaji: {GajiPegawai.mata_uang} {GajiPegawai.total_pengeluaran:.0f}")

    del cabang
    print("Data pegawai setelah cabang dihapus:")
    print(f"{pegawai1.nama} masih ada")
    print(f"{pegawai2.nama} masih ada")

    pegawai1.layani_pembayaran(50000)
    pegawai2.siapkan_pesanan("Kebab Spesial")

    print(f"isinstance(pegawai1, Pegawai): {isinstance(pegawai1, Pegawai)}")
    print(f"issubclass(Kasir, Pegawai): {issubclass(Kasir, Pegawai)}")

    try:
        pegawai1.pin_absen = "12"
    except ValueError as e:
        print(f"Validasi PIN: {e}")
