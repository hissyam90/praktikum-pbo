from __future__ import annotations

from .aplikasi import AplikasiKebabCendana
from .pegawai import Pegawai


def demonstrasi_lengkap(app: AplikasiKebabCendana) -> str:
    baris = ["Kebab Cendana Pusat", "Pendataan pegawai dan shift", ""]
    try:
        Pegawai("Contoh", "Pegawai", "1234", 100_000)
    except TypeError as exc:
        baris.append(f"Pegawai tidak bisa dibuat langsung karena class tersebut abstrak ({type(exc).__name__}).")
    baris.extend(["", app.demonstrasi_polimorfisme()])
    baris.extend(["", "Jadwal dan pemberitahuan:", app.demonstrasi_duck_typing()])
    baris.extend(["", "Jam kerja:", app.demonstrasi_operator()])
    pegawai = app.cabang.daftar_pegawai[0]
    berhasil = app.mesin_absensi.proses_absensi(pegawai, pegawai.pin_absen)
    hasil_absen = "berhasil" if berhasil else "gagal"
    baris.extend(["", f"Absensi {pegawai.nama} {hasil_absen}.", "", "Tugas pada shift pagi:", app.daftar_shift[0].info_jadwal()])
    return "\n".join(baris)
