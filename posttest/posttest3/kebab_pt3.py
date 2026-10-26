from __future__ import annotations

import sys

from kebab_cendana import (
    AplikasiKebabCendana,
    GajiPegawai,
    Kasir,
    KebabCendana,
    LaporanShift,
    MemilikiRingkasan,
    MesinAbsensi,
    NotifikasiJadwal,
    Pegawai,
    PegawaiDapur,
    PelaksanaPembayaran,
    PenugasanShift,
    PenyiapMenu,
    PengawasOperasional,
    RekapJamKerja,
    RincianGaji,
    ShiftKerja,
    SupervisorShift,
    demonstrasi_lengkap,
    tampilkan_ringkasan,
)
from kebab_cendana.terminal import main


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print(demonstrasi_lengkap(AplikasiKebabCendana()))
    else:
        main()
