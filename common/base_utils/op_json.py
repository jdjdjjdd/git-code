# -*- coding: utf-8 -*-

import json
from config.Config import Config
cf = Config()

class operationJson(object):
    def __init__(self, file_path= cf.rootPath + "/test_data/api_documents.json"):
        self.file_path = file_path
        self.data = self.get_data()

    def get_data(self):
        with open(self.file_path) as f:
            data = json.load(f)
            return data

    def get_key_words(self, key=None):
        if key:
            return self.data[key]
        else:
            return self.data


