from __future__ import annotations

from datetime import datetime

from .pegawai import Pegawai

class MesinAbsensi:
    def __init__(self, id_mesin: str, lokasi: str):
        self.id_mesin = id_mesin.strip()
        self.lokasi = lokasi.strip()
        if not self.id_mesin or not self.lokasi:
            raise ValueError("ID mesin dan lokasi wajib diisi")
        self._log_absensi: list[dict[str, str]] = []

    @property
    def log_absensi(self) -> tuple[dict[str, str], ...]:
        return tuple(dict(item) for item in self._log_absensi)

    def proses_absensi(self, pegawai: Pegawai, pin: str, waktu: datetime | None = None) -> bool:
        if not isinstance(pegawai, Pegawai):
            raise TypeError("Absensi hanya dapat dilakukan oleh object Pegawai")
        waktu_absen = waktu or datetime.now()
        berhasil = str(pin) == pegawai.pin_absen and pegawai.status_aktif
        status = "Berhasil" if berhasil else "Gagal"
        alasan = "Terverifikasi" if berhasil else "PIN salah atau pegawai nonaktif"
        self._log_absensi.append(
            {
                "id_pegawai": pegawai.id_pegawai,
                "nama": pegawai.nama,
                "waktu": waktu_absen.strftime("%Y-%m-%d %H:%M:%S"),
                "status": status,
                "alasan": alasan,
            }
        )
        return berhasil

    def tampilkan_log(self) -> str:
        if not self._log_absensi:
            return "Belum ada catatan absensi."
        baris = [f"Log Absensi {self.id_mesin} - {self.lokasi}"]
        for catatan in self._log_absensi:
            baris.append(
                f"{catatan['waktu']} | {catatan['id_pegawai']} {catatan['nama']} | "
                f"{catatan['status']} ({catatan['alasan']})"
            )
        return "\n".join(baris)
