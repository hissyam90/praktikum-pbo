from __future__ import annotations

from .aplikasi import AplikasiKebabCendana
from .demonstrasi import demonstrasi_lengkap
from .pegawai import Pegawai
from .penggajian import GajiPegawai
from .shift import ShiftKerja


def _pilih_pegawai(app: AplikasiKebabCendana) -> Pegawai:
    print(app.cabang.tampilkan_daftar_pegawai())
    return app.cari_pegawai(input("Masukkan ID pegawai: ").strip())


def _pilih_shift(app: AplikasiKebabCendana) -> ShiftKerja:
    if not app.daftar_shift:
        raise LookupError("Belum ada shift yang terdaftar")
    for nomor, shift in enumerate(app.daftar_shift, start=1):
        print(f"{nomor}. {shift.jenis_shift} | {shift.tanggal} | {shift.jam}")
    try:
        nomor = int(input("Pilih nomor shift: "))
    except ValueError as exc:
        raise ValueError("Nomor shift harus berupa angka") from exc
    return app.cari_shift(nomor)


def _menu_tambah_pegawai(app: AplikasiKebabCendana) -> None:
    print("1. Kasir\n2. Pegawai Dapur\n3. Supervisor Shift")
    jenis = input("Jenis pegawai: ").strip()
    nama = input("Nama: ").strip()
    pin = input("PIN absensi (minimal 4 digit angka): ").strip()
    if jenis == "1":
        detail = input("Metode pembayaran: ").strip()
    elif jenis == "2":
        detail = input("Spesialisasi menu: ").strip()
    elif jenis == "3":
        detail = input("Tanggung jawab: ").strip()
    else:
        raise ValueError("Jenis pegawai harus 1, 2, atau 3")
    pegawai = app.tambah_pegawai(jenis, nama, pin, detail)
    print(f"Data pegawai tersimpan. ID: {pegawai.id_pegawai}")


def _menu_buat_shift(app: AplikasiKebabCendana) -> None:
    tanggal = input("Tanggal shift (YYYY-MM-DD): ").strip()
    print("Pilihan shift:", ", ".join(ShiftKerja.pilihan_shift))
    jenis = input("Jenis shift: ").strip().title()
    kapasitas_teks = input("Kapasitas pegawai [8]: ").strip()
    kapasitas = int(kapasitas_teks) if kapasitas_teks else 8
    shift = app.buat_shift(tanggal, jenis, kapasitas)
    print(f"Jadwal {shift.jenis_shift} dibuat untuk {shift.tanggal}.")


def _menu_tambah_ke_shift(app: AplikasiKebabCendana) -> None:
    shift = _pilih_shift(app)
    pegawai = _pilih_pegawai(app)
    tugas_teks = input("Daftar tugas, pisahkan dengan koma: ")
    tugas = [item.strip() for item in tugas_teks.split(",") if item.strip()]
    shift.tambah_pegawai(pegawai, tugas)
    print(f"{pegawai.nama} masuk ke shift {shift.jenis_shift}.")


def _menu_absensi(app: AplikasiKebabCendana) -> None:
    pegawai = _pilih_pegawai(app)
    pin = input("Masukkan PIN: ").strip()
    berhasil = app.mesin_absensi.proses_absensi(pegawai, pin)
    print("Absensi tercatat." if berhasil else "Absensi ditolak. Periksa PIN dan status pegawai.")
    print(app.mesin_absensi.tampilkan_log())


def _menu_gaji(app: AplikasiKebabCendana) -> None:
    try:
        hari_kerja = int(input("Jumlah hari kerja (1-31): "))
    except ValueError as exc:
        raise ValueError("Jumlah hari kerja harus berupa angka bulat") from exc
    daftar_gaji = app.daftar_gaji(hari_kerja)
    total = 0
    for gaji in daftar_gaji:
        print(gaji.cetak_slip_gaji())
        print()
        total += gaji.gaji_bersih
    print(f"Total gaji bersih: IDR {total:,.0f}")
    if input("Catat sebagai pembayaran gaji? (y/n): ").strip().casefold() == "y":
        for gaji in daftar_gaji:
            gaji.bayarkan()
        print(f"Pembayaran tersimpan. Akumulasi pengeluaran: IDR {GajiPegawai.total_pengeluaran:,.0f}")


def main() -> None:
    app = AplikasiKebabCendana()
    while True:
        print()
        print(app.cabang.nama_cabang)
        print(app.cabang.alamat)
        print("Pendataan pegawai dan jadwal kerja")
        print(
            "1. Data pegawai\n"
            "2. Tambah pegawai\n"
            "3. Buat shift kerja\n"
            "4. Jadwal shift\n"
            "5. Tugaskan pegawai\n"
            "6. Catat absensi\n"
            "7. Hitung gaji\n"
            "8. Riwayat absensi\n"
            "9. Demo Posttest 3\n"
            "0. Keluar"
        )
        pilihan = input("Pilihan: ").strip()
        try:
            if pilihan == "1":
                print(app.cabang.tampilkan_daftar_pegawai())
            elif pilihan == "2":
                _menu_tambah_pegawai(app)
            elif pilihan == "3":
                _menu_buat_shift(app)
            elif pilihan == "4":
                if not app.daftar_shift:
                    print("Belum ada jadwal shift.")
                else:
                    for shift in app.daftar_shift:
                        print(shift.info_jadwal())
                        print()
            elif pilihan == "5":
                _menu_tambah_ke_shift(app)
            elif pilihan == "6":
                _menu_absensi(app)
            elif pilihan == "7":
                _menu_gaji(app)
            elif pilihan == "8":
                print(app.mesin_absensi.tampilkan_log())
            elif pilihan == "9":
                print(demonstrasi_lengkap(app))
            elif pilihan == "0":
                print("Sampai jumpa.")
                return
            else:
                print("Pilihan tidak tersedia. Silakan pilih nomor pada menu.")
        except (ValueError, TypeError, LookupError, RuntimeError) as exc:
            print(f"Tidak dapat memproses permintaan: {exc}")
        input("\nTekan Enter untuk melanjutkan...")
