from __future__ import annotations

from .pegawai import Pegawai, PelaksanaPembayaran, PenyiapMenu, PengawasOperasional


class Kasir(Pegawai, PelaksanaPembayaran):
    def __init__(
        self,
        nama: str,
        pin: str,
        metode_pembayaran: str,
        transaksi_per_hari: int = 0,
    ):
        metode_pembayaran = metode_pembayaran.strip()
        if not metode_pembayaran:
            raise ValueError("Metode pembayaran tidak boleh kosong")
        if not isinstance(transaksi_per_hari, int) or isinstance(transaksi_per_hari, bool) or transaksi_per_hari < 0:
            raise ValueError("Jumlah transaksi harus berupa bilangan bulat non-negatif")
        super().__init__(nama, "Kasir", pin, 100_000)
        self.metode_pembayaran = metode_pembayaran
        self.transaksi_per_hari = transaksi_per_hari
        self.bonus_per_transaksi = 500

    def profil_pegawai(self) -> str:
        status = "Aktif" if self.status_aktif else "Nonaktif"
        return (
            f"{self.id_pegawai} | Kasir: {self._nama} | "
            f"Metode: {self.metode_pembayaran} | Status: {status}"
        )

    def jalankan_tugas(self) -> str:
        return f"Kasir {self._nama} melayani pelanggan dan memproses pembayaran."

    def hitung_gaji(self, hari_kerja: int) -> int:
        dasar = self._hitung_gaji_dasar(hari_kerja)
        bonus = self.transaksi_per_hari * self.bonus_per_transaksi * hari_kerja
        return dasar + bonus

    def layani_pembayaran(self, nominal: int) -> str:
        if not self.validasi_nominal(nominal):
            raise ValueError("Nominal transaksi harus lebih besar dari nol")
        return f"Kasir {self._nama} memproses pembayaran Rp{nominal:,.0f}."


class PegawaiDapur(Pegawai, PenyiapMenu):
    def __init__(
        self,
        nama: str,
        pin: str,
        spesialisasi_menu: str,
        tunjangan_keahlian_harian: int = 15_000,
    ):
        spesialisasi_menu = spesialisasi_menu.strip()
        if not spesialisasi_menu:
            raise ValueError("Spesialisasi menu tidak boleh kosong")
        if not Pegawai.validasi_nominal(tunjangan_keahlian_harian):
            raise ValueError("Tunjangan keahlian harus berupa angka positif")
        super().__init__(nama, "Dapur", pin, 110_000)
        self.spesialisasi_menu = spesialisasi_menu
        self.tunjangan_keahlian_harian = int(tunjangan_keahlian_harian)

    def profil_pegawai(self) -> str:
        status = "Aktif" if self.status_aktif else "Nonaktif"
        return (
            f"{self.id_pegawai} | Dapur: {self._nama} | "
            f"Spesialisasi: {self.spesialisasi_menu} | Status: {status}"
        )

    def jalankan_tugas(self) -> str:
        return f"Pegawai dapur {self._nama} menyiapkan menu {self.spesialisasi_menu}."

    def hitung_gaji(self, hari_kerja: int) -> int:
        dasar = self._hitung_gaji_dasar(hari_kerja)
        return dasar + self.tunjangan_keahlian_harian * hari_kerja

    def siapkan_pesanan(self, nama_menu: str) -> str:
        if not isinstance(nama_menu, str) or not nama_menu.strip():
            raise ValueError("Nama menu tidak boleh kosong")
        return f"{self._nama} menyiapkan {nama_menu.strip()} ({self.spesialisasi_menu})."


class SupervisorShift(Pegawai, PengawasOperasional):
    def __init__(self, nama: str, pin: str, tanggung_jawab: str, tunjangan_bulanan: int = 300_000):
        tanggung_jawab = tanggung_jawab.strip()
        if not tanggung_jawab:
            raise ValueError("Tanggung jawab tidak boleh kosong")
        if not isinstance(tunjangan_bulanan, int) or isinstance(tunjangan_bulanan, bool) or tunjangan_bulanan < 0:
            raise ValueError("Tunjangan bulanan harus berupa bilangan bulat non-negatif")
        super().__init__(nama, "Supervisor Shift", pin, 140_000)
        self.tanggung_jawab = tanggung_jawab
        self.tunjangan_bulanan = tunjangan_bulanan

    def profil_pegawai(self) -> str:
        status = "Aktif" if self.status_aktif else "Nonaktif"
        return (
            f"{self.id_pegawai} | Supervisor: {self._nama} | "
            f"Tanggung jawab: {self.tanggung_jawab} | Status: {status}"
        )

    def jalankan_tugas(self) -> str:
        return f"Supervisor {self._nama} mengawasi shift dan mengevaluasi pekerjaan tim."

    def hitung_gaji(self, hari_kerja: int) -> int:
        return self._hitung_gaji_dasar(hari_kerja) + self.tunjangan_bulanan

    def awasi_operasional(self) -> str:
        return f"Supervisor {self._nama} mengawasi jalannya operasional, tugas, dan serah terima shift."
