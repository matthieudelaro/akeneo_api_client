# -*- coding: utf-8 -*-

from akeneo_api_client.collection import *
from akeneo_api_client.resources import *
from akeneo_api_client.auth import Auth
from akeneo_api_client.utils import urljoin

import requests
from requests.auth import AuthBase
import unittest
import base64
import json
from time import time

import logging
import logzero
from logzero import logger

from vcr_unittest import VCRTestCase


class TestCollectionMock(VCRTestCase):
    client_id = '1_ovvscbaj0pwwg8sookkgkc8ck4kog8gscg8g44sc88c8w48ww'
    secret = 'rpi0wuiusa8okok4cw8kkkc4s488gc0sggkc0480wskkgkwo0'
    username = 'admin'
    password = 'admin'
    base_url = 'http://localhost:8080'

    def _get_vcr(self, **kwargs):
        logzero.loglevel(logging.INFO)
        myvcr = super(TestCollectionMock, self)._get_vcr(**kwargs)
        myvcr.match_on = ['method', 'path', 'query', 'body', 'headers']
        myvcr.record_mode='none'
        return myvcr
        
    def test_valid_json_text(self):
        c = Collection(requests.Session(), json_text=self.json_text)

    def test_invalid_json_text(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            c = Collection(requests.Session(), json_text=self.invalide_json_text)

    def test_no_json(self):
        with self.assertRaises(ValueError):
            c = Collection(requests.Session())

    def test_loading_json(self):
        c = Collection(requests.Session(), json_text=self.json_text)
        self.assertEqual(len(c._items), 10)
        self.assertEqual(c._items[0].identifier, 'Biker-jacket-polyester-xl')

    def test_fetch_item(self):
        session = requests.Session()
        session.auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        session.headers.update({'Content-Type': 'application/json'})
        pool = ResourcePool(urljoin(self.base_url, '/api/rest/v1/', 'products/'), session)
        item = pool.fetch_item('1111111137')
        logger.debug(item)
        self.assertEqual(item.identifier, '1111111137')
        self.assertEqual(len(item.categories), 3)

    def test_fetch_item_from_invalid_pool(self):
        session = requests.Session()
        session.auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        session.headers.update({'Content-Type': 'application/json'})
        pool = ResourcePool(urljoin(self.base_url, '/api/rest/v1/', 'products_invalid/'), session)
        with self.assertRaises(requests.HTTPError):
            item = pool.fetch_item('1111111137')

    def test_get_invalide_item(self):
        session = requests.Session()
        session.auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        session.headers.update({'Content-Type': 'application/json'})
        pool = ResourcePool(urljoin(self.base_url, '/api/rest/v1/', 'products/'), session)
        with self.assertRaises(requests.HTTPError):
            item = pool.fetch_item('1111111137asdfsdfgsdf')

    def test_loading_fetch_next_page(self):
        session = requests.Session()
        session.auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        session.headers.update({'Content-Type': 'application/json'})
        pool = ResourcePool(urljoin(self.base_url, '/api/rest/v1/', 'products/'), session)
        c = pool.fetch_list()
        self.assertEqual(len(c._items), 10)
        c.fetch_next_page()
        self.assertEqual(len(c._items), 20)
        c.fetch_next_page()
        self.assertEqual(len(c._items), 30)

    def test_auto_loading(self):
        session = requests.Session()
        session.auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        session.headers.update({'Content-Type': 'application/json'})
        pool = ResourcePool(urljoin(self.base_url, '/api/rest/v1/', 'products/'), session)
        c = pool.fetch_list()
        self.assertEqual(len(c._items), 10)
        iterator = iter(c)
        for i in range(15):
            item = next(iterator)
        self.assertEqual(len(c._items), 20)
        iterator = iter(c)
        for i in range(25):
            item = next(iterator)
        self.assertEqual(len(c._items), 30)


    json_text = '''{"_embedded":{"items":[{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/Biker-jacket-polyester-xl"}},"associations":{},"categories":["master_men_blazers"],"created":"2017-10-23T07:50:17+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"Biker-jacket-polyester-xl","parent":"model-biker-jacket-polyester","updated":"2017-10-23T07:50:25+00:00","values":{"collection":[{"data":["summer_2017"],"locale":null,"scope":null}],"color":[{"data":"white","locale":null,"scope":null}],"description":[{"data":"Biker jacket","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890367","locale":null,"scope":null}],"material":[{"data":"polyester","locale":null,"scope":null}],"name":[{"data":"Biker jacket","locale":null,"scope":null}],"price":[{"data":[{"amount":null,"currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"variation_name":[{"data":"Biker jacket polyester","locale":"en_US","scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/14101037"}},"associations":{},"categories":["led_tvs","toshiba","tvs_projectors_sales"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"led_tvs","groups":[],"identifier":"14101037","parent":null,"updated":"2017-10-23T07:50:36+00:00","values":{"description":[{"data":"<b>LED</b>\\nLEDs wandeln Strom effizient in Licht um und liefern zusätzlich bessere Kontraste und leuchtendere Farben. Die Full-HD-Auflösung unterstreicht diese hervorragenden Eigenschaften zusätzlich.\\n\\n<b>FULL HD</b>\\nFür Bilder in High Definition Auflösung, wie sie durch HDTV und Blu-ray bereitgestellt werden, hat sich in Europa die Auflösung 1.920x1.080 Bildpunkte für das übertragene Signal weitgehend durchgesetzt.\\n\\n<b>DVD-Player integriert</b>\\nDieser TV hat einen integrierten DVD Player, so dass Sie auf ein externes Gerät verzichten können und trotzdem all Ihre Lieblingsfilme genießen können.\\n\\n<b>Dualtuner</b>\\nDieser TV bietet neben einem analogen Tuner ebenfalls einen Tuner für DVB-T und DVB-C (HD).\\n\\n<b>Videos, Musik und Bilder per USB Schnittstelle</b>\\nMit diesem TV können Sie Videos, Musik und Bilder per USB Schnittstelle genießen.\\nVideos, Musik und Bilder per USB Schnittstelle","locale":"de_DE","scope":"print"},{"data":"Toshiba 23DL933G. HD type: Full HD, Display resolution: 1920 x 1080, Aspect ratio: 16:9. Tuner type: Analogue & Digital, Analog signal format system: PAL BG, PAL DK, PAL I, SECAM B/G, SECAM D/K, SECAM L, Digital signal format system: DVB-C, DVB-T. RMS rated power: 2.5. Optical disc player type: DVD player, Disc types supported: DVD+R, DVD+RW, DVD-R, DVD-RW. Video formats supported: AVI, DAT, H.264, ISO, MKV, MP4, MPEG1, MPEG2, MPEG4, VOB, XVID, Audio formats supported: AAC, MP3, MP4, Image formats supported: JPG","locale":"en_US","scope":"print"}],"display_diagonal":[{"data":{"amount":23,"unit":"INCH"},"locale":null,"scope":null}],"name":[{"data":"Toshiba 23DL933G LED TV","locale":null,"scope":null}],"release_date":[{"data":"2012-05-02T00:00:00+00:00","locale":null,"scope":"ecommerce"}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111130"}},"associations":{},"categories":["master_men_blazers_deals","supplier_zaro"],"created":"2017-10-23T07:50:33+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111130","parent":"apollon_yellow","updated":"2017-10-23T07:50:35+00:00","values":{"collection":[{"data":["winter_2016"],"locale":null,"scope":null}],"color":[{"data":"yellow","locale":null,"scope":null}],"description":[{"data":"Long gray suit jacket and matching pants unstructured. 61% wool, 30% polyester, 9% ramie. Dry clean only.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890142","locale":null,"scope":null}],"erp_name":[{"data":"Apollon","locale":"en_US","scope":null}],"image":[{"_links":{"download":{"href":"http://localhost:8080/api/rest/v1/media-files/8/5/d/6/85d68741cf9aee975f9585b107d43ea30eb02e25_apollon.jpg/download"}},"data":"8/5/d/6/85d68741cf9aee975f9585b107d43ea30eb02e25_apollon.jpg","locale":null,"scope":null}],"name":[{"data":"Long gray suit jacket and matching pants unstructured","locale":null,"scope":null}],"price":[{"data":[{"amount":"899.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xs","locale":null,"scope":null}],"supplier":[{"data":"zaro","locale":null,"scope":null}],"variation_image":[{"_links":{"download":{"href":"http://localhost:8080/api/rest/v1/media-files/9/1/4/1/9141b1262701c16d7d9cfc03277ab321a900ccde_apollon.jpg/download"}},"data":"9/1/4/1/9141b1262701c16d7d9cfc03277ab321a900ccde_apollon.jpg","locale":null,"scope":null}],"variation_name":[{"data":"Apollon yellow","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"600.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111131"}},"associations":{},"categories":["master_men_blazers_deals","supplier_zaro"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111131","parent":"apollon_yellow","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["winter_2016"],"locale":null,"scope":null}],"color":[{"data":"yellow","locale":null,"scope":null}],"description":[{"data":"Long gray suit jacket and matching pants unstructured. 61% wool, 30% polyester, 9% ramie. Dry clean only.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890143","locale":null,"scope":null}],"erp_name":[{"data":"Apollon","locale":"en_US","scope":null}],"image":[{"_links":{"download":{"href":"http://localhost:8080/api/rest/v1/media-files/8/5/d/6/85d68741cf9aee975f9585b107d43ea30eb02e25_apollon.jpg/download"}},"data":"8/5/d/6/85d68741cf9aee975f9585b107d43ea30eb02e25_apollon.jpg","locale":null,"scope":null}],"name":[{"data":"Long gray suit jacket and matching pants unstructured","locale":null,"scope":null}],"price":[{"data":[{"amount":"899.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"supplier":[{"data":"zaro","locale":null,"scope":null}],"variation_image":[{"_links":{"download":{"href":"http://localhost:8080/api/rest/v1/media-files/9/1/4/1/9141b1262701c16d7d9cfc03277ab321a900ccde_apollon.jpg/download"}},"data":"9/1/4/1/9141b1262701c16d7d9cfc03277ab321a900ccde_apollon.jpg","locale":null,"scope":null}],"variation_name":[{"data":"Apollon yellow","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111132"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111132","parent":"ares_blue","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"blue","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890144","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xxl","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares blue","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111133"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111133","parent":"ares_blue","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"blue","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890145","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"m","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares blue","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111134"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111134","parent":"ares_blue","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"blue","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890146","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"s","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares blue","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111135"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111135","parent":"ares_pink","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"pink","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890147","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares pink","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111136"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111136","parent":"ares_pink","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"pink","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890148","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"m","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares pink","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}},{"_links":{"self":{"href":"http://localhost:8080/api/rest/v1/products/1111111137"}},"associations":{},"categories":["master_men_blazers_deals","print_clothing","supplier_mongo"],"created":"2017-10-23T07:50:34+00:00","enabled":true,"family":"clothing","groups":[],"identifier":"1111111137","parent":"ares_pink","updated":"2017-10-23T07:50:36+00:00","values":{"collection":[{"data":["spring_2015"],"locale":null,"scope":null}],"color":[{"data":"pink","locale":null,"scope":null}],"description":[{"data":"Blazer wool mixed with sand print foot hen, single breasted with two buttons, patch pockets and contrasting lapel collar, model 'Vienna'. Das Model 185 cm groß ist und trägt Größe 40 (DE Größe 50 - 101cm Brustumfang) 60% wool, 30% polyester, 10% cotton. Machine washable.","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567890149","locale":null,"scope":null}],"erp_name":[{"data":"Ares","locale":"en_US","scope":null}],"name":[{"data":"Blazer wool mixed with sand print foot hen","locale":null,"scope":null}],"price":[{"data":[{"amount":"1099.00","currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"s","locale":null,"scope":null}],"supplier":[{"data":"mongo","locale":null,"scope":null}],"variation_name":[{"data":"Ares pink","locale":"en_US","scope":null}],"wash_temperature":[{"data":"600","locale":null,"scope":null}],"weight":[{"data":{"amount":"800.0000","unit":"GRAM"},"locale":null,"scope":null}]}}]},"_links":{"first":{"href":"http://localhost:8080/api/rest/v1/products?page=1&with_count=false&pagination_type=page&limit=10&search=%7B%22enabled%22%3A%5B%7B%22operator%22%3A%22%3D%22%2C%22value%22%3Atrue%7D%5D%2C%22completeness%22%3A%5B%7B%22operator%22%3A%22%3E%22%2C%22value%22%3A70%2C%22scope%22%3A%22ecommerce%22%7D%5D%7D"},"next":{"href":"http://localhost:8080/api/rest/v1/products?page=2&with_count=false&pagination_type=page&limit=10&search=%7B%22enabled%22%3A%5B%7B%22operator%22%3A%22%3D%22%2C%22value%22%3Atrue%7D%5D%2C%22completeness%22%3A%5B%7B%22operator%22%3A%22%3E%22%2C%22value%22%3A70%2C%22scope%22%3A%22ecommerce%22%7D%5D%7D"},"self":{"href":"http://localhost:8080/api/rest/v1/products?page=1&with_count=false&pagination_type=page&limit=10&search=%7B%22enabled%22%3A%5B%7B%22operator%22%3A%22%3D%22%2C%22value%22%3Atrue%7D%5D%2C%22completeness%22%3A%5B%7B%22operator%22%3A%22%3E%22%2C%22value%22%3A70%2C%22scope%22%3A%22ecommerce%22%7D%5D%7D"}},"current_page":1}'''
    invalide_json_text = '''"_embedded":{"i'''

