import server
import unittest


class TestStringMethods(unittest.TestCase):
    def test_import_from_excel(self):
        server.import_from_excel("store.xls", append=False)

    def test_export_to_excle(self):
        server.export_to_excel("fake_store.xls")


if __name__ == "__main__":
    unittest.main()
