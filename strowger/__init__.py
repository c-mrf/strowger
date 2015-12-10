import os
from inspect import currentframe


class Package(object):
    service_properties = {
            'service': 'a name for the service, e.g. `database`',
            'shorthand': 'a shorthand, e.g. `db`',
            'uri': 'uri for the service',
            'required': 'boolean value denoting whether the service is required'
            }

    globalvars = {
            'engine': 'engine',
            'metadata': 'metadata',
            'pkg_root': 'pkg_root_dir',
            'session': 'session',
        }

    root_envvar = None

    def __init__(self, name):
        """
        :param name: The name of the being developed
        """
        self.name = name

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
        pass

    def update_global_var(self, varname, value):
        currentframe().f_globals[varname] = value
