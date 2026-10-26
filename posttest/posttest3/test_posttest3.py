import unittest
from datetime import datetime

from kebab_pt3 import (
    AplikasiKebabCendana,
    GajiPegawai,
    Kasir,
    KebabCendana,
    LaporanShift,
    MesinAbsensi,
    NotifikasiJadwal,
    Pegawai,
    PegawaiDapur,
    PelaksanaPembayaran,
    PenyiapMenu,
    PengawasOperasional,
    RekapJamKerja,
    RincianGaji,
    ShiftKerja,
    SupervisorShift,
    tampilkan_ringkasan,
)


class TestPosttest3(unittest.TestCase):
    def setUp(self):
        Pegawai.total_pegawai = 0
        ShiftKerja.total_shift_dibuat = 0
        GajiPegawai.total_pengeluaran = 0
        self.kasir = Kasir("Antung", "1024", "Cash / QRIS", 10)
        self.dapur = PegawaiDapur("Dita", "2048", "Kebab Original", 15_000)
        self.supervisor = SupervisorShift("Rafi", "3096", "Pengawasan operasional")

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Pegawai("Contoh", "Pegawai", "1234", 100_000)

    def test_every_employee_subclass_implements_abstract_behaviour(self):
        for pegawai in (self.kasir, self.dapur, self.supervisor):
            with self.subTest(jabatan=pegawai.jabatan):
                self.assertTrue(pegawai.profil_pegawai())
                self.assertTrue(pegawai.jalankan_tugas())
                self.assertGreater(pegawai.hitung_gaji(1), 0)

    def test_method_overriding_is_different_for_subclasses(self):
        outputs = [pegawai.profil_pegawai() for pegawai in (self.kasir, self.dapur, self.supervisor)]
        self.assertIn("Metode", outputs[0])
        self.assertIn("Spesialisasi", outputs[1])
        self.assertIn("Tanggung jawab", outputs[2])
        self.assertEqual(len(set(outputs)), 3)

    def test_shared_concrete_method_requires_assignment(self):
        shift = ShiftKerja("2026-10-26", "Pagi")
        with self.assertRaises(ValueError):
            self.kasir.mulai_shift(shift)
        shift.tambah_pegawai(self.kasir, ["Membuka kas"])
        self.assertIn("mulai shift Pagi", self.kasir.mulai_shift(shift))

    def test_pin_validation_and_private_attribute(self):
        self.assertEqual(self.kasir.pin_absen, "1024")
        self.assertTrue(hasattr(self.kasir, "_Pegawai__pin_absen"))
        self.assertFalse(hasattr(self.kasir, "__pin_absen"))
        with self.assertRaises(ValueError):
            self.kasir.pin_absen = "12"
        self.kasir.pin_absen = "9999"
        self.assertEqual(self.kasir.pin_absen, "9999")

    def test_protected_attributes_and_unique_subclass_attributes(self):
        self.assertEqual(self.kasir._nama, "Antung")
        self.assertEqual(self.kasir._jabatan, "Kasir")
        self.assertEqual(self.kasir.metode_pembayaran, "Cash / QRIS")
        self.assertEqual(self.dapur.spesialisasi_menu, "Kebab Original")
        self.assertEqual(self.supervisor.tanggung_jawab, "Pengawasan operasional")

    def test_role_interfaces_are_separated_by_capability(self):
        self.assertIsInstance(self.kasir, PelaksanaPembayaran)
        self.assertIsInstance(self.dapur, PenyiapMenu)
        self.assertIsInstance(self.supervisor, PengawasOperasional)
        self.assertNotIsInstance(self.kasir, PenyiapMenu)
        self.assertIn("pembayaran", self.kasir.layani_pembayaran(50_000))
        self.assertIn("Kebab Spesial", self.dapur.siapkan_pesanan("Kebab Spesial"))
        self.assertIn("mengawasi", self.supervisor.awasi_operasional())

    def test_class_and_static_methods_from_previous_posttests_remain(self):
        nama_awal = Pegawai.nama_instansi
        try:
            Pegawai.ubah_nama_instansi("Kebab Cendana Cabang Uji")
            self.assertEqual(Pegawai.nama_instansi, "Kebab Cendana Cabang Uji")
        finally:
            Pegawai.ubah_nama_instansi(nama_awal)
        self.assertTrue(Pegawai.cek_format_pin("1234"))
        self.assertFalse(Pegawai.cek_format_pin("12"))
        self.assertTrue(ShiftKerja.cek_ketersediaan_shift("Pagi"))
        self.assertTrue(GajiPegawai.validasi_nominal(100_000))
        self.assertFalse(GajiPegawai.validasi_nominal(-1))

    def test_salary_detail_rejects_invalid_deductions(self):
        with self.assertRaises(ValueError):
            RincianGaji(100_000, persentase_pajak=1.5)
        with self.assertRaises(ValueError):
            RincianGaji(100_000, potongan_lain=100_001)

    def test_polymorphic_salary_calculation(self):
        self.assertEqual(self.kasir.hitung_gaji(2), 210_000)
        self.assertEqual(self.dapur.hitung_gaji(2), 250_000)
        self.assertEqual(self.supervisor.hitung_gaji(2), 580_000)

    def test_salary_rejects_invalid_working_days(self):
        with self.assertRaises(ValueError):
            self.kasir.hitung_gaji(0)
        with self.assertRaises(ValueError):
            self.dapur.hitung_gaji(32)
        with self.assertRaises(TypeError):
            self.supervisor.hitung_gaji(2.5)

    def test_payroll_composes_salary_details_and_calculates_tax(self):
        kasir_without_transactions = Kasir("Nisa", "4567", "Tunai", 0)
        slip = GajiPegawai(kasir_without_transactions, 1, persentase_pajak=0.05)
        self.assertIsInstance(slip.rincian, RincianGaji)
        self.assertEqual(slip.gaji_kotor, 100_000)
        self.assertEqual(slip.rincian.potongan_pajak, 5_000)
        self.assertEqual(slip.gaji_bersih, 95_000)
        self.assertIn("Gaji bersih", slip.cetak_slip_gaji())

    def test_payroll_payment_is_recorded_only_once(self):
        slip = GajiPegawai(self.kasir, 1)
        paid = slip.bayarkan()
        self.assertEqual(GajiPegawai.total_pengeluaran, paid)
        with self.assertRaises(RuntimeError):
            slip.bayarkan()
        self.assertEqual(GajiPegawai.total_pengeluaran, paid)

    def test_aggregation_branch_does_not_own_employee_lifecycle(self):
        branch = KebabCendana("Kebab Cendana Pusat", "Samarinda")
        branch.tambah_pegawai(self.kasir)
        self.assertEqual(branch.total_pegawai, 1)
        removed = branch.keluarkan_pegawai(self.kasir.id_pegawai)
        self.assertIs(removed, self.kasir)
        self.assertEqual(branch.total_pegawai, 0)
        self.assertEqual(self.kasir.nama, "Antung")
        self.assertEqual(self.kasir.hitung_gaji(1), 105_000)

    def test_association_attendance_success_and_failure(self):
        machine = MesinAbsensi("ABS-01", "Kebab Cendana Pusat")
        now = datetime(2026, 10, 26, 8, 0, 0)
        self.assertTrue(machine.proses_absensi(self.kasir, "1024", now))
        self.assertFalse(machine.proses_absensi(self.kasir, "0000", now))
        self.assertEqual(len(machine.log_absensi), 2)
        self.assertEqual(machine.log_absensi[0]["status"], "Berhasil")
        self.assertEqual(machine.log_absensi[1]["status"], "Gagal")

    def test_composition_shift_creates_private_assignments_and_enforces_rules(self):
        shift = ShiftKerja("2026-10-26", "Pagi", kapasitas=1)
        shift.tambah_pegawai(self.kasir, ["Membuka kas"])
        self.assertEqual(shift.total_penugasan, 1)
        self.assertEqual(shift.penugasan[0]["nama"], "Antung")
        with self.assertRaises(ValueError):
            shift.tambah_pegawai(self.dapur, ["Persiapan bahan"])
        with self.assertRaises(ValueError):
            shift.tambah_pegawai(self.kasir, ["Tugas ganda"])
        shift.tandai_tugas_selesai(self.kasir.id_pegawai)
        self.assertTrue(shift.penugasan[0]["selesai"])
        shift.keluarkan_pegawai(self.kasir.id_pegawai)
        self.assertEqual(shift.total_penugasan, 0)

    def test_invalid_shift_date_and_type_are_rejected(self):
        with self.assertRaises(ValueError):
            ShiftKerja("26-10-2026", "Pagi")
        with self.assertRaises(ValueError):
            ShiftKerja("2026-10-26", "Subuh")

    def test_duck_typing_with_unrelated_classes(self):
        shift = ShiftKerja("2026-10-26", "Pagi")
        shift.tambah_pegawai(self.kasir, ["Membuka kas"])
        report = LaporanShift([shift])
        notification = NotifikasiJadwal("Antung", "Shift dimulai pukul 08:00")
        self.assertFalse(issubclass(LaporanShift, NotifikasiJadwal))
        self.assertIn("1 shift", tampilkan_ringkasan(report))
        self.assertIn("Notifikasi", tampilkan_ringkasan(notification))

    def test_operator_overloading_adds_hours_without_mutating_inputs(self):
        first = RekapJamKerja("Antung", 8)
        second = RekapJamKerja("Dita", 7)
        total = first + second
        self.assertEqual(total.total_jam, 15)
        self.assertEqual(first.total_jam, 8)
        self.assertEqual(str(total), "Antung + Dita: 15 jam")
        with self.assertRaises(TypeError):
            _ = first + 3

    def test_employee_name_and_details_have_validation(self):
        with self.assertRaises(ValueError):
            self.kasir.nama = "   "
        with self.assertRaises(ValueError):
            Kasir("", "1234", "Tunai")
        with self.assertRaises(ValueError):
            PegawaiDapur("Dapur", "1234", "")

    def test_application_has_seed_data_shifts_and_demos(self):
        Pegawai.total_pegawai = 0
        ShiftKerja.total_shift_dibuat = 0
        app = AplikasiKebabCendana()
        self.assertEqual(app.cabang.total_pegawai, 3)
        self.assertGreaterEqual(len(app.daftar_shift), 2)
        self.assertIn("Daftar pegawai", app.demonstrasi_polimorfisme())
        self.assertIn("Notifikasi", app.demonstrasi_duck_typing())
        self.assertIn("15 jam", app.demonstrasi_operator())


if __name__ == "__main__":
    unittest.main(verbosity=2)
