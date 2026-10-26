from __future__ import annotations

from abc import ABC, abstractmethod


class Pegawai(ABC):
    nama_instansi = "Kebab Cendana"
    total_pegawai = 0
    batas_pegawai = 50
    pajak_gaji = 0.05

    def __init__(self, nama: str, jabatan: str, pin: str, gaji_harian: int):
        nama = nama.strip()
        jabatan = jabatan.strip()
        if not nama:
            raise ValueError("Nama pegawai tidak boleh kosong")
        if not jabatan:
            raise ValueError("Jabatan tidak boleh kosong")
        if Pegawai.total_pegawai >= Pegawai.batas_pegawai:
            raise ValueError("Batas pegawai sudah tercapai")
        if not self.validasi_nominal(gaji_harian):
            raise ValueError("Gaji harian harus berupa angka positif")

        self.id_pegawai = f"PGW-{Pegawai.total_pegawai + 1:03d}"
        self._nama = nama
        self._jabatan = jabatan
        self._gaji_harian = int(gaji_harian)
        self.__pin_absen = None
        self.pin_absen = pin
        self.status_aktif = True
        Pegawai.total_pegawai += 1

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, nama_baru: str) -> None:
        if not isinstance(nama_baru, str) or not nama_baru.strip():
            raise ValueError("Nama pegawai tidak boleh kosong")
        self._nama = nama_baru.strip()

    @property
    def jabatan(self) -> str:
        return self._jabatan

    @property
    def pin_absen(self) -> str:
        return self.__pin_absen

    @pin_absen.setter
    def pin_absen(self, pin_baru: str) -> None:
        if not self.cek_format_pin(pin_baru):
            raise ValueError("PIN harus berupa angka dan minimal 4 digit")
        self.__pin_absen = str(pin_baru)

    @property
    def gaji_harian(self) -> int:
        return self._gaji_harian

    @gaji_harian.setter
    def gaji_harian(self, nominal: int) -> None:
        if not self.validasi_nominal(nominal):
            raise ValueError("Gaji harian harus berupa angka positif")
        self._gaji_harian = int(nominal)

    @staticmethod
    def cek_format_pin(pin: str) -> bool:
        return str(pin).isdigit() and len(str(pin)) >= 4

    @staticmethod
    def validasi_nominal(nominal: int | float) -> bool:
        return isinstance(nominal, (int, float)) and not isinstance(nominal, bool) and nominal > 0

    @staticmethod
    def validasi_hari_kerja(hari_kerja: int) -> None:
        if not isinstance(hari_kerja, int) or isinstance(hari_kerja, bool):
            raise TypeError("Jumlah hari kerja harus berupa bilangan bulat")
        if not 1 <= hari_kerja <= 31:
            raise ValueError("Jumlah hari kerja harus antara 1 sampai 31 hari")

    @classmethod
    def ubah_nama_instansi(cls, nama_baru: str) -> None:
        if not isinstance(nama_baru, str) or not nama_baru.strip():
            raise ValueError("Nama instansi tidak boleh kosong")
        cls.nama_instansi = nama_baru.strip()

    @abstractmethod
    def profil_pegawai(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def jalankan_tugas(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def hitung_gaji(self, hari_kerja: int) -> int:
        raise NotImplementedError

    def mulai_shift(self, shift: ShiftKerja) -> str:
        if not shift.memiliki_pegawai(self):
            raise ValueError(f"{self.nama} belum terdaftar pada shift {shift.jenis_shift}")
        return f"{self.nama} mulai shift {shift.jenis_shift} pada {shift.tanggal}."

    def _hitung_gaji_dasar(self, hari_kerja: int) -> int:
        self.validasi_hari_kerja(hari_kerja)
        return self._gaji_harian * hari_kerja

    def __str__(self) -> str:
        return f"{self.id_pegawai} | {self._nama} | {self._jabatan}"


class PelaksanaPembayaran(ABC):
    @abstractmethod
    def layani_pembayaran(self, nominal: int) -> str:
        raise NotImplementedError


class PenyiapMenu(ABC):
    @abstractmethod
    def siapkan_pesanan(self, nama_menu: str) -> str:
        raise NotImplementedError


class PengawasOperasional(ABC):
    @abstractmethod
    def awasi_operasional(self) -> str:
        raise NotImplementedError
