from __future__ import annotations

from typing import Iterable, Protocol

from .shift import ShiftKerja

class MemilikiRingkasan(Protocol):
    def ringkasan(self) -> str:
        ...


class LaporanShift:
    def __init__(self, daftar_shift: Iterable[ShiftKerja]):
        self.daftar_shift = tuple(daftar_shift)

    def ringkasan(self) -> str:
        total_penugasan = sum(len(shift.penugasan) for shift in self.daftar_shift)
        return (
            f"Laporan: {len(self.daftar_shift)} shift, "
            f"{total_penugasan} penugasan pegawai."
        )


class NotifikasiJadwal:
    def __init__(self, penerima: str, pesan: str):
        self.penerima = penerima.strip()
        self.pesan = pesan.strip()
        if not self.penerima or not self.pesan:
            raise ValueError("Penerima dan pesan notifikasi wajib diisi")

    def ringkasan(self) -> str:
        return f"Notifikasi untuk {self.penerima}: {self.pesan}"


def tampilkan_ringkasan(objek: MemilikiRingkasan) -> str:
    """Duck typing: fungsi hanya mensyaratkan object menyediakan ringkasan()."""
    return objek.ringkasan()


class RekapJamKerja:
    def __init__(self, nama_pegawai: str, total_jam: int):
        nama_pegawai = nama_pegawai.strip()
        if not nama_pegawai:
            raise ValueError("Nama pegawai wajib diisi")
        if not isinstance(total_jam, int) or isinstance(total_jam, bool) or total_jam < 0:
            raise ValueError("Total jam harus berupa bilangan bulat non-negatif")
        self.nama_pegawai = nama_pegawai
        self.total_jam = total_jam

    def __add__(self, lainnya: object) -> RekapJamKerja:
        if not isinstance(lainnya, RekapJamKerja):
            return NotImplemented
        if self.nama_pegawai == lainnya.nama_pegawai:
            nama_hasil = self.nama_pegawai
        else:
            nama_hasil = f"{self.nama_pegawai} + {lainnya.nama_pegawai}"
        return RekapJamKerja(nama_hasil, self.total_jam + lainnya.total_jam)

    def __str__(self) -> str:
        return f"{self.nama_pegawai}: {self.total_jam} jam"
