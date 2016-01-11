import os
import strowger.lib as lib

from ConfigParser import ConfigParser
from inspect import currentframe, getframeinfo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Service(object):
    def __init__(self, service=None, shorthand=None, globalvars=None, uri=None, required=False, configs=None):
        """
        :param service: A name for the service, e.g. `database`
        :param shorthand: A shorthand, e.g. `db`
        :param globalvars: An iterable of the globalvars of interest
        :param uri: config option for URI for the service e.g. `db_uri`
        :param required: Boolean value denoting whether the service is required
        :param configs: A path to the folder holding the config files for this service
        """

        self.service = service
        self.shorthand = service[:2] if shorthand is None else shorthand
        self.uri = uri
        self.requried = required
        self.globalvars = (service,) if globalvars is None else globalvars
        self.config_folder = configs
        self.config_func = None
        self.uri_func = self.default_uri_func

    def __repr__(self):
        return '< Service | %s | %s >' % (self.service, self.shorthand)

    def configure_func(self, func):
        """
        A hook for setting the function to configure the global vars
        associated with the service
        """
        assert self.config_func is None, \
                "Configure function is already specified for this service"
        self.config_func = func
        return

    def configure_service(self, **kwargs):
        return self.config_func(**kwargs)

    def _read_config(self, environment=None, state=None):
        parser = ConfigParser()
        if environment is None:
            environment = 'default'
        env_file = '%s.ini' % environment

        if state is None:
            section = self.service
        else:
            section = "%s:%s" % (self.service, state)

        with open(os.path.join(self.config_folder, env_file)) as fp:
            parser.readfp(fp)
            out = parser.items(section)
            fp.close()
        del parser
        return dict(out)

    def default_uri_func(self, **kwargs):
        d = self._read_config(environment=kwargs.get('environment'), state=kwargs.get('state'))
        return d.get(self.uri)

    def get_uri(self, **kwargs):
        return self.uri_func(**kwargs)


class Package(object):
    def __init__(self, name, root_gvar=None):
        """
        :param name: The name of the package being developed
        :param root_gvar: The name of the variable in the global scope holding a
        string with the directory location of the package root 
        """
        self.name = name
        self.services = []
        self.root_envvar = None
        self.root_gvar = root_gvar

    def add_service(self, service):
        self.services.append(service)

    def set_root_var(self, vname):
        """
        param vname: The name of the variable in the local frame 
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
                frame = self.correct_frame()
                prd = os.path.dirname(frame.f_globals['__file__'])
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
        self.correct_frame().f_globals[varname] = value

    def set_global_attr(self, var, attr, val):
        pass

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
            'Base': 'Base',
            'engine': 'engine',
            'metadata': 'metadata',
            'session': 'session',
        }

    def __init__(self, name, root_gvar=None):
        super(self.__class__, self).__init__(name, root_gvar=root_gvar)
        self.db = Service(service='database', shorthand='db', globalvars=self.globalvars, uri='uri', required=True)
        self.add_service(self.db)

        @self.db.configure_func
        def configure_db(environment=None, state=None, **kwargs):
            if not self.db.config_folder:
                self.db.config_folder = os.path.join(self.get_root_dir(), 'config')

            db_uri = self.db.get_uri(environment=environment, state=state)
            engine_var = self.db.globalvars['engine']
            self.update_global_var(engine_var, create_engine(db_uri))

            engine = self.fetch_global_val(engine_var)
            base_obj = self.db.globalvars['Base']
            base = self.fetch_global_val(base_obj)
            lib.rsetattr(base, 'metadata.bind', engine)
            self.update_global_var(base_obj, base)

            metadata_var = self.db.globalvars['metadata']
            self.update_global_var(metadata_var, base.metadata)

            session_var = self.db.globalvars['session']
            Session = sessionmaker()
            Session.configure(bind=engine)
            self.update_global_var(session_var, Session())


