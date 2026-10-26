from __future__ import annotations

from datetime import date

from .absensi import MesinAbsensi
from .cabang import KebabCendana
from .pegawai import Pegawai
from .peran_pegawai import Kasir, PegawaiDapur, SupervisorShift
from .penggajian import GajiPegawai
from .polimorfisme import LaporanShift, NotifikasiJadwal, RekapJamKerja, tampilkan_ringkasan
from .shift import ShiftKerja

class AplikasiKebabCendana:
    def __init__(self):
        self.cabang = KebabCendana("Kebab Cendana Pusat", "Jl. Cendana, Samarinda")
        self.mesin_absensi = MesinAbsensi("ABS-01", self.cabang.nama_cabang)
        self.daftar_shift: list[ShiftKerja] = []
        self._isi_data_awal()

    def _isi_data_awal(self) -> None:
        pegawai_awal = [
            Kasir("Antung Hissyam", "1024", "Cash / QRIS", 35),
            PegawaiDapur("Dita", "2048", "Kebab Original", 15_000),
            SupervisorShift("Rafi", "3096", "Pengawasan operasional dan pembagian tugas"),
        ]
        for pegawai in pegawai_awal:
            self.cabang.tambah_pegawai(pegawai)

        shift_pagi = ShiftKerja(date.today().isoformat(), "Pagi")
        shift_pagi.tambah_pegawai(pegawai_awal[0], ["Membuka kas", "Melayani pembayaran"])
        shift_pagi.tambah_pegawai(pegawai_awal[1], ["Menyiapkan bahan", "Menyiapkan pesanan"])
        shift_pagi.tambah_pegawai(pegawai_awal[2], ["Memeriksa operasional"])
        self.daftar_shift.append(shift_pagi)

        shift_sore = ShiftKerja(date.today().isoformat(), "Sore")
        shift_sore.tambah_pegawai(pegawai_awal[0], ["Rekap transaksi"])
        shift_sore.tambah_pegawai(pegawai_awal[2], ["Serah terima shift"])
        self.daftar_shift.append(shift_sore)

    def cari_shift(self, nomor: int) -> ShiftKerja:
        if not 1 <= nomor <= len(self.daftar_shift):
            raise LookupError("Nomor shift tidak ditemukan")
        return self.daftar_shift[nomor - 1]

    def tambah_pegawai(self, jenis: str, nama: str, pin: str, detail: str) -> Pegawai:
        if jenis == "1":
            pegawai = Kasir(nama, pin, detail)
        elif jenis == "2":
            pegawai = PegawaiDapur(nama, pin, detail)
        elif jenis == "3":
            pegawai = SupervisorShift(nama, pin, detail)
        else:
            raise ValueError("Jenis pegawai harus 1, 2, atau 3")
        try:
            self.cabang.tambah_pegawai(pegawai)
        except Exception:
            Pegawai.total_pegawai -= 1
            raise
        return pegawai

    def buat_shift(self, tanggal: str, jenis_shift: str, kapasitas: int) -> ShiftKerja:
        shift = ShiftKerja(tanggal, jenis_shift, kapasitas)
        self.daftar_shift.append(shift)
        return shift

    def cari_pegawai(self, id_pegawai: str) -> Pegawai:
        return self.cabang.cari_pegawai(id_pegawai)

    def daftar_gaji(self, hari_kerja: int) -> list[GajiPegawai]:
        return [GajiPegawai(pegawai, hari_kerja) for pegawai in self.cabang.daftar_pegawai]

    def demonstrasi_polimorfisme(self) -> str:
        baris = ["Daftar pegawai"]
        for pegawai in self.cabang.daftar_pegawai:
            baris.append(pegawai.profil_pegawai())
            baris.append(pegawai.jalankan_tugas())
            baris.append(f"Gaji kotor 20 hari: IDR {pegawai.hitung_gaji(20):,.0f}")
        return "\n".join(baris)

    def demonstrasi_duck_typing(self) -> str:
        laporan = LaporanShift(self.daftar_shift)
        notifikasi = NotifikasiJadwal("Antung Hissyam", "Shift Pagi dimulai pukul 08:00.")
        return "\n".join([tampilkan_ringkasan(laporan), tampilkan_ringkasan(notifikasi)])

    def demonstrasi_operator(self) -> str:
        rekap_antung = RekapJamKerja("Antung Hissyam", 8)
        rekap_dita = RekapJamKerja("Dita", 7)
        return "\n".join([str(rekap_antung), str(rekap_dita), str(rekap_antung + rekap_dita)])
