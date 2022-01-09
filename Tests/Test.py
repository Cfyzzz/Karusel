import json
import unittest

import requests

import tools


class TestImportExportMethods(unittest.TestCase):
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
    base_url = tools.get_base_url()

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
        assert resp_body['component']['quantity'] == 10
        assert resp_body['component']['id'] > 0
        assert resp_body['component']['type'] == payload['type']

    def test_components_get_by_id(self):
        url = self.base_url + "/components"
        quantity = 9
        headers = {'Content-Type': 'application/json'}
        payload = {'type': "резисторы", 'designation': 'R9994', 'address': 'X-Y', 'box': 'ZZ', 'quantity': quantity}
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 201
        resp_body = resp.json()
        the_id = resp_body['component']['id']
        url += f"?id={the_id}"
        resp = requests.get(url, headers=headers)
        resp_body = resp.json()
        assert resp_body['components'][0]['quantity'] == quantity
        assert resp_body['components'][0]['id'] == the_id

    def test_new_component_components_post_empty_body_failed(self):
        url = self.base_url + "/components"
        headers = {'Content-Type': 'application/json'}
        payload = {}
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 400

    def test_new_component_components_post_no_type_failed(self):
        url = self.base_url + "/components"
        headers = {'Content-Type': 'application/json'}
        payload = {'designation': 'R9998', 'address': 'X-Y', 'box': 'ZZ', 'quantity': 10}
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 400

    def test_new_component_components_post_without_quantity(self):
        url = self.base_url + "/components"
        headers = {'Content-Type': 'application/json'}
        payload = {'type': "резисторы", 'designation': 'R9995', 'address': 'X-Y', 'box': 'ZZ'}
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 201
        resp_body = resp.json()
        assert resp_body['component']['quantity'] == 0

    def test_new_component_components_push_put_empty_body_failed(self):
        url = self.base_url + "/components/push"
        headers = {'Content-Type': 'application/json'}
        payload = {}
        resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 400

    def test_new_component_components_push_put_without_address_failed(self):
        url = self.base_url + "/components/push"
        headers = {'Content-Type': 'application/json'}
        payload = {'type': "резисторы", 'designation': 'R9997', 'box': 'ZZ', 'quantity': 10}
        resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code == 400

    def test_new_component_components_push_put(self):
        url = self.base_url + "/components/push"
        headers = {'Content-Type': 'application/json'}
        payload = {'type': "резисторы", 'designation': 'R9996', 'address': 'X-Y', 'box': 'ZZ', 'quantity': 10}
        resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
        assert resp.status_code in [201, 204]

    def test_new_component_components_pop_put(self):
        url_create = self.base_url + "/components/push"
        url_pop = self.base_url + "/components/pop"
        headers = {'Content-Type': 'application/json'}
        payload_create = {'type': "резисторы", 'designation': 'R9996', 'address': 'X-Y', 'box': 'ZZ', 'quantity': 10}
        payload_pop = {'designation': 'R9996', 'address': 'X-Y', 'box': 'ZZ', 'quantity': 4}
        requests.put(url_create, headers=headers, data=json.dumps(payload_create, indent=4))
        resp = requests.put(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
        assert resp.status_code == 204
        resp = requests.delete(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
        assert resp.status_code == 204


if __name__ == "__main__":
    unittest.main()

# ref: https://peter-jp-xie.medium.com/rest-api-testing-using-python-751022c364b8
