import os
from inspect import currentframe


class Service(object):
    def __init__(self, service=None, shorthand=None, globalvars=None, uri=None, required=False):
        """
        :param service: A name for the service, e.g. `database`
        :param shorthand: A shorthand, e.g. `db`
        :param uri: config option for URI for the service e.g. `db_uri`
        :param required: Boolean value denoting whether the service is required
        :param globalvars: An iterable of the globalvars of interest
        """

        self.service = service
        self.shorthand = service[:2] if shorthand is None else shorthand
        self.uri = shorthand if uri is None else uri
        self.requried = required
        self.globalvars = (service,) if globalvars is None else globalvars
        self.config_func = None

        def configure_func(self, func):
            assert self.config_func is None, \
                    "Configure function is already specified for this service"
            self.config_func = func

        def configure_service(self, **kwargs):
            return self.config_func(**kwargs)


class Package(object):
    services = []
    root_envvar = None

    def __init__(self, name):
        """
        :param name: The name of the being developed
        """
        self.name = name

    def add_service(self, service):
        self.services.append(service)

    def set_root_var(self, vname):
        """
        param vname: The local frame 
        """
        assert self.root_envvar is None, \
                "root_envvar has already been set"
        self.root_envvar = vname

    def get_root_dir(self, *packages):
        root_dir_vname = self.globalvars['pkg_root'] 
        prd = currentframe().f_globals[root_dir_vname]
        
        if self.root_envvar is None:
            rv = '%s_ROOT' % self.name.upper()
        else:
            rv = self.root_envvar

        if prd is None:
            if os.environ.get(rv):
                prd = os.environ[rv]
            else:
                prd = os.path.dirname(os.path.abspath(__file__))
        if packages:
            path = os.path.join(prd, *packages)
        else:
            path = prd
        if not os.path.exists(path):
            raise Exception("%s does not exist" % path)
        return path

    def fetch_global_val(self, varname):
        return currentframe().f_globals[varname]

    def update_global_var(self, varname, value):
        currentframe().f_globals[varname] = value

    def configure_service(self, service, **kwargs):
        (s,) = [l for l in self.services if l.name==service]
        return s.configure_service(**kwargs)

    def configure(self, **kwargs):
        return {s.name: s.configure_service(**kwargs) for s in self.services}


class DBPackage(Package):
    globalvars = {
            'engine': 'engine',
            'metadata': 'metadata',
            'pkg_root': 'pkg_root_dir',
            'session': 'session',
        }
    pass
