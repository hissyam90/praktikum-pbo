from __future__ import annotations

from .pegawai import Pegawai

class RincianGaji:
    def __init__(self, gaji_kotor: int, persentase_pajak: float = 0.05, potongan_lain: int = 0):
        if not isinstance(gaji_kotor, int) or isinstance(gaji_kotor, bool) or gaji_kotor <= 0:
            raise ValueError("Gaji kotor harus berupa bilangan bulat positif")
        if not isinstance(persentase_pajak, (int, float)) or not 0 <= persentase_pajak <= 1:
            raise ValueError("Persentase pajak harus berada di antara 0 dan 1")
        if not isinstance(potongan_lain, int) or isinstance(potongan_lain, bool) or potongan_lain < 0:
            raise ValueError("Potongan lain harus berupa bilangan bulat non-negatif")
        self.gaji_kotor = gaji_kotor
        self.persentase_pajak = float(persentase_pajak)
        self.potongan_pajak = round(gaji_kotor * self.persentase_pajak)
        self.potongan_lain = potongan_lain
        self.gaji_bersih = gaji_kotor - self.potongan_pajak - potongan_lain
        if self.gaji_bersih < 0:
            raise ValueError("Total potongan tidak boleh melebihi gaji kotor")


class GajiPegawai:
    mata_uang = "IDR"
    total_pengeluaran = 0

    def __init__(
        self,
        pegawai: Pegawai,
        hari_kerja: int,
        persentase_pajak: float = Pegawai.pajak_gaji,
        potongan_lain: int = 0,
    ):
        if not isinstance(pegawai, Pegawai):
            raise TypeError("Perhitungan gaji membutuhkan object Pegawai")
        self.pegawai = pegawai
        self.hari_kerja = hari_kerja
        self.gaji_kotor = pegawai.hitung_gaji(hari_kerja)
        self._rincian = RincianGaji(self.gaji_kotor, persentase_pajak, potongan_lain)
        self._sudah_dibayarkan = False

    @property
    def rincian(self) -> RincianGaji:
        return self._rincian

    @property
    def gaji_bersih(self) -> int:
        return self._rincian.gaji_bersih

    @staticmethod
    def validasi_nominal(nominal: int | float) -> bool:
        return Pegawai.validasi_nominal(nominal)

    @classmethod
    def akumulasi_pengeluaran(cls, nominal: int) -> None:
        if not isinstance(nominal, int) or isinstance(nominal, bool) or nominal < 0:
            raise ValueError("Nominal pengeluaran harus berupa bilangan bulat non-negatif")
        cls.total_pengeluaran += nominal

    def bayarkan(self) -> int:
        if self._sudah_dibayarkan:
            raise RuntimeError("Gaji untuk periode ini sudah dicatat sebagai pembayaran")
        type(self).akumulasi_pengeluaran(self.gaji_bersih)
        self._sudah_dibayarkan = True
        return self.gaji_bersih

    def cetak_slip_gaji(self) -> str:
        rincian = self._rincian
        return "\n".join(
            [
                f"Slip Gaji {self.pegawai.nama} ({self.pegawai.id_pegawai})",
                f"Jabatan            : {self.pegawai.jabatan}",
                f"Hari kerja         : {self.hari_kerja} hari",
                f"Gaji kotor         : {self.mata_uang} {rincian.gaji_kotor:,.0f}",
                f"Potongan pajak     : {self.mata_uang} {rincian.potongan_pajak:,.0f}",
                f"Potongan lain      : {self.mata_uang} {rincian.potongan_lain:,.0f}",
                f"Gaji bersih        : {self.mata_uang} {rincian.gaji_bersih:,.0f}",
            ]
        )
