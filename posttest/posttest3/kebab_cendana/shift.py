from __future__ import annotations

from datetime import date
from typing import Iterable

from .pegawai import Pegawai

class PenugasanShift:
    def __init__(self, pegawai: Pegawai, daftar_tugas: Iterable[str]):
        tugas = [item.strip() for item in daftar_tugas if isinstance(item, str) and item.strip()]
        if not tugas:
            raise ValueError("Penugasan harus memiliki minimal satu tugas")
        self.pegawai = pegawai
        self._daftar_tugas = tugas
        self.selesai = False

    @property
    def daftar_tugas(self) -> tuple[str, ...]:
        return tuple(self._daftar_tugas)

    def tambah_tugas(self, tugas: str) -> None:
        if not isinstance(tugas, str) or not tugas.strip():
            raise ValueError("Deskripsi tugas tidak boleh kosong")
        self._daftar_tugas.append(tugas.strip())

    def tandai_selesai(self) -> None:
        self.selesai = True

    def ringkasan(self) -> str:
        status = "Selesai" if self.selesai else "Belum selesai"
        return f"{self.pegawai.nama}: {', '.join(self._daftar_tugas)} [{status}]"


class ShiftKerja:
    total_shift_dibuat = 0
    pilihan_shift = {
        "Pagi": "08:00-14:00",
        "Sore": "14:00-20:00",
        "Malam": "18:00-24:00",
    }
    jam_operasional = "08:00-24:00"

    def __init__(self, tanggal: str, jenis_shift: str, kapasitas: int = 8):
        try:
            tanggal_valid = date.fromisoformat(tanggal)
        except (TypeError, ValueError) as exc:
            raise ValueError("Tanggal harus menggunakan format YYYY-MM-DD") from exc
        if jenis_shift not in self.pilihan_shift:
            raise ValueError(f"Shift tidak tersedia. Pilihan: {', '.join(self.pilihan_shift)}")
        if not isinstance(kapasitas, int) or isinstance(kapasitas, bool) or kapasitas < 1:
            raise ValueError("Kapasitas shift minimal 1 pegawai")
        self.tanggal = tanggal_valid.isoformat()
        self.jenis_shift = jenis_shift
        self.jam = self.pilihan_shift[jenis_shift]
        self.kapasitas = kapasitas
        self.__penugasan: list[PenugasanShift] = []
        ShiftKerja.total_shift_dibuat += 1

    @property
    def penugasan(self) -> tuple[dict[str, object], ...]:
        return tuple(
            {
                "id_pegawai": item.pegawai.id_pegawai,
                "nama": item.pegawai.nama,
                "daftar_tugas": item.daftar_tugas,
                "selesai": item.selesai,
            }
            for item in self.__penugasan
        )

    @property
    def pegawai(self) -> tuple[Pegawai, ...]:
        return tuple(item.pegawai for item in self.__penugasan)

    @property
    def total_penugasan(self) -> int:
        return len(self.__penugasan)

    def memiliki_pegawai(self, pegawai: Pegawai) -> bool:
        return any(item.pegawai is pegawai for item in self.__penugasan)

    @classmethod
    def tambah_pilihan_shift(cls, nama_shift: str, jam: str) -> None:
        nama_shift = nama_shift.strip().title()
        jam = jam.strip()
        if not nama_shift or not jam:
            raise ValueError("Nama shift dan jam kerja wajib diisi")
        if nama_shift in cls.pilihan_shift:
            raise ValueError("Nama shift sudah terdaftar")
        cls.pilihan_shift[nama_shift] = jam

    @staticmethod
    def cek_ketersediaan_shift(jenis_shift: str) -> bool:
        return jenis_shift in ShiftKerja.pilihan_shift

    def tambah_pegawai(self, pegawai: Pegawai, daftar_tugas: Iterable[str]) -> None:
        if not isinstance(pegawai, Pegawai):
            raise TypeError("Penugasan harus menggunakan object Pegawai")
        if not pegawai.status_aktif:
            raise ValueError("Pegawai nonaktif tidak dapat diberi shift")
        if len(self.__penugasan) >= self.kapasitas:
            raise ValueError("Kapasitas shift sudah penuh")
        if any(item.pegawai.id_pegawai == pegawai.id_pegawai for item in self.__penugasan):
            raise ValueError("Pegawai sudah ditugaskan pada shift ini")
        penugasan = PenugasanShift(pegawai, daftar_tugas)
        self.__penugasan.append(penugasan)

    def keluarkan_pegawai(self, id_pegawai: str) -> Pegawai:
        for penugasan in self.__penugasan:
            if penugasan.pegawai.id_pegawai.casefold() == id_pegawai.casefold():
                pegawai = penugasan.pegawai
                self.__penugasan.remove(penugasan)
                return pegawai
        raise LookupError(f"Pegawai {id_pegawai} tidak ditemukan di shift ini")

    def tandai_tugas_selesai(self, id_pegawai: str) -> None:
        for penugasan in self.__penugasan:
            if penugasan.pegawai.id_pegawai.casefold() == id_pegawai.casefold():
                penugasan.tandai_selesai()
                return
        raise LookupError(f"Pegawai {id_pegawai} tidak ditemukan di shift ini")

    def info_jadwal(self) -> str:
        baris = [
            f"Shift {self.jenis_shift} | {self.tanggal} | {self.jam}",
            f"Kapasitas: {len(self.__penugasan)}/{self.kapasitas}",
        ]
        if not self.__penugasan:
            baris.append("Belum ada pegawai yang ditugaskan.")
        else:
            baris.extend(f"- {item.ringkasan()}" for item in self.__penugasan)
        return "\n".join(baris)
