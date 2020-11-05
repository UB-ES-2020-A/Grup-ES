import unittest

from db import db
from config import config
from init_app import init


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app, self.api, self.migrate = init(config['test'])
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()
