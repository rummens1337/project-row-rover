import unittest
from src.processing.api import Api
import flask

server = flask(__name__)
api = None
api_key = 1234


class TestApi(unittest.TestCase):
    def setUp(self):
        # setup server
        api = Api(server, api_key)
        server.run(port=80, host='0.0.0.0')

    def tearDown(self):
        # TODO
        pass

    def test_print(self):
        self.assertEqual({
            "description": "Request was successful.",
            "status": 200,
            "data": {
                "result": 1
            },
            "message": "OK"
        }, api.print(200, {"result": 1}))

    def test_get_root(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
