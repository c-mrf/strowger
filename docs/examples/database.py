from astor import Base
from strowger import DBPackage

pkg_name = 'astor'
astor_root = None

engine = None
metadata = None
session = None

__all__ = [
    "pkg_name",
    "astor_root",
    "engine",
    "metadata",
    "session",
    "configure",
    "release",
]

astor_pkg = DBPackage(pkg_name, '%s_root' % pkg_name)

"""
By default strowger assumes a folder '/config/'
in the package root.
"""

def configure(environment, state=None):
    astor_pkg.configure(
        pkg_root=True,
        services=True,
        environment=environment,
        state=state
    )

def get_root(packages=None):
    return astor_pkg.get_root_dir(packages=packages)

def release():
    session.close()
    engine.dispose()
