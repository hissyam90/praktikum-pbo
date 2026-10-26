from __future__ import annotations

from .pegawai import Pegawai

class KebabCendana:
    def __init__(self, nama_cabang: str, alamat: str):
        nama_cabang = nama_cabang.strip()
        alamat = alamat.strip()
        if not nama_cabang or not alamat:
            raise ValueError("Nama cabang dan alamat wajib diisi")
        self.nama_cabang = nama_cabang
        self.alamat = alamat
        self._daftar_pegawai: list[Pegawai] = []

    @property
    def daftar_pegawai(self) -> tuple[Pegawai, ...]:
        return tuple(self._daftar_pegawai)

    @property
    def total_pegawai(self) -> int:
        return len(self._daftar_pegawai)

    def tambah_pegawai(self, pegawai: Pegawai) -> None:
        if not isinstance(pegawai, Pegawai):
            raise TypeError("Data yang ditambahkan harus berupa object Pegawai")
        if any(item.id_pegawai == pegawai.id_pegawai for item in self._daftar_pegawai):
            raise ValueError("Pegawai sudah terdaftar di cabang ini")
        if not pegawai.status_aktif:
            raise ValueError("Pegawai nonaktif tidak dapat dimasukkan ke daftar aktif")
        self._daftar_pegawai.append(pegawai)

    def cari_pegawai(self, id_pegawai: str) -> Pegawai:
        for pegawai in self._daftar_pegawai:
            if pegawai.id_pegawai.casefold() == id_pegawai.casefold():
                return pegawai
        raise LookupError(f"Pegawai dengan ID {id_pegawai} tidak ditemukan")

    def keluarkan_pegawai(self, id_pegawai: str) -> Pegawai:
        pegawai = self.cari_pegawai(id_pegawai)
        self._daftar_pegawai.remove(pegawai)
        return pegawai

    def tampilkan_daftar_pegawai(self) -> str:
        baris = [f"Daftar Pegawai - {self.nama_cabang}", f"Alamat: {self.alamat}"]
        if not self._daftar_pegawai:
            baris.append("Belum ada pegawai terdaftar.")
        else:
            baris.extend(pegawai.profil_pegawai() for pegawai in self._daftar_pegawai)
        baris.append(f"Total pegawai aktif: {self.total_pegawai}")
        return "\n".join(baris)
