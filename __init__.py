import os


class Package(object):
    service_properties = {
            'service': 'a name for the service, e.g. `database`',
            'shorthand': 'a shorthand, e.g. `db`',
            'uri': 'uri for the service',
            'required': 'boolean value denoting whether the service is required'
            }

    root_var = None

    def __init__(self, name):
        pass

    def set_root_var(self, name):
        pass

    def root_dir(self, package):
        pass
