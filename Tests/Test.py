import requests
import json

import settings
import tools
import unittest


class TestStringMethods(unittest.TestCase):
    def test_import_from_excel(self):
        tools.import_from_excel("store.xls", append=False)

    def test_export_to_excle(self):
        tools.export_to_excel("fake_store.xls")


class TestConvertValue(unittest.TestCase):
    def test_number_union_metric_format(self):
        fact = tools.union_metric_format("10")
        expected = "10.0"
        self.assertEqual(expected, fact)

    def test_numberAndLetterR_union_metric_format(self):
        fact = tools.union_metric_format("0R")
        expected = "0.0"
        self.assertEqual(expected, fact)

    def test_floatNumber_union_metric_format(self):
        fact = tools.union_metric_format("0.025")
        expected = "0.025"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraU_union_metric_format(self):
        fact = tools.union_metric_format("0.01u")
        expected = "10000.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraUAndVolt_union_metric_format(self):
        fact = tools.union_metric_format("0.1u/100V")
        expected = "100000.0"
        self.assertEqual(expected, fact)

    def test_NumberLiteraP_union_metric_format(self):
        fact = tools.union_metric_format("1000p")
        expected = "1000.0"
        self.assertEqual(expected, fact)

    def test_NumberLiteraNAndVolt_union_metric_format(self):
        fact = tools.union_metric_format("10n/50V")
        expected = "10000.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraPAndVolt_union_metric_format(self):
        fact = tools.union_metric_format("2.2p/50V")
        expected = "2.2"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraK_union_metric_format(self):
        fact = tools.union_metric_format("1.1k")
        expected = "1100.0"
        self.assertEqual(expected, fact)

    def test_floatNumberLiteraM_union_metric_format(self):
        fact = tools.union_metric_format("1.1M")
        expected = "1100000.0"
        self.assertEqual(expected, fact)

    def test_nonNumberFormat_union_metric_format(self):
        fact = tools.union_metric_format("AN6651")
        expected = "AN6651"
        self.assertEqual(expected, fact)


class TestRestServer(unittest.TestCase):
    base_url = f"http://{settings.DATABASE['host']}:{settings.DATABASE['port']}"

    def test_new_component_components_post(self):
        url = self.base_url + "/components"

        # Additional headers.
        headers = {'Content-Type': 'application/json'}

        # Body
        payload = {'type': "резисторы", 'designation': 'R9997', 'address': 'X-Y', 'box': 'ZZ', 'quantity': 10}

        # convert dict to json string by json.dumps() for body data.
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

        # Validate response headers and body contents, e.g. status code.
        assert resp.status_code == 201
        resp_body = resp.json()
        assert resp_body['component']['quantity'] >= 10
        assert resp_body['component']['id'] > 0
        assert resp_body['component']['type'] == payload['type']


if __name__ == "__main__":
    unittest.main()

# ref: https://peter-jp-xie.medium.com/rest-api-testing-using-python-751022c364b8
