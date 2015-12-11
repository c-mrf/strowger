import os
from inspect import currentframe, getframeinfo


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
        self.uri_func = self.default_uri_func

    def configure_func(self, func):
        """
        A hook for setting the function to configure the global vars
        associated with the service
        """
        assert self.config_func is None, \
                "Configure function is already specified for this service"
        self.config_func = func
        return

    def default_uri_func(self, environment, state, **kwargs):
        pass

    def configure_service(self, **kwargs):
        self.config_func(**kwargs)
        return

    def _read_config(self, environment=None, state=None):
        pass

    def get_uri(self, environment=None, state=None, **kwargs):
        pass


class Package(object):
    services = []
    root_envvar = None
    root_gvar = None

    def __init__(self, name):
        """
        :param name: The name of the being developed
        """
        self.name = name

    def add_service(self, service):
        service 
        self.services.append(service)

    def set_root_var(self, vname):
        """
        param vname: The local frame 
        """
        assert self.root_envvar is None, \
                "root_envvar has already been set"
        self.root_envvar = vname

    def get_root_var(self):
        if self.root_envvar is None:
            rv = '%s_ROOT' % self.name.upper()
        else:
            rv = self.root_envvar
        return rv

    def get_root_dir(self, packages=None):
        prd = self.fetch_global_val(self.root_gvar)
        rv = self.get_root_var()

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
            raise ValueError("%s does not exist" % path)
        return path

    def correct_frame(self):
        frame = currentframe(1)
        while getframeinfo(frame)[0] == getframeinfo(currentframe())[0]:
            frame = frame.f_back
        return frame

    def fetch_global_val(self, varname):
        fglobals = self.correct_frame().f_globals
        
        if varname not in fglobals.keys():
            raise ValueError("%s is not a variable in the global scope" % varname)
        val =  fglobals.get(varname)
        return val

    def update_global_var(self, varname, value):
        currentframe(1).f_globals[varname] = value

    def configure_service(self, service, **kwargs):
        (s,) = [l for l in self.services if l.name==service]
        s.configure_service(**kwargs)
        return

    def configure(self, pkg_root=True, services=False, **kwargs):
        if pkg_root:
            pkgroot = self.get_root_dir(kwargs.get('packages')) 
            self.update_global_var(self.root_gvar, pkgroot)
        
        if services:
            for s in self.services:
                s.configure_service(**kwargs)
        return


class DBPackage(Package):
    globalvars = {
            'engine': 'engine',
            'metadata': 'metadata',
            'session': 'session',
        }
    pass
