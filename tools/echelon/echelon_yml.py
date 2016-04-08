#!/usr/bin/python

# Yaml loader backen for echelon

from ansible.errors import AnsibleError
from ansible.parsing.dataloader import DataLoader

import yaml
import os.path

class Backend(object):
    def __init__(self, backend, conf):
        self.backend = backend
        self.conf = conf

    def main(self, path):
        data_dir = self.conf['data_dir']
        loader = DataLoader()

        full_path="%s/%s" % (data_dir, path)

        if os.path.isfile("%s.yaml" % full_path):
            ds = loader.load_from_file("%s.yaml" % full_path)
        elif os.path.isfile("%s.yml" % full_path):
            ds = loader.load_from_file("%s.yml" % full_path)
        else:
            ds={}
        if ds is None:
            ds = {}

        return ds