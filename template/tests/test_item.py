import json

import pytest
import requests
import vcr
from mock import patch, Mock

from template.item import main
import azure.functions as func


class TestItem(object):

    @patch('template.item.get_items_from_collection')
    def test_main_get(self, mock_get_items):
        mock_get_items.return_value = [{'test': 'test'}]
        req = func.HttpRequest(method='GET', url='https://httpbin.org/get', body={})
        main_result = main(req, func.Out[func.Document])
        assert isinstance(main_result, func.HttpResponse)
        assert json.loads(main_result.get_body()) == [{'test': 'test'}]
        assert main_result.status_code == 200


class TestItemLocalHost(object):

    @vcr.use_cassette()
    def test_get_item(self):
        response = requests.get('http://0.0.0.0:7071/api/item/1')
        assert response.status_code == 200
        assert json.loads(response.text)['id'] == '1'

