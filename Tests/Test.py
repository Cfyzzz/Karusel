import server
import unittest


class TestStringMethods(unittest.TestCase):
    def test_import_from_excel(self):
        server.import_from_excel("store.xls", append=False)

    def test_export_to_excle(self):
        server.export_to_excel("fake_store.xls")


class TestConvertValue(unittest.TestCase):
    def test_number_union_metric_format(self):
        fact = server.union_metric_format("10")
        expected = "10.0"
        self.assertEqual(expected, fact)

    def test_numberAndLetterR_union_metric_format(self):
        fact = server.union_metric_format("0R")
        expected = "0.0"
        self.assertEqual(expected, fact)

    def test_floatNumber_union_metric_format(self):
        fact = server.union_metric_format("0.025")
        expected = "0.025"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraU_union_metric_format(self):
        fact = server.union_metric_format("0.01u")
        expected = "10000.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraUAndVolt_union_metric_format(self):
        fact = server.union_metric_format("0.1u/100V")
        expected = "100000.0"
        self.assertEqual(expected, fact)

    def test_NumberLiteraP_union_metric_format(self):
        fact = server.union_metric_format("1000p")
        expected = "1000.0"
        self.assertEqual(expected, fact)

    def test_NumberLiteraNAndVolt_union_metric_format(self):
        fact = server.union_metric_format("10n/50V")
        expected = "10000.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraPAndVolt_union_metric_format(self):
        fact = server.union_metric_format("2.2p/50V")
        expected = "2.2"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraK_union_metric_format(self):
        fact = server.union_metric_format("1.1k")
        expected = "1100.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraM_union_metric_format(self):
        fact = server.union_metric_format("1.1M")
        expected = "1100000.0"
        self.assertEqual(expected, fact)


if __name__ == "__main__":
    unittest.main()
